class DataListSubExtension:

    def __init__(self, extension_type, var_name, content):
        self.extension_type = extension_type
        self.var_name       = var_name
        self.content        = content

    @staticmethod
    def from_data(reader):
        extension_type  = reader.read_byte()
        var_name        = reader.read_byte_string()
        content         = 'Empty'
        
        if extension_type == 2:     # Delta of something, not sure what it does
            content = reader.read_uint32()
        elif extension_type == 3:   # Some float value, not sure what it does
            content = reader.read_float()
        elif extension_type == 5:    # Translation vector
            content = []
            for i in range(3):
                content.append(reader.read_float())
        elif extension_type == 6:    # Tag
            content = reader.read_byte_string()
        elif extension_type == 7:   # Go into another recursive loop :c
            content = DataListSubExtension.from_data(reader)
        elif extension_type == 8:   # Rotation quaternion
            content = []
            for i in range(4):
                content.append(reader.read_float())
        elif extension_type == 9:   # Length of following data, not sure what it means
            data_length = reader.read_int32()
            content = []
            for i in range(data_length):
                content.append(reader.read_byte())
        
        return DataListSubExtension(extension_type, var_name, content)
    
    def print(self):
        print('\t\tcDataListExtension (SubNode):')
        print('\t\t\tExtension type:\t', self.extension_type, sep="")
        print('\t\t\tVariable name:\t', self.var_name, sep="")

        if self.extension_type == 7:
            print('\t\t\tContent:')
            self.content.print()
        else:
            print('\t\t\tContent:', self.content, sep="")