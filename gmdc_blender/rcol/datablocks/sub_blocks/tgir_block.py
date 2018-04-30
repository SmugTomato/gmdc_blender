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


class TgirBlock:


    def __init__(self, group_id, instance_id, resource_id, type_id):
        self.group_id       = group_id
        self.instance_id    = instance_id
        self.resource_id    = resource_id
        self.type_id        = type_id
    

    @staticmethod
    def from_data(reader, do_tgi):
        group_id        = reader.read_uint32()
        instance_id     = reader.read_uint32()
        resource_id     = None
        if not do_tgi:
            resource_id     = reader.read_uint32()
        type_id         = reader.read_uint32()

        return TgirBlock(group_id, instance_id, resource_id, type_id)
    

    def print(self):
        print('TGIR Block:')
        print('\tGroup ID:\t', hex(self.group_id), sep="")
        print('\tInstance ID:\t', hex(self.instance_id), sep="")
        print('\tResource ID:\t', hex(self.resource_id), sep="")
        print('\tType ID:\t', hex(self.type_id), sep="")
                