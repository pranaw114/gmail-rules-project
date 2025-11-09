import json
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from db import engine
from models import Email
from gmail import get_service, get_or_create_label, modify_message_labels

with open('rules.json','r') as f:
    RULES = json.load(f)

service = get_service()

def match_predicate(email: Email, rule: dict) -> bool:
    field = rule['field']
    pred = rule['predicate']
    val = rule['value']

    # if field == 'received':
    #     if not email.received:
    #         return False
    now = datetime.now()
    if pred == 'less_than_days':
        return (now - email.received) < timedelta(days=int(val))
    if pred == 'greater_than_days':
        return (now - email.received) > timedelta(days=int(val))
    if pred == 'less_than_months':
        return (now - email.received) < timedelta(days=30*int(val))
    if pred == 'greater_than_months':
        return (now - email.received) > timedelta(days=30*int(val))
        # return False

    source = ''
    if field == 'from':
        source = email.sender or ''
    elif field == 'to':
        source = email.to or ''
    elif field == 'subject':
        source = email.subject or ''
    elif field == 'message':
        source = (email.body or email.snippet or '')

    s = source.lower()
    v = str(val).lower()

    if pred == 'contains':
        return v in s
    if pred == 'does_not_contain':
        return v not in s
    if pred == 'equals':
        return s == v
    if pred == 'does_not_equal':
        return s != v
    return False

def matches(email: Email, spec: dict) -> bool:
    preds = [match_predicate(email, r) for r in spec.get('rules', [])]
    mode = (spec.get('predicate') or 'All').lower()
    return all(preds) if mode == 'all' else any(preds)

with Session(engine) as session:
    emails = session.execute(select(Email)).scalars().all()
    for e in emails:
        if not matches(e, RULES):
            continue
        for action in RULES.get('actions', []):
            if action == 'mark_read':
                modify_message_labels(service, e.gmail_id, add=[], remove=['UNREAD'])
            elif action == 'mark_unread':
                modify_message_labels(service, e.gmail_id, add=['UNREAD'], remove=[])
            elif isinstance(action, dict) and 'move' in action:
                label_id = get_or_create_label(service, action['move'])
                modify_message_labels(service, e.gmail_id, add=[label_id], remove=[])

print('Rules applied via Gmail REST API.')
