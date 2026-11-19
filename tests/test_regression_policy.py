import csv
import re
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "TOR_EXPERT_CURRENT_KNOWLEDGE"


def manifest_rows():
    with (KNOWLEDGE / "06_KNOWLEDGE_MANIFEST.csv").open(
        encoding="utf-8-sig", newline=""
    ) as stream:
        return {row["id"]: row for row in csv.DictReader(stream)}


class LegalStatusRegressionTests(unittest.TestCase):
    def test_superseded_chain_is_enforced(self):
        rows = manifest_rows()
        expected = {
            "OLD-299": "ว714",
            "OLD-298": "ว715",
            "OLD-300": "ว753",
            "OLD-108": "ว755",
        }
        for item_id, replacement in expected.items():
            with self.subTest(item_id=item_id):
                self.assertEqual(rows[item_id]["status"], "SUPERSEDED")
                self.assertEqual(rows[item_id]["replaced_by"], replacement)

    def test_unverified_documents_cannot_be_presented_as_current(self):
        rows = manifest_rows()
        self.assertEqual(rows["AR-001"]["status"], "UNVERIFIED")
        self.assertEqual(rows["EG-001"]["status"], "UNVERIFIED")
        self.assertEqual(rows["OLD-570"]["status"], "SUPERSEDED")
        skill = (ROOT / "skills" / "tor-government-expert" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("ห้ามใช้ `SUPERSEDED` หรือ `UNVERIFIED`", skill)
        self.assertIn("ยังสรุปไม่ได้จากข้อมูลที่มี", skill)

    def test_current_local_documents_have_hashes(self):
        rows = manifest_rows()
        local = [row for row in rows.values() if row["local_path"]]
        self.assertGreaterEqual(len(local), 18)
        for row in local:
            with self.subTest(item_id=row["id"]):
                self.assertIn(row["status"], {"CURRENT", "AMENDED"})
                self.assertRegex(row["sha256"], r"^[0-9a-f]{64}$")

    def test_new_w777_is_in_current_knowledge(self):
        row = manifest_rows()["CR-777"]
        self.assertEqual(row["status"], "CURRENT")
        self.assertEqual(row["issued_date"], "2026-10-08")
        self.assertTrue(row["local_path"])


class SkillBehaviorRegressionTests(unittest.TestCase):
    def test_regression_catalog_has_at_least_ten_cases(self):
        text = (KNOWLEDGE / "09_REGRESSION_TESTS.md").read_text(encoding="utf-8")
        cases = re.findall(r"^\d+\. \*\*", text, flags=re.MULTILINE)
        self.assertGreaterEqual(len(cases), 10)

    def test_tor_review_covers_required_risks(self):
        text = (
            ROOT
            / "skills"
            / "tor-government-expert"
            / "references"
            / "tor-review-workflow.md"
        ).read_text(encoding="utf-8")
        for term in (
            "Spec Lock",
            "POC/Demo",
            "Appeal Risk",
            "Integrity Risk",
            "PDPA",
            "Vendor Lock-in",
        ):
            with self.subTest(term=term):
                self.assertIn(term, text)


class DistributionRegressionTests(unittest.TestCase):
    def test_built_archives_contain_installable_layouts(self):
        dist = ROOT / "dist"
        knowledge_zip = dist / "TOR_EXPERT_CURRENT_KNOWLEDGE.zip"
        plugin_zip = dist / "tor-government-expert-chatgpt-plugin.zip"
        gemini_zip = dist / "tor-government-expert-gemini-skill.zip"
        for path in (knowledge_zip, plugin_zip, gemini_zip):
            self.assertTrue(path.exists(), f"ไม่พบ {path.name}")
            self.assertGreater(path.stat().st_size, 0)

        with zipfile.ZipFile(plugin_zip) as archive:
            names = set(archive.namelist())
            self.assertIn("plugin.json", names)
            self.assertIn("skills/tor-government-expert/SKILL.md", names)
            self.assertTrue(
                any(name.endswith("06_KNOWLEDGE_MANIFEST.csv") for name in names)
            )

        with zipfile.ZipFile(gemini_zip) as archive:
            names = set(archive.namelist())
            self.assertIn(".gemini/skills/tor-government-expert/SKILL.md", names)
            self.assertTrue(
                any(
                    "references/knowledge/TOR_EXPERT_CURRENT_KNOWLEDGE/"
                    "06_KNOWLEDGE_MANIFEST.csv" in name
                    for name in names
                )
            )


if __name__ == "__main__":
    unittest.main()
