from _Main import main
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        
        widget = QWidget()
        self.mainWidget = main(self)
        self.setCentralWidget(self.mainWidget)
        
        message = "ready"
        self.statusBar = self.statusBar()
        self.statusBar.showMessage(message)
        
        self.menuAction()
        self.menu()
        
        self.setWindowTitle("Monitoring")
        self.setWindowState(Qt.WindowMaximized)
        
    def menu(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.addInvAct)
        self.fileMenu.addAction(self.addCsvAct)
        self.fileMenu.addAction(self.exportInvAct)
        self.fileMenu.addAction(self.exportCsvAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        
        self.editMenu = self.menuBar().addMenu("E&dit")
        self.editMenu.addAction(self.filterAct)
        
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)
        
    def menuAction(self):
        self.addInvAct = QAction("Add from &INV", self, shortcut="Ctrl+Shift+I",
                statusTip="Add data from INV file", triggered=self.addInv)
        self.addCsvAct = QAction("Add from &CSV", self, shortcut="Ctrl+Shift+C",
                statusTip="Add data from CSV file", triggered=self.addCsv)
        self.exportInvAct = QAction("Export to I&NV", self, shortcut="Ctrl+Shift+N",
                statusTip="Export data to INV file", triggered=self.exportInv)
        self.exportCsvAct = QAction("Export to C&SV", self, shortcut="Ctrl+Shift+S",
                statusTip="Export data to CSV file", triggered=self.exportCsv)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Close the App", triggered=self.close)
        self.filterAct = QAction("&Filter", self, shortcut="Ctrl+F",
                statusTip="Filter data", triggered=self.filter_)
        self.aboutAct = QAction("About", self,
                statusTip="Show the App's brief explanation", triggered=self.about)
        self.aboutQtAct = QAction("About Qt", self,
                statusTip="Show the Qt Library's brief explanation", triggered=self.aboutQt)
        
        self.aboutQtAct.triggered.connect(QApplication.instance().aboutQt)
        
    def addInv(self):
        pass
    def addCsv(self):
        pass
    def exportInv(self):
        pass
    def exportCsv(self):
        pass
    def filter_(self):
        pass
    def about(self):
        QMessageBox.about(self, "About This GUI",
                          "asdlkjaegiolkdsfjeoijgnlksdnflksnelfijskldnf Pain"
                          "-PekoPekoPekoPekoPekoPekoPekoPekoPekoPekoPekoPeko?")
    def aboutQt(self):
        pass
    
app = QApplication([])

# dark theme
# Force the style to be the same on all OSs:
app.setStyle("Fusion")
# use a palette to switch to dark colors:
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.white)
palette.setColor(QPalette.ToolTipText, Qt.black)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.Highlight, QColor(Qt.white))
palette.setColor(QPalette.HighlightedText, Qt.black)
palette.setColor(QPalette.Disabled, QPalette.Base, QColor(49, 49, 49))
palette.setColor(QPalette.Disabled, QPalette.Text, QColor(90, 90, 90))
palette.setColor(QPalette.Disabled, QPalette.Button, QColor(42, 42, 42))
palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(90, 90, 90))
palette.setColor(QPalette.Disabled, QPalette.Window, QColor(49, 49, 49))
palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(90, 90, 90))
app.setPalette(palette)
mainWindow = mainWindow()
mainWindow.show()

app.exec_()