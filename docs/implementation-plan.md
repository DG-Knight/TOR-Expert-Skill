# แผนดำเนินงาน TOR Expert Current Knowledge

## สถานะรอบปรับปรุง 19 พฤศจิกายน 2569

งานตามแผนเดิมส่วนที่สร้าง Plugin, Gemini Skill, คลังเอกสาร และชุดทดสอบฐานเดิมเสร็จแล้วตาม `docs/task.md` ส่วนงานปรับปรุงรอบนี้เพิ่มตัวอัปเดตคลังความรู้แบบปลอดภัย ตัวตรวจแพ็กเกจ ตัวประเมินกรณีใช้งาน และ CI แล้ว หลักฐานล่าสุดอยู่ใน `tmp/knowledge-update-2026-11-19-apply.json`, ผลการทดสอบใน `README.md` และรายงานแหล่งราชการใน `docs/research/tor-legal-source-audit-2026-11-19.md`

รายการที่ยังต้องทำบนบัญชีผู้ใช้จริงคืออัปโหลด ZIP เข้า ChatGPT/Gemini CLI และทดลองสนทนาแบบ end-to-end; หน้า ChatGPT ตรวจแล้วว่ามีเมนูอัปโหลด แต่การส่งไฟล์ขึ้นบัญชียังไม่ได้ดำเนินการในเซสชันนี้

## การเผยแพร่

- เผยแพร่โค้ด Skill ปลั๊กอิน สคริปต์ และเอกสารที่จัดทำขึ้นภายใต้ MIT License
- ไม่นำ PDF และเนื้อหาต้นฉบับจากหน่วยงานรัฐมารวมเป็นผลงาน MIT ของโครงการ
- แนบไฟล์ลิขสิทธิ์และคำชี้แจงไปกับไฟล์ส่งมอบทุกชุด

> **สำหรับเอเจนต์ผู้ปฏิบัติงาน:** ให้ทำตามลำดับงานนี้และบันทึกสถานะด้วยช่องทำเครื่องหมาย ห้ามจัดเอกสารเป็น CURRENT โดยอาศัยเพียงชื่อไฟล์หรือการพบสำเนาบนเว็บไซต์

**เป้าหมาย:** สร้าง ChatGPT Plugin และ Gemini CLI Agent Skill ที่ใช้คลังความรู้กฎหมายจัดซื้อจัดจ้างภาครัฐไทยชุดเดียวกัน พร้อมไฟล์ต้นฉบับที่ตรวจสอบได้และชุดทดสอบย้อนหลังอย่างน้อย 10 กรณี

**สถาปัตยกรรม:** Plugin แบบ Skills-only เป็นแพ็กเกจหลัก โฟลเดอร์ `TOR_EXPERT_CURRENT_KNOWLEDGE` เป็นคลังเอกสารกลาง และ Gemini CLI ใช้สำเนาที่สร้างจาก Skill ต้นฉบับแบบตรวจสอบความตรงกันได้ การดาวน์โหลดใช้รายการ URL ที่ผ่านการวิจัยและบันทึกค่าแฮชทุกไฟล์

**เทคโนโลยี:** Markdown, CSV, JSON, PowerShell 7/Windows PowerShell, Python standard library, pypdf, Poppler, Git

---

## Task 1: ตั้งโครงสร้างและเอกสารควบคุม

**ไฟล์:**
- สร้าง `plugin.json`
- สร้าง `docs/task.md`
- สร้าง `docs/walkthrough.md`
- สร้าง `docs/changelog.md`
- สร้างโครงสร้าง `TOR_EXPERT_CURRENT_KNOWLEDGE/`

- [ ] สร้าง manifest ของ Plugin ตาม Agent Plugins schema
- [ ] สร้างเอกสารกลางทั้งสี่ไฟล์และบันทึกขอบเขตล่าสุด
- [ ] ตรวจ JSON และตรวจว่าไม่มี placeholder
- [ ] คอมมิตโครงสร้างเริ่มต้น

## Task 2: วิจัยและสร้างทะเบียนเอกสาร

**ไฟล์:**
- สร้าง `docs/research/tor-legal-source-audit.md`
- สร้าง `TOR_EXPERT_CURRENT_KNOWLEDGE/06_KNOWLEDGE_MANIFEST.csv`
- สร้าง `TOR_EXPERT_CURRENT_KNOWLEDGE/08_SOURCE_AND_STATUS_LOG.md`

- [ ] ตรวจรายการกฎหมาย ระเบียบ หนังสือเวียน กฎกระทรวง และคู่มือทุกฉบับจากเว็บไซต์ราชการ
- [ ] บันทึกชื่อเต็ม เลขที่ วันที่ หน่วยงาน URL หน้าเผยแพร่ URL ไฟล์ และหลักฐานสถานะ
- [ ] ใช้สถานะ `CURRENT`, `AMENDED`, `SUPERSEDED`, `UNVERIFIED` ตามหลักฐานเท่านั้น
- [ ] ระบุรายการที่สถานะในบทสนทนาเดิมไม่สามารถยืนยันได้
- [ ] ตรวจว่า URL ทุกตัวใช้ HTTPS และชี้ไปยังโดเมนราชการหรือราชกิจจานุเบกษา

## Task 3: ดาวน์โหลดและตรวจไฟล์ต้นฉบับ

**ไฟล์:**
- สร้างไฟล์ภายใต้ `TOR_EXPERT_CURRENT_KNOWLEDGE/01_LEGAL_CORE/`
- สร้างไฟล์ภายใต้ `TOR_EXPERT_CURRENT_KNOWLEDGE/02_CURRENT_CIRCULARS/`
- สร้างไฟล์ภายใต้ `TOR_EXPERT_CURRENT_KNOWLEDGE/03_SPECIAL_REGULATIONS/`
- สร้างไฟล์ภายใต้ `TOR_EXPERT_CURRENT_KNOWLEDGE/04_EGP_AND_APPEALS/`
- สร้าง `scripts/download_knowledge.ps1`
- สร้าง `scripts/validate_knowledge.py`

- [ ] เขียนตัวตรวจให้ปฏิเสธ HTML ที่เปลี่ยนนามสกุลเป็น PDF
- [ ] เขียนตัวตรวจค่า SHA-256 จำนวนหน้า และข้อความต้นเอกสาร
- [ ] ดาวน์โหลดเฉพาะ URL ที่บันทึกใน Manifest
- [ ] ตรวจชื่อ เลขที่ และวันที่จากเนื้อหาไฟล์เท่าที่ระบบอ่านข้อความได้
- [ ] ย้ายรายการที่ตรวจไม่ผ่านเป็น `UNVERIFIED` โดยไม่อ้างว่าสำเร็จ

## Task 4: สร้าง Skill แกนกลาง

**ไฟล์:**
- สร้าง `skills/tor-government-expert/SKILL.md`
- สร้าง `skills/tor-government-expert/references/legal-source-policy.md`
- สร้าง `skills/tor-government-expert/references/tor-review-workflow.md`
- สร้าง `skills/tor-government-expert/references/output-formats.md`

- [ ] กำหนดเงื่อนไขเรียกใช้ Skill ให้เฉพาะงาน TOR/จัดซื้อจัดจ้างภาครัฐ
- [ ] บังคับแยกข้อเท็จจริง หลักเกณฑ์ การวิเคราะห์ ความเสี่ยง และข้อเสนอแนะ
- [ ] รองรับ Requirement + Metric + Evidence + Test Method + Pass Criteria
- [ ] รองรับ Appeal Risk, Integrity Risk, Spec Lock และงาน IT
- [ ] บังคับตอบ “ยังสรุปไม่ได้จากข้อมูลที่มี” เมื่อหลักฐานไม่เพียงพอ
- [ ] ตรวจ Skill ด้วย `quick_validate.py`

