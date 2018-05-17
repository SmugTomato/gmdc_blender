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


    BLEND_INDICES           = 0x1C4AFC56
    BLEND_WEIGHTS           = 0x5C4AFC5C
    TARGET_INDICES          = 0x7C4DEE82
    NORMAL_MORPH_DELTAS     = 0xCB6F3A6A
    COLOUR                  = 0xCB7206A1
    COLOUR_DELTAS           = 0xEB720693
    NORMALS_LIST            = 0x3B83078B
    VERTICES                = 0x5B830781
    UV_COORDINATES          = 0xBB8307AB
    UV_COORDINATE_DELTAS    = 0xDB830795
    BINORMALS               = 0x9BB38AFB
    BONE_WEIGHTS            = 0x3BD70105
    BONE_ASSIGNMENTS        = 0xFBD70111
    BUMP_MAP_NORMALS        = 0x89D92BA0
    BUMP_MAP_NORMAL_DELTAS  = 0x69D92B93
    MORPH_VERTEX_DELTAS     = 0x5CF2CFE1
    MORPH_VERTEX_MAP        = 0xDCF2CFDC
    EP4_VERTEX_ID           = 0x114113C3
    EP4_REGION_MASK         = 0x114113CD

    SET_MAIN        = 0x00
    SET_NORMS       = 0x01
    SET_UV          = 0x02
    SET_SECONDARY   = 0x03


    def __init__(self, refsize, idenity, id_repetition, block_format,
                    set_format, block_size, list_length,
                    element_values, references):
        self.ref_array_size         = refsize
        self.element_identity       = idenity
        self.identity_repitition    = id_repetition

        self.block_format   = block_format
        self.set_format     = set_format

        self.block_size     = block_size
        self.list_length    = list_length

        self.element_values = element_values
        self.references     = references


    @staticmethod
    def get_set_length(block_format):
        if block_format == 0x01:
            return 2
        elif block_format == 0x02:
            return 3
        elif block_format == 0x04:
            return 4
        return 1


    @staticmethod
    def get_list_length(block_format, block_size, set_length):
        if block_format != 0x04:
            return int(block_size / set_length / 4)
        return int(block_size / 1 / 4)

    @staticmethod
    def from_data(reader, version):
        """"Construct an element from GMDC data"""
        try:
            ref_array_size         = reader.read_int32()
            element_identity       = reader.read_uint32()
            identity_repitition    = reader.read_int32()

            block_format   = reader.read_int32()
            set_format     = reader.read_int32()

            block_size     = reader.read_int32()

            set_length     = GMDCElement.get_set_length(block_format)
            list_length    = GMDCElement.get_list_length(
                block_format, block_size, set_length
            )

            element_values = []
            for i in range(list_length):
                temp_array = []

                for j in range(set_length):
                    if block_format == 0x04:
                        temp_val = reader.read_byte()
                    else:
                        temp_val = reader.read_float()
                    temp_array.append(temp_val)

                element_values.append(temp_array)

            count = reader.read_int32()
            references = []
            for _ in range(count):
                if version == 4:
                    temp_val = reader.read_int16()
                else:
                    temp_val = reader.read_int32()
                references.append(temp_val)
        except:
            print("Error reading element!")
            return False
        else:
            return GMDCElement(ref_array_size, element_identity,
                    identity_repitition, None, None, None, None, element_values,
                    references)


    def print(self):
        print('Items:', self.list_length)
        for i, val in enumerate(self.element_values):
            print(i, '\t', val, sep='')


    def write(self, writer):
        writer.write_int32(self.ref_array_size)
        writer.write_uint32(self.element_identity)
        writer.write_int32(self.identity_repitition)

        writer.write_int32(self.block_format)
        writer.write_int32(self.set_format)

        writer.write_int32(self.block_size)
        for set in self.element_values:
            for val in set:
                if self.block_format == 0x04:
                    writer.write_byte( val )
                else:
                    writer.write_float( val )

        writer.write_int32(len(self.references))
        for ref in self.references:
            writer.write_int16(ref)


    @staticmethod
    def make_empty(block_format, set_format, identity, repetition):
        return GMDCElement(
            0, identity, repetition, block_format, set_format, 0, 0, [], []
        )

    @staticmethod
    def from_datalist(data, identity, repetition):
        ref_array_size = len(data)
        block_format = None
        set_format = GMDCElement.SET_SECONDARY
        block_size   = None

        _data_len = len(data[0])
        if _data_len == 4:
            block_format = 0x04
            block_size = ref_array_size * 4
        elif _data_len == 3:
            block_format = 0x02
            block_size = ref_array_size * 4 * 3
        elif _data_len == 2:
            block_format = 0x01
            block_size = ref_array_size * 4 * 2
        else:
            block_format = 0x00
            block_size = ref_array_size * 4

        references = []

        return GMDCElement(
            ref_array_size, identity, repetition, block_format, set_format,
            block_size, ref_array_size, data, []
        )


    # Horrible code down here... Will fix this later
    @staticmethod
    def empty_elements(b_models):
        elements = []

        # Empty elements first
        elements.append(
            GMDCElement.make_empty(0x02, GMDCElement.SET_MAIN,
                                    GMDCElement.VERTICES, 0)
        )
        elements.append(
            GMDCElement.make_empty(0x02, GMDCElement.SET_NORMS,
                                    GMDCElement.NORMALS_LIST, 0)
        )
        for i in range(4):
            elements.append(
                GMDCElement.make_empty(0x01, GMDCElement.SET_UV,
                                        GMDCElement.UV_COORDINATES, i)
            )
        for i in range(2):
            elements.append(
                GMDCElement.make_empty(0x04, GMDCElement.SET_UV,
                                        GMDCElement.UV_COORDINATE_DELTAS, i)
            )
        # Per group empty elements now
        for mod in b_models:
            if len(mod.bone_assign) > 0:
                # Bone Assignments
                elements.append(
                    GMDCElement.make_empty(0x04, GMDCElement.SET_SECONDARY,
                                            GMDCElement.BONE_ASSIGNMENTS, 0)
                )
                # Bone Weights
                elements.append(
                    GMDCElement.make_empty(0x02, GMDCElement.SET_SECONDARY,
                                            GMDCElement.BONE_WEIGHTS, 0)
                )
        for mod in b_models:
            if len(mod.morphs) > 0:
                for i, _ in enumerate(mod.morphs):
                    # Morph Vertex Delta
                    elements.append(
                        GMDCElement.make_empty(0x02, GMDCElement.SET_SECONDARY,
                                                GMDCElement.MORPH_VERTEX_DELTAS, i)
                    )
                for i, _ in enumerate(mod.morphs):
                    # Morph Vertex Delta
                    elements.append(
                        GMDCElement.make_empty(0x02, GMDCElement.SET_SECONDARY,
                                                GMDCElement.NORMAL_MORPH_DELTAS, i)
                    )
                # Morph Vertex Map
                elements.append(
                    GMDCElement.make_empty(0x04, GMDCElement.SET_SECONDARY,
                                            GMDCElement.MORPH_VERTEX_MAP, 0)
                )
        for mod in b_models:
            if len(mod.tangents) > 0:
                elements.append(
                    GMDCElement.make_empty(0x02, GMDCElement.SET_SECONDARY,
                                            GMDCElement.BUMP_MAP_NORMALS, 0)
                )

        return elements


    @staticmethod
    def from_blender(b_models, bones):
        elements = GMDCElement.empty_elements(b_models)
        links = []

        link_index = len( elements )
        for mod in b_models:
            link_list = []

            # Needs to be done for every element
            # Will find a better method later (I hope)
            link_list.append(link_index)
            link_index += 1
            # Vertices
            elements.append(
                GMDCElement.from_datalist(
                    mod.vertices, GMDCElement.VERTICES, 0)
            )
            link_list.append(link_index)
            link_index += 1
            # Normals
            elements.append(
                GMDCElement.from_datalist(
                    mod.normals, GMDCElement.NORMALS_LIST, 0)
            )
            link_list.append(link_index)
            link_index += 1
            # UV
            elements.append(
                GMDCElement.from_datalist(
                    mod.uvs, GMDCElement.UV_COORDINATES, 0)
            )
            if mod.bone_assign:
                link_list.append(link_index)
                link_index += 1
                # Bone Assignment
                elements.append(
                    GMDCElement.from_datalist(
                        mod.bone_assign, GMDCElement.BONE_ASSIGNMENTS, 0)
                )
                link_list.append(link_index)
                link_index += 1
                # Bone Weights
                elements.append(
                    GMDCElement.from_datalist(
                        mod.bone_weight, GMDCElement.BONE_WEIGHTS, 0)
                )
            if mod.morphs:
                for i, morph in enumerate(mod.morphs):
                    link_list.append(link_index)
                    link_index += 1
                    # Morph Vertex Delta
                    elements.append(
                        GMDCElement.from_datalist(
                            morph.deltas, GMDCElement.MORPH_VERTEX_DELTAS, i)
                    )
                for i, morph in enumerate(mod.morphs):
                    link_list.append(link_index)
                    link_index += 1
                    # Morph Vertex Delta
                    elements.append(
                        GMDCElement.from_datalist(
                            morph.ndeltas, GMDCElement.NORMAL_MORPH_DELTAS, i)
                    )
                link_list.append(link_index)
                link_index += 1
                # Morph Vertex Map
                elements.append(
                    GMDCElement.from_datalist(
                        mod.morph_bytemap, GMDCElement.MORPH_VERTEX_MAP, 0)
                )
            if len(mod.tangents) > 0:
                link_list.append(link_index)
                link_index += 1
                # Bump Map Normals
                elements.append(
                    GMDCElement.from_datalist(
                        mod.tangents, GMDCElement.BUMP_MAP_NORMALS, 0)
                )

            links.append(link_list)

        return ( elements, links )
