import struct
from . import gmdc_header, gmdc_element, gmdc_linkage, gmdc_group, gmdc_model, gmdc_subset

file_data = None
byte_offset = None

header = None
elements = None
linkages = None
groups = None
model = None
subsets = None

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

    # LINKAGES

    # GROUPS

    # MODEL

    # SUBSETS


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
    return int.from_bytes(bytes, 'little')

def read_int32():
    bytes = bytearray()
    for i in range(0,4):
        bytes.append(read_byte())
    return int.from_bytes(bytes, 'little')

def read_float():
    bytes = bytearray()
    for i in range(0,4):
        bytes.append(read_byte())
    return struct.unpack('<f', bytes)[0]
