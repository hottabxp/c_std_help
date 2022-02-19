import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import  QStandardItemModel, QStandardItem, QFont, QIcon
import gui

from PyQt5.QtWidgets import QSizePolicy

import sqlite3

class ExampleApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):

        super().__init__()
        self.setupUi(self)

        self.centralwidget.setLayout(self.horizontalLayout)

        self.create_toolbar_items()

        

        self.conn = sqlite3.connect('func.db')
        self.cursor = self.conn.cursor()
        
        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()

        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        main_treeItem = QStandardItem('C stdlib')


        self.cursor.execute('SELECT DISTINCT chapter from funcs')
        chapters = self.cursor.fetchall()

        for chapter in chapters:
            func = QStandardItem(chapter[0])
        
            self.cursor.execute('SELECT name from funcs WHERE chapter = ?',(chapter[0],))
            results = self.cursor.fetchall()
            for result in results:
                func.appendRow(QStandardItem(result[0]))
            
            main_treeItem.appendRow(func)


        rootNode.appendRow(main_treeItem)

        self.treeView.setModel(treeModel)
        # self.treeView.expandAll()
        


        self.treeView.clicked.connect(self.getValue)

    def closeEvent(self, event):
        print('Exit')

    def getValue(self, val):

        self.cursor.execute('SELECT content FROM funcs WHERE name = ?',(val.data(),))
        x = self.cursor.fetchone()
        # TODO Обработать исключение
        self.textBrowser.setText(x[0])

    def create_toolbar_items(self):
        collapse_button = QtWidgets.QToolButton()
        collapse_button.setIcon(QIcon('./assets/collapse.png'))
        collapse_button.clicked.connect(lambda: self.treeView.collapseAll())
        self.toolBar.addWidget(collapse_button)

        expand_button = QtWidgets.QToolButton()
        expand_button.setIcon(QIcon('./assets/expand.png'))
        expand_button.clicked.connect(lambda: self.treeView.expandAll())
        self.toolBar.addWidget(expand_button)

        self.toolBar.addSeparator()

        self.search_box = QtWidgets.QLineEdit()
        self.search_box.setMaximumSize(200,100)
        self.toolBar.addWidget(self.search_box)
        
        self.search_button = QtWidgets.QToolButton()
        self.search_button.setIcon(QIcon('./assets/clear.png'))
        self.search_button.clicked.connect(self.clear_searchBox)
        self.toolBar.addWidget(self.search_button)
        self.toolBar.addSeparator()

        self.zoom_fit_button = QtWidgets.QToolButton()
        self.zoom_fit_button.clicked.connect(self.zoom_fit)
        self.zoom_fit_button.setIcon(QIcon('./assets/zoom-fit.png'))
        self.toolBar.addWidget(self.zoom_fit_button) 

        self.zoom_out_button = QtWidgets.QToolButton()
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.zoom_out_button.setIcon(QIcon('./assets/zoom-out.png'))
        self.toolBar.addWidget(self.zoom_out_button)

        self.zoom_in_button = QtWidgets.QToolButton()
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_in_button.setIcon(QIcon('./assets/zoom-in.png'))
        self.toolBar.addWidget(self.zoom_in_button)


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





def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()