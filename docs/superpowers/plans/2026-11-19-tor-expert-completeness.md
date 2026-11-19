# TOR Expert Completeness Implementation Plan

> **For agentic workers:** ทำงานตามลำดับทีละงาน ตรวจผลทุกช่วง และอัปเดตเครื่องหมายในเอกสารกลางเมื่อหลักฐานยืนยันแล้ว

**Goal:** ทำให้ TOR Expert เป็นแพ็กเกจที่อัปเดตคลังความรู้ได้อย่างปลอดภัย ทดสอบการใช้งานได้จริง เผยแพร่แบบมีเวอร์ชัน และมีหลักฐานเปรียบเทียบก่อน–หลังให้ผู้ใช้ตรวจสอบได้

**Architecture:** คง Skill แกนกลางเป็นแหล่งเดียว แล้วสร้างสำเนา Gemini และ ZIP จากแหล่งนั้น คลังความรู้จะถูกอัปเดตผ่าน Manifest ที่มี URL/สถานะ/แฮช โดยดาวน์โหลดเข้า staging ก่อนแทนที่ไฟล์จริง ส่วนการประเมินคุณภาพจะแยกจากการตรวจโครงสร้างแพ็กเกจและใช้กรณี TOR ตัวอย่างที่มีผลคาดหวังชัดเจน

**Tech Stack:** Python standard library, `pypdf`, PowerShell, Markdown/CSV/JSON, GitHub Actions, Git tags/releases

---

### Task 1: เก็บหลักฐานฐานเดิมและปรับเอกสารสถานะ

**Files:**
- Modify: `docs/task.md`
- Modify: `docs/implementation-plan.md`
- Modify: `docs/walkthrough.md`
- Modify: `docs/changelog.md`
- Create: `docs/research/tor-legal-source-audit-2026-11-19.md`

- [x] บันทึกจำนวนเอกสาร สถานะ และไฟล์ที่มีจริงจาก Manifest
- [x] ตรวจเครื่องหมายงานค้างในแผนเดิมให้ตรงกับหลักฐาน ไม่เปลี่ยนเป็นเสร็จโดยไม่มีผลตรวจ
- [x] รวมผลวิจัยจากแหล่งราชการและระบุรายการที่ยังหาไม่ได้อย่างชัดเจน

### Task 2: อัปเดตคลังความรู้จาก Manifest

**Files:**
- Modify: `TOR_EXPERT_CURRENT_KNOWLEDGE/06_KNOWLEDGE_MANIFEST.csv`
- Modify: `TOR_EXPERT_CURRENT_KNOWLEDGE/07_KNOWLEDGE_INDEX.md`
- Modify: `TOR_EXPERT_CURRENT_KNOWLEDGE/08_SOURCE_AND_STATUS_LOG.md`
- Modify: `TOR_EXPERT_CURRENT_KNOWLEDGE/00_README_AND_STATUS.md`
- Add/modify: `TOR_EXPERT_CURRENT_KNOWLEDGE/**` เฉพาะ PDF ที่ผ่านการตรวจ

- [x] ดาวน์โหลดเฉพาะ URL ทางการที่ระบุใน Manifest ลง staging
- [x] ตรวจ HTTP response, `%PDF-`, จำนวนหน้า, SHA-256 และข้อมูลต้นเอกสาร
- [x] เปลี่ยนไฟล์เฉพาะเมื่อหลักฐานผ่าน และเก็บไฟล์เดิมใน archive เมื่อถูกแทนที่
- [x] สร้างรายงานรายการติดตั้ง คงเดิม ผิดพลาด และยังขาด

### Task 3: ทำระบบอัปเดตแบบปลอดภัยและทดสอบก่อนแก้

**Files:**
- Create: `scripts/update_knowledge.py`
- Modify: `scripts/download_knowledge.ps1`
- Modify: `scripts/validate_knowledge.py`
- Modify: `tests/test_package.py`
- Create: `tests/test_update_knowledge.py`

- [x] เขียน failing tests สำหรับ allowlist URL, staging, HTML masquerading, hash mismatch และรายงานผล
- [x] ทำ implementation ที่เปลี่ยนไฟล์จริงแบบ atomic หลังตรวจผ่าน
- [x] เพิ่มโหมด dry-run และรายงาน JSON เพื่อให้ตรวจสอบย้อนหลังได้
- [x] ทดสอบว่าการซิงก์ Gemini ใช้ staging และไม่ลบสำเนาเดิมก่อนสำเร็จ

### Task 4: เพิ่มการประเมินคุณภาพคำตอบและ smoke test

**Files:**
- Create: `tests/fixtures/tor_quality_cases.json`
- Create: `scripts/evaluate_skill_cases.py`
- Modify: `tests/test_regression_policy.py`
- Modify: `README.md`
- Modify: `docs/walkthrough.md`

- [x] สร้างกรณี TOR ตัวอย่างที่ครอบคลุม Spec Lock, Appeal, Integrity, IT และข้อมูลไม่พอ
- [x] ตรวจองค์ประกอบคำตอบ: ข้อเท็จจริง หลักเกณฑ์ การวิเคราะห์ ความเสี่ยง ข้อเสนอแนะ และหลักฐาน
- [x] สร้างหลักฐานก่อน–หลังเป็นผล JSON พร้อมคะแนนและข้อผิดพลาด
- [x] บันทึกว่าหน้า ChatGPT มีเมนูอัปโหลดแล้ว; การอัปโหลดจริงและทดลองตอบยังต้องทำบนบัญชีผู้ใช้

### Task 5: ตรวจ Schema, CI และการเผยแพร่แบบมีเวอร์ชัน

**Files:**
- Create: `.github/workflows/test.yml`
- Create: `scripts/validate_plugin.py`
- Modify: `tests/test_package.py`
- Modify: `plugin.json`
- Modify: `README.md`
- Create: `RELEASE_NOTES.md`

- [x] ตรวจ JSON/schema และโครงสร้าง ZIP ใน CI
- [x] รันชุดทดสอบและตัวตรวจ Skill ทุกครั้งที่ push/pull request
- [x] เพิ่ม version และ release notes (รอ tag หลังตรวจรอบสุดท้าย)
- [x] ตรวจว่าแพ็กเกจที่เผยแพร่สร้างจากไฟล์ที่ผ่าน validation เท่านั้น

### Task 6: ตรวจรับขั้นสุดท้ายและส่งมอบ

- [x] รันชุดทดสอบเต็ม ตัวตรวจ Skill ตัวตรวจคลัง และสร้าง ZIP ใหม่
- [x] ตรวจ `git diff --check`, ข้อมูลลับ, ขนาดไฟล์ และความสมบูรณ์ ZIP
- [x] เปรียบเทียบผลก่อน–หลังและบันทึกใน `README.md`
- [x] คอมมิต, สร้าง tag/release และ push พร้อมตรวจ hash บน remote
