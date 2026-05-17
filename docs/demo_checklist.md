# Froddy Lead QA — demo checklist

## Demo URL

https://froddy-lead-qa-froddy.amvera.io/cabinet

## Pre-demo checks

Run:

cd "D:\RCL\Avito\froddy-lead-qa\api"

python -m app.scripts.check_prod_ui
python -m app.scripts.smoke_prod

Expected:

Prod UI deploy check passed
Smoke test passed

## Pre-demo reset

1. Open:
   https://froddy-lead-qa-froddy.amvera.io/cabinet?v=14

2. Click:
   Clear journal

3. Expected:
   - Status briefly shows: Journal cleared
   - Then returns to: Ready
   - Decision journal is empty

## Main demo flow

1. Click:
   Run demo analysis

2. Expected:
   - Dialogues: 10
   - Recommended actions: 7
   - Allow: 3
   - Review: 2
   - Hold: 1
   - Block: 1

## Positioning

BotB2B is the executor in the chat.
Froddy Lead QA is the dispatcher/auditor above executors.

Froddy Lead QA is not an Avito bot.
It is a QA/control layer over managers and bots: it finds lost leads, suggests actions, assigns verdicts, and records human decisions.

## Key rows

### d_002 — slow response

- classification: warm_lead
- loss_type: brutal_loss
- verdict: allow
- meaning: safe soft follow-up

### d_003 / d_004 — incomplete context

- verdict: review
- meaning: human should check before sending

### d_006 — conflict

- verdict: hold
- click: Hold
- expected: server decision saved
- refresh page
- click Run demo analysis again
- expected: Server: hold remains

### d_010 — unsafe seller promise

- verdict: block
- reason: seller promised discount / deadline without approval
- click: Block

## Decision journal

Show:

- human decisions are saved server-side
- refresh page
- click Run demo analysis again
- saved decisions are mapped back to rows

## CSV demo

1. Click:
   Load sample CSV

2. Click:
   Analyze CSV

3. Expected:
   - Dialogues: 10
   - Recommended actions: 7

## Privacy point

Show badges:

- PII masked before display/export
- Phone / email / URL / car plate redaction
- Local decision journal

Optional proof:

- paste CSV containing phone/email/link/car plate
- analysis output should show [PHONE], [EMAIL], [URL], [CAR_PLATE]

## Export

After decisions:

1. Click:
   Copy summary

2. Click:
   Export actions CSV

3. Click:
   Export journal CSV

## Current limitations

- Synthetic CSV demo data only
- No Avito API integration
- No auto-send
- No real LLM yet
- Server-side journal is JSONL, not database
- MVP cabinet, not final UI
