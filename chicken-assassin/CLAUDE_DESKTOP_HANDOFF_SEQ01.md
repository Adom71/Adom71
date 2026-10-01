# CHICKEN ASSASSIN — Production Handoff for Claude Desktop
## Sequence 1: "The Shadow"

> **To Claude Desktop:** this file is your brief. Read all of it before doing anything. You're
> the production assistant for an animated film made by a small team of friends in Ghana.
> Your job is to turn the screenplay below into finished video shots, using AI tools in the
> browser, saving everything in the user's **Kweku** folder on the Desktop, and getting the
> user's approval at every checkpoint.

---

## 0. Ground rules (read first)

1. **Never spend money.** Use only free tiers and free daily credits. Never subscribe, start a
   paid plan, buy credits or enter payment details. If a free trial asks for a card, stop and ask
   the user.
2. **Never type passwords.** If a site needs a login, ask the user to log in themselves, then
   continue.
3. **Stop at every ✋ CHECKPOINT** and wait for the user to approve before moving on.
4. **Log everything** in `production-log.md` (format in section 7): every image and video you
   generate, the tool, the exact prompt and the result.
5. **Tell the user before using credits.** At the start of each work session, say roughly how
   many generations you plan to make and which tool's free credits they'll use.
6. **Don't publish or share anything.** Files stay in the Kweku folder.
7. **If a tool refuses a prompt** (usually because of weapons or blood), use the fallback in
   section 6. Never try to trick the tool's safety filters.
8. **If something here is unclear, ask the user.** Don't guess on story or design decisions. The
   user and their friend (who wrote the story and made the character sheets) decide those.

---

## 1. Setup

### 1.1 Create the project folder

Create this structure on the Desktop:

```
Kweku/
└── ChickenAssassin/
    ├── project-files/            ← downloaded from GitHub (step 1.2)
    ├── references/
    │   └── characters/           ← approved character reference images (Phase 1)
    └── seq01-the-shadow/
        ├── images/               ← start frames, e.g. S15_v1.png
        ├── video/                ← clips, e.g. S15_v1.mp4
        ├── selects/              ← the approved version of each shot
        └── production-log.md
```

### 1.2 Get the project files from GitHub

- Repository: `https://github.com/Adom71/Adom71`
- Branch: `claude/clever-euler-41znxo`

If `git` is installed:
```
git clone -b claude/clever-euler-41znxo https://github.com/Adom71/Adom71.git "Kweku/ChickenAssassin/project-files"
```
Otherwise ask the user to download the ZIP: on GitHub, switch to that branch, then
**Code → Download ZIP**, and unzip it into `project-files/`. If the repository is private, the
user will need to be logged into GitHub.

What's inside `project-files/chicken-assassin/`:

| File | What it is |
|---|---|
| `reference/cast_lineup.png` | **Main reference for every character's look.** It wins over any description in this file |
| `reference/mason_reed_sheets.png` | Mason's civilian and assassin character sheets |
| `reference/zhang_lei_sheet.png` | Zhang Lei's sheet (not in Sequence 1) |
| `reference/marcus_white_assassin_pixverse_test.mov` | The team's PixVerse test clip. Use it as the **quality target** |
| `seq01-the-shadow/screenplay.md` | The Sequence 1 screenplay (draft 2) |
| `seq01-the-shadow/renders/shot_A.png`, `shot_B.png`, `shot_C.png` | Blender layout renders: **composition references** for shots S10, S15 and S18 |

### 1.3 Tools (free tiers only)

| Tool | Use it for | Login |
|---|---|---|
| **ChatGPT** (chatgpt.com) | **All still images**: character references and start frames. The character sheets were made here, so new images will match | User's account |
| **Google Flow** (labs.google/flow), Veo | **Main video tool.** Image-to-video, 8-second clips, can generate sound and dialogue | User's Google account, free daily credits |
| **Kling** (klingai.com) | Backup video tool, especially for action and fight shots | Free daily credits |
| **PixVerse** (pixverse.ai) | Second backup. The team already knows it | Free daily credits |

Free tiers add watermarks and give fewer generations. That's fine; this is the test phase. The team
will buy Google AI Pro later for the final versions.

✋ **CHECKPOINT 0:** tell the user the folders are created, the project files are downloaded, and
which tools they're logged into. Ask them to log into any that are missing.

---

## 2. The project in brief

**Chicken Assassin** is a serious animated revenge action film about anthropomorphic animals,
mostly roosters. The tone is crime drama, not comedy. The quality target is a modern animated
feature film.

