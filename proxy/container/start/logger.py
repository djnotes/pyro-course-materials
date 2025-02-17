import logging
import logging.handlers

class AppLogger:
    fh = logging.handlers.RotatingFileHandler(filename="log/app.log", maxBytes=10_000_000, backupCount=3)
    fh.setLevel(logging.INFO)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    fformatter = logging.Formatter("%(asctime)s - %(name)s - %(filename)s - %(lineno)s: %(message)s")
    cformatter = logging.Formatter("%(name)s - %(lineno)s: %(message)s")

    fh.setFormatter(fformatter)
    ch.setFormatter(cformatter)

    def __init__(self, name):
        self.logger = logging.Logger(name)
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)
        

    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
    
    