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


class BoneDataExtension:


    def __init__(self, identity, comptree_node, unknown1, unknown2,
                    unknown3, unknown4, preferred_rotation_angle):
        self.identity = identity
        self.comptree_node = comptree_node
        self.unknown1 = unknown1
        self.unknown2 = unknown2
        self.unknown3 = unknown3
        self.unknown4 = unknown4
        self.preferred_rotation_angle = preferred_rotation_angle
    

    @staticmethod
    def from_data(reader):
        identity = IdentityBlock.from_data(reader)
        comptree_node = IdentityBlock.from_data(reader)

        unknown1 = reader.read_int32()      # ??
        unknown2 = reader.read_float()      # ??
        unknown3 = reader.read_int32()      # ??
        unknown4 = reader.read_float()      # ??

        preferred_rotation_angle = []
        for _ in range(4):
            preferred_rotation_angle.append( reader.read_float() )
        
        return BoneDataExtension(identity, comptree_node, unknown1, unknown2,
                                    unknown3, unknown4, preferred_rotation_angle)
    

    def print(self):
        self.identity.print()

        print('-----|cCompositionTreeNode|-----')
        self.comptree_node.print()

        print('-----|Unknown|-----')
        print('\t?\t', self.unknown1, sep="")
        print('\t?\t', self.unknown2, sep="")
        print('\t?\t', self.unknown3, sep="")
        print('\t?\t', self.unknown4, sep="")

        print('-----|Rotation|-----')
        print('\tPreferred rotation angle:\t', self.preferred_rotation_angle, sep="")