#!/usr/bin/env python3
"""Build the Beast Tamer data mod: re-point Reis' four Dragonkin support abilities to
check-free formula routines so they work on every unit, not only Dragons/Hydras.

Why re-pointing works (offline RE, PSX decomp + FFHacktics Dragon_Check + WotL data):
  The dragon restriction is NOT a data flag. Formulas 0x5A-0x5D are thin wrappers that
  run a "Dragon Check" (target monster-graphic must be 15/Dragon or 16/Hydra -> else
  force miss) and then call a GENERIC routine that other formulas expose directly:
    0x5A Dragon's Charm  = check + InflictStatus        -> 0x33 Hit_(PA+X)% + status
    0x5B Dragon's Gift   = check + Wish + status-cancel -> 0x3C Wish (exact core math)
    0x5C Dragon's Might  = check + Scream               -> 0x3B Scream (IDENTICAL math)
    0x5D Dragon's Speed  = check + Set_Quick            -> 0x12 Hit_F(MA+X)% Set_Quick
  In IVC the check lives inside the Denuvo-virtualized formula code (confirmed by scan:
  no real-code job/graphic range compare), so the data-side Formula re-point is the
  clean, DLL-free way to bypass it.

Known behavior deltas vs vanilla (documented in README):
  - All four abilities now work on ANY unit (humans included), not just monsters.
  - Dragon's Gift loses the cure-ailments rider (heal math itself is exact: caster pays
    20% MaxHP, target heals 2x that).
  - Dragon's Charm rolls Hit_(PA+X)% (X=100 -> effectively guaranteed, vanilla was 100%).
  - Dragon's Speed rolls Hit_F(MA+X)% (X=255 -> near-guaranteed, scales with Faith;
    vanilla was flat 100%).

Usage:
    python tools/build_data.py            # writes work sqlite + prints FF16Tools cmd
    python tools/build_data.py --build-nxd
"""
from __future__ import annotations

import argparse
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BASE_SQLITE = REPO / "data/override_ability.base.sqlite"
OUT_SQLITE = REPO / "work/override_ability.beasttamer.sqlite"
NXD_OUT = REPO / "mod/ffttic.monsterkin/FFTIVC/data/enhanced/nxd/overrideabilityactiondata.nxd"
DEFAULT_FF16TOOLS = Path(
    r"D:/Projects/FFTModNewGame++/tools/FF16Tools.CLI-1.13.2-win-x64/win-x64/FF16Tools.CLI.exe"
)

# ability id -> {column: value}; every untouched column stays -1 (inherit exe base)
REPOINTS: dict[int, dict[str, int]] = {
    251: {"Formula": 0x33, "X": 100},  # Dragon's Charm: Hit_(PA+X)% + InflictStatus(63=Charm inherit)
    252: {"Formula": 0x3C},            # Dragon's Gift: Wish math (heal 40% caster MaxHP, caster pays 20%)
    253: {"Formula": 0x3B},            # Dragon's Might: Scream on target (Brave+X, PA/MA/SP+Y; X=5 Y=2 inherit)
    254: {"Formula": 0x12, "X": 255},  # Dragon's Speed: Hit_F(MA+X)% Set_Quick
}


def build_sqlite() -> None:
    if not BASE_SQLITE.exists():
        sys.exit(f"ERROR: base sqlite missing: {BASE_SQLITE}")
    OUT_SQLITE.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(BASE_SQLITE, OUT_SQLITE)
    con = sqlite3.connect(OUT_SQLITE)
    cur = con.cursor()
    for key, cols in REPOINTS.items():
        row = cur.execute(
            "SELECT COUNT(*) FROM OverrideAbilityActionData WHERE Key=?", (key,)
        ).fetchone()
        if row[0] != 1:
            sys.exit(f"ERROR: ability {key} not present exactly once in base table")
        sets = ", ".join(f"{c}=?" for c in cols)
        cur.execute(
            f"UPDATE OverrideAbilityActionData SET {sets} WHERE Key=?",
            [*cols.values(), key],
        )
    con.commit()
    for row in cur.execute(
        "SELECT Key, Formula, X, Y FROM OverrideAbilityActionData WHERE Key IN (251,252,253,254)"
    ):
        print(f"  row {row[0]}: Formula={row[1]} (0x{row[1]:02X}) X={row[2]} Y={row[3]}")
    con.close()
    print(f"[beasttamer] sqlite written: {OUT_SQLITE}")


def build_nxd(ff16tools: Path) -> None:
    if not ff16tools.exists():
        sys.exit(f"ERROR: FF16Tools CLI not found: {ff16tools}")
    NXD_OUT.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(ff16tools), "sqlite-to-nxd",
        "-i", str(OUT_SQLITE),
        "-o", str(NXD_OUT.parent),
        "-g", "fft",
        "-t", "OverrideAbilityActionData",
    ]
    print("[beasttamer] building NXD:")
    print("  " + " ".join(f'"{p}"' if " " in p else p for p in cmd))
    subprocess.run(cmd, check=True)
    if not NXD_OUT.exists() or NXD_OUT.stat().st_size == 0:
        sys.exit(f"ERROR: FF16Tools did not produce a non-empty NXD: {NXD_OUT}")
    print(f"[beasttamer] NXD written: {NXD_OUT}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Build Beast Tamer OverrideAbilityActionData NXD.")
    ap.add_argument("--build-nxd", action="store_true")
    ap.add_argument("--ff16tools", type=Path, default=DEFAULT_FF16TOOLS)
    args = ap.parse_args()
    build_sqlite()
    if args.build_nxd:
        build_nxd(args.ff16tools)
    else:
        print("[beasttamer] NEXT: python tools/build_data.py --build-nxd")


if __name__ == "__main__":
    main()
