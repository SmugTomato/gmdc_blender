class CDataObj:

    def __init__(self):
        self.exten_type = None
        self.var_name   = None
        self.content    = None  # variable type can change depending on exten_type
        self.objects    = None

    def read_data(self, data_read):

        self.exten_type = data_read.read_byte()
        self.var_name   = data_read.read_byte_string()

        if self.exten_type == 2:     # Delta
            self.content = data_read.read_uint32()
        elif self.exten_type == 3:   # Float
            self.content = data_read.read_float()
        elif self.exten_type == 5:   # Translation (x, y, z)
            self.content = []
            for i in range(3):
                self.content.append(data_read.read_float())
        elif self.exten_type == 6:   # Tag
            self.content = data_read.read_byte_string()
        elif self.exten_type == 7:   # Recursive
            self.content = CDataObj()
            self.content.read_data(data_read)
        elif self.exten_type == 8:   # Rotation (x, y, z, w)
            self.content = []
            for i in range(4):
                self.content.append(data_read.read_float())
        elif self.exten_type == 9:   # Data?
            count = data_read.read_int32()
            self.content = []
            for i in range(count):
                self.content.append(data_read.read_byte())
