'''
Copyright (C) 2018 SmugTomato

Created by SmugTomato

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
''' 
from .sub_blocks.sg_resource            import SgResource
from .sub_blocks.object_graph_node      import ObjectGraphNode

from .sub_blocks.generic.identity_block import IdentityBlock
from .sub_blocks.generic.extension      import Extension


class ResourceNode:


    def __init__(self, identity, typecode, sg_resource, composition_tree, object_graph,
                    chains, is_subnode, is_enabled, purpose_type, object_link, block_count):
        self.identity           = identity
        self.typecode           = typecode
        self.sg_resource        = sg_resource
        self.composition_tree   = composition_tree
        self.object_graph       = object_graph
        self.chains             = chains
        self.is_subnode         = is_subnode
        self.is_enabled         = is_enabled
        self.purpose_type       = purpose_type
        self.object_link        = object_link
        self.block_count        = block_count


    @staticmethod
    def from_data(reader):
        identity = IdentityBlock.from_data(reader)
        typecode = reader.read_byte()

        if typecode == 1:
            return ResourceNode.__type_one(reader, identity, typecode)
        return ResourceNode.__type_zero(reader, identity, typecode)
    

    @staticmethod
    def __type_one(reader, identity, typecode):
        sg_resource = SgResource.from_data(reader)
        composition_tree = IdentityBlock.from_data(reader)
        object_graph = ObjectGraphNode.from_data(reader)

        chain_count = reader.read_int32()
        chains = []
        for _ in range(chain_count):
            chains.append( Extension.from_data(reader) )
        
        is_subnode = reader.read_byte()
        purpose_type = reader.read_int32()

        return ResourceNode(identity, typecode, sg_resource, composition_tree,
                            object_graph, chains, is_subnode, None, 
                            purpose_type, None, None)


    @staticmethod
    def __type_zero(reader, identity, typecode):
        pass
    

    def print(self):
        self.identity.print()
        print('Typecode:\t', self.typecode, sep="")

        if self.typecode == 1:
            self.sg_resource.print()
            print('-----|cCompositionTreeNode|-----')
            self.composition_tree.print()

            self.object_graph.print()

            print('-----|Chains|-----')
            for ob in self.chains:
                print('  >> Chain')
                ob.print()

            print('-----|Misc|-----')
            print('Subnode:\t', self.is_subnode, sep="")
            print('Purpose Type:\t', self.purpose_type, sep="")
        else:
            self.object_graph.print()
            print('-----|Misc|-----')
            print('Enabled:\t', self.is_enabled, sep="")
            print('Subnode:\t', self.is_subnode, sep="")
            print('Link index:\t', self.object_link, sep="")
            print('Block Objects:\t', self.block_count, sep="")
        