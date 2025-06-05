import random
from ..graph.vector_store import VectorStore

class WorldBuilder:
    def __init__(self):
        self.vector_store = VectorStore()
    
    def generate_map(self):
        """Procedurally generate a map."""
        map_data ={
            "regions": ["Forest of Eld", "Mountains of Zor", "Plains of Vyr"],
            "connections": [("Forest of Eld", "Mountains of Zor"), ("Mountains of Zor", "Plains of Vyr")]
        }
        self.vector_store.store("map", map_data)
        return map_data
    
    