import os
import json

from .terminal import Terminal

class Config:
    def __init__(self) -> None:
        self.config_path = os.path.join(
            os.getcwd(),
            "data",
            "config.json"
        )
        self.terminal = Terminal()
        self.data = {}

    def exists(self):
        if os.path.isfile(self.config_path) is False:
            self.terminal.error("config not found!")
            exit()

        return True
        
    def read_config(self):
        with open(self.config_path) as File:
            string = File.read()
            self.data = json.loads(string)
            File.close()
        return True

    def write_config(self, config: dict = None):
        if config is None:
            config = self.data

        data_string = json.dumps(config)
        with open(self.config_path, 'wb') as File:
            File.write(data_string)
            File.close()
