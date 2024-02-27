import os
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/Main.ui", self)
        self.init_ui()

    def init_ui(self):
        # Предполётная подготовка
        menu = self.menuBar()
        gym = menu.addMenu('Тренажёры')
        self.newAction = gym.addAction("Редактирование списка тренажёров")
        gym.triggered.connect(self.show_window2)
        # Загрузка списка тренажёров
        if not os.path.isdir("Exercises"):
            os.mkdir("Exercises")
        # чтение txt в котором прописаны тренажёры

    def show_window2(self):
        self.w2 = Window2()
        self.w2.show()


class Window2(QMainWindow):
    def __init__(self):
        super(Window2, self).__init__()
        uic.loadUi('UI/untitled.ui', self)
        # self.pushButton.clicked.connect()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
