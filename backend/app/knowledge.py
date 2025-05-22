import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from agno.vectordb.pineconedb import PineconeDb
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
import hashlib

# Compute the .env path relative to this file’s location
base_dir = os.path.abspath(os.path.dirname(__file__))      # backend/app
project_root = os.path.dirname(os.path.dirname(base_dir))  # backend
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path) 

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")
index_name = os.getenv("PINECONE_INDEX")

# 2.2 Initialize Pinecone
pc = Pinecone(
    api_key=pinecone_api_key,
    environment=pinecone_env
)

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=pinecone_env)
    )
index = pc.Index(name=index_name)

class ListSentenceTransformerEmbedder:
    """
    Embedder wrapper around SentenceTransformer that returns Python lists
    and provides get_embedding_and_usage API for Agno.
    """
    def __init__(self, model_name: str):
        
        self._model = SentenceTransformer(model_name)

    def get_embedding_and_usage(self, text: str):

        embedding = self._model.encode(text)
        return embedding.tolist(), {}

    def get_embedding(self, text: str):
        embedding, _ = self.get_embedding_and_usage(text)
        return embedding

    def get_embeddings(self, texts: list[str]):
        return [self.get_embedding(text) for text in texts]


st_embedder = ListSentenceTransformerEmbedder("sentence-transformers/all-MiniLM-L6-v2")


def chunk_id_for(text: str, source: str) -> str:
    # e.g. SHA256(source_path + chunk_text)
    h = hashlib.sha256(f"{source}:{text}".encode("utf-8")).hexdigest()
    return h

class IdempotentPDFKnowledgeBase(PDFKnowledgeBase):
    def _make_document(self, page: int, chunk_text: str, metadata: dict):
        doc = super()._make_document(page, chunk_text, metadata)
        # override its .id before embedding/upsert
        doc.id = chunk_id_for(chunk_text, metadata.get("source", ""))
        return doc


vector_db = PineconeDb(
    name=index_name,                   
    dimension=384,                     
    metric="cosine",                    
    spec={                              
        "serverless": {
            "cloud": "aws",
            "region": pinecone_env
        }
    },
    api_key=pinecone_api_key,          
    environment=pinecone_env,           
    embedder=st_embedder,    
    namespace="agno"         
)

knowledge_base = IdempotentPDFKnowledgeBase(
    path="docs",
    vector_db=vector_db,
    reader=PDFReader(),
    num_documents=5,
    chunk_size=1000,      # characters per chunk
    chunk_overlap=200,    # overlap between chunks
)
knowledge_base.load(recreate=False, upsert=True)


# Utility to check empty index
def index_is_empty(vector_db) -> bool:
    stats = vector_db.client.describe_index_stats(
        index_name=vector_db.name,
        # If you’re using a namespace:
        namespace=vector_db.namespace
    )
    # pinecone returns a dict with 'namespaces': { ns: { 'vectorCount': ... } }
    ns_stats = stats.get("namespaces", {}).get(vector_db.namespace, {})
    return ns_stats.get("vectorCount", 0) == 0

if __name__ == "__main__":
    knowledge_base.load(recreate=False, upsert=True)
    print("Ingestion complete.")