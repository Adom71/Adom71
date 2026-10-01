# Sequence 1 — The Shadow: the road scene

The night road outside Monasville where the B-ros' car finds Mason standing in the road.
Everything here is built from code by `build_road_scene.py`. There are no hand-made assets yet.

## What's in the scene

| Part | Notes |
|---|---|
| Road | Wet asphalt with puddles that reflect the lights, centre and edge lines, pavements |
| Streetlights | 12 lamps alternating sides of the road, warm sodium colour |
| Treeline | 160 pine trees on both sides of the road |
| Monasville skyline | ~220 towers with randomly lit windows, plus the **FLYCORP HQ** with the red Syndicate crown, a beacon and a blue FLYCORP sign |
| Fog | Light fog so the lamps and headlights make visible beams |
| B-ros car | A simple placeholder body. Only its headlights matter for these shots |
| Mason (stand-in) | Black hooded assassin gear: hood, mask, red comb, yellow eyes and a sword on the back. **A placeholder for blocking only.** Replace it with the real rigged model later |

## Shots

| Shot | Camera object | Description |
|---|---|---|
| A | `Shot_A` | Establishing: the road leading into Monasville at night |
| B | `Shot_B` | B-ros POV: the headlights find a figure standing in the road |
| C | `Shot_C` | Hero low angle: Mason backlit by a streetlight, with FLYCORP tower behind him |
| D | `Shot_D_PushIn` | 3-second (72-frame) slow push-in from the car toward Mason |

Rendered stills are in `renders/`. The push-in is `renders/shot_D_pushin.mp4`.

## How to use it

**In Blender (4.2 or newer):** open `road_scene.blend`, or open the script in the
*Scripting* tab and press **Run Script**. Every object is grouped into collections
(`Road`, `Streetlights`, `Treeline`, `Monasville_Skyline`, `Atmosphere`, `B-ros_Car`,
`Mason_StandIn`), so you can hide or replace parts.

**From a terminal:**

```bash
# with Blender installed
blender -b -P build_road_scene.py -- --render A,B,C --samples 64
# or with just Python:  pip install bpy
python3 build_road_scene.py --render A,B,C --anim --samples 64 --save road_scene.blend
```

| Option | What it does |
|---|---|
| `--render A,B,C` | Render these shots as stills |
| `--anim` | Render the shot D push-in as numbered frames |
| `--samples N` | Quality (16 = fast preview, 64 = good, 256 = final) |
| `--scale P` | Resolution %, where 100 = 1920×804 (2.39:1 widescreen) |
| `--save FILE` | Save the built scene as a `.blend` file |

## Next steps for this scene

1. **Replace the Mason stand-in** with the real character model: generate it from the
   character sheet with an AI 3D tool, then rig it with Mixamo or AccuRIG. Put the model
   where the stand-in stands (`FIGURE_Y` in the script).
2. **Animate the confrontation:** the B-ros get out of the car, the fight, the blood splash.
   Film a friend acting it out and use phone motion capture.
3. **Add the title card** "CHICKEN ASSASSIN" after the blood splash.
4. **Add sound:** engine idle, a buzzing streetlight, wind, distant city noise.
