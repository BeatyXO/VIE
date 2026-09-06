# VIE Submission Package

VIE is a non-financial impact-attestation registry. It records measurable claims and provenance-bearing evidence, uses GenLayer validator consensus to assess whether the evidence supports the claimed result, and exposes a final structured attestation for downstream systems.

## Trust model

The claimant supplies bounded evidence, but cannot author the attestation alone. Validators independently inspect the evidence and must agree on the stable verdict and verified value. Explanations are informative; the typed verdict controls the state transition.

## Commands

```powershell
python -m py_compile contracts/impact.py
genvm-lint check contracts/impact.py --json
pytest -q tests/direct
```

## Live deployment

- Network: GenLayer StudioNet
- Chain ID: `61999`
- Contract: `0x10A8b3B91F39b829502dDc74F579d9C18cE5b35C`
- Deployment transaction: `0x8619caa604c9391b466484dbe7c36c94f46462985bc54309aab2503f8e1d609c`
- Explorer: https://explorer-studio.genlayer.com/address/0x10A8b3B91F39b829502dDc74F579d9C18cE5b35C

## Measured lifecycle

- Create claim: `0xe9c27cd5f65992269b131449ffe9762b9fc3c39431a11c0e27da6176830feb10`
- Submit evidence: `0x57ff98b694326b40c8a82c19fabbc81999bef3a233477322c3fd7ed4aef1c1f1`
- Real-validator assessment: `0x0964aef4945e25f0d19c0047c0dd99be12c4109c1f28c6eaf7b81457983ff117`
- Final observed state: `ASSESSED`, verdict `PARTIAL`, verified value `50t`, challenge deadline `2026-09-13T07:51:26Z`.
