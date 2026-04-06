from app.evaluation.metrics import recall_at_k, precision_at_k

def test_recall_hit():
    assert recall_at_k(["prices.md","rules.md"], {"prices.md"}) ==1.0

def test_recall_miss():
    assert recall_at_k(["rules.md"], {"prices.md"}) == 0.0

def test_precision_basic():
    assert precision_at_k(["a.md","b.md"], {"b.md"}) == 0.5

def test_precision_empty():
    assert precision_at_k([], {"a.md"}) == 0.0