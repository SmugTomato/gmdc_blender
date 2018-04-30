class GMDCSubset:

    vertex_coords = 3    # position [x,y,z]

    def __init__(self):
        self.vertices   = None
        self.faces      = None

    def read_data(self, data_read):
        vert_count = data_read.read_int32()
        if vert_count > 0:
            face_count = data_read.read_int32()

            self.vertices = []
            for i in range(0,vert_count):
                temp_verts = []
                for i in range(0,GMDCSubset.vertex_coords):
                    temp_val = data_read.read_float()
                    temp_verts.append(temp_val)
                self.vertices.append(temp_verts)

            self.faces = []
            for i in range(0,face_count):
                temp_val = data_read.read_int16()
                self.faces.append(temp_val)
