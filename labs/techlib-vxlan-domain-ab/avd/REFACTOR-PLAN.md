# Data-Model Refactor Plan — the DRY campaign

**Mission:** same fabric, minimum data-model lines. Reviewer feedback on the
released Domain A/B models: too much duplication (repetitive host_vars, etc.).

**Contract (decided):** ON-BOX EQUIVALENCE — renders may drift from the
byte-exact parity baseline when the running-config outcome is identical,
verified two-tier:
- **Tier 1 (every rev, sandbox):** `scripts/equiv_gate.py` — rebuild, diff
  `intended/` against golden (HEAD at refactor start), classify every changed
  line against `equivalence_ledger.yml`. Unclassified drift = FAIL.
- **Tier 2 (per milestone, lab):** deploy + full ANTA suite green + per-node
  `show run` diff within the ledger's on-box expectations.

**Baseline (2026-07-28):** 4,427 raw lines / 26 files
(inventory 97, group_vars 3,579 × 8, host_vars 751 × 17).
Golden render = commit `47012c7` `intended/configs/`.

## Census highlights (what the duplication actually is)
- `custom_structured_configuration_router_multicast: {}` shadow ×17 host files
- 34 eos_cli blocks (102 lines), 18 identical dupes; near-dupes differ only in
  mld vlan lists / vrf sets
- ~238 hoistable duplicate instances across group_vars (B-pod anchor triplets)
- 51 `structured_config` drops

## Passes (one class per commit, single-variable revs, gate every rev)
- **P0 ✓ (this commit): probe relocation** — fleet router-multicast probe moves
  from all.yml to its actual consumers (spine groups + BACKBONE inventory
  vars); all 17 host shadows deleted. Byte-zero.
- **P1: eos_cli parameterization** — one Jinja-templated
  `custom_structured_configuration_eos_cli` per leaf group; per-host deltas
  (mld vlans, vrf sets) become 1-line vars. Est −250 to −350.
- **P2: B-pod anchor consolidation** — shared payload of csc_b_pod1/2/3
  extracted (YAML anchors / group-level CSC), per-pod deltas stay. Est −200+.
- **P3: dead-pin audit** — parity pins added mid-campaign, one class at a
  time; gate decides survivors.
- **P4: derivation over enumeration** — formulaic per-node values → AVD
  pool/offset knobs or Jinja.
- **P5 (contract-unlocked): cosmetic machinery deletion** — switchport
  dialect nulls, ordering pins, default-suppression probes (candidate: delete
  the router-multicast probe entirely and ledger the `software forwarding`
  line — needs a live default-behavior check first).

## Scoreboard log
| Pass | Commit | Model lines | Δ | Ledger classes |
|---|---|---|---|---|
| baseline | 47012c7 | 4,427 | — | 0 |
| P0 probe relocation | (this) | 4,376 | −51 | 0 (byte-zero) |

## Claude Code bootstrap (the marathon runs there)
1. Clone aclabs (branch `techlib-avd-update`) + adventures-with-claude; read
   HANDOFF → DISCIPLINES → STATE.
2. Read this file + `equivalence_ledger.yml`.
3. Loop: pick next class → single-variable rev → `python3
   scripts/equiv_gate.py` → commit with per-class accounting → update
   scoreboard here.
4. Tier-2 milestone after P1/P2 and again at campaign end.
