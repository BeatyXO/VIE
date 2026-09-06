from pathlib import Path

CONTRACT = str(Path(__file__).parents[2] / "contracts" / "impact.py")
ZERO = "0x0000000000000000000000000000000000000000"


def test_impact_claim_records_baseline_and_target(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy(CONTRACT)
    direct_vm.sender = direct_alice
    claim_id = contract.create_impact_claim("100 tonnes", "50 tonnes", "tonnes CO2e", "2026", "metered methodology", ZERO)
    assert claim_id == 1
    assert '"status": "OPEN"' in contract.get_claim(claim_id)


def test_only_claimant_can_submit_impact_evidence(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = direct_deploy(CONTRACT)
    direct_vm.sender = direct_alice
    claim_id = contract.create_impact_claim("100", "50", "units", "2026", "metered", ZERO)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only claimant"):
        contract.submit_impact_evidence(claim_id, "REPORT", "https://example.com/report", "50", "source")
