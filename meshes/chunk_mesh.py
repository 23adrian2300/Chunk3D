from meshes.base_mesh import BaseMesh
from utils.config import *


def is_void(voxel_pos, chunk_voxels):
    x, y, z = voxel_pos
    if 0 <= x < CHUNK_SIZE and 0 <= y < CHUNK_SIZE and 0 <= z < CHUNK_SIZE:
        if chunk_voxels[x + z * CHUNK_SIZE + y * CHUNK_AREA]:
            return False
    return True


def add_data(vertex_data, index, *vertices):
    for vertex in vertices:
        for attr in vertex:
            vertex_data[index] = attr
            index += 1
    return index


def build_chunk_mesh(chunk_voxels, format_size):
    vertex_data = np.empty(CHUNK_VOLUME * 18 * format_size, dtype='uint8')
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                id = chunk_voxels[x + z * CHUNK_SIZE + y * CHUNK_AREA]
                if not id:
                    continue
                # top
                if is_void((x, y + 1, z), chunk_voxels):
                    v0 = (x, y + 1, z, id, 0)
                    v1 = (x + 1, y + 1, z, id, 0)
                    v2 = (x + 1, y + 1, z + 1, id, 0)
                    v3 = (x, y + 1, z + 1, id, 0)

                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # bottom
                if is_void((x, y - 1, z), chunk_voxels):
                    v0 = (x, y, z, id, 1)
                    v1 = (x + 1, y, z, id, 1)
                    v2 = (x + 1, y, z + 1, id, 1)
                    v3 = (x, y, z + 1, id, 1)

                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # right
                if is_void((x + 1, y, z), chunk_voxels):
                    v0 = (x + 1, y, z, id, 2)
                    v1 = (x + 1, y + 1, z, id, 2)
                    v2 = (x + 1, y + 1, z + 1, id, 2)
                    v3 = (x + 1, y, z + 1, id, 2)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # left
                if is_void((x - 1, y, z), chunk_voxels):
                    v0 = (x, y, z, id, 3)
                    v1 = (x, y + 1, z, id, 3)
                    v2 = (x, y + 1, z + 1, id, 3)
                    v3 = (x, y, z + 1, id, 3)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # back
                if is_void((x, y, z - 1), chunk_voxels):
                    v0 = (x, y, z, id, 4)
                    v1 = (x, y + 1, z, id, 4)
                    v2 = (x + 1, y + 1, z, id, 4)
                    v3 = (x + 1, y, z, id, 4)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # front
                if is_void((x, y, z + 1), chunk_voxels):
                    v0 = (x, y, z + 1, id, 5)
                    v1 = (x, y + 1, z + 1, id, 5)
                    v2 = (x + 1, y + 1, z + 1, id, 5)
                    v3 = (x + 1, y, z + 1, id, 5)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)
    return vertex_data[:index + 1]


class ChunkMesh(BaseMesh):
    def __init__(self, chunk):
        super().__init__()
        self.app = chunk.app
        self.chunk = chunk
        self.ctx = self.app.ctx
        self.program = self.app.shader_program.chunk

        self.vbo_format = '3u1 1u1 1u1'
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attrs = ('in_position', 'voxel_id', 'face_id')
        self.vao = self.get_vao()

    def get_vertex_data(self):
        mesh = build_chunk_mesh(
            chunk_voxels=self.chunk.voxels,
            format_size=self.format_size,
            chunk_pos=self.chunk.position,
            world_voxels=self.chunk.world.voxels
        )
        return mesh

