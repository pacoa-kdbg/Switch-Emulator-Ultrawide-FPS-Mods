# The Legend of Zelda: Link's Awakening v1.0.1 — narrow-aspect mods

## Status

- **4:3 v1.0.1:** field-verified on an **AYANEO Pocket S Mini** (`1280x960`) with **Eden stable**.
- **3:2 WIP v1.0.1:** confirmed build-compatible and applied by Eden, but it has **not** yet received a true 3:2 visual A/B certification.

## Target

- Title ID: `01006BB00C6F0000`
- Game update: `v1.0.1` (Eden reports the installed update as `v0.2.0`)
- Required `main` NSOBID: `909E904AF78AC1B8DEEFE97AB2CCDB51968F0EC7`

The pchtxt header, not the folder name, is authoritative. These files will not apply to a different main build.

## Included mods

```text
[4:3 v1.0.1]/exefs/1.0.1.pchtxt
[3:2 WIP v1.0.1]/exefs/1.0.1.pchtxt
```

Enable **only one** aspect-ratio mod at a time.

## 4:3 setup — verified

Use on a true 4:3 screen/window, such as the Pocket S Mini's `1280x960` panel:

```text
Eden aspect ratio: 4:3
```

Do not use `Stretch` as the 4:3 validation setting. The verified A/B comparison used:

1. Stock game, Eden set to 16:9, on the same updated `main` build.
2. 4:3 mod, Eden set to 4:3, on the same updated `main` build.

The stock capture is letterboxed on the 4:3 panel; the modded capture fills it. Link, house geometry, roof tiles, doors, fence posts, and grass retained natural proportions after the intended 16:9-to-4:3 camera compensation.

## 3:2 setup — pending visual certification

Use a real 3:2 presentation target, for example a `1440x960` desktop window:

```text
Eden aspect ratio: Stretch to window
```

Do **not** use Stretch full-screen on a 4:3 panel: that converts the presentation back to 4:3 and cannot validate 3:2 geometry.

## Patch evidence

The verified 4:3 device run logged:

```text
Renderer.aspect_ratio: R4_3
HasNSOPatch: Querying NSO patch existence for build_id=909E904AF78AC1B8DEEFE97AB2CCDB51968F0EC7, name=main
PatchNSO: Patching NSO for name=main, build_id=909E904AF78AC1B8DEEFE97AB2CCDB51968F0EC7
Applying IPSwitch patch from mod "4-3 Aspect Ratio TEST v1.0.1"
```

The 3:2 patch also produced the same `PatchNSO` / `Applying IPSwitch` evidence on this build, but lacks the required true-3:2 visual A/B test.

## Notes

- Both mods replace the public 21:9 mod's aspect-ratio constant with the requested aspect value.
- Culling is intentionally left at 16:9. Reducing the culling region can cause edge pop-in.
- The source pattern derives from public Link's Awakening 21:9/32:9 ExeFS mods by Jaddey, KeatonTheBot, and Fl4sh9174.
