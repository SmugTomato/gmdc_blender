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
            enabled             = reader.read_byte()
            depends             = reader.read_byte()
            data_extension_ind  = reader.read_int32()
            extension_links.append( (enabled, depends, data_extension_ind) )

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

        for i, ex in enumerate(self.extension_links):
            print('\t\tExtension Link ', i, sep="")
            print('\t\t\tEnabled:\t', ex[0], sep="")
            print('\t\t\tDepends:\t', ex[1], sep="")
            print('\t\t\tData Index:\t', ex[2], sep="")
        
        print('\t\tFilename:\t', self.file_name, sep="")