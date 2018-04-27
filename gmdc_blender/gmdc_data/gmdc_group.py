from . import gmdc

class GMDCGroup:

    def __init__(self):
        self.primitive_type = None
        self.link_index     = None
        self.name           = None
        self.faces          = None
        self.opacity_amount = None
        self.subsets        = None

    def read_data(self):
        self.primitive_type = gmdc.read_int32()
        self.link_index     = gmdc.read_int32()
        self.name           = gmdc.read_byte_string()

        count = gmdc.read_int32()
        self.faces = []
        for i in range(0,count):
            vertex_ref = gmdc.read_int16()
            self.faces.append(vertex_ref)

        self.opacity_amount = gmdc.read_int32()

        if gmdc.header.version != 1:
            count = gmdc.read_int32()
            self.subsets = []
            for i in range(0,count):
                subset_ref = gmdc.read_int16()
                self.subsets.append(subset_ref)
