# -*- coding: utf-8 -*-
"""
effects_manager.py
مدیریت افکت‌های Matrix و Glitch
"""

import random

class EffectsManager:
    """
    کلاس مدیریت افکت‌های گلیچ و ماتریکس
    """
    def __init__(self, matrix_cols=10, matrix_drop_max=15, glitch_len=5):
        # طول افکت glitch
        self.glitch_len = glitch_len
        # تعداد ستون‌های ماتریکس
        self.matrix_cols = matrix_cols
        # حداکثر ارتفاع هر drop در ماتریکس
        self.matrix_drop_max = matrix_drop_max

        # وضعیت فعلی افکت‌ها
        self.glitch_effects = [0] * self.glitch_len
        self.matrix_drops = [0] * self.matrix_cols

    def update_glitch(self):
        """
        بروزرسانی افکت glitch
        """
        self.glitch_effects = [random.randint(0, 1) for _ in range(self.glitch_len)]
        return self.glitch_effects

    def update_matrix(self):
        """
        بروزرسانی افکت Matrix
        """
        self.matrix_drops = [
            drop + 1 if drop < self.matrix_drop_max else 0
            for drop in self.matrix_drops
        ]
        return self.matrix_drops

    def get_glitch(self):
        """
        بازگشت وضعیت فعلی glitch
        """
        return self.glitch_effects

    def get_matrix(self):
        """
        بازگشت وضعیت فعلی ماتریکس
        """
        return self.matrix_drops
    
    def update(self):
        """
        بروزرسانی همزمان glitch و matrix
        """
        self.update_glitch()
        self.update_matrix()
