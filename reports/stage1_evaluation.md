# Stage 1 Evaluation Report - Parking RAG Chatbot


## Retrieval accuracy

Command: 'python -m app.evaluation.retrieval_eval'

- Recall@3: <1.000>
- Precision@3:<0.400>
- Recall@5: <1.000>
- Precision@5:<0.240>
- Recall@10: <1.000>
- Precision@10:<0.200>


## Performance ( latency )
Command: 'python -m app.evaluation.latency_test'
- Retrieval p50/p95 (ms): <233.6/1207.5>
- End-to-end p50/p95 (ms): <3406.5/4294.6>


## Notes
- Static KB stored in weaviate ( ParkingKB )
- Retrieval via Langchain Weaviate VectorStore
- LLM answers are grounded using retrieved context