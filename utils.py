from base64 import urlsafe_b64decode

def get_header(headers, name, default=''):
    for h in headers:
        if h.get('name', '').lower() == name.lower():
            return h.get('value', default)
    return default

def convert_internaldate_to_datetime(internal_ms):
    return None if internal_ms is None else __import__('datetime').datetime.fromtimestamp(int(internal_ms)/1000)

def extract_plain_text(payload):
    #Extract plain text content from a Gmail message payload
    def extract_from_part(part):
        mime = part.get('mimeType', '')
        if mime == 'text/plain' and part.get('body', {}).get('data'):
            data = part['body']['data']
            try:
                return urlsafe_b64decode(data.encode('utf-8')).decode('utf-8', errors='replace')
            except Exception:
                return ''
        for child in part.get('parts', []) or []:
            txt = extract_from_part(child)
            if txt:
                return txt
        return ''

    if not payload:
        return ''
    return extract_from_part(payload)
