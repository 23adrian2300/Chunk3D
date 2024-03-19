from random import randint

from utils.config import *
from meshes.chunk_mesh import ChunkMesh


def build_voxels():
    voxels = np.zeros(CHUNK_VOLUME, dtype='uint8')
    for x in range(CHUNK_SIZE):
        for z in range(CHUNK_SIZE):
            for y in range(CHUNK_SIZE):
                voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = x + y + z + randint(0, 2)
    return voxels


class Chunk:
    def __init__(self, app):
        self.mesh = None
        self.app = app
        self.voxels: np.array = build_voxels()
        self.build_mesh()

    def build_mesh(self):
        self.mesh = ChunkMesh(self)

    def render(self):
        self.mesh.render()
