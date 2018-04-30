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


class DataListExtension:


    def __init__(self, extension_type, var_name, content):
        self.extension_type = extension_type
        self.var_name = var_name
        self.content = content
    

    @staticmethod
    def from_data(reader):
        extension_type = reader.read_byte()
        var_name = reader.read_byte_string()
        content = None

        if extension_type == 2:         # Delta, no further description
            content = reader.read_uint32()
        elif extension_type == 3:       # Float, no further description
            content = reader.read_float()
        elif extension_type == 5:       # Translation [x, y, z]
            content = []
            for _ in range(3):
                content.append( reader.read_float() )
        elif extension_type == 6:       # Tag, name
            content = reader.read_byte_string()
        elif extension_type == 7:       # Another level of recursion
            content = DataListExtension.from_data(reader)
        elif extension_type == 8:       # Rotation [x, y, z, w]
            content = []
            for _ in range(4):
                content.append( reader.read_float() )
        elif extension_type == 9:       # Some data?
            length = reader.read_int32()
            content = []
            for _ in range(length):
                content.append( reader.read_byte() )
        
        return DataListExtension(extension_type, var_name, content)
    

    def print(self):
        print('\t-----|Subnode|-----')
        print('\tExtension type:\t', self.extension_type, sep="")
        print('\tVariable name:\t', self.var_name, sep="")

        if self.extension_type == 7:
            for ob in self.content:
                ob.print()
        else:
            print('\tContent:\t', self.content, sep="")