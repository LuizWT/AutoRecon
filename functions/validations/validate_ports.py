import re

def validate_ports(ports_string):
    # Valida se a entrada está entre os seguintes formatos:
    # - Portas individuais: 8080
    # - Portas individuais separadas por vírgulas: 21,22,80
    # - Faixas de portas: 1-100
    # - Combinações: 21,22,80,100-200
    pattern = re.compile(r'^(\d{1,5}(-\d{1,5})?)(,(\d{1,5}(-\d{1,5})?))*$')
    if not pattern.match(ports_string):
        return False

    try:
        for part in ports_string.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                if start > end or start < 1 or end > 65535:
                    return False
            else:
                port = int(part)
                if port < 1 or port > 65535:
                    return False
    except ValueError:
        return False

    return True
