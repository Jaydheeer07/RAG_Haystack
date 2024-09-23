# ingestion.py
from haystack import Pipeline
from haystack.components.converters import PyPDFToDocument
from haystack.components.embedders import OpenAIDocumentEmbedder
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.utils import Secret
from .config import EMBEDDING_MODEL, OPENAI_API_KEY

def create_ingestion_pipeline(document_store):
    converter = PyPDFToDocument()
    cleaner = DocumentCleaner()
    splitter = DocumentSplitter(split_by='word', split_length=250, split_overlap=25)
    embedder = OpenAIDocumentEmbedder(
        api_key=Secret.from_token(OPENAI_API_KEY),
        model=EMBEDDING_MODEL
    )
    writer = DocumentWriter(document_store=document_store)

    pipeline = Pipeline()
    pipeline.add_component("converter", converter)
    pipeline.add_component("cleaner", cleaner)
    pipeline.add_component("splitter", splitter)
    pipeline.add_component("embedder", embedder)
    pipeline.add_component("writer", writer)

    pipeline.connect("converter", "cleaner")
    pipeline.connect("cleaner", "splitter")
    pipeline.connect("splitter", "embedder")
    pipeline.connect("embedder", "writer")

    return pipeline

def ingest_document(pipeline, file_path):
    results = {"converter": {"sources": [file_path]}}
    return pipeline.run(results)