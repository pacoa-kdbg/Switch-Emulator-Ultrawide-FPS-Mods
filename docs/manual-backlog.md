# Manual aspect-ratio mod backlog

Games that do NOT have a convertible 21:9 float-load patch upstream, so they need
a from-scratch reverse-engineering pass (Ghidra on the main executable) to find
the aspect-ratio constant / projection matrix / FOV path before a 3:2 or 4:3
mod can be written.

## Priority

1. **Kirby and the Forgotten Land** — no existing convertible ultrawide `.pchtxt`
   upstream; only `Kirby's Return to Dream Land Deluxe` was mechanically
   convertible. Requested by Paco 2026-07-14. Interest: 4:3 for Ayaneo Pocket
   S Mini / Pocket ACE testing. Approach: dump main NSO, load in Ghidra using
   StevensND's Switch port-mods guide, search for `0x3fe38e39` (16:9 float
   `1.777...`) or nearby projection setup, then patch to `0x3faaaaab` (4:3)
   or `0x3fc00000` (3:2). Verify HUD separately.

## Pokémon Sword v1.3.2 4:3 HUD/UI fix — FULLY WORKING (2026-07-14, field-confirmed 2026-07-31)

Status: **resolved / fully working** on AYANEO Pocket S Mini with Eden nightly.
The final shipped mod is `[4:3 + UI fix v1.3.2]`, committed in `e3a0647` and
documented in `docs/pokemon-sword-4-3-ui-fix.md` with field photos. The correct
Pocket S Mini recommendation is 4:3 for both the world aspect float and the UI
aspect double; emulator global stretch is not a substitute.

Build ID `A3B75BCD3311385AEED67FBEEB79CBB7BF02F471`.

Existing Fl4sh 21:9 mod (`[21.9 Ultrawide v1.3.2]/1.3.2.pchtxt`) patches only
the float-aspect load at file offset `0x00607664/0x00607668`:

```
00607664 c9719c52  // movz w9, #0xe38e   -> low16 of 2.388f
00607668 0903a872  // movk w9, #0x4018,lsl16 -> full 2.388f
```

Derived narrow mods (`[4:3 WIP v1.3.2]`, `[3:2 WIP v1.3.2]`) rewrite w9 to
`0x3faaaaab` / `0x3fc00000`. Culling (`00d93414`) and camera-distortion
(`006076c4/6c`) branches were preserved from Fl4sh's set.

A separate aspect **double** is built into `x9` at `0x00607de8/0x00607dec`:

```
00607de8 C971DCF2  // movk x9, #0xe38e,lsl#32
00607dec 0903E8F2  // movk x9, #0x4018,lsl#48   -> x9 = 0x4018E38E00000000 (2.388 dbl)
```

None of the current mods touch this double. Hypothesis: this untouched double
feeds the UI/HUD subsystem or another aspect-dependent codepath, and it is
why menus/HUD stretch horizontally at 4:3 (world uses the corrected float,
UI still uses the original 2.388 or a value derived from it).

### Candidate A deployed on Pocket S Mini (2026-07-14)

`[4-3-UIFix-A-v1.3.2]` — keeps world float at 4:3, forces the aspect double
to 16:9 (`0x3FFC71C71C71C71C` truncated to high32 = `0x3FFC71C7`):

```
00607de8 E938CEF2  // movk x9, #0x71C7,lsl#32
00607dec 89FFE7F2  // movk x9, #0x3FFC,lsl#48   -> x9 = 0x3FFC71C700000000 (~16:9 dbl)
```

Pushed to
`/sdcard/Android/data/dev.eden.eden_emulator.nightly/files/load/0100ABF008968000/4-3-UIFix-A-v1.3.2/exefs/1.3.2.pchtxt`.
Also set `dump_nso=true` / `dump_exefs=true` in Eden config so a merged main
NSO gets dropped in `.../files/dump/` on the next boot for proper RE.

Expected outcomes when Paco enables ONLY this mod (disabling `[4:3 WIP v1.3.2]`):

