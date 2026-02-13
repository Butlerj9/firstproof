# Claude Research Breakdown — P03 (Round 3)

Date: 2026-02-13  
Source: User-provided frontier response  
Lane: P03  
Purpose: Distill executable signal for Claude Code from the round-3 intake.

---

## 1) High-value signal

1. Keep lane status at `BLOCKED_WITH_FRONTIER`.
2. Prioritize a bounded top-3 sequence:
   - D1 BinAS,
   - D2 SMLQ,
   - D3 SSD.
3. Treat all other routes as backlog unless one of D1-D3 fails quickly.

---

## 2) Immediate execution implications

1. First run D1 kill-test on `n=3` with symbolic extraction.
2. If D1 lacks structural pattern, run D2 queue-enumeration kill-test.
3. If D2 stalls (combinatorial blowup or indeterminate weights), run D3 duality-evaluation kill-test.
4. Only escalate to `n=4/n=5` after one route passes its small-case structural gate.

---

## 3) Stop-loss carried from intake

1. Abort a route if runtime/complexity threshold is exceeded in its own kill-test.
2. Do not claim closure from numerical agreement alone.
3. If all D1-D3 fail kill-tests, return explicit frontier delta and park remaining 11 routes.

---

## 4) Checklist delta recommendation

Add to next P03 Claude Code checklist:
1. Route order fixed to D1 -> D2 -> D3.
2. Per-route stop-loss gate copied explicitly.
3. Mandatory output: one pass/fail table with failure reason and next-route trigger.

