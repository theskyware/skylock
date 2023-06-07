class Terminal:
    def __init__(self) -> None:
        self.verbose = False

    def set_verbose(self, verbose: bool = False):
        self.verbose = verbose
        
    def log(self, message, force_verbose: bool = False):
        if self.verbose is False and force_verbose is False:
            return False
        print (f"LOG: {message}")

    def error(self, message, force_verbose: bool = False):
        if self.verbose is False and force_verbose is False:
            return False
        print (f"ERR: {message}")

    def info(self, message, force_verbose: bool = False):
        if self.verbose is False and force_verbose is False:
            return False
        print (f"INFO: {message}")

    def warn(self, message, force_verbose: bool = False):
        if self.verbose is False and force_verbose is False:
            return False
        print (f"WARN: {message}")