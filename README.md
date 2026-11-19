# TOR งานภาครัฐ Expert

แพ็กเกจพร้อมใช้สำหรับร่าง ตรวจ และวิเคราะห์ TOR งานจัดซื้อจัดจ้างภาครัฐไทย โดยใช้แกนความรู้เดียวกันกับ ChatGPT Plugin และ Gemini CLI Agent Skill

## ไฟล์ส่งมอบ

- `dist/TOR_EXPERT_CURRENT_KNOWLEDGE.zip` — คลังความรู้และ PDF ที่กู้คืนได้
- `dist/tor-government-expert-chatgpt-plugin.zip` — ปลั๊กอินสำหรับ ChatGPT Work/Codex
- `dist/tor-government-expert-gemini-skill.zip` — Skill สำหรับ Gemini CLI

## ติดตั้ง ChatGPT Plugin

1. เปิดหน้าจัดการ Plugins ใน ChatGPT Work หรือ Codex
2. เลือกติดตั้งจากไฟล์ แล้วเลือก `tor-government-expert-chatgpt-plugin.zip`
3. ตรวจว่าปลั๊กอินชื่อ “TOR งานภาครัฐ Expert” ปรากฏและเปิดใช้งานอยู่
4. ทดลองพิมพ์ `ตรวจ TOR ฉบับนี้และสรุป Red Flags พร้อมข้อความเสนอแก้ไข`

## ติดตั้ง Gemini CLI Agent Skill

1. แตกไฟล์ `tor-government-expert-gemini-skill.zip` ที่รากของโปรเจกต์
2. ตรวจว่ามี `.gemini/skills/tor-government-expert/SKILL.md`
3. เปิด Gemini CLI ในโปรเจกต์นั้น แล้วใช้ `/skills list` เพื่อตรวจว่า Skill ถูกค้นพบ
4. ทดลองพิมพ์ `ใช้ทักษะ TOR งานภาครัฐ Expert ตรวจความเสี่ยงล็อกสเปกของ TOR นี้`

## ผลทดสอบและหลักฐานก่อน–หลัง

| รายการ | ก่อนปรับปรุง (commit `dc76c77`) | หลังปรับปรุง (รอบ 19 พ.ย. 2569) |
|---|---:|---:|
| การทดสอบอัตโนมัติ | 18 ผ่าน | **30 ผ่าน** |
| ตัวอัปเดตคลังความรู้ | ไม่มี | มี dry-run/apply, staging, ตรวจ PDF และรายงาน JSON |
| การเก็บไฟล์เดิมก่อนแทนที่ | ไม่มี | มี archive อัตโนมัติ |
| ตัวตรวจ Plugin/Skill | ตรวจโครงสร้างพื้นฐาน | ตรวจ manifest, ZIP, Skill ทั้งสองสำเนา และ CI |
| การประเมินคุณภาพคำตอบ | ไม่มี fixture กลาง | **5/5 กรณีผ่าน** |
| PDF ที่กู้คืนและตรวจ SHA-256 | 18 ไฟล์ | **19 ไฟล์** (กู้ CR-753 เพิ่ม 1 ไฟล์) |

หลักฐานที่ตรวจซ้ำได้:

- `python -m unittest discover -s tests -v` → **Ran 30 tests … OK**
- `python scripts/evaluate_skill_cases.py ...` → **passed 5 / failed 0**
- `python scripts/validate_plugin.py plugin.json` → `PLUGIN_MANIFEST_OK`
- ตัวตรวจ Skill ทั้งแกนกลางและ Gemini → `SKILL_VALID`
- `powershell.exe -File scripts/build_packages.ps1` → `PACKAGE_BUILD_OK` และสร้าง ZIP 3 ชุดใหม่
- รายงานดาวน์โหลดจริง: `tmp/knowledge-update-2026-11-19-apply.json` → 16 คงเดิม, 1 ติดตั้ง, 5 ข้อผิดพลาดจากต้นทาง, 7 รายการยังไม่มี URL/ไฟล์ในเครื่อง
- หน้า ChatGPT ตรวจแล้วมีเมนู “อัปโหลดไฟล์เก็บถาวรของปลั๊กอิน” และ “อัปโหลดจากคอมพิวเตอร์” สำหรับ Skill; ยังไม่ได้ส่งไฟล์ขึ้นบัญชีหรืออ้างว่าทดสอบสนทนาจริงแล้ว

## สถานะคลังความรู้และข้อจำกัดสำคัญ

สถานะเอกสารอ้างอิงตรวจซ้ำ ณ วันที่ **19 พฤศจิกายน 2569**: `CURRENT` 19 รายการ, `AMENDED` 3 รายการ, `SUPERSEDED` 5 รายการ และ `UNVERIFIED` 2 รายการ

- CR-753 มี PDF ทางการและตรวจ SHA-256 แล้ว
- CR-1203 ยืนยันว่าใช้เฉพาะงานจ้างที่ปรึกษา แต่ยังไม่มี PDF ในชุด
- SP-001 และ SP-002 เป็น `AMENDED` ต้องอ่านร่วมกับฉบับแก้ไข; ยังไม่มี PDF ในชุด
- ว570 เป็น `SUPERSEDED` ตามสายที่มีหลักฐาน `ว570 → ว298 → ว715`; ยังไม่ยืนยันลูกศรตรง `ว570 → ว851`
- `AR-001` และ `EG-001` ยังเป็น `UNVERIFIED` ห้ามใช้สรุปว่าเป็นกฎหมายปัจจุบัน

ก่อนตอบว่าเอกสารใด “ล่าสุด” ต้องตรวจจากแหล่งราชการใหม่เสมอ รายการ `SUPERSEDED` และ `UNVERIFIED` ห้ามใช้เป็นฐานกฎหมายปัจจุบัน รายละเอียดอยู่ใน `TOR_EXPERT_CURRENT_KNOWLEDGE/00_README_AND_STATUS.md`, `06_KNOWLEDGE_MANIFEST.csv` และ [รายงานตรวจแหล่งราชการ](docs/research/tor-legal-source-audit-2026-11-19.md)

## ลิขสิทธิ์และเอกสารอ้างอิง

ส่วนที่โครงการสร้างขึ้นเองเปิดให้ใช้ แก้ไข และแจกจ่ายต่อได้ภายใต้ [MIT License](LICENSE) ส่วน PDF และเนื้อหาต้นฉบับจากหน่วยงานรัฐยังคงเป็นไปตามเงื่อนไขของแหล่งต้นฉบับ ดู [คำชี้แจงเนื้อหาจากบุคคลที่สาม](THIRD_PARTY_NOTICES.md)
