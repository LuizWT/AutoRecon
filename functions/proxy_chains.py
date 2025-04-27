import subprocess

class ProxyManager:
    _enabled = False

    @classmethod
    def check_installed(cls):
        try:
            subprocess.run(["proxychains", "true"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False

    @classmethod
    def toggle(cls):
        cls._enabled = not cls._enabled
        return cls._enabled

    @classmethod
    def is_enabled(cls):
        return cls._enabled

