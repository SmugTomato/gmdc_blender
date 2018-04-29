from .subnodes.tgir_node import TgirNode

class CresHeader:

    def __init__(self, version_mark, file_links, tgir_list, item_count, ids):
        self.version_mark   = version_mark
        self.file_links     = file_links
        self.tgir_list      = tgir_list
        self.item_count     = item_count
        self.ids            = ids
    
    @staticmethod
    def from_data(reader):
        """Build the object from given data"""
        version_mark = reader.read_uint32()

        file_links = reader.read_int32()
        tgir_list = []
        for i in range(file_links):
            tgir_list.append(TgirNode.from_data(reader, version_mark == 0xffff0001))

        item_count = reader.read_int32()
        ids = []
        for i in range(item_count):
            tmp_id = reader.read_uint32()
            ids.append(tmp_id)

        return CresHeader(version_mark, file_links, tgir_list, item_count, ids)
    
    def print(self):
        print('Version mark:\t', hex(self.version_mark))
        print('# File links:\t', self.file_links)
        for ob in self.tgir_list:
            ob.print()
        print('Item count:\t', self.item_count)
        for val in self.ids:
            print('\t', hex(val), sep="")