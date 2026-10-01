"""
CHICKEN ASSASSIN - Sequence 1 "The Shadow"
Scene: the night road outside Monasville where Mason stands in the road.

Builds the whole set from code: wet road, streetlights, fog, tree line,
the Monasville skyline with FLYCORP tower, the B-ros' car headlights and a
stand-in figure for Mason (hooded assassin look).

Run inside Blender (Scripting tab -> Open -> Run Script), or headless:
    blender -b -P build_road_scene.py -- --render A,B,C
    python3 build_road_scene.py --render A,B,C        (with `pip install bpy`)

Options (after `--` when using the blender binary):
    --render A,B,C     which camera shots to render as stills
    --anim             also render the push-in shot (shot D) as frames
    --samples N        Cycles samples (default 64)
    --scale P          resolution percentage (default 100 = 1920x804)
    --out DIR          output folder (default ./renders next to this file)
    --save FILE.blend  save the built scene so it can be opened in Blender
"""

import argparse
import math
import os
import random
import sys

import bpy
from mathutils import Vector

random.seed(7)  # same layout every run

# Colour palette from the series character lineup
STREETLIGHT = (1.0, 0.62, 0.32)
HEADLIGHT = (0.85, 0.9, 1.0)
SYNDICATE_RED = (0.85, 0.03, 0.03)
FLYCORP_BLUE = (0.05, 0.25, 1.0)

FIGURE_Y = 40.0  # where Mason stands on the road


# ---------------------------------------------------------------- helpers

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    return bpy.context.scene


def link(obj, collection=None):
    (collection or bpy.context.scene.collection).objects.link(obj)
    return obj


def new_collection(name):
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


def principled(name, color, roughness=0.5, metallic=0.0, emission=None, strength=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = strength
    return mat


def add_prim(kind, name, location, scale=(1, 1, 1), rotation=(0, 0, 0), material=None,
             collection=None, **kw):
    ops = {
        "cube": bpy.ops.mesh.primitive_cube_add,
        "cylinder": bpy.ops.mesh.primitive_cylinder_add,
        "cone": bpy.ops.mesh.primitive_cone_add,
        "sphere": bpy.ops.mesh.primitive_uv_sphere_add,
        "plane": bpy.ops.mesh.primitive_plane_add,
    }
    ops[kind](location=location, rotation=rotation, **kw)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    if material:
        obj.data.materials.append(material)
    if collection:
        for c in obj.users_collection:
            c.objects.unlink(obj)
        collection.objects.link(obj)
    return obj


def smooth(obj):
    for poly in obj.data.polygons:
        poly.use_smooth = True
    return obj


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def node(tree, kind, **inputs):
    n = tree.nodes.new(kind)
    for key, value in inputs.items():
        if key == "operation":
            n.operation = value
        else:
            n.inputs[key].default_value = value
    return n


def math_node(tree, op, a, b=None):
    n = tree.nodes.new("ShaderNodeMath")
    n.operation = op
    for i, v in enumerate((a, b)):
        if v is None:
            continue
        if isinstance(v, (int, float)):
            n.inputs[i].default_value = v
        else:
            tree.links.new(v, n.inputs[i])
    return n.outputs[0]


# --------------------------------------------------------------- materials

def window_material():
    """Dark building facade with a grid of randomly lit windows."""
    mat = bpy.data.materials.new("Building_Windows")
    mat.use_nodes = True
    t = mat.node_tree
    bsdf = t.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.012, 0.015, 0.022, 1)
    bsdf.inputs["Roughness"].default_value = 0.35

    geo = t.nodes.new("ShaderNodeNewGeometry")
    info = t.nodes.new("ShaderNodeObjectInfo")
    sep = t.nodes.new("ShaderNodeSeparateXYZ")
    t.links.new(geo.outputs["Position"], sep.inputs[0])
    nsep = t.nodes.new("ShaderNodeSeparateXYZ")
    t.links.new(geo.outputs["Normal"], nsep.inputs[0])

    u = math_node(t, "ADD", sep.outputs["X"], sep.outputs["Y"])
    u = math_node(t, "DIVIDE", u, 3.2)
    v = math_node(t, "DIVIDE", sep.outputs["Z"], 3.6)

    def band(val, lo, hi):
        f = math_node(t, "FRACT", val)
        return math_node(t, "MULTIPLY",
                         math_node(t, "GREATER_THAN", f, lo),
                         math_node(t, "LESS_THAN", f, hi))

    mask = math_node(t, "MULTIPLY", band(u, 0.22, 0.78), band(v, 0.3, 0.75))
    # no windows on the roofs
    side = math_node(t, "LESS_THAN", math_node(t, "ABSOLUTE", nsep.outputs["Z"]), 0.5)
    mask = math_node(t, "MULTIPLY", mask, side)

    cell = t.nodes.new("ShaderNodeCombineXYZ")
    t.links.new(math_node(t, "FLOOR", u), cell.inputs["X"])
    t.links.new(math_node(t, "FLOOR", v), cell.inputs["Y"])
    t.links.new(math_node(t, "MULTIPLY", info.outputs["Random"], 97.0), cell.inputs["Z"])

    noise = t.nodes.new("ShaderNodeTexWhiteNoise")
    noise.noise_dimensions = "3D"
    t.links.new(cell.outputs[0], noise.inputs["Vector"])
    lit = math_node(t, "GREATER_THAN", noise.outputs["Value"], 0.58)
    lit = math_node(t, "MULTIPLY", mask, lit)

    warm_cool = t.nodes.new("ShaderNodeMix")
    warm_cool.data_type = "RGBA"
    sepc = t.nodes.new("ShaderNodeSeparateColor")
    t.links.new(noise.outputs["Color"], sepc.inputs[0])
    t.links.new(math_node(t, "GREATER_THAN", sepc.outputs[0], 0.7), warm_cool.inputs["Factor"])
    warm_cool.inputs["A"].default_value = (1.0, 0.68, 0.35, 1)
    warm_cool.inputs["B"].default_value = (0.55, 0.75, 1.0, 1)
    t.links.new(warm_cool.outputs["Result"], bsdf.inputs["Emission Color"])
    t.links.new(math_node(t, "MULTIPLY", lit, 7.0), bsdf.inputs["Emission Strength"])
    return mat


