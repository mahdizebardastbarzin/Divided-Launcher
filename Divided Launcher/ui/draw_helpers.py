# -*- coding: utf-8 -*-
"""
draw_helpers.py
توابع کمکی برای رسم عناصر UI، متن‌ها، رنگ‌ها و افکت‌ها.
می‌تواند توسط PaintManager یا سایر ماژول‌ها استفاده شود.
"""

from PyQt6.QtGui import QColor, QFont
import random

def random_glitch_offset(max_offset=1):
    """
    تولید یک عدد تصادفی کوچک برای افکت glitch
    :param max_offset: حداکثر تغییر
    :return: عدد صحیح بین -max_offset تا +max_offset
    """
    return random.randint(-max_offset, max_offset)

def draw_colored_text(painter, x, y, text, color=None, font=None):
    """
    رسم متن با رنگ و فونت مشخص
    :param painter: QPainter
    :param x: موقعیت X
    :param y: موقعیت Y
    :param text: متن
    :param color: QColor
    :param font: QFont
    """
    if color:
        painter.setPen(color)
    if font:
        painter.setFont(font)
    painter.drawText(x, y, text)

def draw_matrix_column(painter, x, start_y, num_chars=15, char_set='01', color=QColor(0, 255, 0), spacing=12):
    """
    رسم یک ستون ماتریکس از کاراکترها
    :param painter: QPainter
    :param x: موقعیت X
    :param start_y: موقعیت Y شروع
    :param num_chars: تعداد کاراکترها
    :param char_set: مجموعه کاراکترها
    :param color: QColor
    :param spacing: فاصله بین خطوط
    """
    painter.setPen(color)
    for i in range(num_chars):
        y_pos = start_y + i * spacing
        painter.drawText(x, y_pos, random.choice(char_set))

def format_number(value, decimals=2):
    """
    فرمت عدد با جداکننده هزار و تعداد اعشار مشخص
    :param value: عدد
    :param decimals: تعداد اعشار
    :return: رشته فرمت‌شده
    """
    try:
        return f"{value:,.{decimals}f}"
    except:
        return str(value)
