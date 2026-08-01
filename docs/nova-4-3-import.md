# Nova 4:3 patch import

Imported from Paco's supplied `Switch Mods for Nova` archive on 2026-08-01.
These are **WIP** patches: they have not been device-validated by this repository.
Use only one aspect-ratio mod per title at a time.

## Included explicit 4:3 patches

- Donkey Kong Country: Tropical Freeze — v1.0.2
- Mario Kart 8 Deluxe — v3.0.5
- Metroid Dread — v2.1.0, 1280x960 output
- Super Mario 3D World + Bowser's Fury — v1.0.0 crop fix
- Super Mario Odyssey — v1.3.0

Mario vs. Donkey Kong v1.0.0 was not imported again: the supplied 4:3 patch
matches the existing `[4:3 WIP v1.0.1] 4:3 WIP Camera` v1.0.0 patch payload.

## Nova aspect-ratio notes

- **Captain Toad: Treasure Tracker v1.3.0** — included under its supplied
  `4:3 Source Label` name. Its source folder/title say 4:3 while an internal
  comment says `32:9`; the patch payload is preserved unchanged.
- **Kirby and the Forgotten Land v1.0.0** and **Luigi's Mansion 3 v1.4.0** —
  included and accurately labelled as **1.375 / 11:8**, not 4:3.

## Included performance and visual patches

All of these are labelled by their actual function and version, rather than as
aspect-ratio mods:

- Captain Toad: Treasure Tracker v1.3.0 — Disable Depth of Field; Disable
  On-Screen Cursor
- Kirby and the Forgotten Land v1.0.0 — 60 FPS Full; Disable Dynamic
  Resolution v2
- Metroid Dread v2.1.0 — 60 FPS + Cutscene Fix (two build-ID-specific patches
  kept together in one mod folder)
- Super Mario Odyssey v1.3.0 — Disable Dynamic Resolution; Disable FXAA
