# FINAL VALIDATION PASSED — v1.1.0 (user in-game test)

Setup: Beast Tamer v1.1.0 + TestKit ON; probe/Generic Chronicle OFF.

- Dragon's Might on THREE different monster species: ALL WORKED.
- Dragon's Might on a human: BLOCKED (vanilla Dragon Check active for graphic=0).

The shipped mechanism (JobData.MonsterGraphic=15 on the 47 generic monster jobs,
vanilla formulas untouched) delivers the exact requested semantics: all wild
monsters, humans excluded, vanilla behavior preserved. Project goal reached.

Release artifact: release/BeastTamer-v1.1.0.zip (TestKit is NOT part of the release).
