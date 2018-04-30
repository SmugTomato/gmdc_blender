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
from .data_list_extension               import DataListExtension


class DataListExtensionContainer:


    def __init__(self, identity, comptree_node, extension_type, var_name, content):
        self.identity = identity
        self.comptree_node = comptree_node
        self.var_name = var_name
        self.content = content
        self.extension_type = extension_type
    

    @staticmethod
    def from_data(reader):
        identity = IdentityBlock.from_data(reader)
        comptree_node = IdentityBlock.from_data(reader)
        extension_type = reader.read_byte()
        var_name = reader.read_byte_string()

        content_count = reader.read_int32()
        content = []
        for _ in range(content_count):
            content.append( DataListExtension.from_data(reader) )
        
        return DataListExtensionContainer(identity, comptree_node, extension_type, 
                                            var_name, content)
    

    def print(self):
        self.identity.print()

        print('-----|cCompositionTreeNode|-----')
        self.comptree_node.print()

        print('-----|Content|-----')
        print('Extension type:\t', self.extension_type, sep="")
        print('Variable name:\t', self.var_name, sep="")

        for ob in self.content:
            ob.print()