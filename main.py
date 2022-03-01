import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget
from main_ui import Ui_MainWindow
from addEditCoffeeForm import Ui_Form

con = sqlite3.connect('data/coffe.sqlite')
cur = con.cursor()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_table()
        self.btn_add_edit.clicked.connect(self.open_window_add_edit)

    def open_window_add_edit(self):
        if self.tableWidget.selectedItems():
            data = cur.execute(f"""SELECT main.ID, main.specie, main.grade, grind.type,
                                   main.taste, main.price, main.volume FROM main
                                   JOIN grind ON grind.ID = main.grind
                                   WHERE main.ID={self.tableWidget.selectedItems()[0].row() + 1}""").fetchone()
            self.change_element_window = AddEditWindow(data)
            self.change_element_window.show()
        else:
            self.add_element_window = AddEditWindow()
            self.add_element_window.show()

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


class AddEditWindow(QWidget, Ui_Form):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        for typ in cur.execute('SELECT type FROM grind'):
            self.comboBox_grind.addItem(typ[0])
        if args:
            self.id = args[0][0]
            self.load_data(args[0])
            self.btn_add.clicked.connect(self.edit)
        else:
            self.btn_add.clicked.connect(self.add)

    def load_data(self, args):
        self.lineEdit_specie.setText(args[1])
        self.lineEdit_grade.setText(args[2])
        self.comboBox_grind.setCurrentText(args[3])
        self.lineEdit_taste.setText(args[4])
        self.lineEdit_price.setText(str(args[5]))
        self.lineEdit_volume.setText(str(args[6]))

    def add(self):
        try:
            specie = self.lineEdit_specie.text()
            grade = self.lineEdit_grade.text()
            grind = int(cur.execute(f'''SELECT ID FROM grind
                                    WHERE type = "{self.comboBox_grind.currentText()}"'''
                                    ).fetchone()[0])
            taste = self.lineEdit_taste.text()
            price = int(self.lineEdit_price.text())
            volume = int(self.lineEdit_volume.text())
            if price < 0 or volume < 0:
                self.label_error.setText('Неправильно заполнена форма')
                return
        except ValueError:
            self.label_error.setText('Неправильно заполнена форма')
            return
        values = [specie, grade, grind, taste, price, volume]
        cur.execute(f'''INSERT INTO main(specie, grade, grind, taste, price, volume) VALUES(?,?,?,?,?,?)''',
                    values)
        cur.connection.commit()
        main_menu_window.load_table()
        self.close()

    def edit(self):
        try:
            specie = self.lineEdit_specie.text()
            grade = self.lineEdit_grade.text()
            grind = int(cur.execute(f'''SELECT ID FROM grind
                                    WHERE type = "{self.comboBox_grind.currentText()}"'''
                                    ).fetchone()[0])
            taste = self.lineEdit_taste.text()
            price = int(self.lineEdit_price.text())
            volume = int(self.lineEdit_volume.text())
            if price < 0 or volume < 0:
                self.label_error.setText('Неправильно заполнена форма')
                return
        except ValueError:
            self.label_error.setText('Неправильно заполнена форма')
            return
        values = [specie, grade, grind, taste, price, volume, self.id]
        cur.execute(f'''UPDATE main SET specie=?, grade=?, grind=?, taste=?, price=?, volume=? WHERE ID=?''',
                    values)
        cur.connection.commit()
        main_menu_window.load_table()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_menu_window = MainWindow()
    main_menu_window.show()
    sys.exit(app.exec())