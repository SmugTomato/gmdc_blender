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


class GMDCGroup:

    def __init__(self):
        self.primitive_type = None
        self.link_index     = None
        self.name           = None
        self.faces          = None
        self.opacity_amount = None
        self.subsets        = None

    def read_data(self, data_read, version):
        self.primitive_type = data_read.read_int32()
        self.link_index     = data_read.read_int32()
        self.name           = data_read.read_byte_string()

        count = data_read.read_int32()
        self.faces = []
        for i in range(0,count):
            vertex_ref = data_read.read_int16()
            self.faces.append(vertex_ref)

        self.opacity_amount = data_read.read_int32()

        if version != 1:
            count = data_read.read_int32()
            self.subsets = []
            for i in range(0,count):
                subset_ref = data_read.read_int16()
                self.subsets.append(subset_ref)
