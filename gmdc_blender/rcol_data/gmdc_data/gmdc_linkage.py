class GMDCLinkage:

    def __init__(self):
        self.indices            = None

        self.ref_array_size     = None
        self.active_elements    = None

        self.submodel_vertices  = None
        self.submodel_normals   = None
        self.submodel_uvs       = None

    def read_data(self, data_read):
        count = data_read.read_int32()
        self.indices = []
        for i in range(0,count):
            temp_val = data_read.read_int16()
            self.indices.append(temp_val)

        self.ref_array_size = data_read.read_int32()
        self.active_elements = data_read.read_int32()

        count = data_read.read_int32()
        self.submodel_vertices = []
        for i in range(0,count):
            temp_val = data_read.read_int16()
            self.submodel_vertices.append(temp_val)

        count = data_read.read_int32()
        self.submodel_normals = []
        for i in range(0,count):
            temp_val = data_read.read_int16()
            self.submodel_normals.append(temp_val)

        count = data_read.read_int32()
        self.submodel_uvs = []
        for i in range(0,count):
            temp_val = data_read.read_int16()
            self.submodel_uvs.append(temp_val)
