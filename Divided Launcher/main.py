# -*- coding: utf-8 -*-
"""
main.py
اجرای اصلی برنامه DividedScreen
مدیریت ویجت‌ها، تقسیم‌بندی صفحه و اتصال رویدادها
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QLineEdit, QPushButton, QTreeView
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtGui import QPainter, QColor, QFont, QFontMetrics
from PyQt6.QtCore import Qt, QUrl, QTimer

from PyQt6.QtWebEngineWidgets import QWebEngineView

# ماژول‌های پروژه
from utils.crypto_fx import CryptoManager
from utils.system_info import SystemInfo
from utils.effects_manager import EffectsManager
from ui.paint_manager import PaintManager

class DividedScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Divided Launcher Complete Terminal v5")

        # مسیر فعلی برنامه
        self.current_dir = os.getcwd()

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

        self.btn_back = QPushButton("Back", self)
        self.btn_back.clicked.connect(self.go_back)

        self.btn_forward = QPushButton("Forward", self)
        self.btn_forward.clicked.connect(self.go_forward)

        # ----------------------------
        # Address bar بالا
        # ----------------------------
        self.address_bar_top = QLineEdit(self)
        self.address_bar_top.setPlaceholderText("Top URL Bar")
        self.address_bar_top.returnPressed.connect(self.load_address_bar_top_url)

        self.btn_forward_top = QPushButton("→", self)
        self.btn_forward_top.clicked.connect(self.load_address_bar_top_url)

        # ----------------------------
        # ترمینال
        # ----------------------------
        self.terminal_output = QTextEdit(self)
        self.terminal_output.setReadOnly(True)
        self.cmd_input = QLineEdit(self)
        self.cmd_input.returnPressed.connect(self.run_command)

        # ----------------------------
        # فایل اکسپلورر
        # ----------------------------
        self.fs_model = QFileSystemModel()
        self.fs_model.setRootPath(self.current_dir)
        self.tree_view = QTreeView(self)
        self.tree_view.setModel(self.fs_model)
        self.tree_view.setRootIndex(self.fs_model.index(self.current_dir))
        try:
            self.tree_view.header().hide()
        except Exception:
            pass
        self.tree_view.clicked.connect(self.on_tree_clicked)

        # ----------------------------
        # مدیریت داده‌ها و افکت‌ها
        # ----------------------------
        self.crypto_manager = CryptoManager()
        self.system_info = SystemInfo()
        self.effects_manager = EffectsManager()
        self.paint_manager = PaintManager(self)

        # تایمرها
        self.info_timer = QTimer()
        self.info_timer.timeout.connect(self.update_system_info)
        self.info_timer.start(3000)

        self.effect_timer = QTimer()
        self.effect_timer.timeout.connect(self.update_effects)
        self.effect_timer.start(150)

        self.crypto_timer = QTimer()
        self.crypto_timer.timeout.connect(self.update_crypto_info)
        self.crypto_timer.start(3000)

        # نمایش پنجره
        self.update_system_info()
        self.showFullScreen()
        self.display_prompt()

    # ----------------------------
    # توابع مرورگر
    # ----------------------------
    def load_url(self, url):
        if not url.startswith("http"):
            url = "https://" + url
        self.browser_r1.setUrl(QUrl(url))

    def load_address_bar_url(self):
        self.load_url(self.address_bar.text())

    def load_address_bar_top_url(self):
        self.load_url(self.address_bar_top.text())

    def apply_dark_mode(self):
        js_code = f"""
    var style = document.createElement('style');
    style.type = 'text/css';
    style.innerHTML = `{self.dark_css}`;
    document.head.appendChild(style);
    """
        self.browser_r1.page().runJavaScript(js_code)

    def go_back(self):
        if self.browser_r1.history().canGoBack():
            self.browser_r1.back()

    def go_forward(self):
        if self.browser_r1.history().canGoForward():
            self.browser_r1.forward()

    # ----------------------------
    # ترمینال
    # ----------------------------
    def display_prompt(self):
        self.terminal_output.append(f"{self.current_dir} $ ")
        self.terminal_output.verticalScrollBar().setValue(self.terminal_output.verticalScrollBar().maximum())

    def run_command(self):
        import subprocess
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
    # وقتی آیتمی در tree کلیک شود
    # ----------------------------
    def on_tree_clicked(self, index):
        try:
            path = self.fs_model.filePath(index)
            self.cmd_input.setText(path)
        except Exception:
            pass

    # ----------------------------
    # بروزرسانی سیستم و افکت‌ها
    # ----------------------------
    def update_system_info(self):
        self.system_info.update()
        self.update()

    def update_effects(self):
        self.effects_manager.update()
        self.update()

    def update_crypto_info(self):
        self.crypto_manager.update()
        self.update()

    # ----------------------------
    # تنظیم ابعاد
    # ----------------------------
    def resizeEvent(self, event):
        self.paint_manager.resize_widgets()

    # ----------------------------
    # رسم UI
    # ----------------------------
    def paintEvent(self, event):
        self.paint_manager.paint(event)

# ----------------------------
# اجرای برنامه
# ----------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = DividedScreen()
    screen.show()
    sys.exit(app.exec())
