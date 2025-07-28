from langchain_ollama import OllamaEmbeddings
from llama_index.core.settings import Settings
import glob
import os
from datetime import datetime
from langchain_chroma import Chroma
from langchain_core.documents import Document

def setup_obsidian():
    """
    Sets up and returns a `query engine` object to then query obsidian

    Args: 
        llm (any): LLM object that's going to be used 
    
    Return:
        BaseQueryEngine: Query Engine to utilize
    """
    vault_path = "/Users/patelpratham11/Documents/Pratham"
    embedding_model = "mxbai-embed-large"

    # === EMBEDDINGS ===
    # Settings.embed_model = OllamaEmbedding(model_name=embedding_model)

    # === LOAD OR BUILD INDEX ===
    # if os.path.exists(storage_path):
    #     print("📦 Loading index from storage...")
    #     storage_context = StorageContext.from_defaults(persist_dir=storage_path)
    #     index = load_index_from_storage(storage_context, llm=llm)
    # else:
    #     print("🛠 Building index from markdown files...")
    #     documents = SimpleDirectoryReader(
    #         vault_path, recursive=True, required_exts=[".md"]
    #     ).load_data()
    #     index = VectorStoreIndex.from_documents(documents, llm=llm)
    #     index.storage_context.persist(persist_dir=storage_path)

    # query_engine = index.as_query_engine(llm=llm)
    # return query_engine


    embeddings = OllamaEmbeddings(model=embedding_model)

    db_location = "./chrome_langchain_db"
    add_documents = not os.path.exists(db_location)

    if add_documents:
        documents = []
        ids = []

        # Get all .md files in the vault recursively
        md_files = glob.glob(os.path.join(vault_path, "**/*.md"), recursive=True)

        for i, file_path in enumerate(md_files):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                file_stat = os.stat(file_path)
                modified_time = datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                file_title = os.path.splitext(os.path.basename(file_path))[0]

                document = Document(
                    page_content=content,
                    metadata={
                        "title": file_title,
                        "path": file_path,
                        "modified": modified_time
                    },
                    id=str(i)
                )
                documents.append(document)
                ids.append(str(i))
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")

            
    vector_store = Chroma(
        collection_name="obsidian_vault",
        persist_directory=db_location,
        embedding_function=embeddings
    )

    if add_documents:
        vector_store.add_documents(documents=documents, ids=ids)
        
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 5}
    )

    return retriever