#!/usr/bin/python3
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import  QStandardItemModel, QStandardItem, QFont, QIcon
import gui
import os

from PyQt5.QtWidgets import QSizePolicy

import sqlite3

class ExampleApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):

        super().__init__()
        self.setupUi(self)

        self.CURRENT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        self.ASSETS_DIR = (os.path.join(self.CURRENT_DIR,'assets/'))
        self.DATA_DIR = (os.path.join(self.CURRENT_DIR,'data/'))


        self.centralwidget.setLayout(self.horizontalLayout)

        self.create_toolbar_items()
        self.fill_treeview_from_db()


        self.treeView.clicked.connect(self.getValue)

    def fill_treeview_from_db(self):

        self.conn = sqlite3.connect(os.path.join(self.DATA_DIR,'func.db'))
        self.cursor = self.conn.cursor()
        
        self.treeModel = QStandardItemModel()
        rootNode = self.treeModel.invisibleRootItem()

        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) # TreeView ReadOnly

        self.main_treeItem = QStandardItem('C stdlib')


        self.cursor.execute('SELECT DISTINCT chapter from funcs')
        chapters = self.cursor.fetchall()

        for chapter in chapters:
            func = QStandardItem(chapter[0])
        
            self.cursor.execute('SELECT name from funcs WHERE chapter = ?',(chapter[0],))
            results = self.cursor.fetchall()
            for result in results:
                func.appendRow(QStandardItem(result[0]))
            
            self.main_treeItem.appendRow(func)


        rootNode.appendRow(self.main_treeItem)

        self.treeView.setModel(self.treeModel)
        
        pass

    def closeEvent(self, event):
        print('Exit')

    def getValue(self, val):

        self.cursor.execute('SELECT content FROM funcs WHERE name = ?',(val.data(),))
        x = self.cursor.fetchone()
        # TODO Обработать исключение
        self.textBrowser.setText(x[0])

    def create_toolbar_items(self):
        collapse_button = QtWidgets.QToolButton()
        collapse_button.setIcon(QIcon(os.path.join(self.ASSETS_DIR,'collapse.png')))
        collapse_button.clicked.connect(lambda: self.treeView.collapseAll())
        self.toolBar.addWidget(collapse_button)

        expand_button = QtWidgets.QToolButton()
        expand_button.setIcon(QIcon(os.path.join(self.ASSETS_DIR,'expand.png')))
        expand_button.clicked.connect(lambda: self.treeView.expandAll())
        self.toolBar.addWidget(expand_button)

        self.toolBar.addSeparator()

        self.search_box = QtWidgets.QLineEdit()
        self.search_box.setMaximumSize(200,100)
        self.search_box.setPlaceholderText('Поиск...')
        # self.search_box.textChanged.connect(self.search)
        self.toolBar.addWidget(self.search_box)
        
        self.clear_button = QtWidgets.QToolButton()
        self.clear_button.setIcon(QIcon(os.path.join(self.ASSETS_DIR,'clear.png')))
        self.clear_button.clicked.connect(self.clear_searchBox)
        self.toolBar.addWidget(self.clear_button)
        self.toolBar.addSeparator()

        self.zoom_fit_button = QtWidgets.QToolButton()
        self.zoom_fit_button.clicked.connect(self.zoom_fit)
        self.zoom_fit_button.setIcon(QIcon(os.path.join(self.ASSETS_DIR,'zoom-fit.png')))
        self.toolBar.addWidget(self.zoom_fit_button) 

        self.zoom_out_button = QtWidgets.QToolButton()
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.zoom_out_button.setIcon(QIcon(os.path.join(self.ASSETS_DIR,'zoom-out.png')))
        self.toolBar.addWidget(self.zoom_out_button)

        self.zoom_in_button = QtWidgets.QToolButton()
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_in_button.setIcon(QIcon(os.path.join(self.ASSETS_DIR,'zoom-in.png')))
        self.toolBar.addWidget(self.zoom_in_button)

    def search(self):
        # select name from funcs where name like '%print%'
        # BUG Исправить поиск
        self.treeView.setModel(None)
        self.treeView.setModel(self.treeModel)
        if self.search_box.text():
            self.cursor.execute('SELECT name from funcs WHERE name like ?',('%'+self.search_box.text()+'%',))
            result = self.cursor.fetchall()
            print(result)
            for x in result:
                self.main_treeItem.appendRow(QStandardItem(x[0]))

    def zoom_in(self):
        font_size = self.textBrowser.fontInfo().pointSize()
        font = QFont()
        font.setPointSize(font_size+1)
        self.textBrowser.setFont(font)

    def zoom_out(self):
        font_size = self.textBrowser.fontInfo().pointSize()
        font = QFont()
        font.setPointSize(font_size-1)
        self.textBrowser.setFont(font)


    def zoom_fit(self):
        font = QFont()
        font.setPointSize(10)
        self.textBrowser.setFont(font)        

    def clear_searchBox(self):
        self.search_box.setText('')
        self.fill_treeview_from_db()





def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()