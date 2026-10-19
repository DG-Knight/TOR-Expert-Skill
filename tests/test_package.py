import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "TOR_EXPERT_CURRENT_KNOWLEDGE"


class PackageStructureTests(unittest.TestCase):
    def test_powershell_scripts_are_windows_legacy_safe(self):
        for path in (ROOT / "scripts").glob("*.ps1"):
            with self.subTest(path=path.name):
                path.read_bytes().decode("ascii")

    def test_downloader_stops_after_network_failure(self):
        script = (ROOT / "scripts" / "download_knowledge.ps1").read_text(
            encoding="ascii"
        )
        self.assertIn("$ErrorActionPreference = \"Stop\"", script)

    def test_plugin_manifest_is_portable_and_names_the_plugin(self):
        manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(
            manifest["$schema"],
            "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        )
        self.assertEqual(manifest["name"], "tor-government-expert")

    def test_required_knowledge_structure_exists(self):
        required = [
            "00_README_AND_STATUS.md",
            "01_LEGAL_CORE",
            "02_CURRENT_CIRCULARS",
            "03_SPECIAL_REGULATIONS",
            "04_EGP_AND_APPEALS",
            "05_PRACTICAL_TOR_REVIEW",
            "06_KNOWLEDGE_MANIFEST.csv",
            "07_KNOWLEDGE_INDEX.md",
            "08_SOURCE_AND_STATUS_LOG.md",
            "09_REGRESSION_TESTS.md",
            "99_SUPERSEDED_ARCHIVE",
        ]
        missing = [name for name in required if not (KNOWLEDGE / name).exists()]
        self.assertEqual(missing, [])

    def test_chatgpt_and_gemini_skills_are_identical(self):
        source = ROOT / "skills" / "tor-government-expert"
        gemini = ROOT / ".gemini" / "skills" / "tor-government-expert"
        source_files = {
            path.relative_to(source): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in source.rglob("*")
            if path.is_file()
        }
        gemini_files = {
            path.relative_to(gemini): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in gemini.rglob("*")
            if path.is_file()
        }
        self.assertTrue(source_files)
        self.assertEqual(source_files, gemini_files)


class KnowledgeValidationTests(unittest.TestCase):
    def test_manifest_has_required_columns_and_valid_statuses(self):
        required = {
            "id",
            "title",
            "document_number",
            "issued_date",
            "effective_date",
            "owner",
            "status",
            "replaced_by",
            "source_page_url",
            "direct_file_url",
            "checked_date",
            "local_path",
            "sha256",
            "notes",
        }
        with (KNOWLEDGE / "06_KNOWLEDGE_MANIFEST.csv").open(
            encoding="utf-8-sig", newline=""
        ) as stream:
            reader = csv.DictReader(stream)
            self.assertTrue(required.issubset(set(reader.fieldnames or [])))
            rows = list(reader)
        self.assertGreaterEqual(len(rows), 20)
        self.assertTrue(
            all(
                row["status"] in {"CURRENT", "AMENDED", "SUPERSEDED", "UNVERIFIED"}
                for row in rows
            )
        )

    def test_pdf_validator_rejects_html_disguised_as_pdf(self):
        from scripts.validate_knowledge import inspect_pdf

        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "fake.pdf"
            fake.write_text("<html><body>ไม่ใช่ PDF</body></html>", encoding="utf-8")
            report = inspect_pdf(fake)
        self.assertFalse(report["valid"])
        self.assertIn("ลายเซ็นไฟล์", report["errors"])

    def test_current_local_files_match_manifest_hashes(self):
        from scripts.validate_knowledge import validate_manifest_files

        report = validate_manifest_files(KNOWLEDGE / "06_KNOWLEDGE_MANIFEST.csv", ROOT)
        self.assertEqual(report["errors"], [])


if __name__ == "__main__":
    unittest.main()
