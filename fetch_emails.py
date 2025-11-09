import json
from sqlalchemy import select
from sqlalchemy.orm import Session
from db import engine
from models import Base, Email
from gmail import get_service, list_messages, get_message
from utils import get_header, convert_internaldate_to_datetime, extract_plain_text

Base.metadata.create_all(engine)

with open('config.json','r') as f:
    cfg = json.load(f)

service = get_service()
max_fetch = int(cfg.get('max_fetch', 100))

fetched = 0
page_token = None

with Session(engine) as session:
    while fetched < max_fetch:
        resp = list_messages(service, max_results=min(100, max_fetch - fetched), page_token=page_token)
        msgs = resp.get('messages', [])
        if not msgs:
            break
        for m in msgs:
            gmail_id = m['id']
            exists = session.execute(select(Email).where(Email.gmail_id == gmail_id)).scalar_one_or_none()
            if exists:
                continue
            full = get_message(service, gmail_id, fmt='full')
            payload = full.get('payload', {})
            headers = payload.get('headers', [])
            sender = get_header(headers, 'From')
            to = get_header(headers, 'To')
            subject = get_header(headers, 'Subject')
            snippet = full.get('snippet', '')
            received = convert_internaldate_to_datetime(full.get('internalDate'))
            body = extract_plain_text(payload)

            row = Email(gmail_id=gmail_id, thread_id=full.get('threadId'), sender=sender, to=to, subject=subject, snippet=snippet, body=body, received=received)
            session.add(row)
        session.commit()
        fetched += len(msgs)
        page_token = resp.get('nextPageToken')
        if not page_token:
            break

print(f'Emails Fetched & stored')
