# CHICKEN ASSASSIN — Project Brief

> **To Claude Desktop:** read this first. It's the whole project: the story, every decision the
> team has made, and how production works. Then read `CLAUDE_DESKTOP_HANDOFF_SEQ01.md` for the
> current task.

## The project

An animated feature film made by a small team of friends in Ghana (computer science and ICT
students). The friend who created the story wrote the outline and made the character sheets
with ChatGPT. Planning happens in a separate Claude session, which writes a handoff file for
each sequence. **Claude Desktop runs the AI tools and saves everything to the `Kweku` folder on
the Desktop.**

- **Genre:** serious animated revenge action film with anthropomorphic animals (mostly roosters).
  Crime drama tone, not comedy.
- **Quality target:** a modern animated feature film.
- **Tagline:** "A family. A fall. A mission."

## Folder contents

| Path | What it is |
|---|---|
| `PROJECT_BRIEF.md` | This file |
| `CLAUDE_DESKTOP_HANDOFF_SEQ01.md` | **Current task:** produce Sequence 1 (31 shots with prompts) |
| `reference/` | Character sheets (cast lineup, Mason, Zhang Lei) and the team's PixVerse test clip |
| `seq01-the-shadow/screenplay.md` | Sequence 1 screenplay, draft 2 |
| `seq01-the-shadow/build_road_scene.py`, `road_scene.blend`, `renders/` | Blender layout of the Ridge Road scene, with composition references for three shots |

## Production decisions

| Decision | Answer |
|---|---|
| Format | **16:9 widescreen** film. Vertical 9:16 clips are cut from it later for TikTok and Shorts |
| City look | **Warm and realistic:** sodium-orange streetlights, lit office windows, fog, wet streets. **No neon** |
| Still images | **ChatGPT** (it made the character sheets), with Gemini as backup |
| Video | **Free tiers for now:** Google Flow/Veo (main), Kling and PixVerse (backups). Google AI Pro will be bought later for final shots |
| Blender | Layouts and composition references only. The team's computers have no strong graphics card |
| Blood | Never generated with AI. Added as an overlay in editing |
| Budget | No spending without the user's approval |

## Characters

The images in `reference/` define how characters look. **They always win over written descriptions.**

| Character | Who they are |
|---|---|
| **Marcus Reed** | Rooster, the protagonist. **15** at the start, **21** when he returns as the **White Assassin** (white tactical suit, silver weapons). Focused, disciplined, loyal |
| **Mason Reed** | Rooster, 40s, Marcus's father. A former Syndicate assassin, now a **bank accountant who also volunteers in the community**. Assassin kit: **suppressed pistol, knife, sword and shurikens** (no spear) |
| **Sarah Reed** | Marcus's mother. Kind, strong, loving. Killed in Sequence 5 |
| **Zhang Lei** | Rooster, 50s+, legendary retired assassin, "The Master". **Mason's old Syndicate partner.** Trains Marcus in Centurion |
| **Alexander Voss** | Bull, 50s, Syndicate boss and FLYCORP CEO. Wears a gold ring with the **red phoenix** |
| **Robert Mitchell** | Bison, 50s, mayor of Monasville. Honest and brave. Knows Mason saved him |
| **Helios** | Mysterious crow informant. **Identity never revealed** |
| **Billy & Bill ("the B-ros")** | Syndicate hitmen in their 20s. **Billy is a rooster** (loud driver), **Bill is a dog** in a cap (quiet, cold). Partners, not brothers. **Both survive Sequence 1** |
| **Ashley Parker** | Cat, Marcus's school friend. Smart, tech-savvy. A future sequel character |
| **The Bullies** | A teenage dog gang |
| **Sam** | Labrador dog, the mayor's driver (Sequence 1) |

**The Syndicate:** a secret criminal organisation. Its mark is a **red phoenix rising from
flames**. Motto: "Power. Control. No mercy." **FLYCORP** is its public front, and FLYCORP Tower
is the tallest building in Monasville.

