# Adactin Hotel Automation Framework 

Rangkaian otomatisasi pengujian ujung-ke-ujung (*end-to-end*) untuk komponen reservasi dan pembayaran pada aplikasi Adactin Hotel. Framework ini dibangun menggunakan arsitektur **Page Object Model (POM)** berbasis Python, Playwright, dan Pytest.

## Tech Stack & Prasyarat
* **Bahasa Pemrograman:** Python 3.10+
* **Framework Pengujian:** Pytest
* **Pustaka Otomatisasi UI:** Playwright
* **Mesin Paralelisme:** Pytest-xdist
* **Pelaporan:** Allure Framework

## Panduan Instalasi Lokal

1. **Kloning Repositori:**
   ```bash
   git clone [https://github.com/ekayuliansyah/adactin-hotel-playwright.git](https://github.com/ekayuliansyah/adactin-hotel-playwright.git)
   cd adactin-hotel-playwright

Siapkan Virtual Environment & Aktifkan:
    Bash

    python -m venv venv
    # Di Windows (Git Bash / Command Prompt):
    source venv/Scripts/activate
    # Di Mac/Linux:
    source venv/bin/activate

    Instal Dependensi & Browser Playwright:
    Bash

    pip install -r requirements.txt
    playwright install --with-deps

    Konfigurasi Environment:
    Buat berkas .env di direktori utama (root) proyek Anda, lalu sesuaikan isinya:
    Code snippet

    BASE_URL=[https://adactinhotelapp.com/](https://adactinhotelapp.com/)
    ADACTIN_USERNAME=username_anda
    ADACTIN_PASSWORD=password_anda

🏃‍♂️ Cara Menjalankan Pengujian

Framework ini mendukung eksekusi paralel secara otomatis untuk menghemat waktu tunggu eksekusi pada pipeline maupun lokal.
1. Menjalankan Seluruh Test Suite (Rekomendasi)

Untuk menjalankan seluruh file pengujian yang ada di dalam proyek secara bersamaan menggunakan performa multi-core CPU:
Bash

pytest -n auto --alluredir=allure-results

2. Menjalankan Folder Tertentu Saja

Jika Anda hanya ingin mengeksekusi modul booking saja:
Bash

pytest tests/booking/ -n auto --alluredir=allure-results

3. Melihat Laporan Allure secara Lokal

Setelah pengujian selesai, generate dan buka laporan interaktif Allure menggunakan perintah:
Bash

allure serve allure-results