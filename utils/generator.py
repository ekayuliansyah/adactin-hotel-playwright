import random
import string

def generate_fake_credit_card() -> str:
    """Menghasilkan 16 digit angka acak unik untuk kartu kredit"""
    # Menghasilkan 16 digit angka string acak
    return "".join(random.choices(string.digits, k=16))

def generate_fake_cvv() -> str:
    """Menghasilkan 4 digit angka acak untuk CVV"""
    return "".join(random.choices(string.digits, k=4))