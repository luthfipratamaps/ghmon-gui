from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt
    
class tableModel(QAbstractTableModel):
    def __init__ (self, headers, rows):
        super (tableModel, self).__init__()
        self.headers = headers
        self.rows = rows
    def rowCount(self, parent):
        return len(self.rows)
    def columnCount(self, parent):
        return len(self.headers)
    def data(self, index, role):
        if role != Qt.DisplayRole:
            return QVariant()
        return self.rows[index.row()][index.column()]
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return QVariant()
        return self.headers[section]