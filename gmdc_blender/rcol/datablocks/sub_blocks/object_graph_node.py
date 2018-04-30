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
from .generic.identity_block    import IdentityBlock
from .generic.extension         import Extension


class ObjectGraphNode:


    def __init__(self, identity, extensions, filename):
        self.identity = identity
        self.extensions = extensions
        self.filename = filename
    

    @staticmethod
    def from_data(reader):
        identity = IdentityBlock.from_data(reader)

        extension_count = reader.read_int32()
        extensions = []
        for _ in range(extension_count):
            extensions.append( Extension.from_data(reader) )
        
        filename = None
        if identity.version == 4:
            filename = reader.read_byte_string()
        
        return ObjectGraphNode(identity, extensions, filename)
    

    def print(self):
        print('-----|cObjectGraphNode|-----')
        self.identity.print()
        for ob in self.extensions:
            print('  >> Extenstion:')
            ob.print()
        print('Filename:\t', self.filename, sep="")