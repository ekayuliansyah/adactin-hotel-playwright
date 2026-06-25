import os
import json
import pytest
import allure
import re
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.search_hotel_page import SearchHotelPage
from pages.select_hotel_page import SelectHotelPage
from dotenv import load_dotenv

load_dotenv(override=True)

# 2. Jika os.getenv menghasilkan string kosong "", Python akan otomatis memakai string di sebelah kanan 'or'
BASE_URL = os.getenv("BASE_URL") or "https://adactinhotelapp.com/"
USERNAME = os.getenv("ADACTIN_USERNAME") or "IsiUsernameDummyAndaDisini"
PASSWORD = os.getenv("ADACTIN_PASSWORD") or "IsiPasswordDummyAndaDisini"

@allure.feature("Select Hotel Management")
@allure.story("Math Audit - Total Price Calculation")
@pytest.mark.xfail(reason="Bug matematika bawaan Adactin Build 1 (surplus $10)")
def test_hotel_total_price_calculation_audit(page: Page):
    """Menguji keakuratan perhitungan harga total (Days x Price per Night)"""
    login_page = LoginPage(page)
    search_page = SearchHotelPage(page)
    select_page = SelectHotelPage(page)
    
    # 1. Load Data dari JSON agar tidak hardcode
    with open("data/search_data.json") as f:
        search_data = json.load(f)["paris_long_stay"]
    
    # 2. Alur Masuk
    login_page.navigate(BASE_URL)
    login_page.login(USERNAME, PASSWORD)
    
    # 3. Mengisi Data Menggunakan Fungsi Dinamis POM Anda
    with allure.step("Mengisi form pencarian menggunakan data JSON Paris"):
        # Ini akan otomatis mengisi dropdown dan tanggal tanpa hardcode
        search_page.search_hotel_complete(search_data) 
    
    # 4. Ekstraksi Data dari Tabel menggunakan get_attribute("value") karena elemennya adalah tag <input>
    with allure.step("Mengambil data kalkulasi dari baris pertama tabel"):
        days_text = select_page.first_days.get_attribute("value") # Menghasilkan "32 Days"
        price_text = select_page.first_price_per_night.get_attribute("value") # Menghasilkan "AUD $ 100"
        total_price_text = select_page.first_total_price.get_attribute("value") # Menghasilkan "AUD $ 3210"
        
        # Bersihkan string untuk mengambil angka saja menggunakan regex
        days_num = int(re.search(r'\d+', days_text).group())
        price_num = int(re.search(r'\d+', price_text).group())
        total_price_num = int(re.search(r'\d+', total_price_text).group())
    
    # 5. Asersi Audit Matematika
    expected_math_total = days_num * price_num
    with allure.step(f"Verifikasi Hitungan: {days_num} hari x AUD ${price_num} = AUD ${expected_math_total}"):
        assert total_price_num == expected_math_total, f"Bug Perhitungan Ditemukan! Di layar: {total_price_num}, Seharusnya: {expected_math_total}"