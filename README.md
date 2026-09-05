# VIE — Verifiable Impact Escrow

VIE is a standalone GenLayer Intelligent Contract primitive for releasing impact funding only when validator consensus confirms that submitted evidence demonstrates a predefined, measurable impact. Sponsors fund an impact commitment, providers submit bounded evidence, and validators independently assess the result.

## Live deployment

- Network: GenLayer StudioNet
- Chain ID: `61999`
- Contract: `0x76aE34bF991Fd5ffA406C598B67A23C9a6edCD5a`
- [Open VIE in Studio Explorer](https://explorer-studio.genlayer.com/address/0x76aE34bF991Fd5ffA406C598B67A23C9a6edCD5a)
- Deployment transaction: `0x3b80be3ea52cb41c8969138ef992b3d4b82bfc49fc71749670ce1d214c26954d`

The exact source in `contracts/aase.py` was deployed successfully to StudioNet. The deployment transaction was accepted with a one-round majority consensus result and five revealed validator votes.

Validators independently acquire public evidence, attach visual evidence to vision-capable model calls, and return a structured verdict. Deterministic contract code handles the state machine, weighted deliverables, partial payout calculation, timeout recovery, bonds, fees, cancellation, callbacks, bilateral settlement, and zero-before-transfer escrow safety.

VIE is reusable for grants, climate and sustainability commitments, public-good milestones, community programs, and outcome-based funding. It is intentionally contract-only: downstream applications can consume its machine-readable verdict and payout state without trusting a backend operator.

## Interface

- `create_service_intent(...)` — create and fund an agent service intent.
- `add_agent_bond(...)` — post an optional agent bond.
- `submit_agent_evidence(...)` — submit bounded work evidence.
- `resolve(...)` — run validator consensus and settle.
- `timeout_refund(...)`, `cancel_before_evidence(...)` — recovery paths.
- `accept_mutual_agent_settlement(...)` — bilateral split after inconclusive review.

## Documentation basis

https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle

https://docs.genlayer.com/developers/intelligent-contracts/features/web-access

https://docs.genlayer.com/developers/intelligent-contracts/features/image-processing

https://skills.genlayer.com/