def road_material():
    """Asphalt with wet patches so the lights reflect."""
    mat = bpy.data.materials.new("Wet_Asphalt")
    mat.use_nodes = True
    t = mat.node_tree
    bsdf = t.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.022, 0.022, 0.025, 1)
    tex = t.nodes.new("ShaderNodeTexCoord")
    noise = t.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 0.08
    noise.inputs["Detail"].default_value = 6
    t.links.new(tex.outputs["Object"], noise.inputs["Vector"])
    ramp = t.nodes.new("ShaderNodeMapRange")
    ramp.inputs["From Min"].default_value = 0.4
    ramp.inputs["From Max"].default_value = 0.6
    ramp.inputs["To Min"].default_value = 0.08   # puddles
    ramp.inputs["To Max"].default_value = 0.55   # dry asphalt
    t.links.new(noise.outputs["Fac"], ramp.inputs["Value"])
    t.links.new(ramp.outputs["Result"], bsdf.inputs["Roughness"])
    return mat


# ------------------------------------------------------------------ world

def build_world(scene):
    world = bpy.data.worlds.new("Monasville_Night")
    scene.world = world
    world.use_nodes = True
    t = world.node_tree
    bg = t.nodes["Background"]
    coord = t.nodes.new("ShaderNodeTexCoord")
    sep = t.nodes.new("ShaderNodeSeparateXYZ")
    t.links.new(coord.outputs["Generated"], sep.inputs[0])
    ramp = t.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (0.05, 0.035, 0.05, 1)    # city glow at horizon
    ramp.color_ramp.elements[1].position = 0.35
    ramp.color_ramp.elements[1].color = (0.003, 0.006, 0.018, 1)  # deep night blue
    t.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    t.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 1.0

    # cold moonlight for rim light on silhouettes
    moon = bpy.data.lights.new("Moon", "SUN")
    moon.energy = 0.08
    moon.color = (0.6, 0.7, 1.0)
    moon.angle = math.radians(1.5)
    obj = link(bpy.data.objects.new("Moon", moon))
    obj.rotation_euler = (math.radians(65), 0, math.radians(160))


