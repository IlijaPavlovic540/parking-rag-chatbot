import os
from dotenv import load_dotenv

import weaviate
from weaviate.classes.init import Auth

from langchain_openai import OpenAIEmbeddings
from langchain_weaviate import WeaviateVectorStore

load_dotenv()

INDEX_NAME = "ParkingKB"
TEXT_KEY = "text"  # property in Weaviate that holds chunk text

def get_weaviate_client():
    return weaviate.connect_to_weaviate_cloud(
        cluster_url=os.environ["WEAVIATE_URL"],
        auth_credentials=Auth.api_key(os.environ["WEAVIATE_API_KEY"]),
    )

def get_embeddings():
    # Uses OPENAI_API_KEY from environment
    model = os.getenv("EMBED_MODEL", "text-embedding-3-small")
    return OpenAIEmbeddings(model=model)

def get_vectorstore(client):
    """
    LangChain VectorStore wrapper for Weaviate.
    - index_name must match the collection/class name in Weaviate.
    - text_key must match the property storing the raw text.
    """
    return WeaviateVectorStore(
        client=client,
        index_name=INDEX_NAME,
        text_key=TEXT_KEY,
        embedding=get_embeddings(),
    )