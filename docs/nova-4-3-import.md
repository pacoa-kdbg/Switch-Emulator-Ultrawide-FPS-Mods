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

## Deliberately not labelled 4:3

- **Captain Toad: Treasure Tracker v1.3.0** — its title says 4:3, but its
  internal comment says `32:9`; it needs source/runtime verification before
  adding it as a 4:3 patch.
- **Kirby and the Forgotten Land v1.0.0** and **Luigi's Mansion 3 v1.4.0** —
  both explicitly identify themselves as **1.375 / 11:8**, not 4:3.

Non-aspect patches from the archive (60 FPS, dynamic-resolution, DOF, cursor,
and FXAA changes) were intentionally excluded.
