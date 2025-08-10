import ipaddress
import re

def is_valid_cidr(cidr: str) -> bool:
    try:
        ipaddress.ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False

def is_valid_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_domain(domain: str) -> bool:
    if domain is None:
        return False
    pattern = re.compile(r'^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,}$')
    return bool(pattern.match(domain))

def is_valid_ip_or_domain(entry: str) -> bool:
    entry = re.sub(r'^[a-zA-Z]+://', '', entry)  # remove protocolo
    return is_valid_ip(entry) or is_valid_domain(entry)
