# VIE Submission Package

VIE is a standalone Intelligent Contract. Its load-bearing property is consensus-backed verification of impact evidence before deterministic escrow release. External evidence is acquired inside nondeterministic execution; payout calculations and all state transitions are deterministic.

## Deployment

- Network: GenLayer StudioNet
- Chain ID: `61999`
- Contract address: `0x76aE34bF991Fd5ffA406C598B67A23C9a6edCD5a`
- Explorer: https://explorer-studio.genlayer.com/address/0x76aE34bF991Fd5ffA406C598B67A23C9a6edCD5a
- Deployment transaction: `0x3b80be3ea52cb41c8969138ef992b3d4b82bfc49fc71749670ce1d214c26954d`

The exact `contracts/vie.py` source was accepted by StudioNet deployment consensus.

## Live verification

Verification results will be recorded after the fresh deployment and funded impact lifecycle.

## Reproducible commands

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install genlayer gltest pytest
python -m py_compile contracts/vie.py
genvm-lint check contracts/vie.py --json
pytest -q tests/direct
pytest -q tests/integration/test_live_aase_cycle.py
pytest -q -s tests/integration/test_real_validator_cycle.py
```
