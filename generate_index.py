from llama_index.core import (
    Settings,
    VectorStoreIndex,
    StorageContext,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.storage.docstore import SimpleDocumentStore
from qdrant_client import QdrantClient, AsyncQdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()

# Set the default embedding and large language models.
Settings.llm = OpenAI(model='gpt-4o-mini', temperature=0.1,
                      system_prompt="""
                      You are a helpful bot that answers questions for:
                        a) dental hygienists looking for temp work.
                        b) dental offices looking for temp dental hygienists
                      """)

Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large")

# Load the documents that are saved to disk
docstore = SimpleDocumentStore.from_persist_dir(persist_dir="kwikly-docstore")
documents_list = list(docstore.docs.values())

# Instantiate the Qdrant client
# Note: Make sure the qdrant docker container is running (3ad075461275 is ID)
client = QdrantClient(host="localhost", port=6333)

aclient = AsyncQdrantClient(host="localhost", port=6333)

vector_store = QdrantVectorStore(
    client=client,
    collection_name="kwikly_support_agent",
    aclient=aclient,
    enable_hybrid=True
)

# Set the storage_context
storage_context = StorageContext.from_defaults(docstore=docstore, vector_store=vector_store)

Settings.chunk_size = 512
Settings.chunk_overlap = 64

index = VectorStoreIndex.from_documents(documents=documents_list,
                                        storage_context=storage_context,
                                        show_progress=True
                                        )


