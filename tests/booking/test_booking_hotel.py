import allure
import os
import json
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.search_hotel_page import SearchHotelPage
from pages.select_hotel_page import SelectHotelPage
from pages.book_hotel_page import BookHotelPage
# ---- 1. IMPORT UTILS GENERATOR ----
from utils.generator import generate_fake_credit_card, generate_fake_cvv
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("ADACTIN_USERNAME")
PASSWORD = os.getenv("ADACTIN_PASSWORD")

def load_test_data():
    with open("data/search_data.json") as f:
        return json.load(f)

def test_end_to_end_booking_hotel(page: Page):
    """Skenario E2E: Validasi harga & pengisian data kartu kredit dinamis hasil generator utils"""
    login_page = LoginPage(page)
    search_hotel_page = SearchHotelPage(page)
    select_hotel_page = SelectHotelPage(page)
    book_hotel_page = BookHotelPage(page)
    
    all_data = load_test_data()
    search_data = all_data["valid_search_complete"]
    billing_data = all_data["billing_info"]
    
    # ---- 2. GENERATE DATA DINAMIS & VALIDASI ----
    generated_cc = generate_fake_credit_card()
    generated_cvv = generate_fake_cvv()
    
    # Lapis validasi sebelum input: Pastikan panjang karakter sesuai ekspektasi
    assert len(generated_cc) == 16, f"Gagal! Panjang CC harus 16 digit, terbuat: {len(generated_cc)}"
    assert len(generated_cvv) == 4, f"Gagal! Panjang CVV harus 4 digit, terbuat: {len(generated_cvv)}"
    
    # Masukkan data dinamis ke dictionary billing_data
    billing_data["cc_no"] = generated_cc
    billing_data["cc_cvv"] = generated_cvv
    
    # 3. Alur Jalan Web
    login_page.navigate(BASE_URL)
    login_page.login(USERNAME, PASSWORD)
    
    search_hotel_page.search_hotel_complete(search_data)
    select_hotel_page.select_first_hotel_and_continue()
    
    expect(page).to_have_url(f"{BASE_URL}BookHotel.php")
    
    # 4. Ambil Summary & Jalankan Asersi Matematika Harga
    summary = book_hotel_page.get_billing_summary()
    assert summary["hotel_name"] == search_data["hotel"]
    
    total_price_num = float(summary["total_price"].replace("AUD $", "").strip())
    gst_num = float(summary["gst"].replace("AUD $", "").strip())
    final_price_num = float(summary["final_price"].replace("AUD $", "").strip())
    
    assert gst_num == (total_price_num * 0.10)
    assert final_price_num == (total_price_num + gst_num)
    
    # 5. Eksekusi Pengisian Form Menggunakan Gabungan JSON + Data Utils
    book_hotel_page.fill_billing_and_book(billing_data)
    
    # Konfirmasi Akhir Sukses Booking
    expect(page).to_have_url(f"{BASE_URL}BookingConfirm.php", timeout=10000)