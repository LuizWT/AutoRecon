def validate_ports(port_string):
    try:
        port = int(port_string.strip())
        return 1 <= port <= 65535
    except ValueError:
        return False
