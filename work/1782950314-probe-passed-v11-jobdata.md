# PROBE PASSED — Dragon Check consumes JobData.MonsterGraphic (live decisive test)

User test, vanilla formulas (Beast Tamer main OFF) + TestKit + probe (goblins 97-99
MonsterGraphic=15):

- Dragon's Might on a GOBLIN: WORKED ("funcionou perfeitamente") - appearance normal.
- Dragon's Might on a SKELETON (graphic 6, unpatched): blocked (control PASS).
- Dragon's Might on a HUMAN: blocked (control PASS).

PROVES: the IVC Dragon Check's species input is JobData.MonsterGraphic (boot-time table
patch reaches ENTD-spawned battle units), and neither rendering nor other gameplay is
affected by the value. Note: this test cannot distinguish "VM reads table per-action" vs
"copied to unit at spawn" (boot patch precedes both); irrelevant for the mod.

v1.1 SHIPPED ARCHITECTURE (pure data, replaces the v1.0 re-point):
- JobData.xml: MonsterGraphic=15 on the 47 generic monster jobs (94-135 + variants
  169-173, selected by vanilla graphic 1..14). Humans (0) excluded; dragons/hydras
  (15/16) already pass; story monsters (graphic 0) intentionally excluded.
- overrideabilityactiondata.nxd REMOVED from the package (formulas back to vanilla
  0x5A-0x5D: Gift keeps cleanse, Charm/Speed flat 100%, monsters-only semantics).
- v1.0 re-point kept in history as the "any target" variant.

Final validation queued: with v1.1 deployed, Might on a SKELETON should now WORK,
human still blocked, chocobo works, goblin works (probe now redundant, disable it).
