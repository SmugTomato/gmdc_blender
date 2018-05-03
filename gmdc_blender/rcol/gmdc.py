from .gmdc_data import gmdc_header, gmdc_element, gmdc_linkage, gmdc_group, gmdc_model, gmdc_subset
from .data_reader import DataReader

class GMDC:

    GMDC_IDENTIFIER = 0xAC4F8687

    def __init__(self, file_data, byte_offset):
        self.data_read  = DataReader(file_data, byte_offset)

        self.header     = None
        self.elements   = None
        self.linkages   = None
        self.groups     = None
        self.model      = None
        self.subsets    = None

    @staticmethod
    def from_test_func(file_path):
        print("reading .5gd file...\n")

        file = open(file_path, "rb")
        file_data = file.read()
        byte_offset = 0
        file.close()
        return GMDC(file_data, byte_offset)

    @staticmethod
    def from_file_data(file_path):
        print("reading .5gd file...\n")

        file = open(file_path, "rb")
        file_data = file.read()
        byte_offset = 0
        file.close()
        return GMDC(file_data, byte_offset)

    def load_header(self):
        self.header = gmdc_header.GMDCHeader()
        self.header.read_data(self.data_read)

        if self.header.version != 4 or self.header.file_type != self.GMDC_IDENTIFIER:
            return False
        return True

    def load_data(self):
        # ELEMENTS
        count = self.data_read.read_int32()
        self.elements = []
        for i in range(0,count):
            temp_element = gmdc_element.GMDCElement()
            temp_element.read_data(self.data_read)
            self.elements.append(temp_element)

        # LINKAGES
        count = self.data_read.read_int32()
        self.linkages = []
        for i in range(0,count):
            temp_linkage = gmdc_linkage.GMDCLinkage()
            temp_linkage.read_data(self.data_read)
            self.linkages.append(temp_linkage)

        # GROUPS
        count = self.data_read.read_int32()
        self.groups = []
        for i in range(0,count):
            temp_group = gmdc_group.GMDCGroup()
            temp_group.read_data(self.data_read, self.header.version)
            self.groups.append(temp_group)

        # MODEL
        self.model = gmdc_model.GMDCModel()
        self.model.read_data(self.data_read)

        # SUBSETS
        count = self.data_read.read_int32()
        self.subsets = []
        for i in range(0,count):
            temp_subset = gmdc_subset.GMDCSubset()
            temp_subset.read_data(self.data_read)
            self.subsets.append(temp_subset)