- If HUD/menus stop stretching (become pillarboxed inside the 4:3 window) →
  double at `0x607de8` is the UI aspect. Ship as `[4:3 WIP v1.3.2 + UI fix]`.
- If world re-stretches back to 16:9 → double is the world's aspect; revert.
- If nothing changes → double drives some other path; iterate by disassembling
  the merged NSO in Ghidra to trace xrefs from both aspect sites into UI code.

### Tools setup on GPD Win5 (deck)

Nothing installed yet. Plan for iteration 2+:

```
sudo pacman -S --needed jdk-openjdk unzip python-keystone aarch64-linux-gnu-binutils
mkdir -p ~/tools && cd ~/tools
# fetch Ghidra 11.x release
```

Use StevensND's Switch port-mods guide + Ghidra headless on the dumped main
NSO (once available at `/sdcard/Android/data/dev.eden.eden_emulator.nightly/files/dump/`).

## Notes

- Method reference: <https://github.com/StevensND/ghidra-port-mods-guide>
- Aspect float constants:
  - 16:9  → `0x3fe38e39` (1.77777779)
  - 21:9  → `0x4018e38e` (approx, matches Fl4sh set)
  - 3:2   → `0x3fc00000` (1.5)
  - 4:3   → `0x3faaaaab` (1.33333333)

### Iteration 2 test results (2026-07-14)

Candidate A on device: text rendered correctly, but menu icons were
misaligned / mis-scaled. Paco stopped emulation without checking world or
battle scenes. Interpretation: the double at `0x00607de8` partially drives
UI (menu backgrounds + text anchoring look fine at 16:9) but the icon
(sprite quad) path reads the SAME double and multiplies quad width by it.
With the double at 16:9 (1.778) instead of native 21:9.5 (2.388), sprite
quads shrink and/or land off their anchor grid.

