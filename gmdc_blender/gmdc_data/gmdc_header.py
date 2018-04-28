from . import gmdc

class GMDCHeader:

    def __init__(self):
        self.language           = None
        self.string_style       = None
        self.repeat_value       = None
        self.index_value        = None
        self.file_type          = None
        self.name               = None
        self.block_id           = None
        self.version            = None
        self.block_name         = None
        self.resource_id        = None
        self.resource_version   = None
        self.file_name          = None

    def read_data(self, data_read):
        self.language           = data_read.read_int16()
        self.string_style       = data_read.read_int16()
        self.repeat_value       = data_read.read_int32()
        self.index_value        = data_read.read_int32()
        self.file_type          = data_read.read_uint32()
        self.name               = data_read.read_byte_string()
        self.block_id           = data_read.read_uint32()
        self.version            = data_read.read_int32()
        self.block_name         = data_read.read_byte_string()
        self.resource_id        = data_read.read_int32()
        self.resource_version   = data_read.read_int32()
        self.file_name          = data_read.read_byte_string()
