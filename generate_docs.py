from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core.storage.docstore import SimpleDocumentStore


# Generate Document objects from the scraped markdown files.
text_corpus_path = "kwikly_scraper/kwikly_scraper/output"

# Instantiate the reader and generate list of documents
simple_reader = SimpleDirectoryReader(input_dir=text_corpus_path, recursive=True)
documents_list = simple_reader.load_data(show_progress=True)

# Instantiate docstore and add values
docstore = SimpleDocumentStore()
docstore.add_documents(documents_list)

# Persist the docstore to disk
storage_context = StorageContext.from_defaults(docstore=docstore)
storage_context.persist(persist_dir="kwikly-docstore")


