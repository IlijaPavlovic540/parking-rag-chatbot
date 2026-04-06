import json
import statistics
from typing import Dict, List, Set


from app.rag.vectorstore import get_weaviate_client, get_vectorstore
from app.evaluation.metrics import recall_at_k, precision_at_k


def load_questions(path: str):
    with open(path,"r", encoding = "utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def evaluate(path = "data/static_kb/eval/questions.jsonl", k_vaules = (3,5,10))->Dict[int, dict]:
    client = get_weaviate_client()

    try:
        vs = get_vectorstore(client)
        results : Dict[int, Dict[str,List[float]]]= {k:{"recall":[], "precision":[]} for k in k_vaules}


        for item in load_questions(path):
            q: str = item ["q"]
            gold: Set[str] = set (item["gold_sources"])

            for k in k_vaules:
                retriever = vs.as_retriever(search_kwargs = {"k":k})
                docs = retriever.invoke(q)

                retrieved_sources = [d.metadata.get("source", "") for d in docs]
                results[k]["recall"].append(recall_at_k(retrieved_sources, gold))
                results[k]["precision"].append(precision_at_k(retrieved_sources, gold))


        summary = {}
        for k in k_vaules:
            summary[k] = {
                "n": len(results[k]["recall"]),
                "recall@k_mean": statistics.mean(results[k]["recall"]) if results[k]["recall"] else 0.0,
                "precision@k_mean": statistics.mean(results[k]["precision"]) if results[k]["precision"] else 0.0,

            }

        return summary

    finally:
        client.close()
if __name__ == "__main__":
    s = evaluate()
    for k,v in s.items():
        print(f"k={k}  recall@k ={v['recall@k_mean']:.3f} precision@k={v['precision@k_mean']:.3f} n={v['n']}")