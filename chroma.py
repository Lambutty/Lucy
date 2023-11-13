import chromadb
from enum import Enum
from spots import Spots
from chromadb.config import Settings



class ChromaDB: 
    
    DEFAULTNAME = "collection"
    __slots__ = ["collection_name","documents","metadatas","ids", 
                "client","collection"]
    
    def __init__(self,*,
                 persistent: bool = False, collection_name: str = DEFAULTNAME,
                 documents:list = None,
                 metadatas: list[dict] = None,
                 ids: list[str] = None  
                 ) -> None:
        self.collection_name = collection_name
        self.documents = documents
        self.metadatas = metadatas
        self.ids = ids
        self.client = chromadb.PersistentClient() if persistent else chromadb.EphemeralClient()
        # TODO: Implemented proper persistent mode
        if not persistent:
            self.collection = self.client.create_collection(collection_name)
            self.collection.add(
                    documents=["Metten Bratwürstchen", "Metten Bockwürstchen", "Metten"], # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
                    metadatas=[{ Spots.GANG.value: "9" }, { Spots.GANG.value: "7" },{ Spots.GANG.value: "12" }], # filter on these!
                    ids=["1", "2", "3"], # unique for each doc
                )
            
        
