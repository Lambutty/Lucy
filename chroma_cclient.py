from enum import Enum
from spots import Spots
import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings

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


class ChromaCClient: 
    
    
    def __init__(self,*,
                 ) -> None:
