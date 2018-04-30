from .comptree_node             import CompositionTreeNode
from .objectgraph_node          import ObjectGraphNode
from .generic.childnode_info    import ChildNodeInfo

class TransformNode:

    def __init__(self, name, block_id, block_version, comptree, objgraph,
                    extension_links, transform, rotation, assigned_subset):
        self.name               = name
        self.block_id           = block_id
        self.block_version      = block_version
        self.comptree           = comptree
        self.objgraph           = objgraph
        self.extension_links    = extension_links
        self.transform          = transform
        self.rotation           = rotation
        self.assigned_subset    = assigned_subset
    
    @staticmethod
    def from_data(reader):
        name            = reader.read_byte_string()
        block_id        = reader.read_uint32()
        block_version   = reader.read_int32()

        comptree = CompositionTreeNode.from_data(reader)
        objgraph = ObjectGraphNode.from_data(reader)

        count = reader.read_int32()
        extension_links = []
        for i in range(count):
            extension_links.append( ChildNodeInfo.from_data(reader) )
        
        transform = []
        for i in range(3):
            transform.append( reader.read_float() )
        
        rotation = []
        for i in range(4):
            rotation.append( reader.read_float() )
        
        assigned_subset = reader.read_uint32()

        return TransformNode(name, block_id, block_version, comptree, objgraph,
                                extension_links, transform, rotation, assigned_subset)
    
    def print(self):
        print('\tcTransformNode:')
        print('\t\tBlock name:\t\t', self.name, sep="")
        print('\t\tBlock ID:\t\t', hex(self.block_id), sep="")
        print('\t\tVersion:\t\t', self.block_version, sep="")

        self.comptree.print()
        self.objgraph.print()

        print(len(self.extension_links))
        for ex in self.extension_links:
            ex.print()
        
        print('\t\tTransform:\t\t', self.transform, sep="")
        print('\t\tRotation:\t\t', self.rotation, sep="")
        print('\t\tAssigned Subset:\t', self.assigned_subset, sep="")
