from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2) 
scene.set_floor(0, (1.0, 1.0, 1.0))
scene.set_background_color((0.5, 0.5, 0.4))
scene.set_directional_light((1, 1, -1), 0.2, (1, 0.8, 0.6))

t = vec2(36, 16)
c = vec3(0, 10, 0)
h = 8
offset = vec3(0, t.y, 0)


@ti.func
def length(i):
    return ti.sqrt(i.x * i.x + i.y * i.y)


@ti.kernel
def initialize_voxels():
    n = 60
    for i, j, k in ti.ndrange((-n, n), (-n, n), (-n, n)):
        p = vec3(i, j, k)
        if length(vec2(length(p.xz)-t.x, p.y))-t.y < 0:
            scene.set_voxel(p + offset, 1, vec3(0.8, 0.3, 0.3) + vec3(0.15) * ti.random())
            if j > h + (h - 1) * ti.sin(6 * pi * (i / ti.sqrt(i * i + k * k))):
                scene.set_voxel(p + offset + vec3(0, 1, 0), 2, vec3(0.8, 0.4, 0.1) - vec3(0.15) * (j / t.y) ** 2)
            if ti.random() < (j / t.y) ** 5 * 0.02:
                scene.set_voxel(p + offset + vec3(0, 2, 0), 1, vec3(0.5, 0.25, 0.05))


initialize_voxels()

scene.finish()
