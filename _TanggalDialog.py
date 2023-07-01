from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class tanggalDialog(QDialog):
    def __init__(self, listTanggal):
        super (tanggalDialog, self).__init__()

        self.listTanggal = listTanggal
        self.getDate()
        
        mainLayout = QGridLayout()
        
        tanggalLabel = QLabel("Akses data monitoring pada tanggal:")
                
        self.tahunCombo = QComboBox()
        self.bulanCombo = QComboBox()
        self.hariCombo = QComboBox()
        
        self.submitButton = QPushButton("&Submit")
        
        comboLayout = QHBoxLayout()
        comboLayout.addWidget(self.tahunCombo)
        comboLayout.addWidget(self.bulanCombo)
        comboLayout.addWidget(self.hariCombo)
                
        mainLayout.addWidget(tanggalLabel, 0, 0)
        mainLayout.addLayout(comboLayout, 1, 0, 1, 3)
        mainLayout.addWidget(self.submitButton, 2, 3)
        
        self.setLayout(mainLayout)
        self.setWindowTitle("Pilih Tanggal")
        
        for year, md in self.dict1.items():
            self.tahunCombo.addItem(str(year), list(md.keys()))

        self.submitButton.clicked.connect(self.submitClicked)
        self.submitButton.clicked.connect(self.accept)

        self.tahunCombo.currentIndexChanged.connect(self.updateBulanCombo)
        self.bulanCombo.currentIndexChanged.connect(self.updateHariCombo)

        self.updateBulanCombo()
        self.updateHariCombo()
        
        self.show()
        
    def updateBulanCombo(self):
        self.bulanCombo.clear()
        index = self.tahunCombo.currentIndex()
        bulan = self.tahunCombo.itemData(index)
        if bulan: self.bulanCombo.addItems(bulan)
        self.updateHariCombo()

    def updateHariCombo(self):
        self.hariCombo.clear()
        index1 = self.tahunCombo.currentIndex()
        index2 = self.bulanCombo.currentIndex()
        k = list(list(self.dict1.items())[index1][1])[index2]
        hari = list(self.dict1.items())[index1][1][k]
        if hari: self.hariCombo.addItems(hari)
            
    def submitClicked(self):
        y = list(self.dict1)[self.tahunCombo.currentIndex()]
        m = list(self.dict1[y])[self.bulanCombo.currentIndex()]
        d = list(self.dict1[y][m])[self.hariCombo.currentIndex()]
        self.chosenDate = f"{y}-{m}-{d}"
        
        self.hide()
        
    def getDate(self):
        result = self.listTanggal[::-1]
        
        y = result[0][0:4]
        m = result[0][5:7]
        d = result[0][8:10]
        
        dict1 = dict()
        dict2 = dict()

        for i, tgl in enumerate(result):
            y = tgl[0:4]
            m = tgl[5:7]
            d = tgl[8:10]
    
            if y not in dict2:
                dict1 = dict()
                
            if m in dict1: 
                dict1[m].append(d)
            else:
                dict1[m] = [d]
    
            dict2[y] = dict1
            
        self.dict1 = dict2
        
    def getDateFromDialog(self):
        return self.chosenDate