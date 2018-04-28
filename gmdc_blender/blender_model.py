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

    @staticmethod
    def groups_from_gmdc(gmdc_data):
        groups = []
        for g in gmdc_data.groups:
            # Load single group from a linkage

            # Get all linked elements
            element_indices = []
            for i in gmdc_data.linkages[g.link_index].indices:
                element_indices.append(i)
            groups.append(element_indices)

        models = []
        for i, element_indices in enumerate(groups):
            tmp_model = BlenderModel.from_gmdc(gmdc_data, element_indices, i)
            models.append(tmp_model)

        return models

    # Build the necessary data for blender from the gmdc data
    @staticmethod
    def from_gmdc(gmdc_data, element_indices, group_index):
        # Get all linked elements
        # elements = []
        # for link in gmdc_data.linkages:
        #     for ref in link.indices:
        #         elements.append(gmdc_data.elements[ref])
        # print(elements)

        vertices    = None
        uvs         = None
        normals     = None
        for ind in element_indices:
            # Vertices
            if gmdc_data.elements[ind].element_identity == ElementID.VERTICES:
                vertices = []
                for v in gmdc_data.elements[ind].element_values:
                    values = (v[0], -v[1], v[2])        # Flip Y axis to make the model front-facing
                    vertices.append(values)

            # UV coordinates
            if gmdc_data.elements[ind].element_identity == ElementID.UV_COORDINATES:
                uvs = []
                for v in gmdc_data.elements[ind].element_values:
                    uv_set = (v[0], -v[1] + 1)          # Flip v value and add 1 to make it work in blender
                    uvs.append(uv_set)

            # Normals
            if gmdc_data.elements[ind].element_identity == ElementID.NORMALS_LIST:
                normals = []
                for v in gmdc_data.elements[ind].element_values:
                    normal_set = (v[0], -v[1], v[2])    # Flip Y axis to match the vertices
                    normals.append(normal_set)


        # Faces
        faces = []
        face_count = int(len(gmdc_data.groups[group_index].faces) / 3)
        for i in range(0,face_count):
            # Faces have to be loaded backwards to work properly with the UV coordinates
            face = ( gmdc_data.groups[group_index].faces[i*3 + 2], gmdc_data.groups[group_index].faces[i*3 + 1], gmdc_data.groups[group_index].faces[i*3] )
            faces.append(face)

        # Name
        name = gmdc_data.groups[group_index].name

        # Vertex Groups


        return BlenderModel(vertices, normals, faces, uvs, name, vertex_groups=None)
