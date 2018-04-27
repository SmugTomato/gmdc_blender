import struct
from . import gmdc_header, gmdc_element, gmdc_linkage, gmdc_group, gmdc_model, gmdc_subset

file_data   = None
byte_offset = None

header      = None
elements    = None
linkages    = None
groups      = None
model       = None
subsets     = None

# Used to get human readable element identities
element_ids = {
    0x1C4AFC56: 'Blend Indices',
    0x5C4AFC5C: 'Blend Weights',
    0x7C4DEE82: 'Target Indices',
    0xCB6F3A6A: 'Normal Morph Deltas',
    0xCB7206A1: 'Colour',
    0xEB720693: 'Colour Deltas',
    0x3B83078B: 'Normals List',
    0x5B830781: 'Vertices',
    0xBB8307AB: 'UV Coordinates',
    0xDB830795: 'UV Coordinate Deltas',
    0x9BB38AFB: 'Binormals',
    0x3BD70105: 'Bone Weights',
    0xFBD70111: 'Bone Assignments',
    0x89D92BA0: 'Bump Map Normals',
    0x69D92B93: 'Bump Map Normal Deltas',
    0x5CF2CFE1: 'Morph Vertex Deltas',
    0xDCF2CFDC: 'Morph Vertex Map',
    0x114113C3: '(EP4) VertexID',
    0x114113CD: '(EP4) RegionMask'
}

def read_file_data():
    global byte_offset, file_data

    file = open("../sims2_files/TestMesh.5gd", "rb")
    file_data = file.read()
    byte_offset = 0

def load_data():
    global header, elements, linkages, groups, model, subsets

    # HEADER
    header = gmdc_header.GMDCHeader()
    header.read_data()

    # ELEMENTS
    count = read_int32()
    elements = []
    for i in range(0,count):
        temp_element = gmdc_element.GMDCElement()
        temp_element.read_data()
        elements.append(temp_element)

    # LINKAGES
    count = read_int32()
    linkages = []
    for i in range(0,count):
        temp_linkage = gmdc_linkage.GMDCLinkage()
        temp_linkage.read_data()
        linkages.append(temp_linkage)

    # GROUPS
    count = read_int32()
    groups = []
    for i in range(0,count):
        temp_group = gmdc_group.GMDCGroup()
        temp_group.read_data()
        groups.append(temp_group)

    # MODEL
    model = gmdc_model.GMDCModel()
    model.read_data()

    print('\nByte Offset:', byte_offset, '/', len(file_data))
    # SUBSETS
    count = read_int32()
    subsets = []
    for i in range(0,count):
        temp_subset = gmdc_subset.GMDCSubset()
        temp_subset.read_data()
        subsets.append(temp_subset)



# Byte reading methods
# Reads a single byte, meant to be used as a helper by methods below
def read_byte():
    global byte_offset, file_data

    byte = file_data[byte_offset]
    byte_offset += 1
    return byte

def read_byte_string():
    str_len = read_byte()
    bytes = bytearray()
    for i in range(0,str_len):
        bytes.append(read_byte())
    return bytes.decode("utf-8")

def read_int16():
    bytes = bytearray()
    for i in range(0,2):
        bytes.append(read_byte())
    return struct.unpack('<h', bytes)[0]

def read_int32():
    bytes = bytearray()
    for i in range(0,4):
        bytes.append(read_byte())
    return struct.unpack('<i', bytes)[0]

def read_uint32():
    bytes = bytearray()
    for i in range(0,4):
        bytes.append(read_byte())
    return struct.unpack('<I', bytes)[0]

def read_float():
    bytes = bytearray()
    for i in range(0,4):
        bytes.append(read_byte())
    return struct.unpack('<f', bytes)[0]
