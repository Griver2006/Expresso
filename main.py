import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


con = sqlite3.connect('coffe.sqlite')
cur = con.cursor()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.load_table()

    def load_table(self):
        data = cur.execute(f"""SELECT main.ID, main.specie, main.grade, grind.type,
                               main.taste, main.price, main.volume FROM main
                               JOIN grind ON grind.ID = main.grind""").fetchall()

        # Загрузка таблицы
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "название сорта", "степень обжарки",
                                                    "молотый/в зернах", "описание вкуса",
                                                    "цена", "объем упаковки"])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_menu_window = MainWindow()
    main_menu_window.show()
    sys.exit(app.exec())