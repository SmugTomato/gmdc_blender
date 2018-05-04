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


class BoneData:


    # Same order as the subgroups section of the GMDC
    bone_parent_table = [
        # Base
        ('__skel',  None),
        ('root_trans',       '__skel'),
        ('root_rot',         'root_trans'),
        ('spine0',           'root_rot'),
        ('spine1',           'spine0'),
        ('spine2',           'spine1'),
        ('neck',             'spine2'),
        ('head',             'neck'),
        ('Joint8',           None),
        # Right arm
        ('r_clavicle',       'spine2'),
        ('r_upperarm',       'r_clavicle'),
        ('r_bicep',          'r_upperarm'),
        ('r_forearm',        'r_bicep'),
        ('r_wrist',          'r_forearm'),
        ('r_hand',           'r_wrist'),
        ('r_thumb0',         'r_hand'),
        ('r_thumb1',         'r_thumb0'),
        ('r_thumb2',         'r_thumb1'),
        ('r_index0',         'r_hand'),
        ('r_index1',         'r_index0'),
        ('r_mid0',           'r_hand'),
        ('r_mid1',           'r_mid0'),
        ('r_pinky0',         'r_hand'),
        ('r_pinky1',         'r_pinky0'),
        # Left arm
        ('l_clavicle',       'spine2'),
        ('l_upperarm',       'l_clavicle'),
        ('l_bicep',          'l_upperarm'),
        ('l_forearm',        'l_bicep'),
        ('l_wrist',          'l_forearm'),
        ('l_hand',           'l_wrist'),
        ('l_thumb0',         'l_hand'),
        ('l_thumb1',         'l_thumb0'),
        ('l_thumb2',         'l_thumb1'),
        ('l_index0',         'l_hand'),
        ('l_index1',         'l_index0'),
        ('l_mid0',           'l_hand'),
        ('l_mid1',           'l_mid0'),
        ('l_pinky0',         'l_hand'),
        ('l_pinky1',         'l_pinky0'),
        # Lower body
        ('breathe_trans',    'spine0'),
        ('pelvis',          'root_rot'),
        # Right leg
        ('r_thigh',          'pelvis'),
        ('r_calf',           'r_thigh'),
        ('r_foot',           'r_calf'),
        ('r_toe',            'r_foot'),
        # Left leg
        ('l_thigh',          'pelvis'),
        ('l_calf',           'l_thigh'),
        ('l_foot',           'l_calf'),
        ('l_toe',            'l_foot'),
        # Clothes
        ('dress',            'pelvis'),
        ('r_longsleeve',     'r_forearm'),
        ('r_shortsleeve',    'r_upperarm'),
        ('l_longsleeve',     'l_forearm'),
        ('l_shortsleeve',    'l_upperarm'),
        ('r_pantsleg',       'r_calf'),
        ('r_shorts',         'r_thigh'),
        ('l_pantsleg',       'l_calf'),
        ('l_shorts',         'l_thigh'),
        # Misc
        ('Joint58',              None),
        ('backtarget_surface',   'spine1'),
        # Hair
        ('c_hair',           'head'),
        ('f_hair',           'head'),
        ('r_hair',           'head'),
        ('l_hair',           'head'),
        ('b_hair',           'head')
    ]


    def __init__(self, name, parent, subset, position, rotation):
        self.name       = name
        self.parent     = parent
        self.subset     = subset
        self.position   = position      # Translate  XYZ
        self.rotation   = rotation      # Quaternion WXYZ


    @staticmethod
    def build_bones(gmdc):
        print('Loading skeleton.\n')
        bones = []

        for subset, nameset in enumerate(BoneData.bone_parent_table):
            trans_bl = gmdc.model.transforms[subset]

            rotation  = ( -trans_bl[3], trans_bl[0], trans_bl[1], trans_bl[2] )
            translate = ( trans_bl[4], trans_bl[5], trans_bl[6] )
            name = nameset[0]
            parent = nameset[1]

            bones.append(BoneData(name, parent, subset, translate, rotation))

        return bones


    def print(self):
        print(self.name)
        print('Parent:', self.parent)
        print('Subset:', self.subset)
        print('Position:', self.position)
        print('Rotation:', self.rotation)
        print()