**Story so far (the whole film):** Mason Reed, a former Syndicate assassin now living quietly as a
bank accountant, secretly saves the mayor from an assassination. That exposes him. The Syndicate
finds him, kills his wife Sarah and kills Mason. His 15-year-old son Marcus is taken in by
Mason's old partner, the master assassin Zhang Lei, trains for six years, and returns at 21 as
the **White Assassin** to destroy the Syndicate and its public front, FLYCORP.

**Sequence 1** is the opening, about 3–4 minutes. Syndicate boss Alexander Voss sends two hitmen,
**the B-ros**, to kill Mayor Mitchell on a dark road. A hooded figure (Mason, though **his face
is never shown**) stands in the road, stops them and wounds them, but lets them live. The film's
title appears after a blood splash. The B-ros report back: "He's alive."

---

## 3. Visual style (use in every prompt)

### 3.1 STYLE block

Start **every** image prompt with this block, unchanged:

> Cinematic still from a high-end stylized 3D animated feature film. Anthropomorphic animal
> characters with detailed feathers and fur, expressive faces, realistic proportions for a
> serious action drama. Dramatic cinematic lighting, shallow depth of field, subtle film grain,
> 16:9 widescreen. No text, no captions, no watermark.

### 3.2 MONASVILLE block

Add this to every exterior city or road shot:

> Monasville at night: a warm, realistic city. Sodium-orange streetlights, thousands of warm lit
> office windows, light fog, wet asphalt with reflections. No neon signs. The tallest building is
> FLYCORP Tower: a dark glass skyscraper with a glowing red band at the top and a blue "FLYCORP"
> sign.

### 3.3 Colour rules

- Night scenes: deep blue shadows, warm orange light.
- The Syndicate and FLYCORP: **red** (the phoenix mark) and **blue** (the FLYCORP logo).
- Headlights: cold white-blue, the only cold light on the road.

---

## 4. Characters in Sequence 1

**Always upload the reference image** when generating a character. Descriptions are only
reminders. If the description and the image disagree, **the image wins**.

