from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, AsyncQdrantClient
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv

load_dotenv()


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



Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large")

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

query_engine = index.as_query_engine(streaming=True)
response = query_engine.query("How quickly can I find temp work usually?")
response.print_response_stream()