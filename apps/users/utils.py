from django.utils.crypto import get_random_string
from django.core.cache import cache


def store_otp(email):
    key = email
    value = cache.get(key)
    if value is None:
        value = get_random_string(4)
        cache.set(key, value, timeout=120)
        
    return value

def check_otp(email, send_otp):
    saved_otp = cache.get(email)
    if saved_otp is None:
        return
    if send_otp != saved_otp:
        return -1
    return True
