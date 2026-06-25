import allure
import os
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("ADACTIN_USERNAME")
PASSWORD = os.getenv("ADACTIN_PASSWORD")

def test_successful_login(page: Page):
    """Skenario Positif: Memastikan user bisa login dengan akun yang valid"""
    login_page = LoginPage(page)
    login_page.navigate(BASE_URL)
    login_page.login(USERNAME, PASSWORD)
    expect(page).to_have_url("https://adactinhotelapp.com/SearchHotel.php")

def test_failed_login_invalid_password(page: Page):
    """Skenario Negatif: Memastikan muncul pesan eror saat password salah"""
    login_page = LoginPage(page)
    login_page.navigate(BASE_URL)
    login_page.login(USERNAME, "password_ngasal_123")
    error_text = login_page.get_error_message_text()
    assert "Invalid Login details or Your Password might have expired. Click here to reset your password" in error_text