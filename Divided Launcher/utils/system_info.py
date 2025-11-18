# -*- coding: utf-8 -*-
"""
system_info.py
مدیریت و دریافت اطلاعات سیستم (CPU, RAM, Temperature, GPU)
"""

import psutil
import platform

class SystemInfo:
    """
    کلاس مدیریت اطلاعات سیستم
    """
    def __init__(self):
        self.cpu = 0
        self.ram = 0
        self.temp = 0
        self.gpu = ""

    def update(self):
        """
        بروزرسانی اطلاعات سیستم
        """
        try:
            self.cpu = psutil.cpu_percent()
            self.ram = psutil.virtual_memory().percent
            self.temp = self._get_temp()
            self.gpu = platform.machine()
        except:
            self.cpu = self.ram = self.temp = self.gpu = "N/A"

    def _get_temp(self):
        """
        دریافت دمای CPU (در صورت پشتیبانی سیستم)
        """
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    first = list(temps.values())[0]
                    return first[0].current
            return "N/A"
        except:
            return "N/A"

    def get_info(self):
        """
        بازگشت اطلاعات سیستم به صورت دیکشنری
        """
        return {
            "cpu": self.cpu,
            "ram": self.ram,
            "temp": self.temp,
            "gpu": self.gpu
        }
