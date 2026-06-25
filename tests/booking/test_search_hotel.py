import os
import pytest
import allure
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.search_hotel_page import SearchHotelPage
from dotenv import load_dotenv

load_dotenv(override=True)

# 2. Jika os.getenv menghasilkan string kosong "", Python akan otomatis memakai string di sebelah kanan 'or'
BASE_URL = os.getenv("BASE_URL") or "https://adactinhotelapp.com/"
USERNAME = os.getenv("ADACTIN_USERNAME") or "IsiUsernameDummyAndaDisini"
PASSWORD = os.getenv("ADACTIN_PASSWORD") or "IsiPasswordDummyAndaDisini"
@pytest.fixture(autouse=True)
def setup_search_page(page: Page):
    """Fixture otomatis untuk login dan stand by di halaman Search Hotel"""
    login_page = LoginPage(page)
    login_page.navigate(BASE_URL)
    login_page.login(USERNAME, PASSWORD)
    return SearchHotelPage(page)


@allure.feature("Search Hotel Management")
@allure.story("Negative Validation Mandatory Fields")
def test_error_validation_when_mandatory_fields_are_empty(page: Page, setup_search_page):
    """Skenario Negatif: Memastikan pesan eror muncul jika field bertanda bintang kosong"""
    search_page = setup_search_page
    
    with allure.step("Mengosongkan nilai bawaan tanggal masuk dan keluar"):
        search_page.datepick_in_input.fill("")
        search_page.datepick_out_input.fill("")
        
    with allure.step("Mengubah jumlah kamar dan dewasa ke opsi silakan pilih"):
        search_page.room_nos_dropdown.select_option(index=0) # Memilih '- Select Number of Rooms -'
        search_page.adult_room_dropdown.select_option(index=0) # Memilih '- Select Adults per Room -'
        
    with allure.step("Klik tombol Search"):
        search_page.search_button.click()
        
    with allure.step("Validasi seluruh pesan eror field wajib muncul di layar"):
        # Kita gunakan ignore_case=True agar aman dari masalah perbedaan kapitalisasi huruf
        expect(search_page.location_err).to_have_text("Please Select a Location", ignore_case=True)
        expect(search_page.room_nos_err).to_have_text("Please Select Total Number of Rooms", ignore_case=True)
        expect(search_page.date_in_err).to_have_text("Please Select Check-In Date", ignore_case=True)
        expect(search_page.date_out_err).to_have_text("Please Select Check-Out Date", ignore_case=True)
        expect(search_page.adult_room_err).to_have_text("Please Select Adults per Room", ignore_case=True)


@allure.feature("Search Hotel Management")
@allure.story("Negative Validation Date Logic")
def test_error_validation_when_checkout_date_is_before_checkin_date(page: Page, setup_search_page):
    """Skenario Negatif: Mengisi tanggal check-out mendahului tanggal check-in"""
    search_page = setup_search_page
    
    with allure.step("Mengisi form lokasi dan data wajib"):
        search_page.location_dropdown.select_option(value="Sydney")
        search_page.room_nos_dropdown.select_option(value="1")
        search_page.adult_room_dropdown.select_option(value="1")
        
    with allure.step("Set tanggal Check-In lebih maju daripada Check-Out"):
        search_page.datepick_in_input.fill("25/06/2026")
        search_page.datepick_out_input.fill("24/06/2026")
        
    with allure.step("Klik tombol Search"):
        search_page.search_button.click()

    with allure.step("Validasi pesan eror anomali urutan tanggal muncul"):
        expect(search_page.date_in_err).to_have_text("Check-In Date shall be before than Check-Out Date", ignore_case=True)
        expect(search_page.date_out_err).to_have_text("Check-Out Date shall be after than Check-In Date", ignore_case=True)

@allure.feature("Search Hotel Management")
@allure.story("Optional Fields - Empty Optional Selection")
def test_search_with_empty_optional_fields(page: Page, setup_search_page):
    """Skenario Positif/Negatif: Mengisi field wajib saja dan mengosongkan field opsional"""
    search_page = setup_search_page
    
    with allure.step("Hanya memilih lokasi wajib (Sydney) dan data wajib lainnya"):
        search_page.location_dropdown.select_option(value="Sydney")
        search_page.room_nos_dropdown.select_option(value="1")
        search_page.adult_room_dropdown.select_option(value="1")
        
    with allure.step("Membiarkan Hotels dan Room Type tetap pada opsi default (- Select -)"):
        # Verifikasi nilai defaultnya sebelum submit jika diperlukan
        expect(search_page.hotels_dropdown).to_have_value("")
        expect(search_page.room_type_dropdown).to_have_value("")
        
    with allure.step("Klik tombol Search"):
        search_page.search_button.click()
        
    with allure.step("Validasi sistem berhasil masuk ke halaman Select Hotel"):
        expect(page).to_have_url(f"{BASE_URL}SelectHotel.php")


@allure.feature("Search Hotel Management")
@allure.story("Optional Fields - Specific Filtering Selection")
def test_search_with_specific_optional_fields(page: Page, setup_search_page):
    """Skenario Positif: Menyaring hotel secara spesifik dengan mengisi field opsional"""
    search_page = setup_search_page
    
    with allure.step("Mengisi seluruh kombinasi form secara spesifik"):
        search_page.location_dropdown.select_option(value="Sydney")
        search_page.hotels_dropdown.select_option(value="Hotel Creek")
        search_page.room_type_dropdown.select_option(value="Standard")
        search_page.room_nos_dropdown.select_option(value="1")
        search_page.adult_room_dropdown.select_option(value="1")
        
    with allure.step("Klik tombol Search"):
        search_page.search_button.click()
        
    with allure.step("Validasi sukses masuk ke SelectHotel.php"):
        expect(page).to_have_url(f"{BASE_URL}SelectHotel.php")


@allure.feature("Search Hotel Management")
@allure.story("Functional UI - Reset Button Verification")
def test_reset_button_functionality(page: Page, setup_search_page):
    """Skenario Fungsional: Memastikan tombol Reset mengembalikan form ke kondisi awal"""""
    search_page = setup_search_page
    
    with allure.step("Mengubah nilai bawaan form secara acak"):
        search_page.location_dropdown.select_option(value="London")
        search_page.room_nos_dropdown.select_option(value="5")
        search_page.datepick_in_input.fill("10/10/2026")
        search_page.datepick_out_input.fill("15/10/2026")
        
    with allure.step("Klik tombol Reset"):
        search_page.reset_button.click()
        
    with allure.step("Validasi seluruh nilai kembali ke setelan default"):
        # Lokasi harus kembali ke kosong / '- Select Location -'
        expect(search_page.location_dropdown).to_have_value("")
        # Room Nos kembali ke default bawaan sistem (biasanya '1')
        expect(search_page.room_nos_dropdown).to_have_value("1")
        # Kalender harus instan bersih atau kembali ke tanggal bawaan asli hari ini
        # Kita cek apakah isinya tidak sama lagi dengan tanggal modifikasi tadi
        expect(search_page.datepick_in_input).not_to_have_value("10/10/2026")
        expect(search_page.datepick_out_input).not_to_have_value("15/10/2026")