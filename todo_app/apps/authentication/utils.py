import hashlib
import time


def generate_custom_id():
    current_time = str(time.time_ns()).encode('utf-8')
    return hashlib.sha256(current_time).hexdigest()[:16]