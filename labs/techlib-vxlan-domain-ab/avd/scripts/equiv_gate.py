#!/usr/bin/env python3
"""equiv_gate.py — on-box-equivalence refactor gate (DRY campaign).

Checks worktree renders against the golden baseline (git HEAD intended/),
classifying every changed line against equivalence_ledger.yml. Unclassified
drift fails. Also reports the data-model line scoreboard vs the 4,427
baseline. Run AFTER rebuilding all targets (or with --build).
"""
from __future__ import annotations

import argparse
import glob
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINE_LINES = 4427
TARGETS = ["DOMAIN_A_FABRIC", "DOMAIN_B_FABRIC", "BACKBONE", "DOMAIN_B_L2_SWITCHES"]

def build() -> None:
    for t in TARGETS:
        r = subprocess.run(
            ["ansible-playbook", "playbooks/build.yml", "-i", "inventory.yml",
             "-e", f"target_hosts={t}"], cwd=ROOT, capture_output=True, text=True)
        if re.search(r"failed=[1-9]", r.stdout) or r.returncode != 0:
            print(f"BUILD FAILED for {t}"); sys.exit(2)
        if "recap" not in r.stdout.lower():
            print(f"BUILD SUSPECT for {t}: no recap"); sys.exit(2)

def model_lines() -> int:
    files = [ROOT / "inventory.yml", *map(Path, glob.glob(str(ROOT / "group_vars/*.yml"))),
             *map(Path, glob.glob(str(ROOT / "host_vars/*.yml")))]
    return sum(len(f.read_text().splitlines()) for f in files if f.exists())

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    args = ap.parse_args()
    if args.build:
        build()

    import yaml
    ledger = yaml.safe_load((ROOT / "equivalence_ledger.yml").read_text())["classes"] or []
    diff = subprocess.run(["git", "diff", "--no-color", "--", "intended/configs"],
                          cwd=ROOT, capture_output=True, text=True).stdout
    hits: Counter = Counter()
    unclassified: list[str] = []
    for raw in diff.splitlines():
        if not raw or raw.startswith(("+++", "---", "@@", "diff ", "index ")):
            continue
        if raw[0] not in "+-":
            continue
        direction = "extra" if raw[0] == "+" else "missing"
        line = raw[1:].strip()
        if not line:
            continue
        for c in ledger:
            if c["direction"] == direction and re.search(c["pattern"], line):
                hits[c["id"]] += 1
                break
        else:
            unclassified.append(f"{raw[0]} {line[:90]}")

    ml = model_lines()
    print(f"scoreboard: model lines {ml} (baseline {BASELINE_LINES}, Δ {ml - BASELINE_LINES:+d})")
    if hits:
        for cid, n in hits.most_common():
            print(f"ledger[{cid}]: {n} lines")
    if unclassified:
        print(f"UNCLASSIFIED DRIFT ({len(unclassified)} lines):")
        for u in unclassified[:20]:
            print(f"  ✗ {u}")
        sys.exit(1)
    print("EQUIV GATE CLEAN" + (" — byte-zero render" if not diff.strip() else ""))

if __name__ == "__main__":
    main()
