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


class GMDCElement:

    def __init__(self):
        self.ref_array_size         = None
        self.element_identity       = None
        self.identity_repitition    = None

        self.block_format   = None
        self.set_format     = None

        self.block_size     = None
        self.list_length    = None
        self.set_length     = None

        self.element_values = None
        self.references     = None

    def __get_set_length(self):
        if self.block_format == 0x01:
            return 2
        elif self.block_format == 0x02:
            return 3
        elif self.block_format == 0x04:
            return 4
        return 1

    def __get_list_length(self):
        if self.block_format != 0x04:
            return int(self.block_size / self.set_length / 4)
        return int(self.block_size / 1 / 4)

    def read_data(self, data_read):
        self.ref_array_size         = data_read.read_int32()
        self.element_identity       = data_read.read_uint32()
        self.identity_repitition    = data_read.read_int32()

        self.block_format   = data_read.read_int32()
        self.set_format     = data_read.read_int32()

        self.block_size     = data_read.read_int32()

        self.set_length     = self.__get_set_length()
        self.list_length    = self.__get_list_length()

        self.element_values = []
        for i in range(0,self.list_length):
            temp_array = []

            for j in range(0,self.set_length):
                if self.block_format == 0x04:
                    temp_val = data_read.read_byte()
                    temp_array.append(temp_val)
                else:
                    temp_val = data_read.read_float()
                    temp_array.append(temp_val)

            self.element_values.append(temp_array)

        count = data_read.read_int32()
        self.references = []
        for i in range(0,count):
            temp_val = data_read.read_int16()
            self.references.append(temp_val)


    def print(self):
        print('Items:', self.list_length)
        for i, val in enumerate(self.element_values):
            print(i, '\t', val, sep='')
