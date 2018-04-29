class CRESHeader:

    def __init__(self):
        self.version_mark   = None
        self.file_links     = None
        self.items          = None

    def read_data(self, data_read):
        file_links_item_count = 4

        # Read version mark, not always present
        self.version_mark   = data_read.read_uint32()
        if self.version_mark != 0xffff0001:
            data_read.byte_offset   = 0
            self.version_mark       = None
            print('No version mark present, resetting byte_offset')
            file_links_item_count = 3
        else:
            print('Version mark present, continuing normally...')

        # Read file link blocks, 3 or 4 values depending on version_mark being present.
        file_link_count = data_read.read_int32()
        file_links = []
        for i in range(file_link_count):
            set = []
            for j in range(file_links_item_count):
                set.append(data_read.read_uint32())
            file_links.append(set)

        item_count = data_read.read_int32()
        self.items = []
        print(item_count, 'items\n')
        for i in range(item_count):
            self.items.append(data_read.read_uint32())