# -------------------------------------------------------------------- set

def build_road():
    col = new_collection("Road")
    road = add_prim("plane", "Road", (0, 150, 0), scale=(5, 200, 1),
                    material=road_material(), collection=col)
    # dashed centre line
    paint = principled("Road_Paint", (0.75, 0.65, 0.35), roughness=0.4)
    dash_mesh = None
    for i in range(80):
        y = -20 + i * 6
        d = add_prim("plane", f"Dash_{i:02d}", (0, y, 0.005), scale=(0.08, 1.5, 1),
                     material=paint if dash_mesh is None else None, collection=col)
        if dash_mesh is None:
            dash_mesh = d.data
        else:
            d.data = dash_mesh
    # edge lines
    for x in (-4.6, 4.6):
        add_prim("plane", f"Edge_{x}", (x, 150, 0.005), scale=(0.06, 200, 1),
                 material=paint, collection=col)
    # kerbs and pavements
    kerb = principled("Concrete", (0.09, 0.09, 0.1), roughness=0.8)
    for x in (-6.5, 6.5):
        add_prim("cube", f"Pavement_{x}", (x, 150, 0.08), scale=(1.5, 200, 0.08),
                 material=kerb, collection=col)
    grass = principled("Dark_Grass", (0.01, 0.018, 0.01), roughness=0.95)
    for x in (-58, 58):
        add_prim("plane", f"Verge_{x}", (x, 150, -0.01), scale=(50, 220, 1),
                 material=grass, collection=col)
    return road


def build_streetlights():
    col = new_collection("Streetlights")
    metal = principled("Pole_Metal", (0.05, 0.05, 0.055), roughness=0.4, metallic=0.8)
    glow = principled("Lamp_Glow", STREETLIGHT, emission=STREETLIGHT, strength=40)
    for i in range(12):
        y = -10 + i * 28
        side = -1 if i % 2 == 0 else 1
        x = side * 6.2
        add_prim("cylinder", f"Pole_{i:02d}", (x, y, 4.5), scale=(0.09, 0.09, 4.5),
                 material=metal, collection=col)
        arm_x = x - side * 1.1
        add_prim("cube", f"Arm_{i:02d}", (x - side * 0.55, y, 8.9), scale=(0.65, 0.06, 0.05),
                 material=metal, collection=col)
        add_prim("cube", f"Head_{i:02d}", (arm_x, y, 8.82), scale=(0.35, 0.18, 0.07),
                 material=metal, collection=col)
        add_prim("plane", f"Bulb_{i:02d}", (arm_x, y, 8.74), scale=(0.3, 0.14, 1),
                 rotation=(math.pi, 0, 0), material=glow, collection=col)
        light = bpy.data.lights.new(f"Street_{i:02d}", "SPOT")
        light.energy = 3500
        light.color = STREETLIGHT
        light.spot_size = math.radians(110)
        light.spot_blend = 0.6
        light.shadow_soft_size = 0.25
        obj = link(bpy.data.objects.new(f"StreetLight_{i:02d}", light), col)
        obj.location = (arm_x, y, 8.65)
    # one lamp right behind Mason flickers in the story - keep it slightly cooler
    return col


