from .cdata_obj import CDataObj

class CDataListExtension:

    def __init__(self):
        self.file_name  = None
        self.block_id   = None
        self.version    = None
        self.type_name  = None
        self.class_id   = None
        self.c_version  = None
        self.exten_type = None
        self.var_name   = None

        self.objects    = None

    def read_data(self, data_read):
        print('CDataListExtenstion:', data_read.byte_offset)

        self.file_name  = data_read.read_byte_string()
        self.block_id   = data_read.read_uint32()
        self.version    = data_read.read_int32()
        self.type_name  = data_read.read_byte_string()
        self.class_id   = data_read.read_uint32()
        self.c_version  = data_read.read_int32()
        self.exten_type = data_read.read_byte()
        self.var_name   = data_read.read_byte_string()

        ob_count = data_read.read_int32()
        self.objects = []
        for i in range(ob_count):
            ob = CDataObj()
            ob.read_data(data_read)
            self.objects.append(ob)
