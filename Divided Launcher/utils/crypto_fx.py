# -*- coding: utf-8 -*-
"""
crypto_fx.py
مدیریت دریافت و پردازش اطلاعات رمزارزها و نرخ ارز
"""

import requests

class CryptoManager:
    """
    دریافت و مدیریت اطلاعات رمزارزها از API
    """
    COINS_LIST = ["bitcoin", "ethereum", "tether", "solana", "dogecoin"]

    def __init__(self, currency="usd"):
        self.currency = currency
        self.data = []

    def update(self):
        """
        بروزرسانی اطلاعات رمزارزها از CoinGecko
        """
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                "vs_currency": self.currency,
                "ids": ",".join(self.COINS_LIST),
                "order": "market_cap_desc"
            }
            r = requests.get(url, params=params, timeout=5)
            if r.status_code == 200:
                self.data = r.json()
            else:
                self.data = []
        except:
            self.data = []

    def get_data(self):
        """
        بازگشت داده‌ها
        """
        return self.data


class FXManager:
    """
    دریافت و مدیریت نرخ ارزها نسبت به IRR
    """
    DEFAULT_NAMES = {
        "USD": "دلار",
        "GBP": "پوند",
        "CNY": "یوآن",
        "RUB": "روبل",
        "INR": "روپیه"
    }

    def __init__(self):
        self.names = self.DEFAULT_NAMES
        self.rates = {k: None for k in self.names.keys()}

    def update(self):
        """
        بروزرسانی نرخ ارزها از exchangerate.host
        """
        try:
            for code in self.names.keys():
                try:
                    r = requests.get(
                        "https://api.exchangerate.host/latest",
                        params={"base": code, "symbols": "IRR"},
                        timeout=5
                    )
                    if r.status_code == 200:
                        j = r.json()
                        self.rates[code] = j.get('rates', {}).get('IRR')
                    else:
                        self.rates[code] = None
                except:
                    self.rates[code] = None
        except:
            self.rates = {k: None for k in self.names.keys()}

    def get_rates(self):
        """
        بازگشت نرخ‌های فعلی
        """
        return self.rates
