from .subnodes.sgresource               import SgResource
from .subnodes.comptree_node            import CompositionTreeNode
from .subnodes.objectgraph_node         import ObjectGraphNode
from .subnodes.datalist_extension       import DataListExtension
from .subnodes.transform_node           import TransformNode
from .subnodes.bonedata_extension       import BoneDataExtension

from .subnodes.generic.childnode_info   import ChildNodeInfo
from .subnodes.generic.identity_block   import IdentityBlock

# Could use some improvement once I get it working
class CresData:

    def __init__(self, id_block, type_code, sgresource,
                    comptree, objectgraph, chains, is_subnode, purpose_type,
                    enabled, link_index, object_count, datalists):
        # self.block_name     = block_name
        # self.block_id       = block_id
        # self.block_version  = block_version
        self.id_block       = id_block
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

        self.datalists       = datalists
        

    @staticmethod
    def from_data(reader):
        # block_name      = reader.read_byte_string()
        # block_id        = reader.read_uint32()
        # block_version   = reader.read_int32()
        id_block        = IdentityBlock.from_data(reader)

        type_code       = reader.read_byte()

        if type_code == 1:
            sgresource      = SgResource.from_data(reader)
            comptree        = IdentityBlock.from_data(reader)
            objectgraph     = ObjectGraphNode.from_data(reader)

            chain_count     = reader.read_int32()
            chains          = []
            for i in range(chain_count):
                chains.append( ChildNodeInfo.from_data(reader) )

            is_subnode      = reader.read_byte()
            purpose_type    = reader.read_int32()

            # datalists        = datalistsExtension.from_data(reader)
            datalists = []
            for i in range(objectgraph.extension_count):
                tmp_dlist = DataListExtension.from_data(reader)
                datalists.append(tmp_dlist)
            
            print('FILE=cres_data.py')
            print('Address: ', hex(reader.byte_offset), '\t', reader.byte_offset, '/', len(reader.file_data), sep='')


            TransformNode.from_data(reader).print()
            print()
            BoneDataExtension.from_data(reader).print()
            # print( reader.read_byte_string() )
            # print( hex(reader.read_uint32()) )
            # print( reader.read_int32() )
            # print(reader.read_byte())


            print('FILE=cres_data.py')
            print('Address: ', hex(reader.byte_offset), ',\tOffset:', reader.byte_offset, '/', len(reader.file_data), sep='')

            return CresData(id_block, type_code, 
                            sgresource, comptree, objectgraph, 
                            chains, is_subnode, purpose_type,
                            [], [], [], datalists)
        
        # ELSE IF type_code == 0
        objectgraph     = ObjectGraphNode.from_data(reader)
        enabled         = reader.read_byte()
        is_subnode      = reader.read_byte()
        link_index      = reader.read_int32()
        object_count    = reader.read_int32()

        # datalists        = datalistsExtension.from_data(reader)
        datalists = []
        for i in range(chain_count):
            tmp_dlist = DataListExtension.from_data(reader)

        print('FILE=cres_data.py')
        print('Address: ', hex(reader.byte_offset), '\t', reader.byte_offset, '/', len(reader.file_data), sep='')



        return CresData(id_block, type_code, 
                            [], [], objectgraph, 
                            [], is_subnode, [],
                            enabled, link_index, object_count, datalists)

    
    def print(self):
        print('Data block:')
        # print('\tBlock name:\t\t', self.block_name, sep="")
        # print('\tBlock ID:\t\t', hex(self.block_id), sep="")
        # print('\tBlock Version:\t', self.block_version, sep="")
        self.id_block.print()
        print('\tTypecode:\t\t', self.type_code, sep="")
        print()

        if self.type_code == 1:
            self.sgresource.print()
            print('\tCompositionTreeNode:')
            self.comptree.print()
            print()
            self.objectgraph.print()

            for ex in self.chains:
                ex.print()
            print()
            
            print('\tIs subnode:\t\t', self.is_subnode, sep="")
            print('\tPurpose type:\t', self.purpose_type, sep="")
        else:
            self.objectgraph.print()
            print('\tEnabled:\t\t', self.enabled, sep="")
            print('\tIs subnode:\t\t', self.is_subnode, sep="")
            print('\tLink index:\t\t', self.link_index, sep="")
            print('\tObject count:\t\t', self.object_count, sep="")
        
        for dlist in self.datalists:
            dlist.print()

        