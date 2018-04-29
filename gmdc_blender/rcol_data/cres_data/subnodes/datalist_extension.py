class DataListExtension:

    def __init__(self, block_name, block_id, version, name, 
                    class_id, class_version, type, var_name, sub_extensions):
        self.block_name     = block_name
        self.block_id       = block_id
        self.version        = version
        self.name           = name
        self.class_id       = class_id
        self.class_version  = class_version
        self.type           = type
        self.var_name       = var_name
        self.sub_extensions = sub_extensions

    @staticmethod
    def from_data(reader):
        pass