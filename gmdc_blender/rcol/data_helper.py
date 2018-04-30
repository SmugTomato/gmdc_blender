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
from .datablocks.resource_node import ResourceNode


class DataHelper:


    BONE_DATA_EXTENSION = 0xE9075BC5
    DATA_LIST_EXTENSION = 0x6A836D56
    SHAPE_REF_NODE      = 0x65245517
    TRANSFORM_NODE      = 0x65246462
    RESOURCE_NODE       = 0xE519C933


    def __init__(self):
        pass


    @classmethod
    def read_datablock(cls, reader, block_id):
        if block_id == cls.BONE_DATA_EXTENSION:
            pass
        elif block_id == cls.DATA_LIST_EXTENSION:
            pass
        elif block_id == cls.SHAPE_REF_NODE:
            pass
        elif block_id == cls.TRANSFORM_NODE:
            pass
        elif block_id == cls.RESOURCE_NODE:
            return ResourceNode.from_data(reader)