# Gmail Rule-Based Processor (Standalone)

Implements: OAuth auth, fetch inbox via Gmail **REST API**, store in RDBMS (SQLite),
rule engine with Any/All predicates over From/Subject/Message/Received date, and actions:
mark read/unread, move message (labels).

## Demo Video
Filename: **demo.mp4**

## Prerequisites
- Enable Gmail API in Google Cloud; create OAuth 2.0 Client (Desktop) and place `client_secret.json` in repo root.
- Python 3.10+

## Install
```bash
pip install -r requirements.txt
```

## Authenticate (one-time)
```bash
python auth.py
```
This opens a browser; after consent a `token.json` is saved.

## Configure
`config.json`:
```json
{
  "database_url": "sqlite:///emails.db",
  "max_fetch": 100,
  "default_move_label": "Processed"
}
```

## Fetch (uses Gmail REST)
```bash
python fetch_emails.py
```

## Define rules
`rules.json`:
```json
{
  "predicate": "All",
  "rules": [
    { "field": "from", "predicate": "contains", "value": "@gmail.com" },
    { "field": "subject", "predicate": "contains", "value": "swiggy" },
    { "field": "received", "predicate": "less_than_days", "value": 1 }
  ],
  "actions": [
    "mark_read",
    { "move": "Processed" }
  ]
}
```

Supported fields: `from`, `to`, `subject`, `message`, `received`.
String predicates: `contains`, `does_not_contain`, `equals`, `does_not_equal`.
Date predicates: `less_than_days`, `greater_than_days`, `less_than_months`, `greater_than_months`.
Collection predicate: `All` or `Any`.
Actions: `mark_read`, `mark_unread`, `{ "move": "LabelName" }`.

## Process rules (acts via Gmail REST)
```bash
python process_rules.py
```

## Tests
```bash
python -m pytest -q
```
