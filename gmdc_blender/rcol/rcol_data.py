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
from .datablocks.sub_blocks.tgir_block import TgirBlock
from .data_helper import DataHelper
from .data_reader import DataReader

import sys


class Rcol:


    def __init__(self, version_mark, file_links, items, data_blocks):
        self.version_mark   = version_mark
        self.file_links     = file_links
        self.items          = items
        self.data_blocks    = data_blocks
    

    @staticmethod
    def from_test_func(file_path):
        print("reading .5gd file...\n")

        file = open(file_path, "rb")
        file_data = file.read()
        byte_offset = 0
        file.close()

        reader = DataReader(file_data, byte_offset)

        return Rcol.from_data(reader)
        

    @staticmethod
    def from_data(reader):
        version_mark = reader.read_uint32()
        if version_mark != 0xffff0001:      # Means the file does not contain a version mark
            reader.byte_offset = 0          # Reset the byte offset to account for lack of version mark
            version_mark = 0
        
        link_count = reader.read_int32()
        file_links = []
        for _ in range(link_count):
            file_links.append( TgirBlock.from_data(reader, version_mark != 0xffff0001) )
        
        item_count = reader.read_int32()
        items = []
        for _ in range(item_count):
            items.append( reader.read_uint32() )
        
        data_blocks = []
        for i in range(1):
            data_blocks.append( DataHelper.read_datablock(reader, items[i]) )
        
        return Rcol(version_mark, file_links, items, data_blocks)
    

    def print(self):
        old_stdout = sys.stdout
        sys.stdout = open('cres_out.txt', 'w')

        print('Version mark:\t', hex(self.version_mark), sep="")

        print('File Links:\t', len(self.file_links), sep="")
        for ob in self.file_links:
            ob.print()
        print()
        
        print('Items:\t', len(self.items), sep="")
        for n in self.items:
            print('\t', hex(n), sep="")
        print()

        for ob in self.data_blocks:
            print('-----||Datablock||-----')
            ob.print()
            print()
        
        sys.stdout = old_stdout
        