## Task 5: สร้าง Gemini CLI Agent Skill

**ไฟล์:**
- สร้าง `.gemini/skills/tor-government-expert/SKILL.md`
- สร้าง `.gemini/skills/tor-government-expert/references/`
- สร้าง `scripts/sync_gemini_skill.ps1`

- [ ] ทำสำเนาจาก Skill แกนกลางโดยไม่แก้เนื้อหาเฉพาะจุดซ้ำ
- [ ] ตรวจว่า name ตรงกับชื่อโฟลเดอร์และมี description ครบ
- [ ] ตรวจ hash ของไฟล์แกนกลางกับไฟล์ Gemini
- [ ] เพิ่มขั้นตอน `/skills reload` และ `/skills list` ในคู่มือ

## Task 6: สร้างเอกสารความรู้เชิงปฏิบัติ

**ไฟล์:**
- สร้างเอกสารภายใต้ `TOR_EXPERT_CURRENT_KNOWLEDGE/05_PRACTICAL_TOR_REVIEW/`

- [ ] จัดทำปัญหา TOR ที่พบบ่อย
- [ ] จัดทำหลักการจัดทำ TOR และจุดตรวจสอบ
- [ ] จัดทำ Checklist ตรวจ TOR
- [ ] จัดทำ Checklist ร้องเรียนและอุทธรณ์
- [ ] จัดทำ Checklist ทุจริตและผลประโยชน์ทับซ้อน
- [ ] จัดทำ Checklist การจำกัดการแข่งขันและล็อกสเปก
- [ ] ติดป้ายทุกไฟล์ว่าเป็นแนวทางวิเคราะห์ ไม่ใช่ตัวบทกฎหมาย

## Task 7: สร้างดัชนี ชุดทดสอบ และ ZIP

**ไฟล์:**
- สร้าง `TOR_EXPERT_CURRENT_KNOWLEDGE/00_README_AND_STATUS.md`
- สร้าง `TOR_EXPERT_CURRENT_KNOWLEDGE/07_KNOWLEDGE_INDEX.md`
- สร้าง `TOR_EXPERT_CURRENT_KNOWLEDGE/09_REGRESSION_TESTS.md`
- สร้าง `tests/test_package.py`
- สร้าง `dist/TOR_EXPERT_CURRENT_KNOWLEDGE.zip`

- [ ] สร้างโจทย์ทดสอบ TOR อย่างน้อย 10 กรณี พร้อมผลที่คาดหวัง
- [ ] ตรวจ manifest, path, hash, PDF และเขตเอกสารเก่าแบบอัตโนมัติ
- [ ] รันชุดทดสอบทั้งหมดและบันทึกผลจริง
- [ ] สร้าง ZIP จากไฟล์ที่ตรวจผ่านจริงเท่านั้น
- [ ] เปิด ZIP ตรวจรายชื่อไฟล์และทดสอบแตกไฟล์ในพื้นที่ชั่วคราว

## Task 8: ตรวจส่งมอบและคอมมิต

**ไฟล์:**
- อัปเดต `docs/task.md`
- อัปเดต `docs/walkthrough.md`
- อัปเดต `docs/changelog.md`

- [ ] สรุปจำนวนไฟล์จริง ลิงก์พร้อมใช้ CURRENT/AMENDED/SUPERSEDED/UNVERIFIED
- [ ] ตรวจ `git diff --check` และตรวจว่าไม่มีคีย์หรือข้อมูลลับ
- [ ] รันการตรวจทั้งหมดซ้ำจากสถานะสะอาด
- [ ] คอมมิตงานพร้อมข้อความสรุปชัดเจน
- [ ] รายงานสิ่งที่ผู้ใช้ทำได้แล้วและข้อจำกัดที่ยังเหลือ
