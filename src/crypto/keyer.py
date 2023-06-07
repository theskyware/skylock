import os
import base64
import binascii
from src.terminal import Terminal
from src.crypto.morse import Morse

class KeyerError:
    def __init__(self) -> None:
        self.message = "asu"

    def __str__(self) -> str:
        return "Asu"

class KeyerLossData:
    pass

class Keyer:
    def __init__(self) -> None:
        self.terminal = Terminal()

    def read_file(self, file: str):
        if os.path.isfile(file) is False:
            self.terminal.error('error load keyer')
        data = ""
        with open(file=file, mode="rb") as File:
            data = File.read().decode()
        if data == "": return KeyerError()
        spliter = data.split(" ")
        if len(spliter) != 2: return KeyerError()
        if spliter[0] != "skl": return KeyerError()
        
        datakeyer = spliter[1].split("://")
        if len(datakeyer) != 2: return KeyerError()
        if datakeyer[0] != "key": return KeyerError()
        base16_data = datakeyer[1]
        try:
            b2hex = base64.b16decode(base16_data)
            hex2morse = binascii.a2b_hex(b2hex)
            morse2data = Morse.decrypt(hex2morse.decode())
            return morse2data
        except Exception as e:
            return KeyerLossData()

    def write_file(self, key: str, file: str):
        if os.path.isfile(file) is True:
            self.terminal.warn("file already exists")
            return False
        key2morse = Morse.encrypt(key)
        morse2hex = binascii.b2a_hex(key2morse.encode())
        hex2base16 = base64.b16encode(morse2hex)
        result = f"skl key://{hex2base16.decode()}".encode()

        with open(file=file, mode="wb") as File:
            File.write(result)
            File.close()
        return True