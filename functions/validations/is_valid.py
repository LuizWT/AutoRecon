import re

def is_valid_cidr(cidr):

    # XXX.XXX.XXX.XXX/XX.

    pattern = re.compile(r'^\d{1,3}(\.\d{1,3}){3}/\d{1,2}$')
    if not pattern.match(cidr):
        return False

    ip, mask = cidr.split('/')
    try:
        ip_parts = [int(part) for part in ip.split('.')]
        if len(ip_parts) != 4 or any(part < 0 or part > 255 for part in ip_parts):
            return False
        if int(mask) < 0 or int(mask) > 32:
            return False
    except ValueError:
        return False
    return True

def is_valid_ip(ip):

    ipv4_regex = re.compile(
        r'^('
        r'25[0-5]|'        # 250-255
        r'2[0-4][0-9]|'    # 200-249
        r'1[0-9]{2}|'      # 100-199
        r'[1-9][0-9]?|'    # 10-99 ou 1-9
        r'0'               # 0
        r')(\.('
        r'25[0-5]|'
        r'2[0-4][0-9]|'
        r'1[0-9]{2}|'
        r'[1-9][0-9]?|'
        r'0'
        r')){3}$'
    )

    return bool(ipv4_regex.match(ip))

def is_valid_domain(domain):

    # Regex para validar domínios
    domain_regex = re.compile(
        r'^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+'  # Subdomínios e nome do domínio
        r'[A-Za-z]{2,}$'                        # Extensão do domínio (TLD)
    )
    return bool(domain_regex.match(domain))

def is_valid_ip_or_domain(entry):
    
    entry = re.sub(r'^[a-zA-Z]+://', '', entry)

    return is_valid_ip(entry) or is_valid_domain(entry)
