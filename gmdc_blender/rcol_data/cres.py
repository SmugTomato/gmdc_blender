from .cres_data.cres_header  import CresHeader
from .cres_data.cres_data    import CresData
from .data_reader   import DataReader

class Cres:

    CRES_IDENTIFIER = 0xE519C933

    def __init__(self, header, data_blocks):
        # self.data_read  = DataReader(file_data, byte_offset)

        self.header         = header
        self.data_blocks    = data_blocks

    @staticmethod
    def from_test_func(file_path):
        print("reading .5cr file...\n")

        file = open(file_path, "rb")
        file_data = file.read()
        byte_offset = 0
        file.close()

        reader = DataReader(file_data, byte_offset)
        header = CresHeader.from_data(reader)
        data_blocks = []
        # data_blocks.append(CresData.from_data(reader))
        for i in range(1):
            data_blocks.append(CresData.from_data(reader))

        return Cres(header, data_blocks)

    def print(self):
        import sys
        oldstdout = sys.stdout
        sys.stdout = open("cres_out.txt", "w+")

        self.header.print()
        self.data_blocks[0].print()

        sys.stdout = oldstdout
