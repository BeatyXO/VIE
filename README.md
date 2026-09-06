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

Live deployment: `0x10A8b3B91F39b829502dDc74F579d9C18cE5b35C` on GenLayer StudioNet (chain ID `61999`). [Studio Explorer](https://explorer-studio.genlayer.com/address/0x10A8b3B91F39b829502dDc74F579d9C18cE5b35C). Deployment transaction: `0x8619caa604c9391b466484dbe7c36c94f46462985bc54309aab2503f8e1d609c`.

Live lifecycle: create `0xe9c27cd5f65992269b131449ffe9762b9fc3c39431a11c0e27da6176830feb10`; evidence `0x57ff98b694326b40c8a82c19fabbc81999bef3a233477322c3fd7ed4aef1c1f1`; successful real-validator assessment `0x0964aef4945e25f0d19c0047c0dd99be12c4109c1f28c6eaf7b81457983ff117`. Result: `PARTIAL`, verified value `50t`, with a seven-day challenge window.
