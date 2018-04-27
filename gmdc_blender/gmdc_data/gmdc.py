import struct
from . import gmdc_header, gmdc_element, gmdc_linkage, gmdc_group, gmdc_model, gmdc_subset
import bpy

file_data   = None
byte_offset = None

header      = None
elements    = None
linkages    = None
groups      = None
model       = None
subsets     = None

def read_file_data(context, filepath):
    global byte_offset, file_data
    print("reading .5gd file...")

    file = open(filepath, "rb")
    file_data = file.read()
    byte_offset = 0
    file.close()

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
