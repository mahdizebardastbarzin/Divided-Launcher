# -*- coding: utf-8 -*-
import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter, QFont, QColor

class MatrixLauncher(QWidget):
    def __init__(self):
        super().__init__()

        self.cols = 50  # تعداد ستون‌ها
        self.char_height = 15
        self.chars = ['0','1','2','3','4','5','6','7','8','9',
                      '@','#','$','%','&','*','+','-','=','?']

        # هر ستون خودش یه لیست از کاراکترها داره
        self.columns = []
        for _ in range(self.cols):
            length = random.randint(5, 20)  # طول ستون
            start_pos = random.randint(0, 40)  # شروع رندوم از پایین صفحه
            self.columns.append({
                "length": length,
                "position": start_pos,
                "chars": [random.choice(self.chars) for _ in range(length)],
                "speed": random.randint(1, 3)  # سرعت متفاوت برای هر ستون
            })

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Matrix Launcher")
        self.showFullScreen()
        self.setStyleSheet("background-color: black;")

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateMatrix)
        self.timer.start(100)  # سرعت تایپ

    def updateMatrix(self):
        for col in self.columns:
            col["position"] += col["speed"]
            if col["position"] > (self.height() // self.char_height):
                col["position"] = 0
                col["chars"] = [random.choice(self.chars) for _ in range(col["length"])]
            else:
                # هر بار یک کاراکتر جدید رندوم اضافه می‌کنه
                col["chars"].append(random.choice(self.chars))
                if len(col["chars"]) > col["length"]:
                    col["chars"].pop(0)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(QFont("Consolas", 12))

        for i, col in enumerate(self.columns):
            painter.setPen(QColor(0, 255, 0))
            for j, char in enumerate(col["chars"]):
                y = self.height() - (col["position"] - j) * self.char_height
                if 0 <= y <= self.height():
                    painter.drawText(i*15, y, char)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = MatrixLauncher()
    launcher.show()
    sys.exit(app.exec())
