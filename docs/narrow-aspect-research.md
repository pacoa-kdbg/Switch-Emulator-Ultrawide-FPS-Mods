# 3:2 and 4:3 Narrow Aspect Research

Status: WIP candidates for emulator testing, not verified on hardware yet.

## What These Mods Are

Most packs in this repo are ExeFS patches in `.pchtxt` format. The common aspect-ratio pattern is an AArch64 patch that loads a floating-point aspect ratio, usually the 3440x1440-friendly 21:9.5 value:

- 21:9.5: `2.3888888`, float bits `0x4018e38e`
- 3:2: `1.5`, float bits `0x3fc00000`
- 4:3: `1.3333334`, float bits `0x3faaaaab`

The simple cases use two ARM64 instructions:

```text
mov  wN, #low16
movk wN, #high16, lsl #16
```

or the same sequence with an `xN` register. The generator only rewrites those obvious 21:9.5 instruction pairs. It does not try to solve game-specific HUD scale, layout positions, field of view, or resolution edits.

## How To Generate

From the repo root:

```bash
python3 tools/generate-narrow-aspect-mods.py
```

Output goes to `generated-narrow-aspect/`, with a `MANIFEST.csv` that lists every generated file and how many aspect-load pairs were changed.

To test one candidate in an emulator, copy the generated mod folder into that game's mod data location and enable it the same way as the existing repo packs. Keep only one aspect-ratio mod active at a time.

## What Needs Testing

For each candidate:

- Does the game boot?
- Is 3D rendering no longer stretched at 3:2 or 4:3?
- Is HUD usable, stretched, cropped, or off-screen?
- Do menus/cutscenes behave differently from gameplay?
- Does it require emulator stretch-to-window or native aspect settings?

## Highest-Priority Nintendo Candidates

These are the games Paco called out, plus Nintendo first-party games that the mechanical scan found.

| Priority | Game | Existing basis | Why it is promising | Risk |
| --- | --- | --- | --- | --- |
| High | The Legend of Zelda Breath of the Wild | 21:9 pchtxt has 3 direct aspect loads | Public issue comments report a working 4:3 conversion | HUD/FOV still needs play testing |
| High | The Legend of Zelda Echoes of Wisdom | 21:9 default-HUD patches are direct aspect loads | Public issue comments report the same two-line 4:3 aspect patch | Adjusted-HUD lines can push HUD off-screen |
| High | Pokemon Legends Arceus | Multiple direct aspect loads; HUD codecave is present | Public issue comments report a working 4:3 conversion | Generated 3:2/4:3 leaves HUD codecave constants unchanged |
| High | Super Mario 3D World + Bowser's Fury | Direct 21:9.5 aspect loads | Public issue comments report a working 4:3 conversion | Needs both gameplay and Bowser's Fury HUD checks |
| Medium | Super Mario Party Jamboree | Many direct aspect loads | Large number of mechanical matches | Lots of UI-heavy scenes to test |
| Medium | Metroid Prime Remastered | Direct aspect loads in default/adjusted HUD packs | 3D view should be easy to evaluate quickly | First-person HUD/visor can be fragile |
| Medium | Metroid Prime 4 Beyond | Direct aspect loads in 3440x1440/6880x2880 packs | Same class of patch as Prime Remastered | Newer game, likely version-sensitive |
| Medium | Pokemon Sword / Shield | One direct aspect-load candidate each | Simple patch surface | Needs camera/menu checks |
| Medium | Pokemon Mystery Dungeon Rescue Team DX | One direct aspect-load candidate | Simple patch surface | UI-heavy game |
| Medium | Super Mario Galaxy / Galaxy 2 | Direct aspect-load candidates | Useful for handheld 3:2 testing | Collection/emulator version differences likely |
| Medium | Super Mario RPG | One direct aspect-load candidate | Simple patch surface | UI and battle framing need checks |
| Low | Splatoon 2 / Splatoon 3 | Direct aspect loads | Good technical candidates | Online-focused titles and HUD may be awkward |

## Full Mechanical Candidate Set

The initial scan found 47 games with at least one clear `0x4018e38e` aspect-load pair in an aspect-ratio mod:

- Animal Crossing New Horizons
- Another Crab's Treasure
- Bayonetta Origins Cereza and the Lost Demon
- Bomb Rush Cyberfunk
- Cruis'n Blast
- DEAD OR ALIVE Xtreme 3 Scarlet
- Diablo III Eternal Collection
- Donkey Kong Country Returns HD
- DRAGON QUEST MONSTERS The Dark Prince
- Eiyuden Chronicle Hundred Heroes
- Endless Ocean Luminous
- FANTASY LIFE i The Girl Who Steals Time
- FIFA 23 Legacy Edition
- Fire Emblem Engage
- Fire Emblem Warriors
- Hollow Knight Silksong
- INAZUMA ELEVEN Victory Road
- Kirby's Return to Dream Land Deluxe
- Mario and Luigi Brothership
- Mario Party Superstars
- Mario vs. Donkey Kong
- Metroid Prime 4 Beyond
- Metroid Prime Remastered
- Nikoderiko the Magical World
- Paper Mario The Origami King
- Paper Mario The Thousand-Year Door
- Pikmin 4
- Pokemon Legends Arceus
- Pokemon Mystery Dungeon Rescue Team DX
- Pokemon Shield
- Pokemon Sword
- Princess Peach Showtime!
- Sonic Frontiers
- Sonic Racing CrossWorlds
- Splatoon 2
- Splatoon 3
- Super Mario 3D World + Bowsers Fury
- Super Mario Galaxy
- Super Mario Galaxy 2
- Super Mario Party Jamboree
- Super Mario RPG
- Super Smash Bros Ultimate
- The Legend of Zelda Breath of the Wild
- The Legend of Zelda Echoes of Wisdom
- Tomodachi Life Living the Dream
- Unicorn Overlord
- Xenoblade Chronicles 2

## Research Sources

- Fl4sh9174 repo README: install flow and repo scope.
- Fl4sh9174 issue #78: confirms there is no universal method; the simple path is replacing aspect-ratio float constants, while HUD work is game-specific.
- ADEMOLA200 Switch Emulator Mod Database: confirms many aspect-ratio mods are IPSwitch/ExeFS patches and often require emulator aspect/stretch settings.
- GameBanana Animal Crossing aspect patches: confirms 4:3 and 16:10 aspect-ratio patches are practical for at least some Switch games.
- StevensND Ghidra port/mod guide: points to the deeper workflow for updating/creating ExeFS/IPSwitch mods when no convertible aspect patch exists.
