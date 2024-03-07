import os
import sys
import subprocess
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog


# Читаем из файла
def loadbd():
    file = open("data.txt", "r+", encoding='utf-8')
    datas = file.read()
    datas = datas.splitlines()
    file.close()
    data = {}
    for i in datas:
        i = i.split('#')
        data[int(i[0])] = {}
        data[int(i[0])]["name"] = i[1]
        data[int(i[0])]["exec_file"] = i[2]
        data[int(i[0])]["instr_file"] = i[3]
    return data


data = loadbd()


# Класс главного окна
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/Main.ui", self)
        # Добавление элементов отсутствующих в QT Designer
        menu = self.menuBar()
        gym = menu.addMenu('Тренажёры')
        self.newAction = gym.addAction("Редактирование списка тренажёров")
        gym.triggered.connect(self.show_window2)
        # Подготовка окна-предпросмотра
        pixmap = QPixmap("instruct/orig2.png")
        self.label.setPixmap(pixmap)
        # Проверка наличия папки с тренажёрами
        if not os.path.isdir("Exercises"):
            os.mkdir("Exercises")
        # Добавление тренажёров в список
        for i in data:
            self.listWidget_main.addItem(data[i]['name'])
        self.pushButton.clicked.connect(self.start_up)
        self.listWidget_main.itemPressed.connect(self.instr_change)
        # print(data)

    def start_up(self):
        print(self.listWidget_main.currentRow())

    def instr_change(self):
        pixmap = QPixmap(data[int(self.listWidget_main.currentRow())]["instr_file"])
        self.label.setPixmap(pixmap)
        print(self.listWidget_main.currentRow())

    def show_window2(self):
        self.w2 = Window2()
        self.w2.show()


# Класс дополнительного окна
class Window2(MainWindow):
    def __init__(self):
        super(Window2, self).__init__()
        uic.loadUi('UI/Redactor.ui', self)
        # Добавление элементов отсутствующих в QT Designer
        menu = self.menuBar()
        gym = menu.addMenu('Файл')
        self.newAction = gym.addAction("Сохранить")
        # Подключение кнопок
        self.browse_btn.clicked.connect(self.browse_exec)
        self.browse_btn2.clicked.connect(self.browse_instr)
        self.add_btn.clicked.connect(self.add_exercise)
        for i in data:
            self.listWidget_red.addItem(data[i]['name'])

    def browse_exec(self):
        exec_name = QFileDialog.getOpenFileName(self, 'Укажите тренажёр', "C:\ТРЕНИНГ")
        self.lineEdit_2.setText(exec_name[0])

    def browse_instr(self):
        instr_name = QFileDialog.getOpenFileName(self, 'Укажите инструкцию', "C:\ТРЕНИНГ")
        self.lineEdit_3.setText(instr_name[0])

    def add_exercise(self):
        if self.lineEdit.text() == '' or self.lineEdit_2.text() == '' or self.lineEdit_3.text() == '':
            self.statusBar.showMessage('Не все поля заполнены!', 5000)
        else:
            # Добавляем во вложенный словарь
            data[len(data)] = {}
            data[len(data) - 1]["name"] = self.lineEdit.text()
            data[len(data) - 1]["exec_file"] = self.lineEdit_2.text()
            data[len(data) - 1]["instr_file"] = self.lineEdit_3.text()
            print(data[len(data) - 1]["name"])
            # Добалвяем в оба списка
            self.listWidget_red.addItem(data[len(data) - 1]['name'])

    def del_exercise(self):
        pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
