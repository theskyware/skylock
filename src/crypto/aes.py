import os
import hashlib
from src.config import Config
from src.crypto.keyer import Keyer
from Crypto.Cipher import AES

class Crypto:
    # thanks: https://devrescue.com/python-encrypt-file-with-aes/
    def __init__(self) -> None:
        self.config = Config()
        self.keyer = Keyer()
        self.keyer.terminal.set_verbose(True)

        self.config.read_config()
        self.terminal = self.keyer.terminal

    def derive_key_and_iv(self, password, salt, key_length, iv_length): #derive key and IV from password and salt.
        d = d_i = b''
        while len(d) < key_length + iv_length:
            d_i = hashlib.md5(d_i + str.encode(password) + salt).digest() #obtain the md5 hash value
            d += d_i
        return d[:key_length], d[key_length:key_length+iv_length]
    
    def parse_key_and_iv(self, salt = None):
        blocksize = AES.block_size
        credentials = self.config.data['credentials']
        keyeyerpath = credentials['keyerpath']
        keyer = self.keyer.read_file(keyeyerpath)
        if salt is None: salt = os.urandom(blocksize)
        key, iv = self.derive_key_and_iv(keyer, salt, 32, blocksize)
        return key, iv, salt
    
    def encrypt(self, infile: str, outfile: str):
        blocksize = AES.block_size
        key, iv, salt = self.parse_key_and_iv()
    
        if os.path.isfile(infile) is False:
            self.terminal.warn('cannot read file, file is not found')
            return False
        
        chiper = AES.new(key, AES.MODE_CBC, iv)
        with open(infile, "rb") as FileInput:
            finished = False
            with open(outfile, "wb") as FileOut:
                FileOut.write(salt)
                while not finished:
                    chunk = FileInput.read(1024 * blocksize)
                    if len(chunk) == 0 or len(chunk) % blocksize != 0:
                        padding_length = (blocksize - len(chunk) % blocksize) or blocksize
                        chunk += str.encode(padding_length * chr(padding_length))
                        finished = True
                    FileOut.write(chiper.encrypt(chunk))
                FileOut.close()
            FileInput.close()
        return True
    
    def decrypt(self, infile: str, outfile: str):
        blocksize = AES.block_size
        with open(infile, "rb") as FileInput:
            salt = FileInput.read(blocksize)
            key, iv, _ = self.parse_key_and_iv(salt=salt)

            cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)

            with open(outfile, "wb") as FileOut:
                next_chunk = ''
                finished = False
                while not finished:
                    chunk, next_chunk = next_chunk, cipher.decrypt(FileInput.read(1024 * blocksize))
                    if len(next_chunk) == 0:
                        padding_length = chunk[-1]
                        chunk= chunk[:-padding_length]
                        finished = True
                    FileOut.write(bytes(x for x in chunk))
                FileOut.close()
            FileInput.close()