| Character | Reference | Description block (add to prompts) |
|---|---|---|
| **THE FIGURE (Mason Reed, assassin)** | `mason_reed_sheets.png` (right half) | An adult rooster in his 40s in black tactical assassin gear: a black hooded coat with the hood up, a black mask over his lower face and beak, black armoured tactical suit with straps, black gloves and boots, a katana hilt over his right shoulder. White feathers, bright red comb just showing under the hood. **His face stays in shadow: only a glint of amber eyes and the red comb are visible.** Silent, very still. |
| **BILLY** (B-ros) | `cast_lineup.png` ("Billy & Bill", left) | A young rooster in his 20s, dark reddish-brown feathers, spiky red comb, dark jacket, cocky grin, chewing gum. Loud, arrogant. |
| **BILL** (B-ros) | `cast_lineup.png` ("Billy & Bill", right) | A young dog in his 20s, short brown fur, black baseball cap, dark jacket. Quiet, cold stare. |
| **ALEXANDER VOSS** | `cast_lineup.png` ("Alexander Voss") | A powerful bull in his 50s, dark brown fur, curved horns, perfectly tailored dark navy suit, white shirt, dark tie. A gold ring with a **red phoenix** emblem. Calm, controlled, dangerous. |
| **MAYOR ROBERT MITCHELL** | `cast_lineup.png` ("Robert Mitchell") | An American bison in his 50s, thick brown fur, navy suit, white shirt, red tie, reading glasses. Honest, tired, brave. |
| **SAM** (mayor's driver) | none, new character | A calm middle-aged Labrador dog with golden fur, dark chauffeur suit. |

**Props:**
- **Syndicate mark:** a red phoenix rising from flames.
- **B-ros' car:** a black, slightly worn sedan with a small dashcam that has a blinking red light.
- **Mayor's car:** a black SUV.
- **Shuriken:** a dark steel four-point throwing star.

---

## 5. Phases

### Phase 1: Character references

In ChatGPT, upload the reference image and generate one clean **full-body reference image** for
each character: front view, neutral pose, plain dark grey background. Prompt:

> Using the attached character sheet, create a clean full-body reference image of [CHARACTER]
> exactly as designed: same species, colours, outfit and proportions. Front view, neutral
> standing pose, plain dark grey background. [STYLE block] [Character description block]

Make one each for: The Figure, Billy, Bill, Voss, Mayor Mitchell and Sam. Save them as
`references/characters/<name>_ref.png`.

✋ **CHECKPOINT 1:** show the user all six. Regenerate any they reject. These images will be
uploaded in every shot from now on, so they must be right.

### Phase 2: Test three shots

Before making the whole sequence, make **S15**, **S18** and **S22** (section 8) in **all three
video tools** if free credits allow. That's 3 shots × 3 tools.

✋ **CHECKPOINT 2:** show the user the results side by side and ask which tool looks best for
(a) characters and (b) action. Use their choice for Phase 3.

### Phase 3: Produce the sequence

For each shot in section 8, in order:

1. **Start frame:** in ChatGPT, upload the relevant character reference images (and the Blender
   layout render where noted). Prompt = **STYLE block** + **MONASVILLE block** (exteriors) +
   character blocks + the shot's **Image prompt**. Save as `images/Sxx_v1.png`.
2. **Video:** in the chosen video tool, use image-to-video with the start frame. Prompt = the
   shot's **Motion prompt**. Generate at the length given, 16:9. Save as `video/Sxx_v1.mp4`.
3. **Check it** against the screenplay and the reference images. If the character drifted (wrong
   colours, wrong outfit, an extra limb, a visible face on the Figure), regenerate. **Maximum 3
   attempts per shot**, then mark it ⚠️ in the log and move on.
4. **Log it.**

✋ **CHECKPOINT 3:** after every **5 shots**, show the user the clips and wait for approval.
Copy approved clips to `selects/`.

When free credits run out for the day, stop, update the log and tell the user where you stopped.

### Phase 4: Hand back

When every shot has a select, give the user a summary: shots done, shots marked ⚠️, credits used,
and what still needs to happen in editing (title card, blood splash, sound and voices; see
section 6).

---

## 6. Special cases

- **Blood:** don't generate blood with AI. Most tools refuse it, and it won't look consistent.
  Generate S26 **without** blood. The team adds a blood-splash overlay and the title card
  when editing.
- **Weapons refused:** if a tool refuses because of a gun or sword, describe the action less
  directly (for example "raises a dark object", or frame the shot so the weapon is out of view), or
  try the backup tool. Note it in the log.
- **Keeping the Figure's face hidden:** if a result shows his face clearly, regenerate with "face
  completely in shadow under the hood, only eyes glinting."
- **Dialogue:** let Veo generate the spoken lines so the mouths move. The team may record their own
  voices later. Write every line exactly as in the screenplay.
- **Fight flashes (S24a–d):** each is a very short 1–2 second clip, dark, lit only by a muzzle flash
  or a spark. These are meant to be fast and hard to read.

---

## 7. Production log format

`seq01-the-shadow/production-log.md`:

```markdown
| Shot | Version | Tool | Prompt used | Credits | Status | File | Notes |
|---|---|---|---|---|---|---|---|
| S15 | v1 | Flow/Veo | (paste full prompt) | 20 | ✅ approved | selects/S15.mp4 | |
| S18 | v2 | Kling | ... | 30 | ⚠️ drift | video/S18_v2.mp4 | comb wrong colour |
```

Status values: 🕓 in progress · 👀 waiting for approval · ✅ approved · ⚠️ problem · ❌ rejected.

---

## 8. Shot list — Sequence 1

Format: **ID — Shot type — Length** · Characters to upload · Image prompt · Motion prompt.
Lines in quotes are dialogue: put them in the motion prompt word for word.

### Scene 1: Monasville skyline

**S01 — Extreme wide, establishing — 8s** · No characters · Exterior
- **Image:** Monasville skyline at night seen from far away across dark pine trees. FLYCORP Tower
  rises above every other building in the centre.
- **Motion:** Very slow push in toward FLYCORP Tower. Fog drifts, windows flicker on and off.
  Sound: low city hum; a car radio news anchor says "...and Mayor Robert Mitchell spoke again
  tonight at the Monasville Charity Gala, repeating his promise to root out corruption in the
  city..."

### Scene 2: Voss's office

**S02 — Wide — 6s** · Voss
- **Image:** A dark luxury penthouse office on the top floor of FLYCORP Tower: polished wood, a
  huge glass window over the glittering city. Voss stands at the window with his back to the
  camera. A wall screen shows the mayor at a podium.
- **Motion:** Voss stands completely still. Camera slowly drifts sideways. Silence except the hum
  of the city.

**S03 — Insert, the wall screen — 6s** · Mayor Mitchell
- **Image:** A TV news broadcast on a wall screen: Mayor Mitchell at a podium at a charity gala,
  speaking with conviction.
- **Motion:** The mayor speaks into the microphones: "Whoever is poisoning this city, hiding
  behind clean buildings and clean suits... I will find you. And I will show Monasville who you
  are."

**S04 — Extreme close-up — 3s** · Voss
- **Image:** Voss's large hand holding a remote. A gold ring on his finger with a red phoenix
  emblem catches the light.
- **Motion:** His thumb presses a button. The TV sound cuts off to silence.

**S05 — Medium close-up — 8s** · Voss
- **Image:** Voss in profile against the window, the city lights behind him, a phone in his hand.
- **Motion:** He says quietly to himself: "Brave man." He lifts the phone and speaks calmly:
  "Send the B-ros. Tonight." Pause. "Make it quiet."

**S06 — Close-up through glass — 4s** · Voss, Mayor Mitchell
- **Image:** Voss's reflection in the dark window glass sits right over the mayor's face on the
  TV screen.
- **Motion:** Voss's reflection doesn't move. The mayor's face on the screen keeps talking
  silently. Slow push in.

### Scene 3: The B-ros' car

**S07 — Interior two-shot — 6s** · Billy, Bill
- **Image:** Inside a black sedan at night, lit by the dashboard. Billy drives, tapping the wheel.
  Bill sits next to him loading a pistol. A small dashcam with a blinking red light sits between
  them.
- **Motion:** Billy taps the wheel to hard drill music. Bill loads rounds slowly. Streetlights pass
  outside.

**S08 — Interior, two-shot — 8s** · Billy, Bill
- **Image:** Same car. Bill reads his phone screen; Billy grins at the road.
- **Motion:** Bill says flatly: "Gala's over. He's taking Ridge Road home. Two cars. No police."
  Billy grins: "Ridge Road. Dark, long, no cameras. It's like he wants it."

**S09 — Interior, two-shot — 5s** · Billy, Bill
- **Image:** Same car, same framing.
- **Motion:** Bill: "Boss said quiet." Billy: "I'm always quiet." Billy turns the music up; Bill
  reaches over and turns it off.

### Scene 4: Ridge Road, the mayor

**S10 — Wide — 6s** · No characters · Exterior · *Composition reference: `renders/shot_A.png`*
- **Image:** A long two-lane road through dark pine trees, streetlights every forty metres making
  pools of orange light in the fog, the city skyline far away. A black SUV drives along it.
- **Motion:** The SUV drives steadily away from the camera through the pools of light.

**S11 — Interior, back seat — 8s** · Mayor Mitchell, Sam
- **Image:** Back seat of the SUV. The mayor in reading glasses with a thick folder on his knees:
  photographs, bank records, one page stamped FLYCORP. Sam, the driver, visible in the rear-view
  mirror.
- **Motion:** Sam glances in the mirror: "You should rest, sir." The mayor, not looking up: "When
  this is finished, Sam." He closes the folder and rubs his eyes.

**S12 — POV through the car window — 4s** · The Figure · Exterior
- **Image:** Looking out of the moving SUV's window: a streetlight passes, and just outside its
  light, among the trees, a hooded figure stands completely still, watching.
- **Motion:** The figure slides past the window as the car drives on. He doesn't move.

**S13 — Interior, close-up — 3s** · Mayor Mitchell
- **Image:** The mayor turning to look back through the rear window.
- **Motion:** He looks back, frowns at the empty darkness, then turns forward again.

### Scene 5: The figure in the road

**S14 — Interior, two-shot — 6s** · Billy, Bill
- **Image:** Inside the B-ros' car, headlights off, very dark. The mayor's red tail lights far
  ahead through the windshield.
- **Motion:** Billy: "After the bend. I pull alongside, you do your thing." Bill screws a silencer
  onto his pistol.

**S15 — Wide, from the car — 4s** · The Figure · Exterior · *Composition reference: `renders/shot_B.png`*
- **Image:** Headlights snap on and light up a hooded figure standing in the middle of a dark wet
  road forty metres ahead, pine trees on both sides, the city glowing far behind him.
- **Motion:** The headlights flash on suddenly. The figure doesn't move. Fog drifts through the
  beams.

**S16 — Exterior, wide — 5s** · B-ros' car
- **Image:** The black sedan braking hard on the wet road at night.
- **Motion:** Billy yells "WHOA—!" Tyres scream, the car slides and stops, and steam rises from the
  hood.

**S17 — Exterior, long lens — 3s** · No characters
- **Image:** Far down the dark road, past the figure, the mayor's red tail lights.
- **Motion:** The tail lights shrink into the dark and disappear.

**S18 — Low angle — 4s** · The Figure · Exterior · *Composition reference: `renders/shot_C.png`*
- **Image:** Low angle looking up at the hooded figure in the road, a streetlight above him, FLYCORP
  Tower glowing far behind.
- **Motion:** The streetlight above him buzzes and flickers. He stays perfectly still. His coat
  moves slightly in the wind.

### Scene 6: The confrontation

**S19 — Wide, from behind the car — 6s** · Billy, Bill, The Figure
- **Image:** Billy and Bill step out of the car into the headlights. Their long shadows stretch down
  the road toward the figure.
- **Motion:** Billy calls out: "Hey! Old man! You lost?" Then: "You got about three seconds to get
  out of my road."

**S20 — Medium, on the figure — 5s** · The Figure
- **Image:** The hooded figure in the headlight beam, face in shadow, only his eyes glinting.
- **Motion:** He speaks low and calm, almost kind: "Turn around." Pause. "Go home."

**S21 — Two-shot — 4s** · Billy, Bill
- **Image:** Billy laughing; Bill beside him, not laughing, slowly raising a silenced pistol.
- **Motion:** Billy: "We are going home. Right after—"

**S22 — Insert, action — 3s** · No characters
- **Image:** A dark steel shuriken spinning through a headlight beam toward the car.
- **Motion:** The shuriken flies into the headlight, which shatters. Glass sprays, and half the
  light goes out.

**S23 — Wide — 4s** · Bill, Billy
- **Image:** Bill firing his silenced pistol at an empty road; sparks off the asphalt.
- **Motion:** Two muffled shots, sparks fly, the figure is gone. Billy: "Where'd he—" The
  streetlight goes out. Darkness.

**S24a–d — Fight flashes — 1–2s each** · Billy, Bill, The Figure
- **a:** Bill spins in the dark, lit only by his own muzzle flash.
- **b:** A muzzle flash lights the figure right behind Bill for an instant.
- **c:** In a flash of sparks, a knife knocks the pistol from Bill's hand.
- **d:** Billy charges with a knife, shouting; in the last headlight we see steel catching the light.
- **Motion (all):** Very dark, chaotic, fast, mostly silhouettes. Add the sound of a sword slowly
  sliding out of its sheath over S24d.

**S25 — Medium wide — 5s** · Billy, Bill, The Figure
- **Image:** The streetlight flickers back on: Bill frozen in the road, eyes wide; Billy groaning on
  the wet ground behind him; the figure standing right behind Bill, sword lowered.
- **Motion:** Bill whispers: "...It's you."

**S26 — Close, fast — 2s** · Bill, The Figure
- **Image:** Bill's hand going for a second pistol at his belt.
- **Motion:** A fast sword slash across his hand. **No blood**: the splash is added in editing
  (section 6).

**S27 — Title card** · *Made in editing, not by AI.* Blood splash → black → a heavy drum hit →
**CHICKEN ASSASSIN**.

### Scene 7: After the title

**S28 — Wide — 6s** · Billy, Bill
- **Image:** Rain on an empty road at night. Bill kneels, gripping his injured hand. Billy is
  slumped against the car, one eye swollen. The figure is gone.
- **Motion:** Billy, shaky but trying to sound tough: "He... he let us live. Why'd he let us live?"

**S29 — Medium close-up — 5s** · Bill
- **Image:** Bill in the rain holding a phone to his ear with his good hand.
- **Motion:** Bill, quietly into the phone: "Tell the boss." Pause. "He's alive."

**S30 — Insert — 3s** · No characters
- **Image:** Inside the empty car, rain on the windshield, a small dashcam with a blinking red
  light.
- **Motion:** The red light keeps blinking. Rain runs down the glass.

**S31 — Extreme close-up — 4s** · No characters
- **Image:** A dark steel shuriken stuck deep in a black car door. Engraved on it is a faded,
  scratched-out red phoenix emblem.
- **Motion:** Slow push in on the phoenix mark. Rain drips off the metal. Cut to black.

---

## 9. When Sequence 1 is done

Tell the user:
1. Which shots are approved, and which need another try with paid credits later.
2. What the editor needs to add: title card, blood splash, drill music for the car, ambient
   sound, and voice recordings if the team replaces the AI voices.
3. That the next handoff file (Sequence 2: "The Mayor's Secret") will come from the planning
   session.
