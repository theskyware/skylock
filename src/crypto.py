from cryptography.fernet import Fernet

class Crypto:
    def __init__(self) -> None:
        self.key = self.generate_key()

    def generate_key(self):
        pass