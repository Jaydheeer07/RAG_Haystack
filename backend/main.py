# main.py
from document_store import initialize_document_store
from ingestion import create_ingestion_pipeline
from retrieval import create_retrieval_pipeline

document_store = initialize_document_store()
ingestion_pipeline = create_ingestion_pipeline(document_store)
retrieval_pipeline = create_retrieval_pipeline(document_store)

# Example usage
# ingest_document(ingestion_pipeline, "path/to/document.pdf")
# answer = query_documents(retrieval_pipeline, "Your question here")
# print(answer)
