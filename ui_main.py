import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
)
from PyQt5.QtGui import QFont
import os


class WordApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("背单词小助手")
        self.setFixedSize(400, 300)

        # 主容器
        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.layout = QVBoxLayout()
        self.container.setLayout(self.layout)

        # 顶部按钮
        self.btn_layout = QHBoxLayout()
        self.btn_review = QPushButton("背单词")
        self.btn_store = QPushButton("存储单词")
        self.btn_layout.addWidget(self.btn_review)
        self.btn_layout.addWidget(self.btn_store)

        self.layout.addLayout(self.btn_layout)

        # 页面切换
        self.review_widget = self.create_review_page()
        self.store_widget = self.create_store_page()
        self.layout.addWidget(self.review_widget)
        self.layout.addWidget(self.store_widget)

        self.btn_review.clicked.connect(self.show_review_page)
        self.btn_store.clicked.connect(self.show_store_page)

        self.show_review_page()

    def create_review_page(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.word_label = QLabel("点击按钮开始背单词")
        self.word_label.setFont(QFont("Arial", 14))
        self.word_label.setStyleSheet("color: #333;")
        layout.addWidget(self.word_label)

        self.meaning_label = QLabel("")
        self.meaning_label.setFont(QFont("Arial", 12))
        self.meaning_label.setStyleSheet("color: #666;")
        layout.addWidget(self.meaning_label)

        nav_layout = QHBoxLayout()
        self.btn_prev = QPushButton("上一个")
        self.btn_next = QPushButton("下一个")
        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.btn_next)
        layout.addLayout(nav_layout)

        self.btn_prev.clicked.connect(self.prev_word)
        self.btn_next.clicked.connect(self.next_word)

        widget.setLayout(layout)

        self.words = self.load_words()
        self.current_index = 0
        if self.words:
            self.display_word()

        return widget

    def create_store_page(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.input_word = QLineEdit()
        self.input_word.setPlaceholderText("输入英文单词")
        self.input_meaning = QLineEdit()
        self.input_meaning.setPlaceholderText("输入中文意思")
        self.btn_add = QPushButton("添加单词")
        self.status_label = QLabel("")

        layout.addWidget(self.input_word)
        layout.addWidget(self.input_meaning)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.status_label)

        self.btn_add.clicked.connect(self.add_word)

        widget.setLayout(layout)
        return widget

    def show_review_page(self):
        self.review_widget.show()
        self.store_widget.hide()

    def show_store_page(self):
        self.store_widget.show()
        self.review_widget.hide()

    def load_words(self):
        if not os.path.exists("words.txt"):
            return []
        with open("words.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        words = [line.strip().split(",") for line in lines if "," in line]
        print(words)
        return words

    def display_word(self):
        if not self.words:
            self.word_label.setText("暂无单词")
            self.meaning_label.setText("")
            return
        word, meaning = self.words[self.current_index]
        self.word_label.setText(f"{word}")
        self.meaning_label.setText(f"{meaning}")

    def next_word(self):
        if not self.words:
            return
        self.current_index = (self.current_index + 1) % len(self.words)
        self.display_word()

    def prev_word(self):
        if not self.words:
            return
        self.current_index = (self.current_index - 1) % len(self.words)
        self.display_word()

    def add_word(self):
        word = self.input_word.text().strip()
        meaning = self.input_meaning.text().strip()
        if not word or not meaning:
            self.status_label.setText("请输入完整信息")
            return
        with open("words.txt", "a", encoding="utf-8") as f:
            f.write(f"{word},{meaning}\n")
        self.status_label.setText("添加成功！")
        self.input_word.clear()
        self.input_meaning.clear()
        self.words = self.load_words()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WordApp()
    win.show()
    sys.exit(app.exec_())
