# from .obj_data import gmdc_data
from .element_id import ElementID

class BlenderModel:

    def __init__(self, vertices, normals, faces, uvs, name, vertex_groups):
        self.name           = name
        self.vertices       = vertices
        self.normals        = normals
        self.faces          = faces
        self.uvs            = uvs
        self.vertex_groups  = vertex_groups

    # Build the necessary data for blender from the gmdc data
    @staticmethod
    def from_gmdc(gmdc_data):
        # Get all linked elements
        elements = []
        for link in gmdc_data.linkages:
            for ref in link.indices:
                elements.append(gmdc_data.elements[ref])
        print(elements)

        # Vertices
        vertices = None
        for e in elements:
            if e.element_identity == ElementID.VERTICES:
                vertices = []
                for v in e.element_values:
                    values = (v[0], -v[1], v[2])    # Flip Y axis to make the model front-facing
                    vertices.append(values)

        # Faces
        faces = []
        face_count = int(len(gmdc_data.groups[0].faces) / 3)
        for i in range(0,face_count):
            # Faces have to be loaded backwards to work properly with the UV coordinates
            face = ( gmdc_data.groups[0].faces[i*3 + 2], gmdc_data.groups[0].faces[i*3 + 1], gmdc_data.groups[0].faces[i*3] )
            faces.append(face)

        # UV coordinates
        uvs = []
        for e in elements:
            if e.element_identity == ElementID.UV_COORDINATES:
                for v in e.element_values:
                    uv_set = (v[0], -v[1] + 1)          # Flip v value and add 1 to make it work in blender
                    uvs.append(uv_set)

        # Normals
        normals = []
        for e in elements:
            if e.element_identity == ElementID.NORMALS_LIST:
                for v in e.element_values:
                    normal_set = (v[0], -v[1], v[2])    # Flip Y axis to match the vertices
                    normals.append(normal_set)

        # Name
        # remove _tslocator_gmdc from the end of the model name, this will be added again on export
        name = gmdc_data.header.file_name.split('_tslocator_gmdc')[0]

        # Vertex Groups


        return BlenderModel(vertices, normals, faces, uvs, name, vertex_groups=None)
