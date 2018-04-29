class CCompositionTreeNode:

    def __init__(self):
        self.file_name  = None
        self.block_id   = None
        self.version    = None

    def read_data(self, data_read):
        self.file_name  = data_read.read_byte_string()
        self.block_id   = data_read.read_uint32()
        self.version    = data_read.read_int32()
