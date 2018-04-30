from .datalist_subextension import DataListSubExtension

class DataListExtension:

    def __init__(self, block_name, block_id, version, name, class_id, class_version, 
                    extension_type, var_name, sub_extensions):
        self.block_name     = block_name
        self.block_id       = block_id
        self.version        = version
        self.name           = name
        self.class_id       = class_id
        self.class_version  = class_version
        self.extension_type = extension_type
        self.var_name       = var_name
        self.sub_extensions = sub_extensions

    @staticmethod
    def from_data(reader):
        block_name          = reader.read_byte_string()
        block_id            = reader.read_uint32()
        version             = reader.read_int32()
        name                = reader.read_byte_string()
        class_id            = reader.read_int32()
        class_version       = reader.read_int32()
        extension_type      = reader.read_byte()
        var_name            = reader.read_byte_string()

        count = reader.read_int32()
        sub_extensions = []
        for i in range(count):
            sub_extensions.append(DataListSubExtension.from_data(reader))

        return DataListExtension(block_name, block_id, version, name, class_id,
                                    class_version, extension_type, var_name, sub_extensions)
    
    def print(self):
        print('\tcDataListExtension:')
        print('\t\tBlock name:\t\t', self.block_name, sep="")
        print('\t\tBlock ID:\t\t', hex(self.block_id), sep="")
        print('\t\tVersion:\t\t', self.version, sep="")
        print('\t\tName:\t\t\t', self.name, sep="")
        print('\t\tClass ID:\t\t', self.class_id, sep="")
        print('\t\tClass version:\t', self.class_version, sep="")
        print('\t\tExtension type:\t', self.extension_type, sep="")
        print('\t\tVariable name:\t', self.var_name, sep="")

        for sub in self.sub_extensions:
            sub.print()
        print()