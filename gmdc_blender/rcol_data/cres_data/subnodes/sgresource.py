class SgResource:
    
    def __init__(self, name, block_id, version, file_name):
        self.name       = name
        self.block_id   = block_id
        self.version    = version
        self.file_name  = file_name
    
    @staticmethod
    def from_data(reader):
        name        = reader.read_byte_string()
        block_id    = reader.read_uint32()
        version     = reader.read_int32()
        file_name   = reader.read_byte_string()

        return SgResource(name, block_id, version, file_name)
    
    def print(self):
        print('\tcSGResource:')
        print('\t\tName:\t\t', self.name, sep="")
        print('\t\tBlock ID:\t', hex(self.block_id), sep="")
        print('\t\tVersion:\t', self.version, sep="")
        print('\t\tFilename:\t', self.file_name, sep="")