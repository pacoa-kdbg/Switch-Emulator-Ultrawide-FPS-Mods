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

## Notes

- Method reference: <https://github.com/StevensND/ghidra-port-mods-guide>
- Aspect float constants:
  - 16:9  → `0x3fe38e39` (1.77777779)
  - 21:9  → `0x4018e38e` (approx, matches Fl4sh set)
  - 3:2   → `0x3fc00000` (1.5)
  - 4:3   → `0x3faaaaab` (1.33333333)
