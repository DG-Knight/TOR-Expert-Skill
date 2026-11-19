import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class QualityEvaluatorTests(unittest.TestCase):
    def test_skill_evaluation_reports_required_policy_coverage(self):
        from scripts.evaluate_skill_cases import evaluate_skill

        fixture = ROOT / "tests" / "fixtures" / "tor_quality_cases.json"
        result = evaluate_skill(ROOT / "skills" / "tor-government-expert", fixture)
        self.assertEqual(result["summary"]["failed"], 0)
        self.assertGreaterEqual(result["summary"]["passed"], 5)

    def test_response_evaluation_finds_missing_sections(self):
        from scripts.evaluate_skill_cases import evaluate_response

        fixture = {
            "id": "sample",
            "required_sections": ["[ข้อเท็จจริง]", "[ความเสี่ยง]"],
            "required_terms": ["ยังสรุปไม่ได้จากข้อมูลที่มี"],
        }
        result = evaluate_response(fixture, "[ข้อเท็จจริง] ข้อมูลยังไม่ครบ")
        self.assertFalse(result["passed"])
        self.assertIn("[ความเสี่ยง]", result["missing"])

    def test_quality_report_is_json_serializable(self):
        from scripts.evaluate_skill_cases import build_quality_report

        report = build_quality_report(
            [{"id": "a", "passed": True}, {"id": "b", "passed": False}]
        )
        json.dumps(report, ensure_ascii=False)
        self.assertEqual(report["summary"], {"passed": 1, "failed": 1, "total": 2})
