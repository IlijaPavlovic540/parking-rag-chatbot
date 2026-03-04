import time 

from app.rag.vectorstore import get_weaviate_client, get_vectorstore
from app.rag.rag_service import rag_answer

QUESTIONS =[
    "Where is the parking located?",
    "What are the standard rates?",
    "How do I reserve a spot?",
    "What are customer support hours?",
    "What is the max vehicle height allowed?",
]

def percentile ( values , p:float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    idx = int(round((p/100.0)*(len(values)-1)))
    return values[idx]

def main ( n = 30 , k = 5):
    retrieval_ms = []
    e2e_ms = []
    client = get_weaviate_client()

    try:
        vs = get_vectorstore ( client )
        retriever = vs.as_retriever(search_kwargs={"k":k})

        for i in range ( n ):
            q = QUESTIONS[i % len(QUESTIONS)]
            t0 = time.perf_counter()
            _docs = retriever.invoke(q)
            t1 = time.perf_counter()
            retrieval_ms.append((t1-t0) * 1000)

            t2 = time.perf_counter()
            _ans,_cities = rag_answer(q, k=k)

            t3 = time.perf_counter()
            e2e_ms.append((t3-t2)*1000)

        print(f"Retrieval lateancy ms: p50 ={percentile(retrieval_ms,50):.1f} p95={percentile(retrieval_ms,95):.1f}")
        print(f"RE2E latency ms:       p50 ={percentile(e2e_ms,50):.1f} p95={percentile(e2e_ms,95):.1f}")
    finally:
        client.close()

if __name__ == "__main__":
    main()