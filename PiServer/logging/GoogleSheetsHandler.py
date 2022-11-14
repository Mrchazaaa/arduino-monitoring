import pygsheets
from logging import StreamHandler

class GoogleSheetsHandler(StreamHandler):

    def __init__(self, serviceFilePath, filename):
        StreamHandler.__init__(self)

        #authorization
        gc = pygsheets.authorize(service_file=serviceFilePath)

        #open the google spreadsheet
        sheets = gc.open(filename)
        self.sheet = sheets[0]

    def emit(self, record):
        msg = self.format(record)
        self.sheet.append_table(values=[msg])