class CompositionTreeNode:
    
    def __init__(self, name, block_id, version):
        self.name       = name
        self.block_id   = block_id
        self.version    = version
    
    @staticmethod
    def from_data(reader):
        name        = reader.read_byte_string()
        block_id    = reader.read_uint32()
        version     = reader.read_int32()

        return CompositionTreeNode(name, block_id, version)
    
    def print(self):
        print('\tcCompositionTreeNode:')
        print('\t\tName:\t\t', self.name, sep="")
        print('\t\tBlock ID:\t', hex(self.block_id), sep="")
        print('\t\tVersion:\t', self.version, sep="")