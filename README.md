# Monsterkin

**Reis' Dragonkin abilities become Monster's Charm / Gift / Might / Speed — and work on ALL monsters, not just Dragons and Hydras.**

A tiny data-only mod for **FINAL FANTASY TACTICS - The Ivalice Chronicles** (Steam, Enhanced),
built on [Nenkai's mod loader](https://github.com/Nenkai/fftivc.utility.modloader) (Reloaded-II).

## What it does

In vanilla, four of Reis' Dragonkin abilities silently force a MISS on any target that is
not a Dragon or Hydra (the classic "Dragon Check"). With Beast Tamer, every wild monster
species qualifies:

| Ability | Vanilla | With Beast Tamer |
|---|---|---|
| **Monster's Charm** (Dragon's Charm) | Charms a Dragon/Hydra (100%); it joins your party after battle | Same, any monster |
| **Monster's Gift** (Dragon's Gift) | Sacrifice HP, heal a Dragon 2x that + cure ailments | Same, any monster |
| **Monster's Might** (Dragon's Might) | +5 Bravery, +2 PA/MA/Speed to a Dragon | Same, any monster |
| **Monster's Speed** (Dragon's Speed) | Grant a Dragon an immediate turn (Quick) | Same, any monster |

- **Humans stay excluded** — the vanilla species gate still applies to them.
- **Exact vanilla behavior**: same 100% rates, same effects, same status-cure rider on
  Dragon's Gift. Nothing about the abilities themselves is altered.
- Covered species: all 14 wild families (Chocobo, Goblin, Bomb, Panther, Squid, Skeleton,
  Ghoul, Ahriman, Aevis, Pig, Treant, Minotaur, Malboro, Behemoth) plus their special
  encounter variants. Dragons/Hydras work as always. Story/unique monsters (Byblos,
  Automaton, Lucavi) are intentionally not included.
- The four abilities are renamed in-game (English) to match their new reach, with
  updated descriptions.
- The three breath attacks and Holy Breath were never dragon-gated and are untouched.

## How it works (tech)

The Dragon Check lives inside the game's (Denuvo-virtualized) formula code, so it cannot
be byte-patched — but it *reads data*: the target species' `MonsterGraphic` id from the
hardcoded JobData table (15 = Dragon family, 16 = Hydra family pass; everything else
force-misses). Rendering resolves sprites through a different path and never reads this
field in gameplay (its only consumer is the check — verified against the PSX decomp and
proven in-game).

Monsterkin simply sets `MonsterGraphic = 15` for the 47 generic monster jobs via a
TableData `JobData.xml` patch (one field per job; everything else inherits vanilla).
Humans keep `MonsterGraphic = 0` and remain blocked.

Sources: FFHacktics [Dragon_Check](https://ffhacktics.com/wiki/Dragon_Check), the
[FFT PSX decomp](https://github.com/Talcall/FFT-1997-Decomp), and
[FFTPatcher](https://github.com/Glain/FFTPatcher) WotL baseline data.

## Install

1. Install [Reloaded-II](https://github.com/Reloaded-Project/Reloaded-II) and
   [fftivc.utility.modloader](https://github.com/Nenkai/fftivc.utility.modloader).
2. Copy `mod/fftivc.monsterkin` into your `Reloaded-II/Mods/` folder
   (or install the packaged zip via Reloaded).
3. Enable **Monsterkin** for FFT_enhanced.exe and launch via Reloaded.

## Variant: "any target" (v1.0 formula re-point)

An alternate flavor from this repo's history (tag `v1.0`): instead of widening the species
gate, it re-points the four abilities to check-free formula routines
(`0x33/0x3C/0x3B/0x12` via `OverrideAbilityActionData`), which makes them work on
**every unit including humans** (with small behavior deltas: Gift loses its ailment-cure
rider, Charm/Speed roll real hit formulas instead of flat 100%). Use one variant or the
other, not both.

## Build from source

```text
python tools/build_jobdata.py   # regenerates the JobData.xml patch from vanilla data
python tools/build_names.py     # rebuilds the renamed ability text NXD (needs FF16Tools.CLI)
.\deploy.ps1                    # copy to Reloaded-II/Mods
```

`tools/build_data.py` builds the v1.0 "any target" NXD variant instead.
