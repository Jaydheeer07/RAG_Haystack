# config.py
import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DOCUMENT_STORE_INDEX = "Documents"
EMBEDDING_MODEL = "text-embedding-3-small"
GENERATION_MODEL = "gpt-4-1106-preview"