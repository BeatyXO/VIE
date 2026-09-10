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

## Deployment

- Network: GenLayer StudioNet
- Chain ID: `61999`
- Contract: `0x66A0CB4b598135270c1e8ea4F9F9DD474Cd399AF`
- Deployment transaction: `0x89564cf613e75d9572c4230e7e2b2fef3fe25052580c4c0320e2f03ae40ceee7`
- Explorer: https://explorer-studio.genlayer.com/address/0x66A0CB4b598135270c1e8ea4F9F9DD474Cd399AF

The deployed source includes real retrieval, enforced challenge deadlines, one-shot challenge reassessment, and deterministic restriction of all-failed evidence bundles to `INCONCLUSIVE` or `STALE`.

## Source parity

The deployed source was retrieved with `genlayer code`. After removing the CLI wrapper and normalizing only terminal newline/encoding formatting, the SHA-256 is identical to the submitted `contracts/impact.py` at commit `eaf91ff`:

`BAB29C7E0493DC8BBA36303C504F06712B7E2836AA3E66EDB6478F5B26A5F823`

The normalized unified diff is empty. The only raw difference was a terminal newline emitted by the CLI wrapper.

## Fresh real-validator lifecycle

Executed against the deployed contract above on 2026-09-10 using the dedicated deployer account and a real public EPA URL:

- Create claim: `0xea72a9bab498e3f27fac716aa7149e003a2935b3d080d0c45eba84b267a84c8a`
- Submit evidence: `0x04c4ab13100f1a22dd19161352d3b6a53f00efe1a8f7566d626bf61b0c7abc56`
- Real-validator assessment: `0x1a1a8f102420ed41d7ece31d41ad1b87cb56266a8b4934c235fd66f18b7197c7`
- Evidence source: `https://www.epa.gov/ghgemissions/overview-greenhouse-gases`
- Final observed status: `ASSESSED`
- Final observed verdict: `NOT_VERIFIED`
- `successful_fetch_count`: `1`

The validators independently retrieved the public EPA page and correctly rejected the claim because it did not substantiate the claimant-specific baseline-to-target measurement. The assessment was finalized on-chain with consensus agreement; the challenge window remains available for finalization.

## Fresh measured lifecycle

- Create claim: `0x6a3619cb2ce75016d940d4dc403e390a254aafa9ca34081399a23c06422850dd`
- Submit evidence: `0x8e154ea5af2d3e9e0f89fd4a6cfb80622629226590a6a05b50feec55634f0ccb`
- Real-validator assessment: `0x8065353820948796506b237522bcfbb1eaef546bfcebfee3f72a8e61eaa978de`
- Final observed state: `ASSESSED`, verdict `NOT_VERIFIED`, no verified value. Validators retrieved the public GenLayer landing page and correctly found no CO2e measurements supporting the submitted claim; challenge deadline: `2026-09-14T13:56:54Z`.
