import sys
import typing
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QModelIndex, Qt
import pandas as pd

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def rowCount(self, index):
        return self._data.shape[0]
    
    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)
            
    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            return True
        return False

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
    
    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable 


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.draw_gui()

    def draw_gui(self):

        self.setWindowTitle("Решалка СЛАУ")
        self.resize(1024, 768)

        self.main_layout = QtWidgets.QHBoxLayout()
    
        # кнопки

        self.button_layout = QtWidgets.QVBoxLayout()

        self.button_solve_slau = QtWidgets.QPushButton("Решить СЛАУ")
        self.button_save_slau = QtWidgets.QPushButton("Сохранить СЛАУ")
        self.button_load_slau = QtWidgets.QPushButton("Загрузить СЛАУ")
        self.button_set_solutions = QtWidgets.QPushButton("Задать количество решений")
        self.button_set_equations = QtWidgets.QPushButton("Задать количество уравнений")

        self.button_layout.addWidget(self.button_solve_slau)
        self.button_layout.addWidget(self.button_save_slau)
        self.button_layout.addWidget(self.button_load_slau)
        self.button_layout.addWidget(self.button_set_solutions)
        self.button_layout.addWidget(self.button_set_equations)


        self.slau_layout = QtWidgets.QVBoxLayout()

        # матрица с коэффициентами

        self.coefs_table = QtWidgets.QTableView()

        self.coefs = pd.DataFrame(
            [[1, 2, 2, 4, 1],
            [1, 2, 2, 4, 1],
            [1, 2, 2, 4, 1]], 
            columns=['x1', 'x2', 'x3', 'x4', 'b']            
        )

        self.coefs_model = TableModel(self.coefs)
        self.coefs_table.setModel(self.coefs_model)

        self.coefs_lable = QtWidgets.QLabel(self)
        self.coefs_lable.setText("Коэффициенты СЛАУ")

        self.slau_layout.addWidget(self.coefs_lable)
        self.slau_layout.addWidget(self.coefs_table)

        # матрица с решениями

        self.solves_table = QtWidgets.QTableView()

        self.solves = pd.DataFrame(
            [[1, 2, 2, 4]],
            columns=['x1', 'x2', 'x3', 'x4']            
        )

        self.solves_model = TableModel(self.solves)
        self.solves_table.setModel(self.solves_model)

        self.solves_lable = QtWidgets.QLabel(self)
        self.solves_lable.setText("Решение СЛАУ")

        self.slau_layout.addWidget(self.solves_lable)
        self.slau_layout.addWidget(self.solves_table)


        self.main_layout.addLayout(self.slau_layout)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
    




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()