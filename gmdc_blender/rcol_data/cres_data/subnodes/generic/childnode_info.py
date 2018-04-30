class ChildNodeInfo:

    def __init__(self, enabled, depends, index):
        self.enabled    = enabled
        self.depends    = depends
        self.index      = index
    
    @staticmethod
    def from_data(reader):
        enabled = reader.read_byte()
        depends = reader.read_byte()
        index   = reader.read_int32()

        return ChildNodeInfo(enabled, depends, index)
    
    def print(self):
        print('\t\tExtension Link:')
        print('\t\t\tEnabled:\t', self.enabled, sep="")
        print('\t\t\tDepends:\t', self.depends, sep="")
        print('\t\t\tIndex:\t\t', hex(self.index), sep="")