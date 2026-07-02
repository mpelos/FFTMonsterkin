#!/usr/bin/env python3
"""Build the Monsterkin ability text patch (English): rename Reis' four Dragonkin
support abilities to Monster's Charm/Gift/Might/Speed and fix their descriptions to
say "monster" instead of "dragon or hydra type" (the mod widens the species gate to
all wild monsters, so the vanilla text would lie).

Ships as a full ability.en.nxd; the mod loader diffs it against vanilla and applies
only the changed cells, so it composes with other text mods.

Usage: python tools/build_names.py [--ff16tools PATH]
"""
from __future__ import annotations

import argparse
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BASE = REPO / "data/ability_en.base.sqlite"
OUT_SQLITE = REPO / "work/ability_en.monsterkin.sqlite"
NXD_DIR = REPO / "mod/ffttic.monsterkin/FFTIVC/data/enhanced/nxd"
DEFAULT_FF16TOOLS = Path(
    r"D:/Projects/FFTModNewGame++/tools/FF16Tools.CLI-1.13.2-win-x64/win-x64/FF16Tools.CLI.exe"
)

TEXTS: dict[int, tuple[str, str]] = {
    251: (
        "Monster's Charm",
        "Communicates mentally in a way perceivable only by beasts to persuade a "
        "distant monster to become an ally. At the end of battle, that unit will "
        "officially join your party.",
    ),
    252: (
        "Monster's Gift",
        "Manifests draconic power to forfeit one's HP to restore HP to a distant "
        "monster and remove its status ailments.",
    ),
    253: (
        "Monster's Might",
        "Manifests draconic power to increase the bravery, speed, and physical and "
        "magickal attack power of a distant monster for the duration of battle.",
    ),
    254: (
        "Monster's Speed",
        "Manifests draconic power to warp time, allowing the next turn of a distant "
        "monster to come immediately.",
    ),
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ff16tools", type=Path, default=DEFAULT_FF16TOOLS)
    args = ap.parse_args()

    if not BASE.exists():
        sys.exit(f"ERROR: base sqlite missing: {BASE}")
    OUT_SQLITE.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(BASE, OUT_SQLITE)
    con = sqlite3.connect(OUT_SQLITE)
    cur = con.cursor()
    for key, (name, desc) in TEXTS.items():
        n = cur.execute(
            'UPDATE "Ability-en" SET Name=?, Description=? WHERE Key=?', (name, desc, key)
        ).rowcount
        if n != 1:
            sys.exit(f"ERROR: ability {key} not updated (rowcount {n})")
    con.commit()
    for row in cur.execute('SELECT Key, Name FROM "Ability-en" WHERE Key IN (251,252,253,254)'):
        print(f"  {row[0]}: {row[1]}")
    con.close()

    if not args.ff16tools.exists():
        sys.exit(f"ERROR: FF16Tools CLI not found: {args.ff16tools}")
    NXD_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(args.ff16tools), "sqlite-to-nxd",
        "-i", str(OUT_SQLITE),
        "-o", str(NXD_DIR),
        "-g", "fft",
        "-t", "Ability-en",
    ]
    print("[monsterkin] building ability.en NXD:")
    print("  " + " ".join(f'"{p}"' if " " in p else p for p in cmd))
    subprocess.run(cmd, check=True)
    nxd = NXD_DIR / "ability.en.nxd"
    if not nxd.exists() or nxd.stat().st_size == 0:
        sys.exit(f"ERROR: expected NXD not produced: {nxd}")
    print(f"[monsterkin] NXD written: {nxd}")


if __name__ == "__main__":
    main()
