import sys
import typing
from typing import Any
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QModelIndex, Qt
import pandas as pd

import qdarktheme
from numpy import empty
from random import random

import json
import socket

HOST = '127.0.0.1'
PORT = 6666
LENGTH_BUFFER = 10**8

class CustomDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Предупреждение!")

        QBtn = QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Некоторые данные могут быть потеряны")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class TableModel2D(QtCore.QAbstractTableModel):
    def __init__(self, data, headerdata, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data
        self._headerdata = headerdata

    def rowCount(self, parent):
        return len(self._data)
    
    def columnCount(self, parent):
        return len(self._data[0])

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data[index.row()][index.column()]
                return value
            
    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole and index.isValid():
            self._data[index.row()][index.column()] = value
            return True
        return False
    
    def headerData(self, col, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._headerdata[col]
    
    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable 

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, headerdata, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data
        self._headerdata = headerdata

    def rowCount(self, parent):
        return 1
    
    def columnCount(self, parent):
        return len(self._data)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data[index.column()]
                return value
            
    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole and index.isValid():
            self._data[index.column()] = value
            return True
        return False
    
    def headerData(self, col, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._headerdata[col]
    
    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable 


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        qdarktheme.setup_theme()

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
        self.button_set_unknowns = QtWidgets.QPushButton("Задать количество неизвестных")
        self.button_set_equations = QtWidgets.QPushButton("Задать количество уравнений")

        self.button_layout.addWidget(self.button_solve_slau)
        #self.button_layout.addWidget(self.button_save_slau)
        #self.button_layout.addWidget(self.button_load_slau)
        self.button_layout.addWidget(self.button_set_unknowns)
        self.button_layout.addWidget(self.button_set_equations)


        self.slau_layout = QtWidgets.QVBoxLayout()

        # матрица с коэффициентами

        self.coefs_table = QtWidgets.QTableView()

        #self.coefs = pd.DataFrame()
        
        self.header_coefs = [
            'x1', 'x2', 'x3', 'x4', 'b'
        ]
    
        
        self.coefs = [
            [1.0, 2.0, 2.0, 4.0, 9.0],
            [1.0, 56.0, 2.0, 4.0, 1.0],
            [1.0, 4.0, 2.0, 4.0, 1.0]
        ]            
        

        self.coefs_model = TableModel2D(self.coefs, self.header_coefs)
        self.coefs_table.setModel(self.coefs_model)

        self.coefs_lable = QtWidgets.QLabel(self)
        self.coefs_lable.setText("Коэффициенты СЛАУ")

        self.slau_layout.addWidget(self.coefs_lable)
        self.slau_layout.addWidget(self.coefs_table)

        # матрица с решениями

        self.solves_table = QtWidgets.QTableView()

        self.header_solves = [
            'x1', 'x2', 'x3', 'x4'
        ]

        self.solves = [
            [1.0, 2.0, 2.0, 4.0]
        ]
         

        self.solves_model = TableModel(self.solves, self.header_solves)
        self.solves_table.setModel(self.solves_model)

        self.solves_lable = QtWidgets.QLabel(self)
        self.solves_lable.setText("Решение СЛАУ")

        self.slau_layout.addWidget(self.solves_lable)
        self.slau_layout.addWidget(self.solves_table)


        self.main_layout.addLayout(self.slau_layout)
        self.main_layout.addLayout(self.button_layout)

        self.connect_buttons()

        self.setLayout(self.main_layout)
    
    def connect_buttons(self):
        self.button_set_unknowns.clicked.connect(self.set_unknowns)
        self.button_set_equations.clicked.connect(self.set_equations)
        self.button_solve_slau.clicked.connect(self.solve_slau)

    def set_unknowns(self):
        unknowns, ok = QtWidgets.QInputDialog.getInt(self, "Установить количество решений", "Введите количество решений", min=1)
        
        if ok:
            if unknowns < len(self.coefs[0]) - 1:
                print('Warning: some date will be lost')

                dlg = CustomDialog()

                if dlg.exec():
                    self.change_unknowns(unknowns) 
                else:
                    print("nope")
            else:   
                self.change_unknowns(unknowns)

    def change_unknowns(self, unknowns):
        if len(self.coefs_model._data) != 0:
            equations = len(self.coefs_model._data)

        print(unknowns)
        print(equations)

        temp = [[0.0 for col in range(unknowns + 1)] for row in range(equations)]
        print(temp)

        if unknowns + 1 == len(self.coefs_model._data[0]):
            print('equal')
            return
        
        if unknowns + 1 > len(self.coefs_model._data[0]):
            print('+')
            for i in range(equations):
                for j in range(len(self.coefs_model._data[0]) - 1):
                    temp[i][j] = self.coefs_model._data[i][j]

            for i in range(equations):
                temp[i][unknowns] = self.coefs_model._data[i][len(self.coefs_model._data[0]) - 1]
        
        else:
            for i in range(equations):
                for j in range(unknowns):
                    temp[i][j] = self.coefs_model._data[i][j]

            for i in range(equations):
                temp[i][unknowns] = self.coefs_model._data[i][len(self.coefs_model._data[0]) - 1]
            print('-')

        header_temp = []
        for i in range(unknowns):
            header_temp += ['x' + str(i + 1)]
        header_temp += ['b']

        print(self.coefs_model._data)
        print(temp)     
        
        self.coefs_model._headerdata = header_temp
        self.coefs_model._data = temp
        self.coefs_model.layoutChanged.emit()

    def set_equations(self):
        equations, ok = QtWidgets.QInputDialog.getInt(self, "Установить количество кравнений", "Введите количество уравнений", min=1)
        
        if ok:
            if equations < len(self.coefs_model._data):
                print('Warning: some date will be lost')

                dlg = CustomDialog()

                if dlg.exec():
                    self.change_equations(equations) 
                else:
                    print("nope")
            else:   
                self.change_equations(equations)
        
    def change_equations(self, equations):
        if len(self.coefs_model._data) != 0:
            unknowns = len(self.coefs_model._data[0])

        print(unknowns)
        print(equations)

        temp = [[0.0 for col in range(unknowns)] for row in range(equations)]

        if equations == len(self.coefs_model._data):
            print('equal')
            return
        
        if equations > len(self.coefs_model._data):
            print('+')
            for i in range(len(self.coefs_model._data)):
                for j in range(unknowns):
                    temp[i][j] = self.coefs_model._data[i][j]
        
        else:
            print('-')
            for i in range(equations):
                for j in range(unknowns):
                    temp[i][j] = self.coefs_model._data[i][j]

        self.coefs_model._data = temp
        self.coefs_model.layoutChanged.emit()

    def solve_slau(self):
        print('solving slau')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            N = len(self.coefs_model._data[0])
            M = len(self.coefs_model._data)

            coefs = ''
            for i in range(M):
                for j in range(N - 1):
                    coefs += str(self.coefs_model._data[i][j]) + ' '

            coefs_free = ''
            for i in range(M):
                coefs_free += str(self.coefs_model._data[i][N - 1]) + ' '

            print(coefs)
            print(coefs_free)

            
            message = {
                "task" : "solve", 
                "column" : N - 1,
                "row" : M,
                "coefs" : coefs.strip(),
                "coefs_free" : coefs_free.strip()
            }

            data = json.dumps(message)
            s.sendall((bytes(data, encoding="utf-8")))

            request = json.loads(s.recv(LENGTH_BUFFER).decode("utf8"))
            print(request)

            print(request["column"])
            print(request["solutions"])

            header_temp = []
            for i in range(request["column"]):
                header_temp += ['x' + str(i + 1)]

            print(header_temp)

            temp = []
            for i in  request["solutions"]:
                temp += [float(i)]

            print(temp)

            self.solves_model._headerdata = header_temp
            self.solves_model._data = temp
            self.solves_model.layoutChanged.emit()

            #s.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()