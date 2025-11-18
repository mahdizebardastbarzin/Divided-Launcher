# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import psutil
import platform
import random
from datetime import datetime
import jdatetime
# جایگزینی بسته‌ی قدیمی با hijridate (همان API مشابه را دارد)
from hijridate import Gregorian
import requests  # اضافه شده برای بارگذاری رمزارزها و نرخ ارز

from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QLineEdit, QPushButton, QTreeView
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtGui import QPainter, QColor, QFont, QFontMetrics
from PyQt6.QtCore import Qt, QUrl, QTimer, QDir
from PyQt6.QtWebEngineWidgets import QWebEngineView

class DividedScreen(QWidget):
    # ----------------------------
    # تعریف رنگ‌های بخش‌ها
    # ----------------------------
    section_rows = {
        1: [QColor(0, 0, 0), QColor(0, 0, 0), QColor(0, 0, 0)],  # S1
        5: [QColor(200, 30, 200), QColor(180, 30, 180), QColor(160, 30, 160)]  # S5
    }
    merged_r2_color = QColor(50, 50, 50)  # بخش merged R2

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Divided Launcher Complete Terminal v5")

        # ----------------------------
        # مرورگر وب (R1)
        # ----------------------------
        self.browser_r1 = QWebEngineView(self)
        self.browser_r1.loadFinished.connect(self.apply_dark_mode)
        self.dark_css = """
        html { filter: invert(1) hue-rotate(180deg); background-color: #121212 !important; }
        img, video { filter: invert(1) hue-rotate(180deg) !important; }
        """

        # ----------------------------
        # Address bar و دکمه‌ها
        # ----------------------------
        self.address_bar = QLineEdit(self)
        self.address_bar.setPlaceholderText("Enter URL and press Enter")
        self.address_bar.returnPressed.connect(self.load_address_bar_url)
        self.address_bar.setStyleSheet("""
        QLineEdit { padding: 6px; border-radius: 8px; border: 2px solid #444; font-size: 16px; background-color: #222; color: white; }
        """)
        self.btn_back = QPushButton("Back", self)
        self.btn_back.setStyleSheet("""
        QPushButton { background-color: #444; color: white; border-radius: 10px; font-size: 16px; padding: 8px 20px; }
        QPushButton:hover { background-color: #666; }
        """)
        self.btn_back.clicked.connect(self.go_back)
        self.btn_forward = QPushButton("Forward", self)
        self.btn_forward.setStyleSheet("""
        QPushButton { background-color: #444; color: white; border-radius: 10px; font-size: 16px; padding: 8px 20px; }
        QPushButton:hover { background-color: #666; }
        """)
        self.btn_forward.clicked.connect(self.go_forward)

        # ----------------------------
        # Address bar بالا
        # ----------------------------
        self.address_bar_top = QLineEdit(self)
        self.address_bar_top.setPlaceholderText("Top URL Bar")
        self.address_bar_top.returnPressed.connect(self.load_address_bar_top_url)
        self.address_bar_top.setStyleSheet("""
        QLineEdit { padding: 5px; border-radius: 6px; border: 2px solid #555; font-size: 14px; background-color: #333; color: white; }
        """)
        self.btn_forward_top = QPushButton("→", self)
        self.btn_forward_top.setStyleSheet("""
        QPushButton { background-color: #555; color: white; border-radius: 6px; font-size: 14px; padding: 4px 12px; }
        QPushButton:hover { background-color: #777; }
        """)
        self.btn_forward_top.clicked.connect(self.load_address_bar_top_url)

        # ----------------------------
        # تنظیمات ترمینال
        # ----------------------------
        self.terminal_output = QTextEdit(self)
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.terminal_output.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.terminal_output.setStyleSheet("""
        QTextEdit { background-color: #0f0f0f; color: #00ff00; font-family: Consolas, monospace; font-size: 14px; border: 2px solid #222; padding: 5px; }
        """)
        self.cmd_input = QLineEdit(self)
        self.cmd_input.setPlaceholderText("Enter command and press Enter")
        self.cmd_input.returnPressed.connect(self.run_command)
        self.cmd_input.setStyleSheet("""
        QLineEdit { background-color: #111; color: #00ff00; font-family: Consolas, monospace; font-size: 14px; padding: 5px; border-radius: 6px; border: 2px solid #222; }
        """)
        self.current_dir = os.getcwd()

        # ----------------------------
        # فایل اکسپلورر برای S1R3 (فقط اضافه شده)
        # ----------------------------
        # model و view را ایجاد می‌کنیم؛ فقط برای نمایش و انتخاب فایل/پوشه
        self.fs_model = QFileSystemModel()
        # تنظیم روت به مسیر فعلی برنامه
        self.fs_model.setRootPath(self.current_dir)
        self.tree_view = QTreeView(self)
        self.tree_view.setModel(self.fs_model)
        # ریشه در current_dir
        self.tree_view.setRootIndex(self.fs_model.index(self.current_dir))
        # سربرگ ستون‌ها را مخفی می‌کنیم تا شبیه اکسپلورر ساده شود
        try:
            self.tree_view.header().hide()
        except Exception:
            pass
        # وقتی فایل یا فولدری کلیک شد، مسیر را در cmd_input قرار می‌دهیم (قابلیت انتخاب)
        self.tree_view.clicked.connect(self.on_tree_clicked)

        # ----------------------------
        # افکت‌ها
        # ----------------------------
        self.glitch_effects = [0,1,0,1,0]
        self.matrix_drops = [0]*10

        # تایمر ۳ ثانیه‌ای برای بروزرسانی اطلاعات سیستم
        self.info_timer = QTimer()
        self.info_timer.timeout.connect(self.update_system_info)
        self.info_timer.start(3000)

        # تایمر افکت glitch سریع
        self.effect_timer = QTimer()
        self.effect_timer.timeout.connect(self.update_effects)
        self.effect_timer.start(150)

        # ----------------------------
        # تایمر دریافت اطلاعات رمز ارزها (S1R1)
        # ----------------------------
        self.crypto_data = []
        self.crypto_timer = QTimer()
        self.crypto_timer.timeout.connect(self.update_crypto_info)
        self.crypto_timer.start(3000)

        # ----------------------------
        # *** اضافه‌شده: تایمر و داده‌های نرخ ارز برای S1R2 ***
        # ----------------------------
        # fx_data ساختار: {'rates': {'USD': 420000.0, ...}, 'names': {'USD':'دلار', ...}}
        self.fx_data = {'rates': {}, 'names': {'USD':'دلار','GBP':'پوند','CNY':'یوآن','RUB':'روبل','INR':'روپیه'}}
        self.fx_timer = QTimer()
        self.fx_timer.timeout.connect(self.update_fx_info)
        self.fx_timer.start(3000)
        # -----------------------------------------------------

        self.cpu = 0
        self.ram = 0
        self.temp = 0
        self.gpu = ''
        self.update_system_info()
        self.showFullScreen()
        self.display_prompt()

    # ----------------------------
    # بروزرسانی اطلاعات سیستم
    # ----------------------------
    def update_system_info(self):
        try:
            self.cpu = psutil.cpu_percent()
            self.ram = psutil.virtual_memory().percent
            self.temp = "N/A"
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    first = list(temps.values())[0]
                    self.temp = first[0].current
            self.gpu = platform.machine()
        except:
            self.cpu = self.ram = self.temp = self.gpu = "N/A"
        self.update()

    # ----------------------------
    # دریافت اطلاعات رمز ارزها (S1R1)
    # ----------------------------
    def update_crypto_info(self):
        try:
            # از requests استفاده می‌کنیم؛ اگر خطا بود لیست خالی می‌شود ولی برنامه کرش نمی‌کند
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                "vs_currency": "usd",
                "ids": "bitcoin,ethereum,tether,solana,dogecoin",
                "order": "market_cap_desc"
            }
            r = requests.get(url, params=params, timeout=5)
            if r.status_code == 200:
                self.crypto_data = r.json()
            else:
                # در صورت خطا از API، مقداردهی خالی
                self.crypto_data = []
        except Exception as e:
            # اگر requests نصب نبود یا اتصال نبود، خالی می‌ماند
            self.crypto_data = []
        # بازنقاشی برای نمایش داده‌های جدید
        self.update()

    # ----------------------------
    # *** اضافه‌شده: دریافت نرخ ارزها (S1R2) ***
    # استفاده: از exchangerate.host برای گرفتن نرخ هر ارز نسبت به IRR
    # ----------------------------
    def update_fx_info(self):
        try:
            rates = {}
            for base in self.fx_data.get('names', {}).keys():
                try:
                    r = requests.get("https://api.exchangerate.host/latest",
                                     params={"base": base, "symbols": "IRR"}, timeout=5)
                    if r.status_code == 200:
                        j = r.json()
                        val = j.get('rates', {}).get('IRR')
                        # بعضی APIها مقدار را بر حسب ریال یا تومان برمی‌گردانند؛ اینجا فرض می‌کنیم IRR همان ریال است
                        rates[base] = val
                    else:
                        rates[base] = None
                except:
                    rates[base] = None
            self.fx_data['rates'] = rates
        except Exception:
            # در صورت بروز هر خطا، داده‌ها خالی می‌مانند ولی برنامه کرش نمی‌کند
            self.fx_data['rates'] = {}
        self.update()
    # -----------------------------------------------------

    # ----------------------------
    # افکت‌های glitch و matrix
    # ----------------------------
    def update_effects(self):
        self.glitch_effects = [random.randint(0, 1) for _ in range(5)]
        self.matrix_drops = [drop+1 if drop < 15 else 0 for drop in self.matrix_drops]
        self.update()

    # ----------------------------
    # بارگذاری URL
    # ----------------------------
    def load_url(self, url):
        if not url.startswith("http"):
            url = "https://" + url
        self.browser_r1.setUrl(QUrl(url))

    def load_address_bar_url(self):
        self.load_url(self.address_bar.text())

    def load_address_bar_top_url(self):
        self.load_url(self.address_bar_top.text())

    # ----------------------------
    # حالت تاریک مرورگر
    # ----------------------------
    def apply_dark_mode(self):
        self.browser_r1.page().runJavaScript(f"""
        var style = document.createElement('style'); style.type = 'text/css'; style.innerHTML = {self.dark_css}; document.head.appendChild(style);
        """)

    # ----------------------------
    # دکمه‌های back و forward
    # ----------------------------
    def go_back(self):
        if self.browser_r1.history().canGoBack():
            self.browser_r1.back()

    def go_forward(self):
        if self.browser_r1.history().canGoForward():
            self.browser_r1.forward()

    # ----------------------------
    # نمایش prompt ترمینال
    # ----------------------------
    def display_prompt(self):
        self.terminal_output.append(f"{self.current_dir} $ ")
        self.terminal_output.verticalScrollBar().setValue(self.terminal_output.verticalScrollBar().maximum())

    # ----------------------------
    # اجرای دستورات ترمینال
    # ----------------------------
    def run_command(self):
        cmd = self.cmd_input.text()
        if not cmd.strip():
            return
        try:
            process = subprocess.Popen(cmd, shell=True, cwd=self.current_dir,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if stdout:
                self.terminal_output.append(stdout)
            if stderr:
                self.terminal_output.append(stderr)
            if cmd.startswith("cd "):
                path = cmd[3:].strip()
                self.current_dir = os.path.abspath(os.path.join(self.current_dir, path))
        except Exception as e:
            self.terminal_output.append(str(e))
        self.cmd_input.clear()
        self.display_prompt()

    # ----------------------------
    # وقتی آیتمی در tree کلیک شود (مسیر را در cmd_input قرار می‌دهیم)
    # ----------------------------
    def on_tree_clicked(self, index):
        try:
            path = self.fs_model.filePath(index)
            self.cmd_input.setText(path)
        except Exception:
            pass

    # ----------------------------
    # تنظیمات ابعاد و چینش بخش‌ها
    # ----------------------------
    def resizeEvent(self, event):
        w, h = self.width(), self.height()
        section_width = w // 5
        row_height = h // 2

        # مرورگر R1
        self.browser_r1.setGeometry(section_width, 30, section_width*3, row_height - 30)
        # Address bar و دکمه‌ها
        self.address_bar.setGeometry(section_width + 10, row_height, 400, 30)
        btn_width, btn_height, spacing = 100, 40, 20
        btn_y = row_height + 40
        self.btn_back.setGeometry(section_width + spacing, btn_y, btn_width, btn_height)
        self.btn_forward.setGeometry(section_width + spacing + btn_width + 20, btn_y, btn_width, btn_height)
        # Address bar بالا
        self.address_bar_top.setGeometry(section_width + 10, 0, 300, 25)
        self.btn_forward_top.setGeometry(section_width + 320, 0, 40, 25)
        # ترمینال
        self.terminal_output.setGeometry(section_width, row_height + 100, section_width*3, row_height - 30)
        self.cmd_input.setGeometry(section_width, h - 30, section_width*3, 30)

        # تنظیم هندسه برای tree_view (S1R3)
        # توجه: paintEvent سه ردیف برای S1 در نظر می‌گیرد (h//3)، پس اینجا هم همان محاسبه را تکرار می‌کنیم
        row_height_paint = h // 3
        s1r3_y = row_height_paint * 2
        self.tree_view.setGeometry(0, s1r3_y, section_width, row_height_paint)
        self.tree_view.show()

    # ----------------------------
    # رسم بخش‌ها
    # ----------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        w, h = self.width(), self.height()
        section_width = w // 5
        row_height = h // 3

        # ----------------------------
        # بخش 1 (S1)
        # ----------------------------
        for j, color in enumerate(self.section_rows[1]):
            y = j * row_height
            painter.fillRect(0, y, section_width, row_height, color)

            if j == 0:
                # ------------------------
                # نمایش اطلاعات رمز ارزها
                # ------------------------
                painter.setPen(QColor(255, 255, 255))
                painter.setFont(QFont("Courier New", 12, QFont.Weight.Bold))

                if not self.crypto_data:
                    painter.drawText(10, y + 30, "Loading crypto data...")
                else:
                    line_h = 22
                    offset = 30

                    for coin in self.crypto_data:
                        # استفاده احتیاطی از get برای جلوگیری از KeyError
                        name = coin.get("name", "N/A")
                        price = coin.get("current_price", 0)
                        change = coin.get("price_change_percentage_24h", 0.0)

                        # رنگ تغییر قیمت
                        change_color = QColor(0, 255, 0) if change >= 0 else QColor(255, 50, 50)
                        painter.setPen(QColor(255, 255, 255))
                        # فرمت قیمت با جداکننده هزار
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

                continue

            # ----------------------------
            # *** اضافه‌شده: S1R2 — نمایش نرخ ارزها نسبت به IRR ***
            # فقط این بخش را تغییر دادم؛ بقیه ردیف‌ها بدون تغییر مانده‌اند
            # ----------------------------
            if j == 1:
                painter.setPen(QColor(255, 255, 255))
                painter.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
                rates = self.fx_data.get('rates', {})
                names = self.fx_data.get('names', {})
                if not rates:
                    painter.drawText(10, y + 30, "Loading FX rates...")
                else:
                    offset = 30
                    for code, persian_name in names.items():
                        rate = rates.get(code)
                        try:
                            # نمایش با جداکننده هزار و بدون اعشار برای خوانایی
                            if isinstance(rate, (int, float)):
                                rate_text = f"{rate:,.0f} IRR"
                            else:
                                rate_text = "N/A"
                        except:
                            rate_text = str(rate)
                        painter.drawText(10, y + offset, f"{persian_name} ({code}): {rate_text}")
                        offset += 20
                continue
            # -----------------------------------------------------

            # ----------------------------
            # S1R3: در این ردیف ما یک QTreeView (File Explorer) قرار داده‌ایم
            # -- هیچ رسم متنی انجام نمی‌شود؛ view جلوی این ناحیه نمایش داده می‌شود
            # ----------------------------
            if j == 2:
                # در resizeEvent هندسهٔ tree_view تنظیم می‌شود؛ اینجا کافیست از نقاشی صرف نظر کنیم
                continue

            # بقیه ردیف‌ها همان حالت قبل
            painter.setPen(Qt.GlobalColor.white)
            painter.setFont(QFont("Arial", 18, QFont.Weight.Bold))
            painter.drawText(20, y + row_height//2, f"S1R{j+1}")

        # ----------------------------
        # بخش اطلاعات سیستم SR51 با افکت گلیچ و ماتریکس
        # ----------------------------
        painter.fillRect(section_width*4, 0, section_width, row_height, QColor(10, 10, 10))
        painter.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        metrics = QFontMetrics(painter.font())
        line_height = metrics.height() + 4

        info_lines = [
            f"[ SYSTEM STATUS ]",
            f"CPU Usage: {self.cpu}%",
            f"RAM Usage: {self.ram}%",
            f"CPU Temp: {self.temp}°C",
            f"GPU: {self.gpu}"
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
        # بخش S5R2 - تاریخ و ساعت با افکت هکری و ماتریکس
        # پس‌زمینه مثل اطلاعات سیستم
        # ----------------------------
        s5r2_x = section_width*4 + 10
        s5r2_y = row_height + 10
        painter.fillRect(section_width*4, row_height, section_width, row_height, QColor(10, 10, 10))
        painter.setFont(QFont("Courier New", 14, QFont.Weight.Bold))

        now = datetime.now()
        time_text = now.strftime("%H:%M:%S.%f")[:-4]
        gregorian_date = now.strftime("%Y-%m-%d")
        jalali_date = jdatetime.datetime.now().strftime("%Y-%m-%d")
        # استفاده از hijridate (API سازگار با hijri-converter)
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
            painter.drawText(s5r2_x + glitch_offset, s5r2_y + offset + glitch_offset, line)
            offset += line_height + 4

        # ماتریکس روی تاریخ و ساعت
        for col in range(10):
            drop = random.randint(1, 15)
            for y_offset in range(drop):
                y_pos = row_height + y_offset * 12
                painter.setPen(QColor(0, 255, 0))
                painter.drawText(section_width*4 + 250 + col*10, y_pos, random.choice('01'))

        # ----------------------------
        # بخش merged R2
        # ----------------------------
        painter.fillRect(section_width, h//2, section_width*3, h//2, self.merged_r2_color)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = DividedScreen()
    screen.show()
    sys.exit(app.exec())
