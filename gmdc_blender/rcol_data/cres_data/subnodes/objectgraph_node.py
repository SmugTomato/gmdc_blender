from .generic.childnode_info import ChildNodeInfo

class ObjectGraphNode:
    
    def __init__(self, name, class_id, version, extension_count, extension_links,
                    file_name):
        self.name               = name
        self.class_id           = class_id
        self.version            = version
        self.extension_count    = extension_count
        self.extension_links    = extension_links
        self.file_name          = file_name
    
    @staticmethod
    def from_data(reader):
        name                = reader.read_byte_string()
        class_id            = reader.read_uint32()
        version             = reader.read_int32()
        extension_count     = reader.read_int32()

        extension_links = []
        for i in range(extension_count):
            extension_links.append( ChildNodeInfo.from_data(reader) )

        file_name = '<<< No filename on versions other than 4 >>>'
        if version == 4:
            file_name = reader.read_byte_string()

        return ObjectGraphNode(name, class_id, version, extension_count, extension_links,
                                file_name)
    
    def print(self):
        print('\tcObjectGraphNode:')
        print('\t\tName:\t\t', self.name, sep="")
        print('\t\tBlock ID:\t', hex(self.class_id), sep="")
        print('\t\tVersion:\t', self.version, sep="")
        print('\t\tExtensions:\t', self.extension_count, sep="")

        for ex in self.extension_links:
            ex.print()
        
        print('\t\tFilename:\t', self.file_name, sep="")
        print()