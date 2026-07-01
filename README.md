# Beast Tamer

**Reis' Dragonkin abilities work on ALL monsters — not just Dragons and Hydras.**

A tiny data-only mod for **FINAL FANTASY TACTICS - The Ivalice Chronicles** (Steam, Enhanced),
built on [Nenkai's mod loader](https://github.com/Nenkai/fftivc.utility.modloader) (Reloaded-II).

## What it does

In vanilla, four of Reis' Dragonkin abilities silently force a MISS on any target whose
sprite family is not Dragon or Hydra (the classic "Dragon Check"). This mod removes that
restriction:

| Ability | Vanilla | With Beast Tamer |
|---|---|---|
| **Dragon's Charm** | Charms a Dragon/Hydra (100%) | Charms any target (~PA+100%) |
| **Dragon's Gift** | Sacrifice 20% max HP, heal a Dragon 2x that + cure ailments | Same heal, any target (ailment-cure rider is lost) |
| **Dragon's Might** | +5 Bravery, +2 PA/MA/Speed to a Dragon | Identical, any target |
| **Dragon's Speed** | Grant a Dragon an immediate turn (Quick) | Same, any target (hit ~F(MA+255)%, scales with Faith) |

The three breath attacks and Holy Breath were never dragon-gated and are untouched.

## Honest fine print

- The restriction is removed entirely, so the abilities also work on **humans**, not just
  monsters. Dragon's Charm on a human is strong; treat it as a fun/utility mod, not a
  balance mod.
- Dragon's Gift keeps its exact heal math but no longer cures status ailments.
- Dragon's Charm/Speed now roll normal hit formulas ((PA+100)% and Faith-scaled
  respectively) instead of a flat 100%, so a rare miss is possible.

## How it works (tech)

The dragon check is hardcoded inside formula routines `0x5A-0x5D` in the game exe
(virtualized, not patchable in data). Each wrapper just runs the check and then calls a
generic routine that other formula ids expose directly. Beast Tamer re-points the four
abilities to those check-free formulas via the `OverrideAbilityActionData` Nex table
(4 rows, a handful of cells; everything else inherits vanilla):

```text
251 Dragon's Charm  Formula 0x5A -> 0x33 (Hit_(PA+X)% + inflict status), X=100
252 Dragon's Gift   Formula 0x5B -> 0x3C (Wish: caster -20% MaxHP, target +2x that)
253 Dragon's Might  Formula 0x5C -> 0x3B (Scream on target: Brave+X, PA/MA/SP+Y) [identical math]
254 Dragon's Speed  Formula 0x5D -> 0x12 (Hit_F(MA+X)% Set_Quick), X=255
```

Sources: FFHacktics [Dragon_Check](https://ffhacktics.com/wiki/Dragon_Check), the
[FFT PSX decomp](https://github.com/Talcall/FFT-1997-Decomp), and
[FFTPatcher](https://github.com/Glain/FFTPatcher) WotL baseline data.

## Install

1. Install [Reloaded-II](https://github.com/Reloaded-Project/Reloaded-II) and
   [fftivc.utility.modloader](https://github.com/Nenkai/fftivc.utility.modloader).
2. Copy `mod/fftivc.beasttamer` into your `Reloaded-II/Mods/` folder
   (or install the packaged zip via Reloaded).
3. Enable **Beast Tamer** for FFT_enhanced.exe and launch via Reloaded.

## Build from source

```text
python tools/build_data.py --build-nxd   # needs FF16Tools.CLI
.\deploy.ps1                             # copy to Reloaded-II/Mods
```

`data/override_ability.base.sqlite` is the vanilla `OverrideAbilityActionData` table
extracted from the game (all cells `-1` = inherit); the build script edits only the four
rows above and rebuilds the NXD.
