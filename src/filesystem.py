import os
from pathlib import Path
from threading import Thread

class Filesystem:
    def __init__(self) -> None:
        self.parrent = ""
        self.dirs = []
        self.files = []
        self.thread = None

    def set_parent(self, parent):
        self.parrent = parent

    def scan(self, target):
        # print ("Scanning: " + os.path.basename(target))
        obj = os.listdir(target)
        for dirs in obj:
            combine_path = os.path.join(target, dirs)
            if os.path.isdir(combine_path):
                self.dirs.append(combine_path)
                self.scan(combine_path)
            elif os.path.isfile(combine_path):
                self.files.append(combine_path)

    def run_scan(self):
        self.thread = Thread(target=self.scan, args=(self.parrent, ))
        self.thread.daemon = True
        self.thread.start()
        while self.thread.is_alive():
            print (f"\rFound: {len(self.dirs)} dirs and {len(self.files)} files", end="")
        print("")