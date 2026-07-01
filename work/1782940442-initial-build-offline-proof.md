# Beast Tamer — initial build + offline proof

Investigation chain (all offline, no live data needed):

1. **Dragon Check semantics** (FFHacktics wiki + Talcall/FFT-1997-Decomp):
   `FUN_BATTLE_BIN__801875bc` reads target Graphic (+0x15E PSX), passes only 15 (Dragon)
   / 16 (Hydra), else force-miss. Called ONLY by formula wrappers 0x5A-0x5D.
2. **IVC data mirrors PSX exactly**: JobData MonsterGraphic 1..16, dragons=15, hydras=16
   (baseline_jobs.csv, FFTGenericChronicle).
3. **WotL base ability data** (FFTPatcher PSP/bin/Abilities.bin, layout 0x1000+14*i):
   251=0x5A st63, 252=0x5B st94, 253=0x5C X5 Y2, 254=0x5D. Quick spell (41) = formula
   0x12 X140 — the check-free Set_Quick.
4. **Decomp wrapper equivalences**: 0x5C = check + _B_Scream(0x3B) → re-point is
   mathematically identical. 0x5B = check + _C_Wish(0x3C) + status-cancel rider.
   0x5A = check + 100% + InflictStatus → 0x33 (Stigma pipeline + InflictStatus).
   0x5D = check + Set_Quick → 0x12 (faith-rolled Set_Quick).
5. **IVC exe scan** (disasm_dragon_check.py/2.py, capstone over .xcode real code
   < 0x610000): NO real-code graphic/job range compare → check is inside Denuvo VM →
   byte-patch route dead, data re-point route chosen.

Build: tools/build_data.py --build-nxd → overrideabilityactiondata.nxd.
Round-trip verified (nxd-to-sqlite): 368 rows, exactly 4 Formula overrides
(251→51, 252→60, 253→59, 254→18) + 2 X overrides (251 X=100, 254 X=255).

Live gate (pending): confirm in-game that Dragon's Might applies +Brave/+PA/MA/SP to a
non-dragon monster (vanilla = forced miss). Then Charm/Gift/Speed spot-checks.
