from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class filterDialog(QDialog):
    def __init__(self, allHeaders):
        super (filterDialog, self).__init__()
        
        self.allHeaders = allHeaders
        self.getKolomInfo()
        
        mainLayout = QGridLayout()
        
        filterLabel = QLabel("Filter data berdasarkan:")
                
        self.kolomCombo = QComboBox()
        self.input1Combo = QComboBox()
        self.input2Combo = QComboBox()
        
        self.submitButton = QPushButton("&Submit")
        
        comboLayout = QHBoxLayout()
        comboLayout.addWidget(self.kolomCombo)
        comboLayout.addWidget(self.input1Combo)
        comboLayout.addWidget(self.input2Combo)
                
        mainLayout.addWidget(filterLabel, 0, 0)
        mainLayout.addLayout(comboLayout, 1, 0, 1, 3)
        mainLayout.addWidget(self.submitButton, 2, 3)
        
        self.setLayout(mainLayout)
        self.setWindowTitle("Filter Data")
        
        for kolom in self.kolomItem:
            self.kolomCombo.addItem(kolom)

        self.submitButton.clicked.connect(self.submitClicked)
        self.submitButton.clicked.connect(self.accept)

        self.kolomCombo.currentIndexChanged.connect(self.updateInput1Combo)
        self.input1Combo.currentIndexChanged.connect(self.updateInput2Combo)

        self.updateInput1Combo()
        self.updateInput2Combo()
        
        self.show()
        
    def updateInput1Combo(self):
        self.input1Combo.clear()
        if self.kolomCombo.currentIndex() == 0: input1 = self.inputItem[0]
        else: input1 = self.inputItem[1]
        self.input1Combo.addItems(input1)
        self.updateInput2Combo()

    def updateInput2Combo(self):
        self.input2Combo.clear()
        if self.kolomCombo.currentIndex() == 0: input2 = self.inputItem[0][self.input1Combo.currentIndex():]
        else: input2 = self.inputItem[1][self.input1Combo.currentIndex():]
        self.input2Combo.addItems(input2)
            
    def submitClicked(self):
        k = self.kolomItem[self.kolomCombo.currentIndex()]
        i1 = self.inputItem[0 if self.kolomCombo.currentIndex() == 0 else 1][self.input1Combo.currentIndex()]
        i2 = self.inputItem[0 if self.kolomCombo.currentIndex() == 0 else 1][self.input1Combo.currentIndex():][self.input2Combo.currentIndex()]
        
        self.filterSetting = [k, i1, i2]
        
        self.hide()
        
    def getKolomInfo(self):
        headers = self.allHeaders
        self.kolomItem = headers[1:56]
        
        i1 = [f"0{i}:00:00" if i < 10 else f"{i}:00:00" for i in range(0, 25)]
        i2 = [f"{i}" for i in range(0, 101, 10)]
        self.inputItem = [i1, i2]
        
    def getFilterSetting(self):
        return self.filterSetting
