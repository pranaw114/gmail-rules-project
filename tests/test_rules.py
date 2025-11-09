from datetime import datetime, timedelta
from types import SimpleNamespace as E
from process_rules import match_predicate, matches

now = datetime.now()

def test_string_contains():
    e = E(sender='demo@gmail.com', to='', subject='The best of this week ', snippet='', body='', received=now)
    assert match_predicate(e, {"field":"from","predicate":"contains","value":"demo1@gmail.com"})

def test_date_predicate():
    e = E(sender='', to='', subject='', snippet='', body='', received=now - timedelta(days=10))
    assert match_predicate(e, {"field":"received","predicate":"less_than_days","value":30})

def test_matches_all():
    e = E(sender='demo@gmail.com', to='', subject='Invoice June', snippet='body', body='body', received=now)
    spec = {"predicate":"All","rules":[
        {"field":"from","predicate":"contains","value":"demo1@gmail.com"},
        {"field":"subject","predicate":"contains","value":"Invoice"}
    ]}
    assert matches(e, spec) is True
