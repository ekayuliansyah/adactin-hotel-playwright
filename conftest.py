import os
import pytest
from dotenv import load_dotenv

# Paksa load .env jika ada
load_dotenv()

@pytest.fixture(scope="session", autouse=True)
def base_url():
    # Prioritaskan env variable dari GitHub Secrets
    # Jika tidak ada, gunakan default-nya
    url = os.environ.get("BASE_URL", "https://adactinhotelapp.com/")
    return url

# Pastikan semua page object menggunakan URL ini
# Jika page object Anda memanggil BASE_URL langsung, 
# tambahkan baris ini agar dikenali global:
os.environ["BASE_URL"] = os.environ.get("BASE_URL", "https://adactinhotelapp.com/")