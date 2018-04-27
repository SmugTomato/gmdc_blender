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

    def read_data(self):
        self.language           = gmdc.read_int16()
        self.string_style       = gmdc.read_int16()
        self.repeat_value       = gmdc.read_int32()
        self.index_value        = gmdc.read_int32()
        self.file_type          = gmdc.read_int32()
        self.name               = gmdc.read_byte_string()
        self.block_id           = gmdc.read_int32()
        self.version            = gmdc.read_int32()
        self.block_name         = gmdc.read_byte_string()
        self.resource_id        = gmdc.read_int32()
        self.resource_version   = gmdc.read_int32()
        self.file_name          = gmdc.read_byte_string()
