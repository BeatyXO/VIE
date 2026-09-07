# VIE — Verifiable Impact Evidence Registry

VIE is a standalone GenLayer Intelligent Contract for publishing machine-readable attestations about measurable impact claims. A claimant commits a baseline, target, unit, measurement period, and methodology; validators independently inspect submitted public evidence and return `VERIFIED`, `PARTIAL`, `NOT_VERIFIED`, `INCONCLUSIVE`, or `STALE`.

VIE does not hold funds. Its reusable output is a versioned impact record that grant systems, sustainability programs, climate registries, and public-good reporting tools can consume.

## Lifecycle

`OPEN → EVIDENCE_SUBMITTED → ASSESSED → FINALIZED`

An independent party may challenge an assessment before finalization. The contract records evidence provenance, observed values, assessment count, challenge state, and the validator-produced verified value. It uses GenLayer consensus because the evidence may be public web material and the question is semantic: whether that evidence supports the claimed measurement without inventing data.

## Interface

- `create_impact_claim(...)` — commit a baseline, target, unit, period, methodology, and optional callback.
- `submit_impact_evidence(...)` — attach bounded source evidence and observed values.
- `assess_impact(...)` — obtain an independently checked structured impact assessment.
- `reassess_challenge(...)` — re-run assessment after an accepted challenge.
- `challenge_assessment(...)` — flag an assessment from an independent address.
- `finalize_assessment(...)` — close the challenge window.
- `get_claim(...)`, `get_evidence(...)`, `get_assessment(...)`, `stats()` — read state.

## Development

```powershell
python -m py_compile contracts/impact.py
genvm-lint check contracts/impact.py --json
pytest -q tests/direct
```

## Deployment

Live deployment: `0x82d532539c2070A9FCea8e5E2B0908b858ab2ed2` on GenLayer StudioNet (chain ID `61999`). [Studio Explorer](https://explorer-studio.genlayer.com/address/0x82d532539c2070A9FCea8e5E2B0908b858ab2ed2). Deployment transaction: `0x3a3b13baf466416c4bd5bca51447cfbb56a69929427ee5d5648dc75a03407a8f`.

The current deployment matches the one-shot challenge and retrieved-evidence source in this repository.
