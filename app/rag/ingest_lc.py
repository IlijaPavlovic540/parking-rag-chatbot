
from pathlib import Path
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.vectorstore import get_weaviate_client, get_vectorstore, INDEX_NAME

load_dotenv()

def load_markdown_docs() -> list[Document]:
    kb_dir = Path("data/static_kb")
    if not kb_dir.exists():
        raise SystemExit("Missing folder: data/static_kb")

    docs: list[Document] = []
    for p in kb_dir.glob("*.md"):
        docs.append(
            Document(
                page_content=p.read_text(encoding="utf-8"),
                metadata={"source": p.name},
            )
        )
    if not docs:
        raise SystemExit("No .md files found in data/static_kb")
    return docs

def main():
    docs = load_markdown_docs()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    client = get_weaviate_client()
    try:
        vs = get_vectorstore(client)

        # Optional: clean re-ingest (recommended once to be consistent)
        # If you don't want deletion, comment these two lines out.
        # --- clean start ---
        client = vs._client

        if client.collections.exists(INDEX_NAME):
            client.collections.delete(INDEX_NAME)
        # --- clean start ---

        vs.add_documents(chunks)
        print(f"✅ LangChain ingested {len(chunks)} chunks into Weaviate index '{INDEX_NAME}'")
    finally:
        client.close()

if __name__ == "__main__":
    main()
