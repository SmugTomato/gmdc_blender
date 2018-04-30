class CompositionTreeNode:
    
    def __init__(self, name, identity, version):
        self.name       = name
        self.identity   = identity
        self.version    = version
    
    @staticmethod
    def from_data(reader):
        name        = reader.read_byte_string()
        identity    = reader.read_uint32()
        version     = reader.read_int32()

        return CompositionTreeNode(name, identity, version)
    
    def print(self):
        print('\tcCompositionTreeNode:')
        print('\t\tName:\t\t', self.name, sep="")
        print('\t\tBlock ID:\t', hex(self.identity), sep="")
        print('\t\tVersion:\t', self.version, sep="")