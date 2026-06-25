import os
import pytest
from dotenv import load_dotenv

# 1. Load data dari file .env (hanya untuk jalankan di laptop lokal)
load_dotenv()

# 2. Ambil nilai dari environment variable
# GitHub Actions akan menyuntikkan secrets ke sini secara otomatis
@pytest.fixture(scope="session", autouse=True)
def env_setup():
    os.environ["BASE_URL"] = os.getenv("BASE_URL", "https://adactinhotelapp.com/")
    os.environ["ADACTIN_USERNAME"] = os.getenv("ADACTIN_USERNAME", "")
    os.environ["ADACTIN_PASSWORD"] = os.getenv("ADACTIN_PASSWORD", "")

# 3. Opsional: Jika Anda menggunakan plugin pytest-base-url
# Ini membantu Playwright mengenali base_url secara otomatis
@pytest.fixture(scope="session")
def base_url():
    return os.environ.get("BASE_URL")