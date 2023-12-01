import sys
import typing
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QModelIndex, Qt
import pandas as pd

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
    
    def rowCount(self, index):
        return self._data.shape[0]
    
    def columnCount(self, index):
        return self._data.shape[1]
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section]) 
            
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section]) 


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Решалка СЛАУ")
    
        button_layout = QtWidgets.QVBoxLayout()

        self.button_solve_slau = QtWidgets.QPushButton("Решить СЛАУ")
        self.button_save_slau = QtWidgets.QPushButton("Сохранить СЛАУ")
        self.button_load_slau = QtWidgets.QPushButton("Загрузить СЛАУ")
        self.button_set_solutions = QtWidgets.QPushButton("Задать количество решений")
        self.button_set_equations = QtWidgets.QPushButton("Задать количество уравнений")

        button_layout.addWidget(self.button_solve_slau)
        button_layout.addWidget(self.button_save_slau)
        button_layout.addWidget(self.button_load_slau)
        button_layout.addWidget(self.button_set_solutions)
        button_layout.addWidget(self.button_set_equations)

        #self.setCentralWidget(self.button_layout)

        table_layout = QtWidgets.QVBoxLayout()

        self.table = QtWidgets.QTableView()

        data = pd.DataFrame(
            [[1, 2, 2, 4, 1],
            [1, 2, 2, 4, 1],
            [1, 2, 2, 4, 1]], 
            columns=['a', 'b', 'c', 'e', 'f'], 
            index = ['1.1', '1.2', '1.3']
        )

        self.model = TableModel(data)
        self.table.setModel(self.model)

        #self.setCentralWidget(self.table)

        table_layout.addWidget(self.table)

        self.setLayout(table_layout)
    



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()