def build_trees():
    col = new_collection("Treeline")
    bark = principled("Bark", (0.02, 0.015, 0.01), roughness=0.9)
    leaves = principled("Leaves", (0.006, 0.014, 0.008), roughness=0.9)
    trunk_mesh = crown_mesh = None
    for i in range(160):
        side = random.choice((-1, 1))
        x = side * random.uniform(12, 40)
        y = random.uniform(-8, 300)
        h = random.uniform(7, 14)
        trunk = add_prim("cylinder", f"Trunk_{i:03d}", (x, y, h * 0.2),
                         scale=(0.2, 0.2, h * 0.2), material=bark if trunk_mesh is None else None,
                         collection=col, vertices=8)
        crown = add_prim("cone", f"Crown_{i:03d}", (x, y, h * 0.62),
                         scale=(h * 0.28, h * 0.28, h * 0.45),
                         material=leaves if crown_mesh is None else None, collection=col,
                         vertices=10)
        top = add_prim("cone", f"CrownTop_{i:03d}", (x, y, h * 0.9),
                       scale=(h * 0.18, h * 0.18, h * 0.3), collection=col, vertices=10)
        top.data = crown.data if crown_mesh is None else crown_mesh
        trunk_mesh = trunk_mesh or trunk.data
        crown_mesh = crown_mesh or crown.data
        trunk.data, crown.data = trunk_mesh, crown_mesh


def build_city():
    col = new_collection("Monasville_Skyline")
    mat = window_material()
    for i in range(220):
        x = random.uniform(-420, 420)
        y = random.uniform(650, 950)
        # taller buildings toward the centre of the skyline
        h = random.uniform(15, 45) + max(0, 80 - abs(x) * 0.3) * random.uniform(0.3, 1.0)
        w = random.uniform(12, 28)
        b = add_prim("cube", f"Tower_{i:03d}", (x, y, h / 2), scale=(w / 2, w / 2, h / 2),
                     material=mat, collection=col)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # FLYCORP headquarters - tallest tower, red Syndicate crown, blue logo
    hq = add_prim("cube", "FLYCORP_HQ", (12, 700, 110), scale=(16, 16, 110),
                  material=mat, collection=col)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    add_prim("cone", "FLYCORP_Spire", (12, 700, 232), scale=(10, 10, 12),
             material=principled("HQ_Glass", (0.02, 0.02, 0.03), 0.2, 0.9), collection=col,
             vertices=4)
    red = principled("Syndicate_Red", SYNDICATE_RED, emission=SYNDICATE_RED, strength=25)
    add_prim("cube", "FLYCORP_Crown", (12, 700, 221), scale=(16.3, 16.3, 0.8),
             material=red, collection=col)
    beacon = add_prim("sphere", "FLYCORP_Beacon", (12, 700, 245), scale=(0.9, 0.9, 0.9),
                      material=red, collection=col)
    smooth(beacon)

    curve = bpy.data.curves.new("FLYCORP_Text", "FONT")
    curve.body = "FLYCORP"
    curve.align_x = "CENTER"
    curve.extrude = 0.2
    text = link(bpy.data.objects.new("FLYCORP_Sign", curve), col)
    text.data.materials.append(
        principled("FLYCORP_Blue", FLYCORP_BLUE, emission=FLYCORP_BLUE, strength=30))
    text.location = (12, 683.8, 205)
    text.rotation_euler = (math.radians(90), 0, 0)
    text.scale = (5.2, 5.2, 5.2)


def build_fog():
    col = new_collection("Atmosphere")
    fog = add_prim("cube", "Fog_Volume", (0, 230, 25), scale=(120, 260, 25), collection=col)
    mat = bpy.data.materials.new("Night_Fog")
    mat.use_nodes = True
    t = mat.node_tree
    t.nodes.remove(t.nodes["Principled BSDF"])
    vol = t.nodes.new("ShaderNodeVolumePrincipled")
    vol.inputs["Density"].default_value = 0.0045
    vol.inputs["Color"].default_value = (0.7, 0.75, 0.85, 1)
    vol.inputs["Anisotropy"].default_value = 0.55  # glow around lamps
    t.links.new(vol.outputs[0], t.nodes["Material Output"].inputs["Volume"])
    fog.data.materials.append(mat)


