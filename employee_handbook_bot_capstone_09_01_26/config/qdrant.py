from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()
qdrant_url = os.getenv('QDRANT_URL')
qdrant_api_key = os.getenv('QDRANT_API_KEY')

qdrant_client = QdrantClient(
    url=qdrant_url, 
    api_key=qdrant_api_key,
)

