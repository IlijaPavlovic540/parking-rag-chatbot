from app.core.guardrails import redact_pii

def test_redact_email():
    out = redact_pii("My email is test@example.com")
    assert "test@exampl.com" not in out

def test_redact_phone():
    out = redact_pii("Call me at +49 151 12345678")
    assert "+49 151 12345678" not in out