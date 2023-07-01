from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime
from time import sleep

class backgroundThread(QThread):
    updateDay = pyqtSignal()
    updateMinute = pyqtSignal()

    def __init__(self, parent=None):
        super(backgroundThread, self).__init__()

    def run(self):
        today = []
        while True:
            date = datetime.now().strftime('%Y-%m-%d')
            if date not in today:
                today = [date]
                self.updateDay.emit()
            sleep(60)
            self.updateMinute.emit()
            
