# Froddy Lead QA

QA/control layer над Avito-переписками, менеджерами и AI-ботами.

Froddy Lead QA не является Avito-ботом и не отправляет сообщения автоматически.
Это диспетчер/аудитор над исполнителями: находит потерянные лиды, предлагает действия, назначает verdict и сохраняет human decisions.

## Demo

Cabinet:
https://froddy-lead-qa-clean-froddy.amvera.io/cabinet

Health:
https://froddy-lead-qa-clean-froddy.amvera.io/health

Demo analysis:
https://froddy-lead-qa-clean-froddy.amvera.io/v1/analyze-demo

## Current scope

V0.1 includes:

- CSV parsing
- deterministic quality scoring
- mock loss detection
- mock follow-up generation
- verdict engine: allow / review / hold / block
- PII masking: phone / email / URL / car plate
- web cabinet
- server-side decision journal
- CSV export
- prod smoke tests

V0.1 does not include:

- Avito API integration
- auto-send
- live bot
- real LLM
- database
- auth
- final UI

## Local setup

PowerShell:

cd "D:\RCL\Avito\froddy-lead-qa\api"
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Run local server:

cd "D:\RCL\Avito\froddy-lead-qa\api"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001

Local URLs:

http://127.0.0.1:8001/health
http://127.0.0.1:8001/v1/analyze-demo
http://127.0.0.1:8001/cabinet

## Useful commands

Inspect demo analysis:

cd "D:\RCL\Avito\froddy-lead-qa\api"
python -m app.scripts.inspect_actions

Run tests:

cd "D:\RCL\Avito\froddy-lead-qa\api"
python -m app.scripts.test_verdict
python -m app.scripts.test_pii
python -m app.scripts.test_journal
python -m compileall app

Check prod deploy:

cd "D:\RCL\Avito\froddy-lead-qa\api"
python -m app.scripts.check_prod_ui
python -m app.scripts.smoke_prod

Expected:

Prod UI deploy check passed
Smoke test passed

## API endpoints

GET /health
Returns app health.

GET /v1/analyze-demo
Runs the demo CSV analysis.

Expected demo result:

total_dialogues = 10
recommended_actions_count = 7

Important demo verdicts:

d_006 = hold
d_010 = block

POST /v1/analyze-csv
Body:

{
  "csv_text": "..."
}

GET /v1/decision-journal
Returns server-side human decision journal.

POST /v1/decision-journal
Saves human decision.

DELETE /v1/decision-journal
Clears server-side decision journal.

## Demo checklist

See:

docs/demo_checklist.md

## Positioning

BotB2B is the executor in the chat.
Froddy Lead QA is the dispatcher/auditor above executors.

Core loop:

dialogue -> problem -> recommended action -> verdict -> human decision -> outcome

Current moat direction:

recommended_actions
verdict engine
decision_journal
future outcome data
