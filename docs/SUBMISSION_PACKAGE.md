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

## Previous deployment

- Network: GenLayer StudioNet
- Chain ID: `61999`
- Contract: `0x82d532539c2070A9FCea8e5E2B0908b858ab2ed2`
- Deployment transaction: `0x3a3b13baf466416c4bd5bca51447cfbb56a69929427ee5d5648dc75a03407a8f`
- Explorer: https://explorer-studio.genlayer.com/address/0x82d532539c2070A9FCea8e5E2B0908b858ab2ed2

The deployed source includes real retrieval, enforced challenge deadlines, and one-shot challenge reassessment.

## Fresh measured lifecycle

- Create claim: `0x6a3619cb2ce75016d940d4dc403e390a254aafa9ca34081399a23c06422850dd`
- Submit evidence: `0x8e154ea5af2d3e9e0f89fd4a6cfb80622629226590a6a05b50feec55634f0ccb`
- Real-validator assessment: `0x8065353820948796506b237522bcfbb1eaef546bfcebfee3f72a8e61eaa978de`
- Final observed state: `ASSESSED`, verdict `NOT_VERIFIED`, no verified value. Validators retrieved the public GenLayer landing page and correctly found no CO2e measurements supporting the submitted claim; challenge deadline: `2026-09-14T13:56:54Z`.
