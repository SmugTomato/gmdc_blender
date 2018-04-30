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
from .sub_blocks.generic.identity_block import IdentityBlock
from .sub_blocks.object_graph_node      import ObjectGraphNode
from .sub_blocks.generic.extension      import Extension


class TransformNode:
    

    def __init__(self, identity, comptree_node, objectgraph, 
                    extensions, transform, rotation, assigned_subset):
        self.identity = identity
        self.comptree_node = comptree_node
        self.objectgraph = objectgraph
        self.extensions = extensions
        self.transform = transform
        self.rotation = rotation
        self.assigned_subset = assigned_subset
    

    @staticmethod
    def from_data(reader):
        identity = IdentityBlock.from_data(reader)
        comptree_node = IdentityBlock.from_data(reader)
        objectgraph = ObjectGraphNode.from_data(reader)

        extension_count = reader.read_int32()
        extensions = []
        for _ in range(extension_count):
            extensions.append( Extension.from_data(reader) )

        transform = []
        for _ in range(3):
            transform.append( reader.read_float() )
        
        rotation = []
        for _ in range(4):
            rotation.append( reader.read_float() )
        
        assigned_subset = reader.read_int32()

        return TransformNode(identity, comptree_node, objectgraph, 
                                extensions, transform, rotation, assigned_subset)
    

    def print(self):
        self.identity.print()

        print('-----|cCompositionTreeNode|-----')
        self.comptree_node.print()

        self.objectgraph.print()

        print('-----|Extensions|-----')
        for ob in self.extensions:
            print('  >> Extension:')
            ob.print()
        
        print('-----|Misc|-----')
        print('Transform:\t\t\t\t', self.transform, sep="")  
        print('Rotation:\t\t\t\t\t', self.rotation, sep="")  
        print('Assigned subset:\t', hex(self.assigned_subset), sep="")  