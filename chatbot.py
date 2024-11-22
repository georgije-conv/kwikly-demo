from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, AsyncQdrantClient
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding


# make sure docker container is running before doing this
# run the docker container by doing:
# docker start qdrant_dev

client = QdrantClient(host="localhost", port=6333)

aclient = AsyncQdrantClient(host="localhost", port=6333)

vector_store = QdrantVectorStore(
    client=client,
    collection_name="kwikly_support_agent",
    aclient=aclient,
    enable_hybrid=True
)


# docstore = SimpleDocumentStore.from_persist_path(r"kwikly-docstore\docstore.json")
# documents_list = [doc_item for doc_item in docstore.docs.values()] # if we need the actual doc objects for later


Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

Settings.llm = OpenAI(model='gpt-4o-mini', temperature=0.3,
                      system_prompt="""You are an intelligent and supportive assistant specifically designed to help dental hygienists find temporary work and dental offices to discover available hygienists to meet their staffing needs. 
                      Your role is to provide accurate, helpful, and encouraging responses.
                      Welcome dental hygienists by understanding their skills and availability, helping them navigate job opportunities that suit their preferences.
                        Assist dental offices by helping them articulate their staffing needs and guiding them to potential candidates.
                        Use a friendly, professional tone to facilitate a welcoming environment where both parties feel valued and understood.
                        Ensure all interactions prioritize clarity, confidentiality, and professionalism.
                        Encourage users to ask questions and provide all the necessary information to ensure successful matches.
                        If possible, provide a link to your source so that the user knows you are telling the truth.
                        """)

index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
# index.storage_context.docstore = docstore

query_engine = index.as_query_engine(OpenAI(model='gpt-4o-mini', temperature=0), streaming=True)
response = query_engine.query(input("What is your question?"))
response.print_response_stream()
#"What day was 'title: Continuing Dental Education In The USA: Common Questions' scraped?"