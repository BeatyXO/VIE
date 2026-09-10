# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json
from datetime import datetime, timedelta, timezone

STATUS_OPEN = "OPEN"
STATUS_EVIDENCE_SUBMITTED = "EVIDENCE_SUBMITTED"
STATUS_ASSESSED = "ASSESSED"
STATUS_FINALIZED = "FINALIZED"
STATUS_CHALLENGED = "CHALLENGED"
VERIFIED = "VERIFIED"
PARTIAL = "PARTIAL"
NOT_VERIFIED = "NOT_VERIFIED"
INCONCLUSIVE = "INCONCLUSIVE"
STALE = "STALE"
MAX_TEXT = 2800
MAX_EVIDENCE = 6
MAX_FETCHED_BODY = 12000
MAX_CLAIMS = 8
CHALLENGE_SECONDS = 60 * 60 * 24 * 7


@gl.contract_interface
class IImpactConsumer:
    class View:
        pass
    class Write:
        def on_impact_attested(self, claim_id: u256, status: str, verified_value: str) -> None:
            pass


class VerifiableImpactRegistry(gl.Contract):
    owner: Address
    next_claim_id: u256
    claims: TreeMap[str, str]
    records: TreeMap[str, str]

    def __init__(self) -> None:
        self.owner = gl.message.sender_address
        self.next_claim_id = u256(1)
        self.claims = TreeMap[str, str]()
        self.records = TreeMap[str, str]()

    @gl.public.write
    def create_impact_claim(self, baseline: str, target: str, unit: str, period: str, methodology: str, callback: Address) -> u256:
        if len(baseline) == 0 or len(baseline) > MAX_TEXT or len(target) == 0 or len(target) > MAX_TEXT:
            raise gl.vm.UserError("EXPECTED: baseline and target required")
        if len(unit) == 0 or len(unit) > 80 or len(period) == 0 or len(period) > 180:
            raise gl.vm.UserError("EXPECTED: invalid measurement fields")
        if len(methodology) == 0 or len(methodology) > MAX_TEXT:
            raise gl.vm.UserError("EXPECTED: methodology required")
        claim_id = self.next_claim_id
        self.next_claim_id = self.next_claim_id + u256(1)
        self.claims[self._key(claim_id)] = json.dumps({
            "claimant": str(gl.message.sender_address), "baseline": baseline, "target": target,
            "unit": unit, "period": period, "methodology": methodology, "callback": str(callback),
            "status": STATUS_OPEN, "verdict": INCONCLUSIVE, "verified_value": "",
            "reason": "", "evidence_count": 0, "assessment_count": 0, "challenged": False,
            "challenge_deadline": "", "finalized": False,
            "challenge_count": 0,
        })
        return claim_id

    @gl.public.write
    def submit_impact_evidence(self, claim_id: u256, kind: str, source: str, observed_value: str, notes: str) -> None:
        rec = self._claim(claim_id)
        if gl.message.sender_address != Address(rec["claimant"]):
            raise gl.vm.UserError("EXPECTED: only claimant can submit evidence")
        if rec["status"] not in (STATUS_OPEN, STATUS_EVIDENCE_SUBMITTED):
            raise gl.vm.UserError("EXPECTED: claim not accepting evidence")
        if len(kind) == 0 or len(kind) > 40 or len(source) == 0 or len(source) > MAX_TEXT or len(observed_value) > 300 or len(notes) > 700:
            raise gl.vm.UserError("EXPECTED: invalid evidence")
        count = int(rec["evidence_count"])
        if count >= MAX_EVIDENCE:
            raise gl.vm.UserError("EXPECTED: evidence cap reached")
        self.records[self._evidence_key(claim_id, count)] = json.dumps({"kind": kind.strip().upper(), "source": source, "observed_value": observed_value, "notes": notes, "submitted_at": gl.message_raw["datetime"], "submitter": str(gl.message.sender_address)})
        rec["evidence_count"] = count + 1
        rec["status"] = STATUS_EVIDENCE_SUBMITTED
        self._write(claim_id, rec)

    @gl.public.write
    def assess_impact(self, claim_id: u256) -> None:
        rec = self._claim(claim_id)
        if rec["status"] != STATUS_EVIDENCE_SUBMITTED:
            raise gl.vm.UserError("EXPECTED: evidence required")
        bundle = self._bundle(claim_id, int(rec["evidence_count"]))
        result = self._judge(rec, bundle)
        rec["verdict"] = result["verdict"]
        rec["verified_value"] = result["verified_value"]
        rec["reason"] = result["reason"]
        rec["assessment_count"] = int(rec["assessment_count"]) + 1
        rec["status"] = STATUS_ASSESSED
        rec["challenge_deadline"] = self._add_days(gl.message_raw["datetime"], 7)
        self.records[self._assessment_key(claim_id)] = json.dumps(result)
        self._write(claim_id, rec)

    @gl.public.write
    def challenge_assessment(self, claim_id: u256, reason: str) -> None:
        rec = self._claim(claim_id)
        if gl.message.sender_address == Address(rec["claimant"]):
            raise gl.vm.UserError("EXPECTED: independent challenger required")
        if rec["status"] != STATUS_ASSESSED or int(rec.get("challenge_count", 0)) >= 1 or len(reason) == 0 or len(reason) > 900:
            raise gl.vm.UserError("EXPECTED: assessment not challengeable")
        if self._after(gl.message_raw["datetime"], str(rec["challenge_deadline"])):
            raise gl.vm.UserError("EXPECTED: challenge window expired")
        rec["challenged"] = True
        rec["challenge_count"] = int(rec.get("challenge_count", 0)) + 1
        rec["status"] = STATUS_CHALLENGED
        rec["reason"] = reason
        self._write(claim_id, rec)

    @gl.public.write
    def reassess_challenge(self, claim_id: u256) -> None:
        rec = self._claim(claim_id)
        if rec["status"] != STATUS_CHALLENGED:
            raise gl.vm.UserError("EXPECTED: challenge required")
        result = self._judge(rec, self._bundle(claim_id, int(rec["evidence_count"])))
        rec["verdict"] = result["verdict"]
        rec["verified_value"] = result["verified_value"]
        rec["reason"] = result["reason"]
        rec["assessment_count"] = int(rec["assessment_count"]) + 1
        rec["status"] = STATUS_ASSESSED
        rec["challenged"] = False
        rec["challenge_deadline"] = gl.message_raw["datetime"]
        self.records[self._assessment_key(claim_id)] = json.dumps(result)
        self._write(claim_id, rec)

    @gl.public.write
    def finalize_assessment(self, claim_id: u256) -> None:
        rec = self._claim(claim_id)
        if rec["status"] != STATUS_ASSESSED:
            raise gl.vm.UserError("EXPECTED: assessment required")
        if int(rec.get("challenge_count", 0)) == 0 and self._after(str(rec["challenge_deadline"]), gl.message_raw["datetime"]):
            raise gl.vm.UserError("EXPECTED: challenge window active")
        rec["status"] = STATUS_FINALIZED
        rec["finalized"] = True
        self._write(claim_id, rec)
        callback = Address(rec["callback"])
        if str(callback) != "0x0000000000000000000000000000000000000000":
            IImpactConsumer(callback).emit(on="finalized").on_impact_attested(claim_id, rec["verdict"], rec["verified_value"])

    @gl.public.view
    def get_claim(self, claim_id: u256) -> str:
        return json.dumps(self._claim(claim_id))

    @gl.public.view
    def get_evidence(self, claim_id: u256, index: u32) -> str:
        return self.records[self._evidence_key(claim_id, int(index))]

    @gl.public.view
    def get_assessment(self, claim_id: u256) -> str:
        return self.records.get(self._assessment_key(claim_id), json.dumps({"verdict": INCONCLUSIVE}))

    @gl.public.view
    def stats(self) -> str:
        return json.dumps({"next_claim_id": str(self.next_claim_id)})

    def _judge(self, rec: dict, bundle: str) -> dict:
        def run():
            retrieved = self._retrieve_bundle_from_json(bundle)
            retrieved_items = json.loads(retrieved)
            successful_fetch_count = sum(1 for item in retrieved_items if item.get("retrieval_status") == "OK")
            prompt = "You are an impact verification validator. Assess only whether the RETRIEVED evidence supports the baseline-to-target impact claim. Failed retrieval is not evidence of absence. If successful_fetch_count is zero, the only permitted verdicts are INCONCLUSIVE or STALE. Return JSON with verdict VERIFIED, PARTIAL, NOT_VERIFIED, INCONCLUSIVE, or STALE; verified_value; reason. Do not invent measurements.\nCLAIM:\n" + json.dumps(rec) + "\nSUCCESSFUL_FETCH_COUNT:\n" + str(successful_fetch_count) + "\nRETRIEVED EVIDENCE:\n" + retrieved
            data = self._dict(gl.nondet.exec_prompt(prompt, response_format="json"))
            verdict = str(data.get("verdict", INCONCLUSIVE)).upper()
            if verdict not in (VERIFIED, PARTIAL, NOT_VERIFIED, INCONCLUSIVE, STALE): verdict = INCONCLUSIVE
            if successful_fetch_count == 0:
                verdict = STALE if verdict == STALE else INCONCLUSIVE
            return {"verdict": verdict, "verified_value": str(data.get("verified_value", ""))[:300], "reason": str(data.get("reason", "No usable reason"))[:700], "successful_fetch_count": successful_fetch_count}
        def validate(leader_result):
            if not isinstance(leader_result, gl.vm.Return): return False
            other = run()
            first = self._dict(leader_result.calldata)
            return str(first.get("verdict", INCONCLUSIVE)).upper() == other["verdict"] and str(first.get("verified_value", ""))[:300] == other["verified_value"] and int(first.get("successful_fetch_count", 0)) == other["successful_fetch_count"]
        return gl.vm.run_nondet_unsafe(run, validate)

    def _bundle(self, claim_id: u256, count: int) -> str:
        out = []
        for i in range(count):
            out.append(self._dict(self.records[self._evidence_key(claim_id, i)]))
        return json.dumps(out)

    def _retrieve_bundle(self, claim_id: u256, count: int) -> str:
        return self._retrieve_bundle_from_json(self._bundle(claim_id, count))

    def _retrieve_bundle_from_json(self, raw: str) -> str:
        items = []
        for item in json.loads(raw):
            try:
                response = gl.nondet.web.get(str(item["source"]))
                status = int(getattr(response, "status_code", getattr(response, "status", 200)))
                if status >= 400:
                    raise gl.vm.UserError("EXTERNAL: source fetch failed")
                item["retrieved_content"] = response.body.decode("utf-8")[:MAX_FETCHED_BODY]
                item["retrieved_at"] = gl.message_raw["datetime"]
                item["retrieval_status"] = "OK"
            except Exception:
                item["retrieval_status"] = "FAILED"
                item["retrieved_content"] = ""
            items.append(item)
        return json.dumps(items)

    def _claim(self, claim_id: u256) -> dict:
        key = self._key(claim_id)
        if key not in self.claims:
            raise gl.vm.UserError("EXPECTED: claim not found")
        return self._dict(self.claims[key])

    def _write(self, claim_id: u256, rec: dict) -> None:
        self.claims[self._key(claim_id)] = json.dumps(rec)

    def _dict(self, raw) -> dict:
        if isinstance(raw, dict): return raw
        try: return json.loads(str(raw))
        except ValueError: return {}

    def _key(self, claim_id): return "claim:" + str(claim_id)
    def _evidence_key(self, claim_id, index): return "evidence:" + str(claim_id) + ":" + str(index)
    def _assessment_key(self, claim_id): return "assessment:" + str(claim_id)
    def _add_days(self, iso, days):
        value = str(iso).replace("Z", "+00:00")
        return (datetime.fromisoformat(value) + timedelta(days=days)).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    def _after(self, left, right):
        return datetime.fromisoformat(str(left).replace("Z", "+00:00")) > datetime.fromisoformat(str(right).replace("Z", "+00:00"))