def build_car():
    """The B-ros' car. Only the headlights matter for these shots."""
    col = new_collection("B-ros_Car")
    paint = principled("Car_Paint", (0.01, 0.01, 0.012), roughness=0.15, metallic=0.6)
    lamp = principled("Headlamp", HEADLIGHT, emission=HEADLIGHT, strength=60)
    add_prim("cube", "Car_Body", (0, -2.4, 0.65), scale=(0.95, 2.3, 0.38), material=paint,
             collection=col)
    add_prim("cube", "Car_Cabin", (0, -2.8, 1.25), scale=(0.85, 1.2, 0.3), material=paint,
             collection=col)
    for x in (-0.65, 0.65):
        add_prim("cube", f"Headlamp_{x}", (x, -0.08, 0.75), scale=(0.2, 0.03, 0.07),
                 material=lamp, collection=col)
        light = bpy.data.lights.new(f"Headlight_{x}", "SPOT")
        light.energy = 16000
        light.color = HEADLIGHT
        light.spot_size = math.radians(30)
        light.spot_blend = 0.35
        light.shadow_soft_size = 0.05
        obj = link(bpy.data.objects.new(f"Headlight_{x}", light), col)
        obj.location = (x, 0.0, 0.75)
        obj.rotation_euler = (math.radians(88.5), 0, 0)


# ----------------------------------------------------------------- Mason

def build_mason():
    """Stand-in for Mason Reed in his black assassin gear (hood, mask, sword).

    Built from simple shapes so the shot can be blocked and lit. Swap this
    collection for the real rigged character model later.
    """
    col = new_collection("Mason_StandIn")
    cloth = principled("Assassin_Black", (0.03, 0.03, 0.034), roughness=0.6)
    leather = principled("Leather", (0.02, 0.018, 0.018), roughness=0.4)
    feather = principled("White_Feathers", (0.82, 0.78, 0.7), roughness=0.8)
    comb = principled("Comb_Red", (0.55, 0.01, 0.01), roughness=0.5)
    eye = principled("Eyes", (0.9, 0.7, 0.2), roughness=0.1, emission=(1, 0.75, 0.3), strength=0.15)
    steel = principled("Sword_Steel", (0.6, 0.6, 0.62), roughness=0.2, metallic=1.0)

    Y = FIGURE_Y
    parts = []

    def p(*a, **k):
        o = add_prim(*a, collection=col, **k)
        parts.append(o)
        return o

    for x in (-0.14, 0.14):
        p("cylinder", "Boot", (x, Y, 0.24), scale=(0.1, 0.12, 0.24), material=leather)
        p("cylinder", "Leg", (x, Y, 0.7), scale=(0.085, 0.085, 0.25), material=cloth)
    smooth(p("cone", "Coat", (0, Y + 0.02, 1.0), scale=(0.44, 0.36, 0.55), material=cloth,
             radius1=1.0, radius2=0.55, depth=2.0, vertices=24))
    smooth(p("cylinder", "Torso", (0, Y, 1.45), scale=(0.27, 0.2, 0.2), material=cloth,
             vertices=24))
    smooth(p("sphere", "Shoulders", (0, Y, 1.6), scale=(0.38, 0.22, 0.13), material=cloth))
    for side in (-1, 1):
        smooth(p("cone", "Arm", (side * 0.35, Y, 1.24), scale=(0.07, 0.07, 0.36),
                 rotation=(0, side * math.radians(5), 0), material=cloth, vertices=16,
                 radius1=0.75, radius2=1.0, depth=2.0))
        smooth(p("sphere", "Glove", (side * 0.385, Y - 0.01, 0.86), scale=(0.06, 0.055, 0.08),
                 material=leather))
    # head, mask and hood (figure faces -Y, toward the car)
    smooth(p("sphere", "Head", (0, Y - 0.04, 1.82), scale=(0.15, 0.16, 0.16), material=feather))
    smooth(p("sphere", "Mask", (0, Y - 0.07, 1.75), scale=(0.15, 0.15, 0.1), material=cloth))
    smooth(p("sphere", "Hood", (0, Y + 0.05, 1.86), scale=(0.21, 0.22, 0.24), material=cloth))
    p("cone", "Hood_Peak", (0, Y - 0.12, 2.0), scale=(0.1, 0.06, 0.08),
      rotation=(math.radians(-70), 0, 0), material=cloth)
    for i, (x, z) in enumerate(((-0.04, 2.06), (0.0, 2.1), (0.045, 2.06))):
        smooth(p("sphere", f"Comb_{i}", (x, Y - 0.15, z), scale=(0.03, 0.05, 0.05),
                 material=comb))
    for x in (-0.06, 0.06):
        smooth(p("sphere", "Eye", (x, Y - 0.185, 1.85), scale=(0.022, 0.012, 0.012),
                 material=eye))
    # sword on the back, handle over the right shoulder
    p("cylinder", "Sword_Handle", (0.2, Y + 0.2, 1.95), scale=(0.022, 0.022, 0.16),
      rotation=(math.radians(-10), math.radians(25), 0), material=leather)
    p("cube", "Sword_Sheath", (-0.05, Y + 0.22, 1.45), scale=(0.035, 0.02, 0.48),
      rotation=(math.radians(-10), math.radians(25), 0), material=steel)
    return col


