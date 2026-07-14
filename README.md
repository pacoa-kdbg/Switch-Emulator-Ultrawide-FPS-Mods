<p align="center">
  <a href="https://github.com/Fl4sh9174/Switch-Emulator-Ultrawide-FPS-Mods/stargazers">
    <img src="https://img.shields.io/github/stars/Fl4sh9174/Switch-Emulator-Ultrawide-FPS-Mods?style=for-the-badge" alt="GitHub stars">
  </a>
  <a href="https://github.com/Fl4sh9174/Switch-Emulator-Ultrawide-FPS-Mods/commits/main">
    <img src="https://img.shields.io/github/last-commit/Fl4sh9174/Switch-Emulator-Ultrawide-FPS-Mods?style=for-the-badge" alt="Last commit">
  </a>
  <a href="https://github.com/Fl4sh9174/Switch-Emulator-Ultrawide-FPS-Mods">
    <img src="https://img.shields.io/github/repo-size/Fl4sh9174/Switch-Emulator-Ultrawide-FPS-Mods?style=for-the-badge" alt="Repo size">
  </a>
</p>

<p align="center">
  <a href="https://ko-fi.com/fl4sh9174">
    <img src="https://img.shields.io/badge/Ko--fi-Support%20Me-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white" alt="Ko-fi">
  </a>
</p>

<h1 align="center">Switch Emulator Ultrawide, FPS, and Graphics Mods</h1>

<p align="center">
  Ultrawide, FPS, resolution, and graphics mods for <strong>Switch games on Switch emulators</strong> such as <strong>Yuzu</strong>, <strong>Ryujinx</strong>, <strong>Citron</strong>, <strong>Eden</strong>, <strong>KenjiNX</strong>, and <strong>Ryubing</strong>.
</p>

---

## About

This repository contains a collection of **Switch emulator mods** focused on:

- **Ultrawide mods** with HUD fixes when possible
- **FPS mods** such as **60 FPS**, **120 FPS**, **240 FPS**, **Dynamic FPS** depending on the game
- **Resolution mods** including **1080p**, **1440p**, **4K**, **8K**, and ultrawide formats when available
- Additional **graphics fixes** and game-specific improvements

Most ultrawide mods are primarily optimized around **3440x1440**, but other aspect ratios and higher resolutions may also be included depending on the title.

---

## Supported emulators

These mods are made primarily for **Switch emulators**, including:

- **Yuzu**
- **Ryujinx**
- **Citron**
- **Eden**
- **KenjiNX**
- **Ryubing**

Some mods may also work on real Switch hardware through **IPS conversion** when needed, but the main focus of this repository is **Switch emulator support**.

---

## Quick installation guide

### Yuzu / Citron / Eden / Ryujinx / KenjiNX / Ryubing

1. Open the Emulator and right-click the game you want to mod
2. Open the **mod data location**
3. Extract the corresponding `.zip` file there
4. Enable the mods you want inside the emulator

### Switch

When needed, files can be converted to **IPS** format for Switch use.

---

## How this repository is organized

- a `.zip` file with the available mods for that title
- optional notes about compatibility, emulator behavior, or supported game versions

This layout makes it easy to download only the mod pack you need for a specific game.

---

## Common mod types

Depending on the game, you may find:

- **21:9 ultrawide**
- **3:2 / 4:3 WIP candidates** in `generated-narrow-aspect/`
- **60 FPS**
- **120 FPS**
- **240 FPS**
- **Dynamic FPS**
- **1080p / 1440p / 4K / 8K**
- **LOD improvements**
- **Depth of Field disable**
- **HUD fixes**
- other game-specific tweaks

Not every game includes every option.

---

## Important notes

- Do **not** delete files inside the `mods` folder unless you know exactly what they do
- Some mod packs include files such as:
  - cheat files
  - `pchtxt`
  - `V2.pchtxt`
- In many cases, all included files are required for the mod to work correctly
- If a mod is broken after a game update, make sure the **game version**, and **mod version** still match

### 3:2 and 4:3 WIP candidates

This fork includes generated narrow-aspect candidates under `generated-narrow-aspect/`.
They are made from existing 21:9 `.pchtxt` mods by changing obvious aspect-ratio
float loads to 3:2 or 4:3. These are meant for emulator testing first; HUD fixes
are still game-specific. See `docs/narrow-aspect-research.md` for details and run
`python3 tools/generate-narrow-aspect-mods.py` to regenerate them.

---

## Support

All mods here are free.

If this repository helped you, improved your emulator experience, or saved you time, you can support the project here:

- **Ko-fi:** https://ko-fi.com/fl4sh9174

Support helps me:
- update older mods
- add support for new games
- test more emulator versions
- improve ultrawide, FPS, and resolution compatibility

---

## Contact

- **GitHub:** https://github.com/Fl4sh9174
- **Ko-fi:** https://ko-fi.com/fl4sh9174
- **GameBanana:** https://gamebanana.com/members/3083977
- **Discord:** `Fl4sh_#9174`

---

## Keywords

Switch emulator mods, Switch ultrawide mods, Switch FPS mods, Switch resolution mods, Yuzu mods, Ryujinx mods, Citron mods, Eden mods, KenjiNX mods, Ryubing mods, 21:9 mods, 60 FPS mods, 120 FPS mods, Dynamic FPS mods 4K mods, 8K mods.
