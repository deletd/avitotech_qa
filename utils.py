import random
import re

def generate_seller_id() -> int:
    return random.randint(111111, 999999)

def validate_uuid(uuid_str: str) -> bool:
    if not uuid_str:
        return False
    pattern = re.compile(r'^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$', re.I)
    return bool(pattern.match(uuid_str))