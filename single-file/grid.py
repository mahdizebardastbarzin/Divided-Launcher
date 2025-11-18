# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt

class DividedScreen(QWidget):
    # رنگ‌های هر بخش و ردیف‌ها
    section_rows = {
        1: [QColor(200, 30, 30), QColor(180, 30, 30), QColor(160, 30, 30)],  # بخش 1، 3 ردیف
        2: [QColor(30, 200, 30), QColor(30, 180, 30)],                       # بخش 2، 2 ردیف
        3: [QColor(30, 30, 200), QColor(30, 30, 180)],                       # بخش 3، 2 ردیف
        4: [QColor(200, 200, 30), QColor(180, 180, 30)],                     # بخش 4، 2 ردیف
        5: [QColor(200, 30, 200), QColor(180, 30, 180), QColor(160, 30, 160)] # بخش 5، 3 ردیف
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Divided Launcher")
        self.showFullScreen()

    def paintEvent(self, event):
        painter = QPainter(self)
        w = self.width()
        h = self.height()

        section_width = w // 5

        # رسم بخش 1 (3 ردیف)
        for j, color in enumerate(self.section_rows[1]):
            row_height = h // 3
            y = j * row_height
            painter.fillRect(0, y, section_width, row_height, color)
            painter.setPen(Qt.GlobalColor.white)
            painter.drawText(20, y + 30, f"S1R{j+1}")

        # رسم بخش‌های 2+3+4 ادغام شده (2 ردیف)
        merged_width = section_width * 3
        for j in range(2):
            # رنگ متوسط برای ادغام (می‌تونی هر رنگی که می‌خوای بده)
            if j == 0:
                color = QColor(60, 80, 160)  # رنگ دلخواه ردیف اول ادغام
            else:
                color = QColor(100, 120, 200) # رنگ ردیف دوم ادغام
            row_height = h // 2
            y = j * row_height
            painter.fillRect(section_width, y, merged_width, row_height, color)
            painter.setPen(Qt.GlobalColor.white)
            painter.drawText(section_width + 20, y + 30, f"Merged R{j+1}")

        # رسم بخش 5 (3 ردیف)
        for j, color in enumerate(self.section_rows[5]):
            row_height = h // 3
            y = j * row_height
            painter.fillRect(section_width*4, y, section_width, row_height, color)
            painter.setPen(Qt.GlobalColor.white)
            painter.drawText(section_width*4 + 20, y + 30, f"S5R{j+1}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = DividedScreen()
    screen.show()
    sys.exit(app.exec())
