from . import gmdc

class GMDCElement:

    def __init__(self):
        self.ref_array_size         = None
        self.element_identity       = None
        self.identity_repitition    = None

        self.block_format   = None
        self.set_format     = None

        self.block_size     = None
        self.list_length    = None
        self.set_length     = None

        self.element_values = None
        self.references     = None

    def get_set_length(self):
        if self.block_format == 0x01:
            return 2
        elif self.block_format == 0x02:
            return 3
        return 1

    def read_data(self):
        self.ref_array_size         = gmdc.read_int32()
        self.element_identity       = gmdc.read_int32()
        self.identity_repitition    = gmdc.read_int32()

        self.block_format   = gmdc.read_int32()
        self.set_format     = gmdc.read_int32()

        self.block_size     = gmdc.read_int32()

        self.set_length     = self.get_set_length()
        self.list_length    = int(self.block_size / self.set_length / 4)

        self.element_values = []
        for i in range(0,self.list_length):
            temp_array = []

            for j in range(0,self.set_length):
                if self.block_format == 0x04:
                    temp_val = gmdc.read_int32()
                    temp_array.append(temp_val)
                else:
                    temp_val = gmdc.read_float()
                    temp_array.append(temp_val)

            self.element_values.append(temp_array)

        count = gmdc.read_int32()
        self.references = []
        for i in range(0,count):
            temp_val = gmdc.read_int16()
            self.references.append(temp_val)
