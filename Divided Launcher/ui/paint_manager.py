# -*- coding: utf-8 -*-
"""
paint_manager.py
مدیریت رندر کل UI، شامل:
- رسم بخش‌ها (S1, S5 و merged R2)
- رسم اطلاعات سیستم
- رسم رمزارزها و نرخ ارز
- افکت‌های Matrix و Glitch
"""

from PyQt6.QtGui import QPainter, QColor, QFont, QFontMetrics
from PyQt6.QtCore import Qt
import random
from datetime import datetime
import jdatetime
from hijridate import Gregorian

class PaintManager:
    def __init__(self, parent):
        self.parent = parent

    def resize_widgets(self):
        w, h = self.parent.width(), self.parent.height()
        section_width = w // 5
        row_height = h // 2

        # مرورگر R1
        self.parent.browser_r1.setGeometry(section_width, 30, section_width*3, row_height - 30)
        # Address bar و دکمه‌ها
        self.parent.address_bar.setGeometry(section_width + 10, row_height, 400, 30)
        btn_width, btn_height, spacing = 100, 40, 20
        btn_y = row_height + 40
        self.parent.btn_back.setGeometry(section_width + spacing, btn_y, btn_width, btn_height)
        self.parent.btn_forward.setGeometry(section_width + spacing + btn_width + 20, btn_y, btn_width, btn_height)
        # Address bar بالا
        self.parent.address_bar_top.setGeometry(section_width + 10, 0, 300, 25)
        self.parent.btn_forward_top.setGeometry(section_width + 320, 0, 40, 25)
        # ترمینال
        self.parent.terminal_output.setGeometry(section_width, row_height + 100, section_width*3, row_height - 30)
        self.parent.cmd_input.setGeometry(section_width, h - 30, section_width*3, 30)
        # tree_view
        row_height_paint = h // 3
        s1r3_y = row_height_paint * 2
        self.parent.tree_view.setGeometry(0, s1r3_y, section_width, row_height_paint)
        self.parent.tree_view.show()

    def paint(self, event):
        painter = QPainter(self.parent)
        w, h = self.parent.width(), self.parent.height()
        section_width = w // 5
        row_height = h // 3

        # ----------------------------
        # بخش S1
        # ----------------------------
        section_rows = {
            1: [QColor(0, 0, 0), QColor(0, 0, 0), QColor(0, 0, 0)]
        }

        for j in range(3):
            color = section_rows[1][j]
            y = j * row_height
            painter.fillRect(0, y, section_width, row_height, color)

            # ردیف اول: رمزارزها
            if j == 0:
                self._draw_crypto(painter, y)
                continue
            # ردیف دوم: نرخ ارز
            if j == 1:
                self._draw_fx(painter, y)
                continue
            # ردیف سوم: tree_view
            if j == 2:
                continue

        # ----------------------------
        # بخش اطلاعات سیستم و افکت‌ها
        # ----------------------------
        self._draw_system_info(painter, section_width, h, row_height)

        # ----------------------------
        # بخش S5R2 - تاریخ و ساعت
        # ----------------------------
        self._draw_time(painter, section_width, row_height, h)

        # ----------------------------
        # بخش merged R2
        # ----------------------------
        merged_color = QColor(50, 50, 50)
        painter.fillRect(section_width, h//2, section_width*3, h//2, merged_color)

    # ----------------------------
    # رسم رمزارزها
    # ----------------------------
    def _draw_crypto(self, painter, y):
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Courier New", 12, QFont.Weight.Bold))

        crypto_data = getattr(self.parent.crypto_manager, 'crypto_data', [])
        if not crypto_data:
            painter.drawText(10, y + 30, "Loading crypto data...")
            return

        offset = 30
        line_h = 22
        for coin in crypto_data:
            name = coin.get("name", "N/A")
            price = coin.get("current_price", 0)
            change = coin.get("price_change_percentage_24h", 0.0)

            change_color = QColor(0, 255, 0) if change >= 0 else QColor(255, 50, 50)
            painter.setPen(QColor(255, 255, 255))
            try:
                price_text = f"${price:,.2f}"
            except:
                price_text = f"${price}"
            painter.drawText(10, y + offset, f"{name}:  {price_text}")

            painter.setPen(change_color)
            try:
                change_text = f"{change:.2f}%"
            except:
                change_text = str(change)
            painter.drawText(10, y + offset + 18, f"{change_text}")

            offset += line_h * 2

    # ----------------------------
    # رسم نرخ ارزها
    # ----------------------------
    def _draw_fx(self, painter, y):
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Courier New", 12, QFont.Weight.Bold))

        fx_data = getattr(self.parent.crypto_manager, 'fx_data', {'rates': {}, 'names': {}})
        rates = fx_data.get('rates', {})
        names = fx_data.get('names', {})

        if not rates:
            painter.drawText(10, y + 30, "Loading FX rates...")
            return

        offset = 30
        for code, persian_name in names.items():
            rate = rates.get(code)
            try:
                rate_text = f"{rate:,.0f} IRR" if isinstance(rate, (int, float)) else "N/A"
            except:
                rate_text = str(rate)
            painter.drawText(10, y + offset, f"{persian_name} ({code}): {rate_text}")
            offset += 20

    # ----------------------------
    # رسم اطلاعات سیستم و افکت‌ها
    # ----------------------------
    def _draw_system_info(self, painter, section_width, h, row_height):
        painter.fillRect(section_width*4, 0, section_width, row_height, QColor(10, 10, 10))
        painter.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        metrics = QFontMetrics(painter.font())
        line_height = metrics.height() + 4

        system = getattr(self.parent, 'system_info', None)
        cpu = getattr(system, 'cpu', 'N/A')
        ram = getattr(system, 'ram', 'N/A')
        temp = getattr(system, 'temp', 'N/A')
        gpu = getattr(system, 'gpu', 'N/A')

        info_lines = [
            f"[ SYSTEM STATUS ]",
            f"CPU Usage: {cpu}%",
            f"RAM Usage: {ram}%",
            f"CPU Temp: {temp}°C",
            f"GPU: {gpu}"
        ]

        max_lines = row_height // line_height
        for i, line in enumerate(info_lines[:max_lines]):
            color = QColor(0, 255, 0) if random.random() > 0.2 else QColor(0, 120, 0)
            painter.setPen(color)
            glitch_offset = random.randint(-1,1)
            painter.drawText(section_width*4 + 10 + glitch_offset, 20 + i*line_height + glitch_offset, line)

        # ماتریکس روی اطلاعات سیستم
        for col in range(10):
            drop = random.randint(1, 15)
            for y_offset in range(drop):
                y_pos = y_offset * 12
                painter.setPen(QColor(0, 255, 0))
                painter.drawText(section_width*4 + 220 + col*10, y_pos, random.choice('01'))

    # ----------------------------
    # رسم زمان‌ها
    # ----------------------------
    def _draw_time(self, painter, section_width, row_height, h):
        painter.fillRect(section_width*4, row_height, section_width, row_height, QColor(10, 10, 10))
        painter.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        line_height = QFontMetrics(painter.font()).height() + 4

        now = datetime.now()
        time_text = now.strftime("%H:%M:%S.%f")[:-4]
        gregorian_date = now.strftime("%Y-%m-%d")
        jalali_date = jdatetime.datetime.now().strftime("%Y-%m-%d")
        hijri = Gregorian(now.year, now.month, now.day).to_hijri()
        hijri_date = f"{hijri.year}-{hijri.month:02}-{hijri.day:02}"

        hacker_lines = [
            f"[ TIME ]   {time_text}",
            f"[ GREG ]   {gregorian_date}",
            f"[ SHAMSI ] {jalali_date}",
            f"[ HIJRI ]  {hijri_date}"
        ]

        offset = 0
        neon_green = QColor(0, 255, 0)
        for line in hacker_lines:
            color = neon_green if random.random() > 0.1 else QColor(0, 120, 0)
            painter.setPen(color)
            glitch_offset = random.randint(-1,1)
            painter.drawText(section_width*4 + 10 + glitch_offset, row_height + offset + glitch_offset, line)
            offset += line_height + 4

        # ماتریکس روی تاریخ و ساعت
        for col in range(10):
            drop = random.randint(1, 15)
            for y_offset in range(drop):
                y_pos = row_height + y_offset * 12
                painter.setPen(QColor(0, 255, 0))
                painter.drawText(section_width*4 + 250 + col*10, y_pos, random.choice('01'))
