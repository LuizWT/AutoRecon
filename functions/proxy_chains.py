import subprocess

def check_proxychains_installed():
    try:
        subprocess.run(["proxychains", "true"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def is_proxychains_enabled():
    return proxychains_enabled

def toggle_proxychains():
    global proxychains_enabled
    proxychains_enabled = not proxychains_enabled
    return proxychains_enabled

proxychains_enabled = False