**Places:** **Monasville** (the city), **Ridge Road** (dark road outside the city), **Centurion**
(Zhang's secluded home).

**Music:** hard drill for the B-ros. Warm, old-school rap belongs to Mason and Marcus: it's their
shared thing.

## The story: 20 sequences (with team decisions applied)

1. **The Shadow.** Monasville at night, Voss and FLYCORP. Voss sends the B-ros to kill Mayor
   Mitchell on Ridge Road. **Mason** (face hidden) stands in the road, tells them "Turn around. Go
   home," then wounds them but lets them live. Blood splash, title. Bill reports: "He's alive." A
   dashcam recorded it, and a shuriken with an old phoenix mark is left behind.
2. **The Mayor's Secret.** The mayor addresses the city but hides the details of the attempt, and
   keeps collecting evidence: assassinations, corruption, money laundering. Voss watches the
   dashcam footage, sees the shuriken, and realises his old assassin is alive and protecting the
   mayor. He orders both eliminated.
3. **The Reed Family.** Morning at home: Mason, Sarah and 15-year-old Marcus at breakfast. Mason
   drives Marcus to school; they listen to their rap. Mason works as an accountant at Monasville
   Bank. The clock reaches 3:00 PM.
4. **The Old Life Returns.** Mason picks Marcus up from school. **Ashley Parker** is Marcus's
   friend; she's the one telling everyone about the assassination attempt. At home, broken glass,
   an open door, signs of a struggle.
5. **Everything Is Taken.** Sarah has been murdered. Marcus is kidnapped. Mason is knocked out,
   wakes beside Sarah, breaks down, and realises his old enemies found him because he saved the
   mayor.
6. **The Assassin Awakens.** Mason contacts Helios, opens his hidden armoury, puts on his black
   assassin gear and takes his suppressed pistol, knife, sword and shurikens. Motorcycle into the
   night.
7. **The Hideout.** Stealth through the Syndicate hideout, the alarm, the fight, and Mason rescues
   Marcus.
8. **The T-Junction.** Escape on the motorcycle, Syndicate vehicles chasing them. Surrounded,
   Mason tells Marcus to run. Marcus watches his father being struck down.
9. **The Boy in the Woods.** Marcus hides alone in an abandoned building. Grief turns into
   determination.
10. **The Master.** Helios tells Zhang that Mason is dead. Zhang finds Marcus being beaten by the
    teenage dog bullies, defeats them without seriously hurting them, and recognises his old
    partner's son.
11. **Come With Me.** Marcus asks to be trained; Zhang refuses. Marcus swings; Zhang catches his
    fist. "I couldn't help them. I am weak." Zhang: "Come with me." They leave for Centurion.
12. **Six Years.** (Was "Two Years".) Training: discipline and emotional control first, then
    hand-to-hand, sword, shooting, shurikens (**no spear**), conditioning and meditation. Marcus
    grows from 15 to 21: he fails as a boy, improves as a teenager and masters it as a man.
13. **The White Assassin.** Marcus receives his white tactical suit and silver weapons and rides
    to Monasville alone.
14. **Return to Monasville.** Helios's intel: the Syndicate is meeting at FLYCORP, and Voss will be
    there. **New:** the **mayor quietly helps Marcus** (a place to stay, support), knowing Mason
    saved his life, and advises him to "take it easy and try to live." Marcus prepares and goes in.
15. **FLYCORP.** Stealth, traps, lockdown, the fight upward, a grenade into the meeting hall.
16. **The Boss.** Voss recognises the fighting style (**Mason and Zhang's**): "You're Mason's son."
    "I ordered your father's death." Marcus loses control, and Voss overwhelms him.
17. **Discipline.** Marcus remembers Zhang's first lesson, calms down, gets back up, fights
    smart, and defeats Voss.
18. **The Fall of FLYCORP.** The tower burns and collapses as Marcus rides away.
19. **The Unsung Hero.** The mayor exposes the Syndicate: "The city may never know who he is...
    but he is an unsung hero." **He secretly knows it's Marcus** and protects the secret. **Ashley
    returns** (sequel hook).
20. **The Legacy.** Zhang watches the news from Centurion. Helios stays a mystery. Final shot:
    Marcus rides away from Monasville into the dark. Cut to black.

## How the team works

1. **Planning session (Claude Code):** writes the screenplay, shot list and prompts for one
   sequence at a time, as a handoff file.
2. **Claude Desktop:** follows the handoff file, generates images and video with the AI tools,
   saves to `Kweku/ChickenAssassin/`, and keeps a production log.
3. **The team:** approves each shot, records voices, and edits (DaVinci Resolve or CapCut).

One sequence at a time. Quality over speed.
