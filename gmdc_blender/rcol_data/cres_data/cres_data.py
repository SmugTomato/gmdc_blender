from .cobject_graph_node        import CObjectGraphNode
from .ccomposition_tree_node    import CCompositionTreeNode
from .csg_resource              import CSGResource

class CRESData:

    def __init__(self):
        self.block_name     = None
        self.block_id       = None
        self.version        = None
        self.type_code      = None

        self.chains         = None
        self.subnode        = None
        self.enabled        = None
        self.purpose        = None

        self.link           = None
        self.bl_obj_count   = None

        self.csg_resource   = None
        self.ccomp_tree     = None
        self.cobj_graph     = None


    def read_data(self, data_read):
        self.block_name = data_read.read_byte_string()
        self.block_id   = data_read.read_uint32()
        self.version    = data_read.read_int32()
        self.type_code  = data_read.read_byte()

        if self.type_code == 1:
            print('offset:', data_read.byte_offset)
            self.csg_resource = CSGResource()
            self.csg_resource.read_data(data_read)

            print('offset:', data_read.byte_offset)
            self.ccomp_tree = CCompositionTreeNode()
            self.ccomp_tree.read_data(data_read)

            print('offset:', data_read.byte_offset)
            self.cobj_graph = CObjectGraphNode()
            self.cobj_graph.read_data(data_read)

            print('offset:', data_read.byte_offset)
            chain_count = data_read.read_int32()
            self.chains = []
            for i in range(chain_count):
                enabled     = data_read.read_byte()
                dependent   = data_read.read_byte()
                location    = data_read.read_uint32()
                self.chains.append( (enabled, dependent, location) )

            self.subnode = data_read.read_byte()
            self.purpose = data_read.read_int32()

        elif self.type_code == 0:
            self.enabled        = data_read.read_byte()
            self.subnode        = data_read.read_byte()
            self.link           = data_read.read_uint32()
            self.bl_obj_count   = data_read.read_int32()
