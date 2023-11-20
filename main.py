from chroma import ChromaDB
from warehouse_assistant import WarehouseAssistant
from dotenv import load_dotenv
import chromadb
import os
from chromadb.config import Settings

def main():

    database = ChromaDB()
    

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
    collection = client.get_collection('artikel')
    assistant = WarehouseAssistant(
        
        agent_name="Maxi",
        collection=collection,
        debug=True,
        insult="kleiner Lappen",
        listen_for_tick_duration=14,
        )

    assistant.run()

if __name__ == "__main__":
    main()