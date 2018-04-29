class CSGResource:

    def __init__(self):
        self.name       = None
        self.block_id   = None
        self.version    = None
        self.file_name  = None

    def read_data(self, data_read):
        self.name       = data_read.read_byte_string()
        self.block_id   = data_read.read_uint32()
        self.version    = data_read.read_int32()
        self.file_name  = data_read.read_byte_string()

        print(self.name)
        print(hex(self.block_id))
        print(self.version)
        print(self.file_name)
