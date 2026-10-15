# راهنمای جامع و ابزار خودکار رفع خطای ۴۰۳، ۵۰۳ و لایسنس #3501 در Google Antigravity

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-orange.svg)](#روش-اجرا-در-انواع-سیستم‌عامل‌ها)
[![English Version](https://img.shields.io/badge/English-README-blue.svg)](README.md)

[🌐 **Switch to English Documentation**](README.md)

---

![بنر ابزار آنتی‌گرویتی](assets/banner.png)

> 🚨 **راهنما و پست آموزشی جدید:**  
> **[آموزش رفع خطای عدم شناسایی اشتراک ۵ ترابایت Google One AI Pro و احراز هویت سن](docs/GOOGLE_ONE_AI_PRO_AGE_VERIFICATION_FA.md)**  
> [🌐 English Guide: Google One 5TB / AI Pro Ineligible Quota & Age Verification Fix](docs/GOOGLE_ONE_AI_PRO_AGE_VERIFICATION.md)

ابزار چندسکویی و اسکریپت خودکار برای حل ارورهای متداول **`HTTP 503 [403]: PERMISSION_DENIED (VALIDATION_REQUIRED)`** و **`License Error #3501`** در ابزارهای Google Antigravity، Gemini Code Assist، Hermes Agent و رله‌های مدل‌های هوش مصنوعی (نظیر 9Router).

---

## 🧐 ریشه‌یابی فنی خطا: چرا این ارور رخ می‌دهد؟

این پیام خطا معمولاً زمانی دریافت می‌شود که کاربر تصور می‌کند اکانت پرو لغو شده یا کلاینت باگ دارد. در واقع:

1. **قفل رفتار انسانی (`VALIDATION_REQUIRED`):** به دنبال ارسال درخواست‌های پیوسته یا به اتمام رسیدن سهمیه (ریت‌لیمیت ۴۲۹)، سیستم امنیتی گوگل رفتار کاربر را مشکوک دانسته و اکانت را ملزم به حل یک چالش امنیتی (کپچا یا لاگین مجدد) می‌کند.
2. **پنهان ماندن لینک تایید هویت:** گوگل یک `validation_url` یکتا و موقت در متادیتای پاسخ خطای JSON ارسال می‌کند. اکثر کلاینت‌ها این لینک طولانی را در لاگ‌ها کوتاه یا پنهان می‌کنند و کاربر متوجه چرایی توقف نمی‌شود.
3. **ارور لایسنس گمراه‌کننده (#3501):** در صورتی که موقعیت مکانی کاربر نشت کند (نشت DNS یا قطع پروکسی)، گوگل به جای خطای صریح ریجن، ارور ۳۵۰۱ (نبود لایسنس معتبر) پرتاب می‌کند یا جریان سشن را به سمت Gemini Enterprise منحرف می‌سازد.
4. **سشن‌های معلق در پس‌زمینه:** پروسه‌های `language_server` و فایل‌های توکن در `~/.gemini` یا `~/.antigravity` در حالت قفل باقی می‌مانند و مانع احراز مجدد می‌شوند.

---

## 🖥️ پیش‌نمایش اجرای ابزار

![پیش‌نمایش ترمینال](assets/screenshot.png)

---

## 🚀 روش اجرا در انواع سیستم‌عامل‌ها

### ۱. ابزار هوشمند پایتون (توصیه شده - Cross Platform)

این اسکریپت با کتابخانه‌های داخلی پایتون ۳ (بدون نیاز به نصب پکیج جانبی) لاگ‌ها را کاوش کرده، لینک `validation_url` را در کسر از ثانیه استخراج کرده و مرورگر را باز می‌کند:

```bash
# کلون ریپازیتوری
git clone https://github.com/nic40246-dot/antigravity-403-fix.git
cd antigravity-403-fix

# اجرای ابزار
python antigravity_fix.py
```

#### پارامترهای اختیاری:
```bash
python antigravity_fix.py --help

  --no-open    فقط لینک را در ترمینال چاپ کند و مرورگر را خودکار باز نکند
  --reset      بستن اجباری پروسه‌ها و پاکسازی کش سشن‌های قفل‌شده
  --log PATH   بررسی یک فایل لاگ مشخص به صورت دستی
```

---

### ۲. ویندوز (PowerShell)

برای اجرای اسکریپت آماده ویندوز:
```powershell
powershell -ExecutionPolicy Bypass -File .\fix-windows.ps1
```

یا دستور پاکسازی سریع تک‌خطی در پاورشل:
```powershell
powershell "Stop-Process -Name *antigravity* -Force -EA 0; Remove-Item -Recurse -Force "$HOME\.antigravity","$HOME\.gemini" -EA 0"
```

---

### ۳. مک‌او‌اس (macOS)

```bash
chmod +x fix-unix.sh
./fix-unix.sh
```

یا دستور تک‌خطی پاکسازی سشن و کی‌چین:
```bash
pkill -9 -f Antigravity; security delete-generic-password -s gemini -a antigravity 2>/dev/null; rm -rf ~/.antigravity ~/.gemini ~/.antigravity-ide
```

---

### ۴. لینوکس و ترموکس (Linux & Termux)

```bash
chmod +x fix-unix.sh
./fix-unix.sh
```

یا دستور تک‌خطی در ترمینال لینوکس:
```bash
pkill -9 -f antigravity; rm -rf ~/.antigravity ~/.gemini ~/.config/Antigravity
```

---

## 📋 چک‌لیست طلایی جلوگیری از مسدودی و نشت ریجن

برای پیشگیری از تکرار ارور ۴۰۳ و قفل شدن مکرر:

1. **بررسی کشور ثبت‌شده اکانت:**
   وارد [policies.google.com/terms](https://policies.google.com/terms) شوید. در فوتر صفحه چک کنید که عبارت **`Country version: United States`** (یا کشور بدون تحریم) درج شده باشد. در صورت مغایرت، از [فرم تغییر کشور گوگل](https://policies.google.com/country-association-form) استفاده کنید.

2. **حذف شماره تلفن ایران:**
   در تنظیمات امنیتی [myaccount.google.com/phone](https://myaccount.google.com/phone)، هرگونه شماره تلفن مربوط به ایران (+98) را کاملاً حذف کنید.

3. **جلوگیری از نشت DNS:**
   ابزار ضدتحریم یا فیلترشکن خود را بر روی حالت **TUN Mode / Global** قرار داده و DNS کارت شبکه را روی `1.1.1.1` یا `8.8.8.8` تنظیم کنید.

4. **ورود صرفاً با Personal Account:**
   در زمان ورود مجدد به Antigravity، فقط و فقط گزینه **Personal Account** را انتخاب کنید و به هیچ عنوان گزینه Enterprise یا Google Cloud Project را انتخاب ننمایید.

---

## 👥 مشارکت و پشتیبانی

- کانال جامعه تلگرام: [@antigravity_iran](https://t.me/antigravity_iran)
- گزارش مشکلات و توسعه: [بخش Issues گیت‌هاب](https://github.com/nic40246-dot/antigravity-403-fix/issues)

## 📄 لایسنس

این پروژه تحت مجوز متن‌باز [MIT License](LICENSE) منتشر شده است.
