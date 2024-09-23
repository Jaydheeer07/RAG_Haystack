# document_store.py
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore
from qdrant_client.http.exceptions import UnexpectedResponse
from .config import QDRANT_URL, DOCUMENT_STORE_INDEX

def initialize_document_store():
    try:
        return QdrantDocumentStore(
            url=QDRANT_URL,
            index=DOCUMENT_STORE_INDEX,
            recreate_index=False,
            return_embedding=True,
            wait_result_from_api=True,
            embedding_dim=1536,
            timeout=60
        )
    except UnexpectedResponse as e:
        if "Not found: Collection 'Documents' doesn't exist" in str(e):
            return QdrantDocumentStore(
                url=QDRANT_URL,
                index=DOCUMENT_STORE_INDEX,
                recreate_index=True,
                return_embedding=True,
                wait_result_from_api=True,
                embedding_dim=1536,
                timeout=60
            )
        raise