Ghidra headless setup on Win5 was attempted but repeatedly SIGKILLed at the
exec-tool layer (~15-45s cap on any SSH-tunneled shell). NSO dump was also
unavailable: `dump_nso` / `dump_exefs` in Eden's `config.ini` read `false`
when re-checked (must have been overwritten by Eden on next launch, or the
prior subagent's edit did not persist). Full RE deferred; iterating on the
same single-constant patch instead.

### Candidate B deployed (2026-07-14)

`[4-3-UIFix-B-v1.3.2]` — HUD aspect double forced to 4:3 dbl
(`0x3FF5555555555555`, effective `0x3FF5555500000000` since only upper
32 bits are movk-patched):

```
00607de8 A9AACAF2  // movk x9, #0x5555,lsl#32
00607dec A9FEE7F2  // movk x9, #0x3FF5,lsl#48   -> x9 = 0x3FF5555500000000 (~1.333 dbl)
```

Rationale: if icons are pre-stretched horizontally by the double as an
X-scale factor for sprite quads, matching it to the ACTUAL output aspect
(4:3) should let icons render at native proportions inside the 4:3 window.
Text path was already OK at 16:9 (candidate A), so text may either
remain OK here or need a separate constant if it now over-shrinks.

### Candidate C deployed (2026-07-14)

`[4-3-UIFix-C-v1.3.2]` — HUD aspect double forced to 1.5 dbl (exact 3:2,
`0x3FF8000000000000`):

```
00607de8 0900C0F2  // movk x9, #0x0000,lsl#32  (no-op-ish on lower16)
00607dec 09FFE7F2  // movk x9, #0x3FF8,lsl#48   -> x9 = 0x3FF8000000000000 (1.5 dbl)
```

Middle bracket between candidate A (16:9, icons broken) and candidate B
(4:3). Try if B under-corrects (icons too small / too far left).

### Deploy pattern (still relevant for future iterations)

1. Write pchtxt on Sync-VM, `scp` to Win5 `/tmp/`.
2. `adb push /tmp/<file> /data/local/tmp/<file>` (u:shell can write here).
3. `adb shell '/debug_ramdisk/magisk su -c /data/local/tmp/deploy_<x>.sh'`
   where `deploy_<x>.sh` does `mkdir -p` + `cp` + `chown u0_a150:ext_data_rw`
   + `chmod 770` in `/sdcard/Android/data/dev.eden.eden_emulator.nightly/`
   `files/load/0100ABF008968000/<mod dir>/exefs/`.

Mods live SIDE-BY-SIDE in that `load/` dir; Eden's mod UI toggles which are
enabled per session. Do NOT enable both an old and a new candidate at the
same time — the last-written `.pchtxt` at conflicting offsets wins and
results are unpredictable.

### If iteration 3+ is needed (real RE)

Enable NSO dump reliably: patch `config.ini` on device while Eden is fully
killed (`am force-stop dev.eden.eden_emulator.nightly` under root), sed the
lines `dump_nso=false` → `dump_nso=true` (and same for `dump_exefs`),
chown back to `u0_a150:ext_data_rw`, then have Paco launch Sword to the
title screen. NSO lands at `.../files/dump/0100ABF008968000/exefs/main`
(or under a build-ID subdir). Pull with `adb pull`.

On Win5, Ghidra headless requires a stable long-running shell. The exec
tool's SSH pipe kept SIGKILLing at 15-45s; workarounds:
- run inside `tmux` on Win5 (see `tmux` skill), send-keys / capture-pane.
- `setsid nohup <cmd> </dev/null >/tmp/log 2>&1 &` and poll log with
  short `ssh` commands.
- The Sync-VM (this gateway) has faster network to GitHub for downloading
  Ghidra. Consider doing the RE here directly (aarch64 host, `python-
  capstone` for xref search over the raw NSO) instead of on Win5.

All three candidates (A / B / C) are committed to fork for reference even
if none proves to be the final ship.


## 2026-07-14 iteration 3 findings

### CRITICAL: iteration 2 briefing was wrong

The iteration 2 hand-off claimed candidates B and C on device were "functionally
identical to base" — only patching offsets `0x00607664/68`. That is FALSE.

Inspecting the on-device pchtxts directly (Eden log + `adb shell cat`):

| Candidate | 0x00607de8 | 0x00607dec | Effective aspect double top32 |
|-----------|-----------|-----------|-------------------------------|
| base 4:3 WIP | C971DCF2  | 0903E8F2  | 0x4018E38E (21:9.5 — untouched from Fl4sh 21:9 mod ancestor) |
| A         | E938CEF2  | 89FFE7F2  | 0x3FFC71C7 (16:9) |
| B         | A9AACAF2  | A9FEE7F2  | 0x3FF55555 (4:3)  |
| C         | 0900C0F2  | 09FFE7F2  | 0x3FF80000 (3:2)  |

So A / B / C are three genuinely-distinct patches of the same aspect double at
0x00607de8/dec. Base also touches that double, but re-stamps it to the
inherited 21:9.5 value.

### Why "all screenshots looked identical"

The three iteration-2 screenshots (12:57:17, 12:58:01, 12:58:31) were all taken
within 74 seconds on the SAME Eden boot, with config disabling B, C, and base.
Only candidate A was ever loaded. The Eden log confirms only A's byte strings
were applied. So Paco's report was accurate observationally: the three shots
ARE all "A". The bug was in the testing methodology, not the mod contents.

### Real bytes each candidate applies (Eden log verified for A)

```
common (all four): 0x00D93514 2C03A8F2  (culling, +0x100 shift = source 0x00D93414)
                   0x006077C4 E8FFFF17  (world branch)
                   0x00607764 69559552  (world float low16 0xAAAB -> 4:3)
                   0x00607768 49F5A772  (world float high16 0x3FAA)
                   0x0060776C 17000014  (world branch)
base only:         0x00607EE8 C971DCF2  0x00607EEC 0903E8F2   -> UI dbl = 21:9.5
A:                 0x00607EE8 E938CEF2  0x00607EEC 89FFE7F2   -> UI dbl = 16:9
B:                 0x00607EE8 A9AACAF2  0x00607EEC A9FEE7F2   -> UI dbl = 4:3
C:                 0x00607EE8 0900C0F2  0x00607EEC 09FFE7F2   -> UI dbl = 3:2
```

Note the +0x100 offset shift: source offsets in the pchtxt are
0x00607de8/dec/etc; the NSO-address form (post-header) is 0x00607EE8/EEC/etc.

### NSO extraction blocked (iteration 3 attempt)

- Base NSP and NAND update NCAs identified at
  `/sdcard/Android/data/dev.eden.eden_emulator.nightly/files/nand/user/Contents/registered/`.
  Big program NCA is `00000005/f13bc7b678b5c86998ff4e847e180142.nca` (3.08 GB).
- Small NCAs (metadata/HTML/control, 3.5 KB–968 KB) pulled cleanly to
  `~/work/pkmn-sword/nand/registered/` on Win5.
- 3 GB NCA pull failed twice: `adb pull` at ~500 KB/s stalled in D-state after
  ~256 MB, and `adb exec-out su -c cat` streamed at only ~8 KB/s. SSH to Win5
  also kept dropping (SIGTERM within 30–60 s of long-running ssh channels
  even for trivial commands during high-load windows). Sudo requires a
  password (task briefing claim of "passwordless sudo" is wrong for
  interactive use), so pacman/tmux install blocked.
- hactool source clone + build never got a stable ssh session long enough.

### Config swap helper deployed

`~/work/pkmn-sword/swap_pkmn.py A|B|C|base|none` on Win5:
- reads Eden's config.ini through magisk root cat,
- rewrites the `[DisabledAddOns]` slot-2 disabled list so exactly one Sword
  mod is enabled,
- pushes it back under the correct u0_a144:ext_data_rw owner,
- force-stops Eden so the next launch reads the new config.

Currently set to: **B** (as of 2026-07-14 ~13:30 UTC).

### Path forward (main agent should coordinate)

1. Ask Paco to boot Sword now (B enabled). Take screenshots of title menu,
   party menu, wild-battle HUD.
2. Run `python3 ~/work/pkmn-sword/swap_pkmn.py C` via a subagent, ask for
   the same three shots.
3. Run `... swap_pkmn.py A` (already-tested set), same three shots.
4. Compare 3×3 shots side by side. The one where HUD/menu backgrounds are
   least stretched / icons are least squished is the winner.
5. If none is acceptable, we've likely got a THIRD aspect site not touched
   by A/B/C — proceed to real NSO extraction, but do it on the Sync-VM
   (aarch64 host with fast GitHub), not Win5. Approach: transfer the 3 GB
   NCA VM-to-VM via `rsync` over Tailscale (much more stable than adb),
   then run hactool locally on the Sync-VM's amd/arm64 build.


## Pokémon Sword v1.3.2 (0100ABF008968000) — UI fix RESOLVED 2026-07-14

Confirmed fully working: `[4:3 + UI fix v1.3.2]`. World float at 0x00607664/68 pinned to 4:3 (from base 4:3 WIP), UI aspect double at 0x00607de8/dec pinned to 4:3 double (0x3FF5555555555555). Icon proportions natural, text natural, world natural. Verified on AYANEO Pocket S Mini / Eden nightly and field-confirmed again with battle/HUD and overworld photos on 2026-07-31. See `docs/pokemon-sword-4-3-ui-fix.md`.

Iterations:
- Candidate A: UI double = 16:9 -> text OK, icons wrong (double drives sprite X-scale).
- Candidate B: UI double = 4:3 -> WORKS.
- Candidate C: UI double = 3:2 -> not needed; B superseded.

Patch encoding for the double at 0x00607de8/dec (movk high dword of x9 via two 16-bit movk):
- 0x00607de8: `A9AACAF2` (`movk x9, #0x5555, lsl #32`)
- 0x00607dec: `A9FEE7F2` (`movk x9, #0x3FF5, lsl #48`)
