from .cdatalist_extension import CDataListExtension

class CObjectGraphNode:

    def __init__(self):
        self.file_name  = None
        self.class_id   = None
        self.version    = None
        self.extensions = None

        self.enabled    = None
        self.depends    = None
        self.index      = None

    def read_data(self, data_read):
        self.file_name  = data_read.read_byte_string()
        self.class_id   = data_read.read_uint32()
        self.version    = data_read.read_int32()

        num_extensions = data_read.read_int32()
        extensions = []
        for i in range(num_extensions):
            dat_exten = CDataListExtension()
            dat_exten.read_data(data_read)
            extensions.append(dat_exten)

        self.enabled = data_read.read_byte()
        self.depends = data_read.read_byte()
        self.index   = data_read.read_int32()

        if self.version == 4:
            data_read.read_byte_string()
