class TgirNode:

    def __init__(self, group_id, instance_id, resource_id, type_id):
        self.group_id       = group_id
        self.instance_id    = instance_id
        self.resource_id    = resource_id
        self.type_id        = type_id
    
    @staticmethod
    def from_data(reader, do_resource):
        group_id    = reader.read_uint32()
        instance_id = reader.read_uint32()
        if do_resource:
            resource_id = reader.read_uint32()
        type_id     = reader.read_uint32()

        return TgirNode(group_id, instance_id, resource_id, type_id)
    
    def print(self):
        print('TGIR Node:')
        print('\tGroup ID:\t\t', hex(self.group_id), sep="")
        print('\tInstance ID:\t', hex(self.instance_id), sep="")
        if self.resource_id != None:
            print('\tResource ID:\t', hex(self.resource_id), sep="")
        print('\tType ID:\t\t', hex(self.type_id), sep="")
    
    