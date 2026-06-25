from playwright.sync_api import Page

class BookHotelPage:
    def __init__(self, page: Page):
        self.page = page
        
        # Locators Form Read-Only (Disabled) Sesuai HTML Anda
        self.hotel_name_read = page.locator("#hotel_name_dis")
        self.location_read = page.locator("#location_dis")
        self.room_type_read = page.locator("#room_type_dis")
        self.room_num_read = page.locator("#room_num_dis") # Perbaikan ID Room Num
        self.total_days_read = page.locator("#total_days_dis")
        self.price_night_read = page.locator("#price_night_dis")
        self.total_price_read = page.locator("#total_price_dis")
        self.gst_read = page.locator("#gst_dis")
        self.final_price_read = page.locator("#final_price_dis")
        
        # Locators Form Input (Enabled)
        self.first_name_input = page.locator("#first_name")
        self.last_name_input = page.locator("#last_name")
        self.address_input = page.locator("#address")
        self.cc_num_input = page.locator("#cc_num")
        self.cc_type_dropdown = page.locator("#cc_type")
        self.cc_exp_month_dropdown = page.locator("#cc_exp_month")
        self.cc_exp_year_dropdown = page.locator("#cc_exp_year")
        self.cc_cvv_input = page.locator("#cc_cvv")
        
        # Tombol Aksi
        self.book_now_button = page.locator("#book_now")
        self.cancel_button = page.locator("#cancel") # Tambahan locator tombol cancel

        # Locators Span Pesan Eror Validasi (Sesuai HTML)
        self.first_name_err = page.locator("#first_name_span")
        self.last_name_err = page.locator("#last_name_span")
        self.address_err = page.locator("#address_span")
        self.cc_num_err = page.locator("#cc_num_span")
        self.cc_type_err = page.locator("#cc_type_span")
        self.cc_expiry_err = page.locator("#cc_expiry_span")
        self.cc_cvv_err = page.locator("#cc_cvv_span")

    def get_billing_summary(self) -> dict:
        """Mengambil nilai teks menggunakan get_attribute untuk bypass elemen disabled"""
        return {
            "hotel_name": self.hotel_name_read.get_attribute("value"),
            "location": self.location_read.get_attribute("value"),
            "room_type": self.room_type_read.get_attribute("value"),
            "total_days": self.total_days_read.get_attribute("value"),
            "price_per_night": self.price_night_read.get_attribute("value"),
            "total_price": self.total_price_read.get_attribute("value"),
            "gst": self.gst_read.get_attribute("value"),
            "final_price": self.final_price_read.get_attribute("value")
        }

    def fill_billing_and_book(self, data: dict):
        """Mengisi data personal tamu hingga klik Book Now"""
        self.first_name_input.fill(data["first_name"])
        self.last_name_input.fill(data["last_name"])
        self.address_input.fill(data["address"])
        self.cc_num_input.fill(data["cc_no"])
        self.cc_type_dropdown.select_option(value=data["cc_type"])
        self.cc_exp_month_dropdown.select_option(value=data["cc_exp_month"])
        self.cc_exp_year_dropdown.select_option(value=data["cc_exp_year"])
        self.cc_cvv_input.fill(data["cc_cvv"])
        self.book_now_button.click()