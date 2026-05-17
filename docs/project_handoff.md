# Froddy Lead QA — project handoff

## Current state

Project is deployed and working.

Prod cabinet:
https://froddy-lead-qa-froddy.amvera.io/cabinet

Prod health:
https://froddy-lead-qa-froddy.amvera.io/health

GitHub:
https://github.com/Bear2020code/froddy-lead-qa

Branch:
master

Working folder:
D:\RCL\Avito\froddy-lead-qa

API folder:
D:\RCL\Avito\froddy-lead-qa\api

## Product positioning

Froddy Lead QA is not an Avito bot.
It is a QA/control layer over Avito dialogues, managers, and AI-bots.

BotB2B / AvBot / Riabot are executors in the chat.
Froddy Lead QA is the dispatcher/auditor above executors.

Core loop:

dialogue -> problem -> recommended action -> verdict -> human decision -> future outcome

Current moat direction:

recommended_actions
verdict engine
decision_journal
future outcome data

## What works now

Backend:

- FastAPI app
- GET /health
- GET /v1/analyze-demo
- POST /v1/analyze-csv
- GET /v1/decision-journal
- POST /v1/decision-journal
- DELETE /v1/decision-journal
- GET /sample-csv
- GET /cabinet
- root / redirects to /cabinet

Pipeline:

- CSV parser
- quality scoring
- mock dialogue classifier
- mock loss detector
- mock follow-up generator
- verdict engine
- PII masking
- server-side decision journal

Cabinet:

- Run demo analysis
- Load sample CSV
- Analyze pasted/uploaded CSV
- Summary dashboard
- Recommended actions table
- allow / review / hold / block verdicts
- server-side human decision saving
- decision journal
- clear journal
- copy summary
- export actions CSV
- export journal CSV
- privacy badges

Prod checks:

- app.scripts.check_prod_ui
- app.scripts.smoke_prod

## Expected demo result

Run demo analysis:

total_dialogues = 10
recommended_actions_count = 7

Verdict breakdown:

allow = 3
review = 2
hold = 1
block = 1

Important rows:

d_006 = hold
d_010 = block

## Key demo flow

1. Open:
   https://froddy-lead-qa-froddy.amvera.io/cabinet?v=14

2. Click:
   Clear journal

3. Click:
   Run demo analysis

4. Show:
   Summary dashboard

5. Show:
   d_002 as slow response / allow

6. Show:
   d_003 or d_004 as incomplete context / review

7. Show:
   d_006 as conflict / hold
   Click Hold
   Show server decision saved

8. Show:
   d_010 as unsafe seller promise / block
   Click Block

9. Refresh page
   Click Run demo analysis again
   Show saved decisions mapped back to rows

10. Load sample CSV
    Analyze CSV
    Show same result

11. Export:
    Copy summary
    Export actions CSV
    Export journal CSV

## Privacy

PII masking is implemented before display/export for:

- phone
- email
- URL
- car plate

Privacy module:

api/app/privacy/pii.py

Test:

cd "D:\RCL\Avito\froddy-lead-qa\api"
python -m app.scripts.test_pii

## Server-side journal

Current storage:

data/decision_journal.jsonl

This is runtime data and should not be committed.

Journal module:

api/app/journal/store.py

Test:

cd "D:\RCL\Avito\froddy-lead-qa\api"
python -m app.scripts.test_journal

## Important commands

Local server:

cd "D:\RCL\Avito\froddy-lead-qa\api"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001

Local cabinet:

http://127.0.0.1:8001/cabinet

Inspect actions:

cd "D:\RCL\Avito\froddy-lead-qa\api"
python -m app.scripts.inspect_actions

Prod UI check:

cd "D:\RCL\Avito\froddy-lead-qa\api"
python -m app.scripts.check_prod_ui

Prod smoke test:

cd "D:\RCL\Avito\froddy-lead-qa\api"
python -m app.scripts.smoke_prod

Full local check before commit:

cd "D:\RCL\Avito\froddy-lead-qa\api"
python -m compileall app
python -m app.scripts.test_verdict
python -m app.scripts.test_pii
python -m app.scripts.test_journal
python -m app.scripts.inspect_actions

## Git workflow

Before commit:

git status --short
git --no-pager diff --check
git --no-pager diff

Use targeted git add only.
Do not use git add .

After push, Amvera UI may show stale "build running" status.
Truth source is:

cd "D:\RCL\Avito\froddy-lead-qa\api"
python -m app.scripts.check_prod_ui
python -m app.scripts.smoke_prod

## Current limitations

- synthetic CSV only
- no Avito API
- no auth
- no real LLM
- no database
- no auto-send
- no Telegram approvals
- MVP UI only
- server journal is JSONL
- no outcome feedback loop yet

## Recommended next steps

1. Add backend summary fields directly to API response:
   verdict_counts
   loss_type_counts
   manager_stats

2. Add simple auth / demo password before showing to outsiders.

3. Add sample CSV schema validation errors:
   missing columns
   empty dialogue_id
   unsupported side
   invalid timestamp

4. Add persistent SQLite storage:
   analyses
   actions
   decision_journal

5. Add outcome field:
   human decision -> later result
   e.g. recovered / lost / ignored / sent / not_sent

6. Add LLMClient abstraction later:
   default GPT-4.1-mini
   provider switch via env
   keep deterministic mode as fallback

7. Prepare real pilot CSV import from Avito/CRM export.
