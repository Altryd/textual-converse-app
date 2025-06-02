import ollama
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QTextEdit
import sys  # Только для доступа к аргументам командной строки


# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.history = []
        self.model = 'llama3'
        self.setWindowTitle("Dialogue")
        font = QFont()
        font.setPointSize(12)

        self.history_view = QTextEdit()
        self.history_view.setReadOnly(True)
        self.history_view.setFont(font)

        self.input = QLineEdit()
        self.input.setFont(font)
        self.input.setPlaceholderText("Введите ваш запрос...")
        self.input.returnPressed.connect(self.send_text)  # При нажатии на Enter посылается текст (VAC!)

        button_send = QPushButton("Send text")
        # button_send.setCheckable(True)
        button_send.clicked.connect(self.send_text)

        button_clear = QPushButton("Clear history")
        # button_clear.setCheckable(True)
        button_clear.clicked.connect(self.clear_history)

        layout = QVBoxLayout()
        layout.addWidget(button_clear)

        # layout.addWidget(self.label)
        layout.addWidget(self.history_view)
        layout.addWidget(self.input)
        layout.addWidget(button_send)


        self.setMinimumSize(QSize(500, 400))

        container = QWidget()
        container.setLayout(layout)


        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(container)

    def chat(self):
        response = ollama.chat(
            model=self.model,
            messages=self.history
        )
        return response['message']['content']

    def clear_history(self):
        self.history.clear()
        print("history is cleared!")
        self.history_view.clear()

    def send_text(self):
        text = self.input.text()
        self.history.append({'role': 'user', 'content': text})
        self.input.clear()

        self.history_view.setText(self.get_history_view())
        try:
            response = self.chat()
            self.history.append({'role': 'assistant', 'content': response})
            self.history_view.setText(self.get_history_view())
            print(response)
        except Exception as e:
            self.history.append(
                {'role': 'assistant', 'content': f"Ошибка: {str(e)} ! Убедитесь, что сервер ollama запущен."})

    def get_history_view(self):
        string_to_show = ""
        for entry in self.history:
            if entry['role'] == 'user':
                string_to_show += "[Пользователь]: " + entry['content'] + "\n"
            elif entry['role'] == 'assistant':
                string_to_show += "[Модель]: " + entry['content'] + "\n"
        return string_to_show


# Приложению нужен один (и только один) экземпляр QApplication.
# Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
# Если не будете использовать аргументы командной строки, QApplication([]) тоже работает
app = QApplication(sys.argv)

# Создаём виджет Qt — окно.
window = MainWindow()
window.show()  # Важно: окно по умолчанию скрыто.

# Запускаем цикл событий.
app.exec()


# Приложение не доберётся сюда, пока вы не выйдете и цикл
# событий не остановится.
