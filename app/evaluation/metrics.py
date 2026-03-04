from __future__ import annotations
from typing import Iterable, Set

def recall_at_k(retrieved_sources: Iterable[str], gold_sources: Set [str])-> float:
    """Doc - level Recall@K: 1 if any gold source appears in treieved results, esle 0"""
    rset = {s for s in retrieved_sources if s}
    return 1.0 if (rset & gold_sources) else 0.0


def precision_at_k(retrieved_sources: Iterable[str], gold_sources: Set [str]) -> float:
    """Doc-level Precision@k: fraction of unique retrieved sources that are gold."""
    rset = {s for s in retrieved_sources if s}
    if not rset:
        return 0.0
    return len(rset & gold_sources) / len(rset)