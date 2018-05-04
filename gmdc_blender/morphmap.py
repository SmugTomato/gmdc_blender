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
from .element_id import ElementID


class MorphMap:



    def __init__(self, name, deltas):
        self.name = name
        self.deltas = deltas


    @staticmethod
    def make_morphs(gmdc_data, group_index, element_indices):
        morphs = []
        namepairs = gmdc_data.model.name_pairs
        iter = 0
        for pair in namepairs:
            name = pair[0] + ', ' + pair[1]
            deltas = None

            # Skip empty morph name pair, the use of these is unknown
            if name == ', ':
                morphs.append( MorphMap(name, None) )
                continue

            for ind in element_indices:
                if gmdc_data.elements[ind].element_identity == \
                    ElementID.MORPH_VERTEX_DELTAS and \
                    gmdc_data.elements[ind].identity_repitition == iter:
                        deltas = MorphMap.__read_deltas( gmdc_data.elements[ind] )
                        break

            iter += 1

            morphs.append( MorphMap(name, deltas) )
        return morphs

    @staticmethod
    def __read_deltas( element ):
        deltas = []
        for line in element.element_values:
            # Flip X and Y just like the verices
            deltas.append( (-line[0], -line[1], line[2]) )
        return deltas
