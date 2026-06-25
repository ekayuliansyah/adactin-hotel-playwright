import allure
import os
import json
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.search_hotel_page import SearchHotelPage
from pages.select_hotel_page import SelectHotelPage
from pages.book_hotel_page import BookHotelPage
from utils.generator import generate_fake_credit_card, generate_fake_cvv
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("ADACTIN_USERNAME")
PASSWORD = os.getenv("ADACTIN_PASSWORD")

@pytest.fixture
def setup_book_page(page: Page) -> BookHotelPage:
    """Fixture untuk mempercepat alur prasyarat sampai mendarat di BookHotel.php"""
    login_page = LoginPage(page)
    search_hotel_page = SearchHotelPage(page)
    select_hotel_page = SelectHotelPage(page)
    
    with open("data/search_data.json") as f:
        all_data = json.load(f)
        
    login_page.navigate(BASE_URL)
    login_page.login(USERNAME, PASSWORD)
    search_hotel_page.search_hotel_complete(all_data["valid_search_complete"])
    select_hotel_page.select_first_hotel_and_continue()
    
    return BookHotelPage(page)


def test_error_validation_when_fields_are_empty(page: Page, setup_book_page):
    """Skenario Negatif: Memastikan pesan eror muncul jika form wajib dikosongkan"""
    book_hotel_page = setup_book_page # Memanggil fixture
    
    # Langsung klik Book Now tanpa mengisi form apa pun
    book_hotel_page.book_now_button.click()
    
    # Asersi pesan eror wajib muncul (Perhatikan typo "you" dari bawaan web Adactin)
    expect(book_hotel_page.first_name_err).to_have_text("Please Enter your First Name")
    expect(book_hotel_page.last_name_err).to_have_text("Please Enter you Last Name")
    expect(book_hotel_page.address_err).to_have_text("Please Enter your Address")
    expect(book_hotel_page.cc_num_err).to_have_text("Please Enter your 16 Digit Credit Card Number")
    expect(book_hotel_page.cc_type_err).to_have_text("Please Select your Credit Card Type")
    expect(book_hotel_page.cc_expiry_err).to_have_text("Please Select your Credit Card Expiry Month")
    expect(book_hotel_page.cc_cvv_err).to_have_text("Please Enter your Credit Card CVV Number")


def test_invalid_credit_card_length_boundary(page: Page, setup_book_page):
    """Skenario Negatif: Memasukkan nomor kartu kredit kurang dari 16 digit"""
    book_hotel_page = setup_book_page
    
    with open("data/search_data.json") as f:
        billing_data = json.load(f)["billing_info"]
        
    # Manipulasi data kartu kredit cacat (hanya 10 digit)
    billing_data["cc_no"] = "1234567890" 
    billing_data["cc_cvv"] = generate_fake_cvv()
    
    book_hotel_page.fill_billing_and_book(billing_data)
    
    # Sistem harus menolak dan mengeluarkan pesan peringatan spesifik digit
    expect(book_hotel_page.cc_num_err).to_have_text("Please Enter your 16 Digit Credit Card Number", ignore_case=True)
    # Memastikan tidak tersesat maju ke halaman konfirmasi
    assert "BookingConfirm.php" not in page.url


@pytest.mark.xfail(reason="Bug Adactin: Sistem menerima kartu kredit yang sudah kedaluwarsa (Masa lalu)")
def test_expired_credit_card_date(page: Page, setup_book_page):
    """Skenario Negatif: Transaksi ditolak jika menggunakan kartu yang kedaluwarsa di masa lalu"""
    book_hotel_page = setup_book_page
    
    with open("data/search_data.json") as f:
        billing_data = json.load(f)["billing_info"]
        
    billing_data["cc_no"] = generate_fake_credit_card()
    billing_data["cc_cvv"] = generate_fake_cvv()
    
    # Set tahun kadaluwarsa ke masa lalu
    billing_data["cc_exp_year"] = "2024" 
    
    book_hotel_page.fill_billing_and_book(billing_data)
    
    # Asersi: Sistem idealnya mendeteksi ketidakvalidan tanggal kadaluwarsa kartu
    expect(book_hotel_page.cc_expiry_err).to_have_text("Please Select your Credit Card Expiry Year")
    assert "BookingConfirm.php" not in page.url


def test_cancel_button_navigation(page: Page, setup_book_page):
    """Skenario Fungsional: Menekan tombol Cancel harus mengembalikan pengguna ke SelectHotel.php"""
    book_hotel_page = setup_book_page
    
    # Klik tombol Cancel
    book_hotel_page.cancel_button.click()
    
    # Browser harus mundur ke halaman pemilihan hotel
    expect(page).to_have_url(f"{BASE_URL}SelectHotel.php")