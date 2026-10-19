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

## ข้อจำกัดสำคัญ

สถานะเอกสารอ้างอิง ณ วันที่ 19 ตุลาคม 2569 เท่านั้น ก่อนตอบว่าเอกสารใด “ล่าสุด” ต้องตรวจจากแหล่งราชการใหม่เสมอ รายการ `SUPERSEDED` และ `UNVERIFIED` ห้ามใช้เป็นฐานกฎหมายปัจจุบัน

รายละเอียดไฟล์ที่มีจริงและรายการที่ยังดาวน์โหลดไม่ได้อยู่ใน `TOR_EXPERT_CURRENT_KNOWLEDGE/00_README_AND_STATUS.md`
