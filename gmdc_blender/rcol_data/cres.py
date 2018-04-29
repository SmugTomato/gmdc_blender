from .cres_data import cres_header, cres_data
from .data_reader import DataReader

class CRES:

    CRES_IDENTIFIER = 0xE519C933

    def __init__(self, file_data, byte_offset):
        self.data_read  = DataReader(file_data, byte_offset)

        self.header         = None
        self.data_blocks    = None

    @staticmethod
    def from_test_func(file_path):
        print("reading .5cr file...\n")

        file = open(file_path, "rb")
        file_data = file.read()
        byte_offset = 0
        file.close()
        return CRES(file_data, byte_offset)

    def load_header(self):
        self.header = cres_header.CRESHeader()
        self.header.read_data(self.data_read)

    def load_data(self):
        self.data_blocks = []
        count = len(self.header.items)
        for i in range(count):
            print('index:', i)
            tmp_data = cres_data.CRESData()
            tmp_data.read_data(self.data_read)
