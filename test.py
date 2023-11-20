
import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
import pandas as pd
import uuid
load_dotenv()
AUTH = os.getenv('AUTHTOKEN')


client = chromadb.HttpClient(
                            host='https://lucy-lmbi.koyeb.app/', 
                            port=8000,
                            settings=Settings(
                            chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
                            chroma_client_auth_credentials=AUTH
                                )
                            )

collection = client.get_collection("artikel")

df = pd.read_csv("your_output_file.csv")


myuuid = uuid.uuid4()
collection.add(
        documents=[str(i) for i in df["Artikelname"]], # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
        metadatas=[{ "Gang": i } for i in df["Gang"]], # filter on these!
        ids=[str(uuid.uuid4()) for _ in range(0,len(df["Gang"]))], # unique for each doc
    )

#results = client.collection.query(
#                                    query_texts=["Bratwürstchen"],
#                                    n_results=1,
#                                    #where={"metadata_field": "document1"}, # optional filter
#                                    #where_document={"$contains": "nuts"} # optional filter
#                            )

"""collection = client.list_collections()
print(collection)"""

"""results = collection.query(
                                    query_texts=["Bockwürstschen"],
                                    n_results=1,
                                    #where={"metadata_field": "document1"}, # optional filter
                                    #where_document={"$contains": "nuts"} # optional filter
                            )
print(results)"""