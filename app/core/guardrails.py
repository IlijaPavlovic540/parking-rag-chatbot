import re
from dataclasses import dataclass
from typing import Optional

from presidio_analyzer import AnalyzerEngine, RecognizerRegistry, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine

_BLOCK_PATTERNS = [
r"\b(system prompt|developer message|hidden instructions)\b",
r"\b(dump|export|leak)\b.*\b(database|vector|weaviate|embeddings)\b",
r"\b(list|show)\b.*\b(all reservations|all users|all customers)\b",
r"\b(api key|secret|token)\b",
]

@dataclass
class GuardrailDecision:
    allowed: bool
    reason: Optional[str] = None

def policy_check(user_text: str ) ->GuardrailDecision:
    text = user_text.lower()
    for pat in _BLOCK_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            return GuardrailDecision(
                allowed=False,
                reason="I cant help with requests for private/system data."
            )
    return GuardrailDecision(allowed= True)


#--- PII redaction usning Presidio ( pre - trained NLP) ---

_analyzer = AnalyzerEngine()
_anonymizer = AnonymizerEngine()

def _register_car_plate_recognizer():
    # Simple EU - style plate patterns; 

    patterns = [
        Pattern(name="plate1", regex=r"\b[A-Z]{1,3}-[A-Z]{1,2}\s?\d{1,4}\b", score=0.6),
        Pattern(name="plate2", regex=r"\b[A-Z]{2}\s?\d{3,4}\s?[A-Z]{2}\b", score=0.6),
    ]
    recognizer = PatternRecognizer(
        supported_entity="CAR_PLATE",
        patterns = patterns,
    )
    registry = RecognizerRegistry()
    registry.load_predefined_recognizers()
    registry.add_recognizer(recognizer)
    _analyzer.registry=registry

_register_car_plate_recognizer()


def redact_pii(text: str)-> str:
    if not text:
        return text
    
    results = _analyzer.analyze(
        text=text,
        language="en",
        entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "LOCATION", "CAR_PLATE"],
    )
    anon = _anonymizer.anonymize(text=text,analyzer_results=results)
    return anon.text