from playwright.sync_api import Page

class SelectHotelPage:
    def __init__(self, page: Page):
        self.page = page
        
        # Tombol navigasi utama
        self.continue_button = page.locator("#continue")
        self.cancel_button = page.locator("#cancel")
        self.error_label = page.locator("#radiobutton_span")

        # SOLUSI ROBUST: Mencari ID yang diawali 'radiobutton_' dan ambil yang pertama muncul
        self.hotel_radio_button = page.locator("input[id^='radiobutton_']").first
        
        # Untuk pencatatan data kolom lainnya, jika indeksnya melompat-lompat, 
        # kita juga bisa memanfaatkan metode .first agar tetap konsisten mengambil baris teratas
        self.first_hotel_name = page.locator("input[id^='hotel_name_']").first
        self.first_location = page.locator("input[id^='location_']").first
        self.first_rooms = page.locator("input[id^='rooms_']").first
        self.first_days = page.locator("input[id^='no_days_']").first
        self.first_price_per_night = page.locator("input[id^='price_night_']").first
        self.first_total_price = page.locator("input[id^='total_price_']").first

    def select_first_hotel_and_continue(self):
        """Memilih hotel pertama yang tersedia di tabel lalu klik Continue"""
        self.hotel_radio_button.click()
        self.continue_button.click()