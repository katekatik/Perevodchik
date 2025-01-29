import requests
import sys
import json
import pyperclip
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Window1(QWidget): # Создаем класс от родителя QWidget - это будет наше первое окно.
    def __init__(self):
        super().__init__() # Наследуем методы и атрибуты класса QWidget.

        self.setWindowTitle("Yandex.Perevod4ik")  # Называем наше окно.
        self.resize(1500, 800)  # Назначаем размер окна.
        self.setWindowIcon(QIcon('best_icon.png'))  # Выбираем иконку для нашего окна.
        self.setFont(QFont('Calibri', 15))  # Назначаем шрифт и размер шрифта.

        self.initUI()

    def initUI(self): # Основная функция для построения нашего окна.

        self.combobox1 = QComboBox()
        self.combobox1.addItems(["английский", "русский", "итальянский", "польский", "казахский"])
        self.combobox2 = QComboBox()
        self.combobox2.addItems(["русский", "английский", "итальянский", "польский", "казахский"])
        self.textedit = QPlainTextEdit()
        self.textedit2 = QPlainTextEdit()
        self.textedit2.setReadOnly(True)
        button1 = QPushButton("Перевести") # Создаем кнопку.
        button1.setStyleSheet("color: white; background-color: green; border-style: outset; border-width: 3px; border-radius: 10px; border-color: black; font: bold 24px; min-width: 5em; padding: 10px;")
        button1.clicked.connect(self.yandex)
        button2 = QPushButton(self) # Создаем кнопку.
        button2.setStyleSheet("background-color: white; border-style: outset; border-width: 3px; border-radius: 10px; border-color: black;")
        button2.setIcon(QIcon('deletion.png'))
        button2.setIconSize(QSize(65, 75))
        button2.setToolTip("Стереть данные")
        button2.clicked.connect(self.delete)
        self.show()
        button3 = QPushButton(self) # Создаем кнопку.
        button3.setIcon(QIcon('files.png'))
        button3.setIconSize(QSize(65, 75))
        button3.setToolTip("Скопировать перевод в буфер обмена")
        button3.clicked.connect(self.copy)
        button3.setStyleSheet("background-color: white; border-style: outset; border-width: 3px; border-radius: 10px; border-color: black;")
        self.show()
        button4 = QPushButton(self)  # Создаем кнопку.
        button4.setIcon(QIcon('txt-file.png'))
        button4.setIconSize(QSize(65, 75))
        button4.setToolTip("Скачать текстовый файл с переводом")
        button4.clicked.connect(self.download)
        button4.setStyleSheet("background-color: white; border-style: outset; border-width: 3px; border-radius: 10px; border-color: black;")
        self.show()

        main_layout = QVBoxLayout()

        groupbox = QGroupBox() # Создаем нашу группу.

        layout2 = QGridLayout()# Создаем дополнительную раскладку для того, чтобы сделать ее группой потом.
        layout2.addWidget(self.combobox1, 0, 0)
        layout2.addWidget(self.combobox2, 0, 1)
        layout2.addWidget(self.textedit, 1, 0)
        layout2.addWidget(self.textedit2, 1, 1)

        groupbox.setLayout(layout2) # Устанавливаем нашу раскладку в группу.

        main_layout.addWidget(groupbox)  # Добавляем группу как виджет.
        main_layout.addWidget(button1)

        layout3 = QHBoxLayout()
        layout3.addWidget(button2)
        layout3.addWidget(button3)
        layout3.addWidget(button4)
        main_layout.addLayout(layout3)

        self.setLayout(main_layout)

    def download(self):
        with open('translation.txt', 'w', encoding='utf8') as file:
            file.write(self.textedit2.toPlainText())
        QMessageBox.information(self, 'Получилось', 'Успешно обработано!')

    def delete(self):

        self.textedit.clear()
        self.textedit2.clear()

    def copy(self):

        pyperclip.copy(self.textedit2.toPlainText())
        QMessageBox.information(self, 'Получилось', 'Перевод скопирован в буфер обмена')

    def choose_language(self, combobox):
        if combobox.currentText() == "английский":
            language = "en"
        if combobox.currentText() == "русский":
            language = "ru"
        if combobox.currentText() == "итальянский":
            language = "it"
        if combobox.currentText() == "польский":
            language = "pl"
        if combobox.currentText() == "казахский":
            language = "kk"

        return language


    def yandex(self):

        IAM_TOKEN = 't1.123457nuHo3...' #здесь был токен (время действия истекло)
        folder_id = '...' #здесь был id папки в облаке Яндекса#
        target_language = self.choose_language(self.combobox2)
        source_language = self.choose_language(self.combobox1)
        texts = []
        texts.append(self.textedit.toPlainText())

        body = {
            "targetLanguageCode": target_language,
            "sourceLanguageCode": source_language,
            "texts": texts,
            "folderId": folder_id,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer t1.123457nuHo3...".format(
                IAM_TOKEN)
        }

        response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                 json=body,
                                 headers=headers
                                 )

        parsedData = json.loads(response.text)
        self.textedit2.setPlainText(parsedData["translations"][0]["text"])



    def closeEvent(self, event):  # Создаем кастомное событие выхода. Пользователю будет задан вопрос.
        reply = QMessageBox.question(self, 'Выход',
                                     "Вы уверены, что хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:  # Если юзер отвечает "да" -
            event.accept()  # то мы выходим.
        else:  # Если юзер отвечает "нет" -
            event.ignore()  # ничего не происходит.


def open_window(): # Наша функция для открытия приложения.
    app = QApplication(sys.argv) # Создаем наше приложение с аргументами из командной строки.
    wind = Window1() # Создаем экземпляр первого окна.
    wind.show() # Показываем наше окно.
    sys.exit(app.exec_()) # Заканчиваем работу приложения в случае выхода.

open_window()
