class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, level, cliStdOut):
       self.logger = logger
       self.level = level
       self.linebuf = ''
       self.cliStdOut = cliStdOut

    def write(self, buf):
       for line in buf.rstrip().splitlines():
          self.cliStdOut.write(line.rstrip())
          self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass
