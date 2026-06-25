from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        # 1. Definisikan Element Locators di awal (Sangat Senior & Mudah Dimaintain)
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login")
        self.error_message = page.locator(".auth_error") # Untuk validasi jika login gagal

    def navigate(self, base_url: str):
        """Membuka halaman utama Adactin Hotel"""
        self.page.goto(base_url)

    def login(self, username: str, password: str):
        """Melakukan aksi pengisian form login hingga klik tombol submit"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message_text(self) -> str:
        """Mengambil teks eror jika login gagal (untuk pengujian negatif)"""
        return self.error_message.text_content()