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
from .sub_blocks.generic.extension      import Extension
from .transform_node                    import TransformNode


class ShapeRefNode:

    # Lots of unknown items in this block
    def __init__(self, identity, renderable_node, bounded_node, transform_node,
                    unknown16, unknown32_1, practical, unknown32_2, unknown8,
                    shape_links, unknown32_3, unknown_list, blend_list, unknown_list_2,
                    unknown32_4):
        self.identity = identity
        self.renderable_node = renderable_node
        self.bounded_node = bounded_node
        self.transform_node = transform_node

        self.unknown16 = unknown16
        self.unknown32_1 = unknown32_1

        self.practical = practical

        self.unknown32_2 = unknown32_2
        self.unknown8 = unknown8

        self.shape_links = shape_links

        self.unknown32_3 = unknown32_3
        self.unknown_list = unknown_list

        self.blend_list = blend_list

        self.unknown_list_2 = unknown_list_2
        self.unknown32_4 = unknown32_4
    

    @staticmethod
    def from_data(reader):
        identity = IdentityBlock.from_data(reader)
        renderable_node = IdentityBlock.from_data(reader)
        bounded_node = IdentityBlock.from_data(reader)
        transform_node = TransformNode.from_data(reader)

        unknown16 = reader.read_int16()
        unknown32_1 = reader.read_int32()

        practical = reader.read_byte_string()

        unknown32_2 = reader.read_int32()
        unknown8 = reader.read_byte()

        shape_link_count = reader.read_int32()
        shape_links = []
        for _ in range(shape_link_count):
            shape_links.append( Extension.from_data(reader) )
        
        unknown32_3 = reader.read_int32()
        count = reader.read_int32()
        unknown_list = []
        blend_list = []
        for _ in range(count):
            unknown_list.append( reader.read_int32() )
            if identity.version == 21:
                blend_list.append( reader.read_byte_string() )
        
        count = reader.read_int32()
        unknown_list_2 = []
        for _ in range(count):
            unknown_list_2.append( reader.read_byte() )
        
        unknown32_4 = reader.read_uint32()

        return ShapeRefNode(identity, renderable_node, bounded_node, transform_node,
                                unknown16, unknown32_1, practical, unknown32_2, unknown8,
                                shape_links, unknown32_3, unknown_list, blend_list, 
                                unknown_list_2, unknown32_4)
    

    def print(self):
        self.identity.print()
        print('-----|IdentityBlock|-----')
        self.renderable_node.print()
        print('-----|IdentityBlock|-----')
        self.bounded_node.print()
        print('-----|cTransformNode|-----')
        self.transform_node.print()

        print('-----|Shape links and unknowns|-----')
        print('?\t', self.unknown16, sep="")
        print('?\t', self.unknown32_1, sep="")
        print('?\t', self.practical, sep="")
        print('?\t', self.unknown32_2, sep="")
        print('?\t', self.unknown8, sep="")
        for ob in self.shape_links:
            print('>> Shape link:')
            ob.print()
        print('?\t', self.unknown32_3, sep="") 
        print('>> Unknown list')       
        for el in self.unknown_list:
            print('\t?\t', el, sep="")
        print('>> Blend list')       
        for el in self.blend_list:
            print('\t?\t', el, sep="")
        print('>> Unknown list 2')       
        for el in self.unknown_list_2:
            print('\t?\t', el, sep="")
        print('?\t', hex(self.unknown32_4), sep="") 
        