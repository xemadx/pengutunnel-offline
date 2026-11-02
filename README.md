# PenguTunnel offline

نصب یا آپدیت به **آخرین ریلیز منتشرشده**؛ همین دستور را روی هر دو سرور اجرا کنید:

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://github.com/xemadx/pengutunnel-offline/releases/latest/download/install.sh | sudo bash
```

برای Linux x86_64 با systemd فعال. پس از بررسی SHA-256، منوی CLI باز می‌شود؛ برای بازکردن دوبارهٔ منو: `sudo pengu`.

دو سمت را با تنظیمات هماهنگ و PSK یکسان بسازید. هستهٔ موجود باینری اصلاح‌شده است؛ سورس اصلی هسته در این مخزن نیست.
