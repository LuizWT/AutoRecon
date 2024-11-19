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
