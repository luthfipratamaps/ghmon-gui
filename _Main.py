from _BackgroundThread import backgroundThread
from _Errors import myErrors
from _FilterDialog import filterDialog
from _TableModel import tableModel
from _TanggalDialog import tanggalDialog
from _PlotWindow import plotWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime
import matplotlib.pyplot as plt
import csv
import glob
import os
import pickle
#import pymysql

class main(QWidget):
    defaultData, filteredData = range(2)
    suhuData, rhData, icData = "Suhu", "RH", "IC"
    
    def __init__(self, parent):
        super(main, self).__init__(parent)
        
        self.parent = parent
        
        self.getCsvList()
        self.getDate()
                
        self.chosenDate = ''
        self.suhuSetData, self.rhSetData = [], []
        self.counter = len(self.csvFiles) - 1
        
        self.currentDataMode = self.defaultData
        self.currentChosenData = self.suhuData
        
        self.dateDialog = tanggalDialog
        self.filterDialog = filterDialog
        
        self.allHeaders = self.getHeaders()
        self.suhuHeaders = self.allHeaders[1:2]+self.allHeaders[2:20]
        self.rhHeaders = self.allHeaders[1:2]+self.allHeaders[20:38]
        self.icHeaders = self.allHeaders[1:2]+self.allHeaders[38:56]
        self.jumlahBaris = len(self.suhuSetData)
        self.jumlahKolom = len(self.suhuHeaders)
        
        tanggalStrLabel = QLabel("Tanggal Pilihan: ")
        self.tanggalLabel = QLabel()
        self.tanggalLabel.setStyleSheet("border: 1px solid black;")
        
        self.suhuButton = QPushButton("Suhu")
        self.suhuButton.setEnabled(False)
        self.rhButton = QPushButton("RH")
        self.rhButton.setEnabled(False)
        self.icButton = QPushButton("IC")
        self.icButton.setEnabled(False)
        self.suhuGraphButton = QPushButton("Grafik Suhu")
        self.suhuGraphButton.setEnabled(True)
        self.rhGraphButton = QPushButton("Grafik RH")
        self.rhGraphButton.setEnabled(True)
        self.icGraphButton = QPushButton("Grafik IC")
        self.icGraphButton.setEnabled(True)
        
        self.nextButton = QPushButton("Next")
        self.nextButton.setEnabled(False)
        self.dateButton = QPushButton("Choose Date")
        self.dateButton.setEnabled(False)
        self.previousButton = QPushButton("Previous")
        self.previousButton.setEnabled(False)
        
        self.filterButton = QPushButton("Filter")
        self.resetButton = QPushButton("Reset")
        self.resetButton.setEnabled(False)
        
        self.suhuButton.setToolTip("Tampilkan data Suhu")
        self.rhButton.setToolTip("tampilkan data RH")
        self.icButton.setToolTip("tampilkan data IC")
        self.suhuGraphButton.setToolTip("Tampilkan jendela grafik Suhu")
        self.rhGraphButton.setToolTip("Tampilkan jendela grafik RH")
        self.icGraphButton.setToolTip("Tampilkan jendela grafik IC")
        self.nextButton.setToolTip("Tampilkan data pada tanggal selanjutnya")
        self.dateButton.setToolTip("Pilih tanggal data")
        self.previousButton.setToolTip("Tampilkan data pada tanggal sebelumnya")
        self.filterButton.setToolTip("Filter data yang ditampilkan")
        self.resetButton.setToolTip("Reset tampilan data")
        
        self.suhuButton.clicked.connect(self.suhu_)
        self.rhButton.clicked.connect(self.rh_)
        self.icButton.clicked.connect(self.ic_)
        self.suhuGraphButton.clicked.connect(self.suhuGraph)
        self.rhGraphButton.clicked.connect(self.rhGraph)
        self.icGraphButton.clicked.connect(self.icGraph)
        self.nextButton.clicked.connect(self.next_)
        self.dateButton.clicked.connect(self.chooseDate)
        self.previousButton.clicked.connect(self.previous)
        self.filterButton.clicked.connect(self.filter_)
        self.resetButton.clicked.connect(self.reset)
        
        labelLayout = QHBoxLayout()
        labelLayout.addWidget(tanggalStrLabel)
        labelLayout.addWidget(self.tanggalLabel)
        labelLayout.addStretch()
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.suhuButton)
        buttonLayout.addWidget(self.rhButton)
        buttonLayout.addWidget(self.icButton)
        buttonLayout.addWidget(self.suhuGraphButton)
        buttonLayout.addWidget(self.rhGraphButton)
        buttonLayout.addWidget(self.icGraphButton)
        buttonLayout.addStretch()
        
        buttonLayout2 = QVBoxLayout()
        buttonLayout2.addWidget(self.filterButton)
        buttonLayout2.addWidget(self.resetButton)
        buttonLayout2.addStretch()
        
        buttonLayout3 = QHBoxLayout()
        buttonLayout3.addWidget(self.previousButton)
        buttonLayout3.addWidget(self.dateButton)
        buttonLayout3.addWidget(self.nextButton)
        
        self.suhuTable = QTableView()
        self.rhTable = QTableView()
        self.rhTable.hide()
        self.icTable = QTableView()
        self.icTable.hide()
        
        tableLayout = QVBoxLayout()
        tableLayout.addWidget(self.suhuTable)
        tableLayout.addWidget(self.rhTable)
        tableLayout.addWidget(self.icTable)
        
        mainLayout = QGridLayout()
        mainLayout.addLayout(labelLayout, 0, 0)
        mainLayout.addLayout(buttonLayout, 1, 0)
        mainLayout.addLayout(tableLayout, 2, 0, 3, 4)
        mainLayout.addLayout(buttonLayout2, 2, 4)
        mainLayout.addLayout(buttonLayout3, 5, 0, 1, 3)
        
        self.setLayout(mainLayout)
        
        self.bgThread = backgroundThread()
        self.bgThread.start()
        self.bgThread.updateDay.connect(self.updateDataDay)
        self.bgThread.updateMinute.connect(self.updateDataMinute)
        
        self.updateDataOnTable()
        self.updateInterface()
        
    def getCsvList(self):
        path = os.getcwd()
        csvFiles = glob.glob(os.path.join(path + '/__csv__', "*.csv"))
        csvFiles.sort()
        #csvFiles.reverse()
        self.csvFiles = csvFiles
        
        #check if the data exists
        if len(self.csvFiles) == 0:
            #close the app
            QMessageBox.warning(self, "Data Tidak Ditemukan",
                                f"Data monitoring tidak dapat ditemukan.")
            self.close()
            raise myErrors("Data Tidak Ditemukan")
    
    def getDate(self):
        self.listTanggal = []
        for csvFile in self.csvFiles:
            self.listTanggal.append(csvFile[-14:][:10]) #getting tanggal from filename
            
    def getHeaders(self):
        with open(str(self.csvFiles[self.counter])) as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            
            for i, row in enumerate(csvReader):
                if i==0: 
                    headers = list(row)
                    break
                
        return headers
            
    def getData(self):
        with open(str(self.csvFiles[self.counter])) as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            
            self.setData = list(csvReader)
        
        print("jml setdata: ", len(self.setData))
        
    def getFilteredData(self, filterSetting):
        with open(str(self.csvFiles[self.counter])) as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            
            self.setData = list(csvReader)
        
        filteredData = []
        for data in self.setData:
            if filterSetting[1] < data[self.allHeaders.index(filterSetting[0])] < filterSetting[2]:
                filteredData.append(data)
        
        self.setData = filteredData
        print("jml setdata: ", len(self.setData))
                
    def suhu_(self):
        self.currentChosenData = self.suhuData
        self.updateInterface()
        self.suhuTable.show()
        self.rhTable.hide()
        self.icTable.hide()
        
    def rh_(self):
        self.currentChosenData = self.rhData
        self.updateInterface()
        self.suhuTable.hide()
        self.rhTable.show()
        self.icTable.hide()

    def ic_(self):
        self.currentChosenData = self.icData
        self.updateInterface()
        self.suhuTable.hide()
        self.rhTable.hide()
        self.icTable.show()

    def suhuGraph(self):
        fig, ax, leg = plotWindow(self.suhuData,
                                self.suhuSetData,
                                self.suhuHeaders)

        #figManager = plt.get_current_fig_manager()
        #figManager.window.showMaximized()

        mgr = plt.get_current_fig_manager()

        """ use this if raspi
        mgr.resize(*mgr.window.maxsize())
        """

        mgr.window.showMaximized()
        plt.show()
        
    def rhGraph(self):
        fig, ax, leg = plotWindow(self.rhData,
                                self.rhSetData,
                                self.rhHeaders)
        mgr = plt.get_current_fig_manager()

        """ use this if raspi
        mgr.resize(*mgr.window.maxsize())
        """

        mgr.window.showMaximized()
        plt.show()

    def icGraph(self):
        fig, ax, leg = plotWindow(self.icData,
                                self.icSetData,
                                self.icHeaders)
        mgr = plt.get_current_fig_manager()

        """ use this if raspi
        mgr.resize(*mgr.window.maxsize())
        """

        mgr.window.showMaximized()
        plt.show()
        
    def next_(self):
        self.counter += 1
        self.updateDataOnTable()
        self.updateInterface()
        
    def chooseDate(self):
        thisDialog = self.dateDialog(self.listTanggal)
        if thisDialog.exec_() == QDialog.Accepted:
            self.chosenDate = thisDialog.getDateFromDialog()
            if not all(self.chosenDate): return
            #change self.counter to this chosen date index
            index = self.listTanggal.index(self.chosenDate)
            self.counter = index
            self.updateDataOnTable()
            self.updateInterface()
    
    def previous(self):
        self.counter -= 1
        print(self.counter)
        self.updateDataOnTable()
        self.updateInterface()
            
    def filter_(self):
        thisDialog = self.filterDialog(self.allHeaders)
        if thisDialog.exec_() == QDialog.Accepted:
            self.filterSetting = thisDialog.getFilterSetting()
            self.currentDataMode = self.filteredData
            self.updateDataOnTable()
            self.updateInterface()
            
    def reset(self):
        self.currentDataMode = self.defaultData
        self.updateDataOnTable()
        self.updateInterface()
        
    def updateDataDay(self):
        self.getCsvList()
        self.getDate()
        self.counter = len(self.csvFiles) - 1
        self.updateDataOnTable()
        self.updateInterface()
        print ("update hari: ", datetime.now().strftime("%Y-%m-%d"))
        
    def updateDataMinute(self):
        if self.counter == len(self.csvFiles) - 1:
            print("mengupdate data thread menit")
            self.updateDataOnTable()
            self.updateInterface()
        print ("update menit: ", datetime.now().strftime("%H:%M:%S"))
        
    def updateInterface(self):
        self.tanggalLabel.setText(self.chosenDate)
        self.suhuButton.setEnabled(self.currentChosenData in [self.rhData, self.icData])
        self.rhButton.setEnabled(self.currentChosenData in [self.suhuData, self.icData])
        self.icButton.setEnabled(self.currentChosenData in [self.suhuData, self.rhData])
        self.resetButton.setEnabled(self.currentDataMode == self.filteredData)
        self.nextButton.setEnabled(self.counter < len(self.csvFiles) - 1)
        self.dateButton.setEnabled(len(self.csvFiles) > 1)
        self.previousButton.setEnabled(self.counter > 0)
        if self.counter != len(self.listTanggal) - 1:
            self.parent.statusBar.showMessage(f"{self.chosenDate}_"+\
                                              f"{len(self.setData)}_"+\
                                              f"{self.currentChosenData} "+\
                                              f"(ready)")
                    
    def updateDataOnTable(self):
        self.updateDataMode(self.currentDataMode)
        self.updateChosenData(self.currentChosenData)
        
        suhuModel = tableModel(self.suhuHeaders, self.suhuSetData)
        rhModel = tableModel(self.rhHeaders, self.rhSetData)
        icModel = tableModel(self.icHeaders, self.icSetData)
        
        self.suhuTable.setModel(suhuModel)
        self.rhTable.setModel(rhModel)
        self.icTable.setModel(icModel)
            
    def updateDataMode(self, mode):
        self.currentDataMode = mode
        if self.currentDataMode == self.defaultData: self.getData()
        elif self.currentDataMode == self.filteredData:
            self.getFilteredData(self.filterSetting)
            
    def updateChosenData(self, data):
        if self.counter != len(self.csvFiles) - 1: self.parent.statusBar.showMessage("Memproses data...")
        self.suhuSetData, self.rhSetData, self.icSetData = [], [], []
        self.chosenDate = self.listTanggal[self.counter]
        if len(self.setData) == 0: return
        
        for i in range(len(self.setData)):
            if i == 0: continue
            self.suhuSetData.append(self.setData[i][1:2]+self.setData[i][2:20])
            self.rhSetData.append(self.setData[i][1:2]+self.setData[i][20:38])
            self.icSetData.append(self.setData[i][1:2]+self.setData[i][38:56])        
