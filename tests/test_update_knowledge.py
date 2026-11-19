import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "TOR_EXPERT_CURRENT_KNOWLEDGE"


class KnowledgeUpdateTests(unittest.TestCase):
    def test_update_cli_starts_from_project_root(self):
        result = subprocess.run(
            [sys.executable, "scripts/update_knowledge.py", "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_source_url_requires_https_and_official_domain(self):
        from scripts.update_knowledge import validate_source_url

        self.assertTrue(validate_source_url("https://www.cgd.go.th/file.pdf")[0])
        self.assertTrue(
            validate_source_url("https://www.ratchakitcha.soc.go.th/DATA/a.pdf")[0]
        )
        self.assertFalse(validate_source_url("http://www.cgd.go.th/file.pdf")[0])
        self.assertFalse(validate_source_url("https://example.com/file.pdf")[0])

    def test_staged_pdf_must_have_pdf_signature_and_valid_pages(self):
        from scripts.update_knowledge import validate_staged_pdf

        source = next((KNOWLEDGE / "01_LEGAL_CORE").glob("*.pdf"))
        with tempfile.TemporaryDirectory() as tmp:
            valid = Path(tmp) / "valid.pdf"
            valid.write_bytes(source.read_bytes())
            invalid = Path(tmp) / "invalid.pdf"
            invalid.write_text("<html>not a pdf</html>", encoding="utf-8")

            self.assertTrue(validate_staged_pdf(valid)["valid"])
            self.assertFalse(validate_staged_pdf(invalid)["valid"])

    def test_atomic_replace_preserves_old_file_when_validation_fails(self):
        from scripts.update_knowledge import atomic_install

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "document.pdf"
            staged = Path(tmp) / "staged.pdf"
            target.write_bytes(b"old")
            staged.write_bytes(b"new")

            with self.assertRaises(ValueError):
                atomic_install(staged, target, lambda path: False)
            self.assertEqual(target.read_bytes(), b"old")
            self.assertTrue(staged.exists())

    def test_atomic_replace_archives_previous_file_after_validation(self):
        from scripts.update_knowledge import atomic_install

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            target = base / "document.pdf"
            staged = base / "staged.pdf"
            archive = base / "archive"
            target.write_bytes(b"old")
            staged.write_bytes(b"new")

            archived = atomic_install(staged, target, lambda path: True, archive)

            self.assertEqual(target.read_bytes(), b"new")
            self.assertIsNotNone(archived)
            self.assertEqual(archived.read_bytes(), b"old")

    def test_report_is_json_serializable_and_records_summary(self):
        from scripts.update_knowledge import build_report

        report = build_report(
            [
                {"id": "A", "action": "unchanged", "reason": "hash matches"},
                {"id": "B", "action": "blocked", "reason": "unofficial source"},
            ]
        )
        json.dumps(report, ensure_ascii=False)
        self.assertEqual(report["summary"]["unchanged"], 1)
        self.assertEqual(report["summary"]["blocked"], 1)


if __name__ == "__main__":
    unittest.main()
