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
from .datablocks.resource_node                  import ResourceNode
from .datablocks.data_list_extension_container  import DataListExtensionContainer
from .datablocks.transform_node                 import TransformNode
from .datablocks.bone_data_extension            import BoneDataExtension
from .datablocks.shape_ref_node                 import ShapeRefNode


class DataHelper:


    BONE_DATA_EXTENSION = 0xE9075BC5
    DATA_LIST_EXTENSION = 0x6A836D56
    SHAPE_REF_NODE      = 0x65245517
    TRANSFORM_NODE      = 0x65246462
    RESOURCE_NODE       = 0xE519C933


    @classmethod
    def read_datablock(cls, reader, block_id):
        if block_id == cls.BONE_DATA_EXTENSION:
            return BoneDataExtension.from_data(reader)
        elif block_id == cls.DATA_LIST_EXTENSION:
            return DataListExtensionContainer.from_data(reader)
        elif block_id == cls.SHAPE_REF_NODE:
            return ShapeRefNode.from_data(reader)
        elif block_id == cls.TRANSFORM_NODE:
            return TransformNode.from_data(reader)
        elif block_id == cls.RESOURCE_NODE:
            return ResourceNode.from_data(reader)
        return None

    @classmethod
    def parent_of_node(cls, data, d_block):
        parent = -1     # Default to -1 for parentless bones

        # Iterate through all data blocks until parent is found
        for i, block in enumerate(data):
            # Check if identity == TransformNode
            if block.identity.identity == cls.TRANSFORM_NODE:
                # Iterate through all its children until the index of d_block is found
                for child in block.children:
                    if child.index == data.index(d_block):
                        # Check if this block is an actual bone and not IK related
                        if block.assigned_subset != 0x7fffffff:
                            return i
                        return cls.parent_of_node(data, block)

        return parent
