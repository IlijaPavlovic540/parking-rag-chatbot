import os 
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts  import ChatPromptTemplate

from app.rag.vectorstore import get_weaviate_client, get_vectorstore

load_dotenv()

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
    "You are a parking assistant. Answer ONLY using the provided context. "
    "If the context does not contain the answer, say you don't gave that information."),
    ("user", "Question: \n {question}\n\nContext:\n{context}")
])

def rag_answer ( question:str,k:int = 5) -> tuple[str,list[str]]:
    client = get_weaviate_client()
    try:
        vs = get_vectorstore(client)
        retriever = vs.as_retriever(search_kwargs={"k":k})
        docs = retriever.invoke(question)

        context = "\n\n".join(
            [f"[{d.metadata.get('source','')}] {d.page_content}" for d in docs]
        ).strip()

        citations = sorted({d.metadata.get("source") for d in docs if d.metadata.get("source")})

        llm = ChatOpenAI(model=os.getenv("CHAT_MODEL","gpt-4o-mini"),temperature=0.2)
        chain = PROMPT | llm
        answer = chain.invoke({"question":question, "context":context}).content.strip()
        return answer,citations
    finally:
        client.close()