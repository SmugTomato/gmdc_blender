from .gmdc_data import gmdc
from .element_id import ElementID

class BlenderModel:

    def __init__(self, vertices, normals, faces, uvs, bones, name):
        self.name       = name
        self.vertices   = vertices
        self.normals    = normals
        self.faces      = faces
        self.uvs        = uvs
        self.bones      = bones

    # Build the necessary data for blender from the gmdc data
    @staticmethod
    def from_gmdc():
        vertices = None
        for e in gmdc.elements:
            if e.element_identity == ElementID.VERTICES and len(e.element_values) > 0:
                vertices = []
                for v in e.element_values:
                    values = (v[0], v[1], v[2])
                    vertices.append(values)
        if vertices == None:
            return 'ERROR, No vertices'

        faces = []
        face_count = int(len(gmdc.groups[0].faces) / 3)
        for i in range(0,face_count):
            face = ( gmdc.groups[0].faces[i*3], gmdc.groups[0].faces[i*3 + 1], gmdc.groups[0].faces[i*3 + 2] )
            faces.append(face)

        uvs = []
        for e in gmdc.elements:
            if e.element_identity == ElementID.UV_COORDINATES and len(e.element_values) > 0:
                for v in e.element_values:
                    uv_set = (v[0], v[1])
                    uvs.append(uv_set)

        normals = []
        for e in gmdc.elements:
            if e.element_identity == ElementID.NORMALS_LIST and len(e.element_values) > 0:
                for v in e.element_values:
                    normal_set = (v[0], v[1], v[2])
                    normals.append(normal_set)

        name = gmdc.header.file_name

        return BlenderModel(vertices, normals, faces, uvs, None, name)
