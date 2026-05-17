# CSV format V0.1

Required columns:
- dialogue_id
- ad_title
- manager_name
- side
- text
- sent_at

side values:
- buyer
- seller

sent_at:
ISO 8601, example: 2026-05-01T10:00:00

Rules:
- one row = one message
- rows with the same dialogue_id belong to one dialogue
- messages must be sorted by sent_at inside each dialogue
- V0.1 niche: repair / construction / b2c services

Example:

dialogue_id,ad_title,manager_name,side,text,sent_at
d_001,"Ремонт ванной под ключ",Анна,buyer,"Здравствуйте, сколько стоит ремонт ванной 4 м²?",2026-05-01T10:00:00
d_001,"Ремонт ванной под ключ",Анна,seller,"Здравствуйте! Обычно от 180 000 ₽, зависит от плитки и состояния стен. Когда удобно сделать замер?",2026-05-01T10:06:00
