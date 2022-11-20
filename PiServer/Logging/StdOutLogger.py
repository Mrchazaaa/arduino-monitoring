import logging
import contextlib

class StdOutLogger:
    def __init__(self, logger, level="INFO"):
        self.logger = logger
        self.level = getattr(logging, level)
        self._redirector = contextlib.redirect_stdout(self)

    def write(self, msg):
        if msg and not msg.isspace():
            self.logger.log(self.level, msg)

    def flush(self): pass

    def __enter__(self):
        self._redirector.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # let contextlib do any exception handling here
        self._redirector.__exit__(exc_type, exc_value, traceback)