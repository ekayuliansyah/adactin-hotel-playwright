from playwright.sync_api import Page

class SearchHotelPage:
    def __init__(self, page: Page):
        self.page = page
        
        # Locators Form Lengkap
        self.location_dropdown = page.locator("#location")
        self.hotels_dropdown = page.locator("#hotels")
        self.room_type_dropdown = page.locator("#room_type")
        self.room_nos_dropdown = page.locator("#room_nos")
        self.datepick_in_input = page.locator("#datepick_in")
        self.datepick_out_input = page.locator("#datepick_out")
        self.adult_room_dropdown = page.locator("#adult_room")
        self.child_room_dropdown = page.locator("#child_room")
        
        # Tombol Aksi
        self.search_button = page.locator("#Submit")
        self.reset_button = page.locator("#Reset")

        # ====================================================================
        # TAMBAHAN: Locators Teks Eror Validasi (Berdasarkan ID di Aplikasi Adactin)
        # ====================================================================
        self.location_err = page.locator("#location_span")
        self.room_nos_err = page.locator("#num_room_span")
        self.date_in_err = page.locator("#checkin_span")
        self.date_out_err = page.locator("#checkout_span")
        self.adult_room_err = page.locator("#adults_room_span")

    def search_hotel_complete(self, data: dict):
        """Mengisi seluruh field form pencarian menggunakan data dari JSON (Happy Path)"""
        self.location_dropdown.select_option(value=data["location"])
        self.hotels_dropdown.select_option(value=data["hotel"])
        self.room_type_dropdown.select_option(value=data["room_type"])
        self.room_nos_dropdown.select_option(value=data["rooms"])
        
        # Handling Kalender
        self.datepick_in_input.clear()
        self.datepick_in_input.fill(data["check_in"])
        self.datepick_out_input.clear()
        self.datepick_out_input.fill(data["check_out"])
        
        self.adult_room_dropdown.select_option(value=data["adults"])
        self.child_room_dropdown.select_option(value=data["children"])
        
        # Klik Submit
        self.search_button.click()

    # ====================================================================
    # TAMBAHAN: Method Pembantu Khusus Skenario Negatif / Parsial
    # ====================================================================
    def clear_dates_and_search(self):
        """Helper untuk mengosongkan tanggal lalu klik submit"""
        self.datepick_in_input.clear()
        self.datepick_out_input.clear()
        self.search_button.click()