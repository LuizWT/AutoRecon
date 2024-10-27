import re

def is_valid_cidr(cidr):
    pattern = re.compile(r'^\d{1,3}(\.\d{1,3}){3}/\d{1,2}$')
    return pattern.match(cidr) is not None