# --------------------------------------------------------------- cameras

SHOTS = {
    # name: (description, location, target, lens)
    "A": ("Establishing - Monasville at night, the road leading into the city",
          (2.5, -22, 6.0), (0, 160, 10), 26),
    "B": ("B-ros POV - headlights find a figure standing in the road",
          (0.35, -0.6, 1.2), (0, FIGURE_Y, 1.4), 55),
    "C": ("Hero low angle - Mason, backlit, city behind him",
          (0.9, FIGURE_Y - 3.6, 0.35), (0, FIGURE_Y, 1.75), 24),
}


def add_camera(name, loc, target, lens):
    cam = bpy.data.cameras.new(name)
    cam.lens = lens
    cam.sensor_width = 36
    cam.clip_end = 2000
    obj = link(bpy.data.objects.new(name, cam))
    obj.location = loc
    look_at(obj, target)
    return obj


def build_cameras():
    cams = {k: add_camera(f"Shot_{k}", loc, tgt, lens) for k, (_, loc, tgt, lens) in SHOTS.items()}
    # Shot D: slow push-in from the car toward Mason (3 seconds)
    d = add_camera("Shot_D_PushIn", (0.35, -0.6, 1.2), (0, FIGURE_Y, 1.4), 55)
    d.keyframe_insert("location", frame=1)
    d.location = (0.15, 14.0, 1.3)
    d.keyframe_insert("location", frame=72)
    cams["D"] = d
    return cams


# ---------------------------------------------------------------- render

def setup_render(scene, samples, scale):
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 6
    scene.cycles.volume_bounces = 1
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 804  # 2.39:1 cinema widescreen
    scene.render.resolution_percentage = scale
    scene.render.fps = 24
    scene.frame_start, scene.frame_end = 1, 72
    scene.view_settings.view_transform = "AgX"
    for look in ("AgX - Punchy", "Punchy"):
        try:
            scene.view_settings.look = look
            break
        except TypeError:
            pass
    scene.view_settings.exposure = 0.6
    scene.render.image_settings.file_format = "PNG"


def build(samples=64, scale=100):
    scene = reset_scene()
    build_world(scene)
    build_road()
    build_streetlights()
    build_trees()
    build_city()
    build_fog()
    build_car()
    build_mason()
    cams = build_cameras()
    setup_render(scene, samples, scale)
    return scene, cams


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", default="")
    ap.add_argument("--anim", action="store_true")
    ap.add_argument("--samples", type=int, default=64)
    ap.add_argument("--scale", type=int, default=100)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  "renders"))
    ap.add_argument("--save", default="")
    args = ap.parse_args(argv)

    scene, cams = build(args.samples, args.scale)
    os.makedirs(args.out, exist_ok=True)
    if args.save:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(args.save))

    for shot in filter(None, args.render.split(",")):
        scene.camera = cams[shot]
        scene.frame_set(1)
        scene.render.filepath = os.path.join(args.out, f"shot_{shot}.png")
        print(f"Rendering shot {shot}: {SHOTS[shot][0]}")
        bpy.ops.render.render(write_still=True)

    if args.anim:
        scene.camera = cams["D"]
        scene.render.filepath = os.path.join(args.out, "shot_D_frames", "frame_")
        bpy.ops.render.render(animation=True)


if __name__ == "__main__":
    main()
