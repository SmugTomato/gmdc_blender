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
from rcol.data_helper import DataHelper
import operator


class BoneData:


    def __init__(self, orig_index, name, subset, position, rotation, parent):
        self.orig_index = orig_index
        self.name       = name
        self.subset     = subset
        self.position   = position
        self.rotation   = rotation
        self.parent     = parent


    @staticmethod
    def dummy_bone(num):
        name = 'Joint' + str(num)
        return BoneData(None, name, num, (0, 0, 0), (0, 0, 0, 1), -1)


    @staticmethod
    def from_data(data, block):
        orig_index = data.index(block)
        name = block.objectgraph.filename
        subset = block.assigned_subset
        position = (-block.transform[0], block.transform[1], block.transform[2])
        rotation = (block.rotation[3], block.rotation[0],
                    block.rotation[1], block.rotation[2])
        parent = DataHelper.parent_of_node(data, block)

        return BoneData(orig_index, name, subset, position, rotation, parent)


    def update_parent_index(self, bones, data):
        for i, b in enumerate(bones):
            if b.orig_index == self.parent:
                self.parent = i


    def print(self):
        print(self.name)
        print('Subset:', self.subset)
        print('OrigIndex:', self.orig_index)
        print('Parent:', self.parent)
        print('Position:', self.position)
        print('Rotation:', self.rotation)
        print()
