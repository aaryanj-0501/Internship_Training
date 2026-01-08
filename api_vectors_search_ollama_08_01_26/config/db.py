import os
from qdrant_client import QdrantClient

qdrant_url=os.getenv("QDRANT_URL")
client=QdrantClient(url=qdrant_url)
