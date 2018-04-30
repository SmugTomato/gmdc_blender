from .generic.identity_block import IdentityBlock

class BoneDataExtension:

    def __init__(self, block_id, extension_id, unknown1, unknown2, 
                    unknown3, unknown4, preferred_rotation_angle):
        self.block_id       = block_id
        self.extension_id   = extension_id

        self.unknown1       = unknown1
        self.unknown2       = unknown2
        self.unknown3       = unknown3
        self.unknown4       = unknown4

        self.preferred_rotation_angle = preferred_rotation_angle
    
    @staticmethod
    def from_data(reader):
        block_id     = IdentityBlock.from_data(reader)
        extension_id = IdentityBlock.from_data(reader)

        unknown1 = reader.read_int32()
        unknown2 = reader.read_float()
        unknown3 = reader.read_int32()
        unknown4 = reader.read_float()

        preferred_rotation_angle = []
        for i in range(4):
            preferred_rotation_angle.append( reader.read_float() )
        
        return BoneDataExtension(block_id, extension_id, unknown1, unknown2,
                                    unknown3, unknown4, preferred_rotation_angle)
    
    def print(self):
        print('\tcBoneDataExtension:')
        self.block_id.print()

        print('\t\tExtension:')
        self.extension_id.print()

        print('\t\tUNKNOWN:\t', self.unknown1, sep="")
        print('\t\tUNKNOWN:\t', self.unknown2, sep="")
        print('\t\tUNKNOWN:\t', self.unknown3, sep="")
        print('\t\tUNKNOWN:\t', self.unknown4, sep="")

        print('\t\tPreferred Rotation Angle:\t', self.preferred_rotation_angle, sep="")
    
