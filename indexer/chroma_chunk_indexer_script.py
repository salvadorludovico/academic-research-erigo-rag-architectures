import os
from dotenv import load_dotenv
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_chroma import Chroma
import pandas as pd
# from langchain_community.docstore.document import Document -> Inserting without metadata

CHROMA_BATCH_DOCS_LIMIT = 5400;

load_dotenv()

SERVICE_ACCOUNT_PATH = os.getenv("SERVICE_ACCOUNT_PATH")
if SERVICE_ACCOUNT_PATH:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_PATH

case = "rinvest"
persist_directory = f'../data/chroma/{case}'
project_id = "energygpt-421317"
model_name = "text-multilingual-embedding-002"
csv_path = f'../data/csv_chunks/{case}.csv'

def load_csv_to_documents(csv_path):
    df = pd.read_csv(csv_path)
    documents = [row['conteudo'] for index, row in df.iterrows()]
    return documents

def create_vector_store():
    vector_store = Chroma(
        collection_name=case,
        persist_directory=persist_directory,
        embedding_function=VertexAIEmbeddings(model_name=model_name)
    )
    return vector_store

def add_chunks_in_batches(vector_store, chunks, batch_size):
    total_batches = (len(chunks) + batch_size - 1) // batch_size
    print(f"---->Dividindo os chunks em {total_batches} lotes.")
    
    for i in range(total_batches):
        start = i * batch_size
        end = start + batch_size
        batch = chunks[start:end]
        
        print(f"Inserindo lote {i + 1}/{total_batches}")
        vector_store.add_texts(batch)
        

print (f"---->Carregando chunks do CSV\n")
chunks = load_csv_to_documents(csv_path)
print (f"-> {len(chunks)} chunks carregados\n")

print (f"---->Criando vectorstore local em {persist_directory}\n")
vector_store = create_vector_store()

add_chunks_in_batches(vector_store, chunks, CHROMA_BATCH_DOCS_LIMIT)
print (f"---->Chunks inseridos no vectorstore com sucesso\n")

