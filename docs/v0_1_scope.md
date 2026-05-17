# Froddy Lead QA V0.1

Product:
QA/control layer над Avito-переписками, менеджерами и AI-ботами.

Positioning:
Не AI-бот для Авито. Не автоответчик. Не live-agent.
Froddy Lead QA проверяет качество обработки лидов, находит потенциальные потери и превращает их в очередь действий с verdict.

ICP:
Малое Avito-агентство 10-25 клиентов, услуги / ремонт / строительство.

V0.1 делает:
- CSV upload
- parse dialogues/messages
- PII masking: phone, email, url, car plate
- quality_score
- loss detection
- follow-up drafts
- verdict: allow/review/hold/block
- action queue
- decision journal
- web cabinet: Summary / Actions / Journal

V0.1 не делает:
- live Avito bot
- auto-send follow-up
- Avito API
- OCR/screenshots
- Telegram approvals
- PDF reports
- client-facing reports
- Solo/Enterprise

Main moat:
dialogue -> problem -> recommended action -> verdict -> human decision -> outcome
