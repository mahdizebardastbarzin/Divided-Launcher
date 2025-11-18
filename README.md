# Divided Launcher Complete Terminal

یک برنامه حرفه‌ای برای نمایش اطلاعات سیستم، رمزارزها، نرخ ارز و مرورگر داخلی با رابط کاربری تقسیم‌شده، افکت‌های Glitch و Matrix، و فایل اکسپلورر داخلی.

---

## 🌟 ویژگی‌ها / Features

* **مرورگر داخلی (R1) / Built-in Web Browser**
* **ترمینال حرفه‌ای با اجرای دستورات سیستم / Professional Terminal**
* **نمایش اطلاعات CPU، RAM، GPU و دما / System Info Display**
* **نمایش رمزارزها (Bitcoin, Ethereum, Tether, Solana, Dogecoin) / Crypto Display**
* **نمایش نرخ ارز نسبت به ریال ایران / FX Rates Display**
* **افکت‌های Matrix و Glitch / Matrix & Glitch Effects**
* **فایل اکسپلورر داخلی / Built-in File Explorer**
* **تاریخ و زمان به فرمت Gregorian, Shamsi, Hijri / Multi-calendar Time Display**

---

## 🗂️ ساختار پروژه / Project Structure

```
project/
│
├─ main.py                         # اجرای اصلی برنامه (UI + تقسیم‌بندی) / Main application entry
│
├─ ui/
│   ├─ __init__.py
│   ├─ paint_manager.py            # مدیریت رندر کل UI + Matrix + Glitch / UI Renderer
│   └─ draw_helpers.py             # توابع کمکی برای رسم / Drawing helper functions
│
├─ utils/
│   ├─ __init__.py
│   ├─ crypto_fx.py                # دریافت و مدیریت رمزارزها و نرخ ارز / Crypto & FX management
│   ├─ system_info.py              # سیستم CPU/RAM/Temperature/GPU / System information utilities
│   └─ effects_manager.py          # مدیریت افکت‌ها (Matrix + Glitch) / Effects management
│
├─ resources/
│   ├─ icons/                      # آیکون‌ها / Icons (optional)
│   └─ images/                     # عکس‌ها / Images (optional)
│
└─ README.md                       # توضیحات پروژه / Project documentation
```

---

## ⚙️ نصب و اجرای پروژه / Installation & Running

1. نصب پایتون 3.10+ / Install Python 3.10+
2. نصب وابستگی‌ها / Install dependencies:

   ```bash
   pip install PyQt6 PyQt6-WebEngine psutil jdatetime hijridate requests
   ```
3. اجرای برنامه / Run the program:

   ```bash
   python main.py
   ```

---

## 📌 توضیحات فایل‌ها / File Descriptions

* **main.py**: نقطه ورود برنامه و مدیریت چینش UI / Main entry point and UI layout manager.
* **ui/paint_manager.py**: مدیریت تمام رسم‌ها، افکت‌های Glitch و Matrix / Handles painting and UI effects.
* **ui/draw_helpers.py**: توابع کمکی برای نمایش متن، رنگ، خطوط / Helper functions for drawing.
* **utils/crypto_fx.py**: بارگذاری و مدیریت داده‌های رمزارز و نرخ ارز / Fetch and manage crypto and FX data.
* **utils/system_info.py**: خواندن اطلاعات CPU, RAM, GPU و دما / System info reader.
* **utils/effects_manager.py**: مدیریت افکت‌های Matrix و Glitch / Effects controller.
* **resources/icons/**: آیکون‌ها و تصاویر مورد استفاده در UI / Icons and images for UI.

---

## 📊 مثال‌ها / Screenshots

*قرار دادن تصاویر مستطیلی زیبا از برنامه و افکت‌ها در این بخش.*

---

## 💻 نیازمندی‌ها / Requirements

* Python 3.10+
* PyQt6
* PyQt6-WebEngine
* psutil
* jdatetime
* hijridate
* requests

---
🤝 Contributing
Contributions are welcome! Please read our Contributing Guidelines to get started.

🤝 مشارکت
مشارکت‌های شما خوش‌آمد است! لطفاً راهنمای مشارکت را مطالعه کنید.
---
## 📝 مجوز / License

MIT License

