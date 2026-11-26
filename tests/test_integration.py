from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "ux-decision-advisor"
sys.path.insert(0, str(SKILL / "scripts"))

import render_report  # noqa: E402
import validate_evidence  # noqa: E402


class IntegrationContractTests(unittest.TestCase):
    def _base_evidence_payload(self) -> dict:
        return json.loads((SKILL / "assets" / "uxda-evidence-example.json").read_text(encoding="utf-8"))

    def test_supported_claim_with_contradicts_is_rejected(self):
        payload = self._base_evidence_payload()
        payload["claims"][0]["status"] = "supported"
        payload["claims"][0]["support_type"] = "contradicts"
        with self.assertRaises(validate_evidence.EvidenceIssue) as caught:
            validate_evidence.validate(payload)
        self.assertIn("SUPPORTED_CLAIM_CONTRADICTS_EVIDENCE", str(caught.exception))

    def test_implemented_decision_with_false_outcome_is_rejected(self):
        payload = self._base_evidence_payload()
        payload["decisions"][0]["status"] = "implemented"
        payload["decisions"][0]["outcome"] = {
            "implemented": False,
            "actual_result": "Rollout was cancelled before shipping.",
        }
        with self.assertRaises(validate_evidence.EvidenceIssue) as caught:
            validate_evidence.validate(payload)
        self.assertIn("DECISION_IMPLEMENTATION_MISMATCH", str(caught.exception))

    def test_restricted_evidence_without_consent_scope_is_rejected(self):
        payload = self._base_evidence_payload()
        payload["evidence"][0]["access_class"] = "restricted"
        payload["evidence"][0]["authorized_for_use"] = True
        payload["evidence"][0].pop("consent_scope", None)
        with self.assertRaises(validate_evidence.EvidenceIssue) as caught:
            validate_evidence.validate(payload)
        self.assertIn("RESTRICTED_EVIDENCE_REQUIRES_CONSENT_SCOPE", str(caught.exception))

    def test_legacy_beta4_report_payload_renders_with_legacy_shell(self):
        legacy_payload = {
            "title": "Legacy Beta.4 Decision Report",
            "recommendation": "Run a 5-user pilot before expanding rollout.",
            "next_step": "Observe task completion and error rate in pilot.",
            "decision_options": [
                {"name": "Pilot first", "benefit": "Limits risk", "tradeoff": "2-day delay", "status": "Recommended"}
            ],
            "findings": [
                {"title": "Button occlusion", "fact": "Glove overlaps 8mm target", "principle": "Fitts/ergonomics", "action": "Increase to 18mm", "evidence": "Observed"}
            ],
        }
        validated = render_report.validate(legacy_payload)
        html = render_report.render(validated)
        self.assertIn("Legacy Beta.4 Decision Report", html)
        self.assertIn("UX Decision Assistant | Review", html)

    def test_mixed_or_unknown_report_schema_fails_clearly(self):
        with self.assertRaises(render_report.InputIssue) as mixed:
            render_report.validate({"title": "X", "summary": "S", "decision_options": []})
        self.assertIn("MIXED_REPORT_SCHEMA_UNSUPPORTED", str(mixed.exception))

        with self.assertRaises(render_report.InputIssue) as unknown:
            render_report.validate({"title": "X"})
        self.assertIn("UNKNOWN_OR_EMPTY_REPORT_SCHEMA", str(unknown.exception))

    def test_precedence_and_evidence_guardrail_preserved(self):
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        contract_text = (SKILL / "references" / "business-facing-output-contract.md").read_text(encoding="utf-8")
        self.assertIn("Precedence & Language Adaptation", skill_text)
        self.assertIn("UXRR", skill_text)
        self.assertIn("Evidence-to-Outcome Guardrail", contract_text)
        self.assertIn("Failure to reject the null hypothesis does not establish equivalence", contract_text)


if __name__ == "__main__":
    unittest.main()
