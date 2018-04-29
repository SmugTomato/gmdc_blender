from .subnodes.sgresource       import SgResource
from .subnodes.comptree_node    import CompositionTreeNode
from .subnodes.objectgraph_node import ObjectGraphNode

# Could use some improvement once I get it working
class CresData:

    def __init__(self, block_name, block_id, block_version, type_code, sgresource,
                    comptree, objectgraph, chains, is_subnode, purpose_type,
                    enabled, link_index, object_count):
        self.block_name     = block_name
        self.block_id       = block_id
        self.block_version  = block_version
        self.type_code      = type_code

        self.sgresource     = sgresource
        self.comptree       = comptree
        self.objectgraph    = objectgraph

        self.chains         = chains
        self.is_subnode     = is_subnode
        self.purpose_type   = purpose_type

        self.enabled        = enabled
        self.link_index     = link_index
        self.object_count   = object_count
        

    @staticmethod
    def from_data(reader):
        print(reader.byte_offset)

        block_name      = reader.read_byte_string()
        block_id        = reader.read_uint32()
        block_version   = reader.read_int32()
        type_code       = reader.read_byte()

        if type_code == 1:
            sgresource      = SgResource.from_data(reader)
            comptree        = CompositionTreeNode.from_data(reader)
            objectgraph     = ObjectGraphNode.from_data(reader)

            chain_count     = reader.read_int32()
            chains          = []
            for i in range(chain_count):
                enabled             = reader.read_byte()
                depends             = reader.read_byte()
                location            = reader.read_int32()
                chains.append( (enabled, depends, location) )

            is_subnode      = reader.read_byte()
            purpose_type    = reader.read_int32()

            return CresData(block_name, block_id, block_version, type_code, 
                            sgresource, comptree, objectgraph, 
                            chains, is_subnode, purpose_type,
                            [], [], [])
        
        # ELSE IF type_code == 0
        objectgraph     = ObjectGraphNode.from_data(reader)
        enabled         = reader.read_byte()
        is_subnode      = reader.read_byte()
        link_index      = reader.read_int32()
        object_count    = reader.read_int32()

        return CresData(block_name, block_id, block_version, type_code, 
                            [], [], objectgraph, 
                            [], is_subnode, [],
                            enabled, link_index, object_count)

    
    def print(self):
        print('Data block:')
        print('\tBlock name:\t\t', self.block_name, sep="")
        print('\tBlock ID:\t\t', hex(self.block_id), sep="")
        print('\tBlock Version:\t', self.block_version, sep="")
        print('\tTypecode:\t\t', self.type_code, sep="")

        if self.type_code == 1:
            self.sgresource.print()
            self.comptree.print()
            self.objectgraph.print()

            for i, ex in enumerate(self.chains):
                print('\tChain Link ', i, sep="")
                print('\t\tEnabled:\t', ex[0], sep="")
                print('\t\tDepends:\t', ex[1], sep="")
                print('\t\tLocation:\t', ex[2], sep="")
            
            print('\tIs subnode:\t\t', self.is_subnode, sep="")
            print('\tPurpose type:\t', self.purpose_type, sep="")
        else:
            self.objectgraph.print()
            print('\tEnabled:\t\t', self.enabled, sep="")
            print('\tIs subnode:\t\t', self.is_subnode, sep="")
            print('\tLink index:\t\t', self.link_index, sep="")
            print('\tObject count:\t\t', self.object_count, sep="")
        
        print('\tcDataListExtension:')


        