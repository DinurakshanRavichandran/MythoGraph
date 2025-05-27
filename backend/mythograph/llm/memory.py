from datetime import datetime
import numpy as np
from sentence_transformers import SentenceTransformer #to convert sentences into vector representations
from typing import List, Dict, Any #used to import type hints from python 
import json #for json serialization
import heapq #for priority queue
from collections import deque #deque is a list-like container with fast appends and pops on either end
import faiss #facebook's efficient similarity search library 

class MemoryItem:
    def __init__(self, content: str, memory_type: str, importance: float = 0.5):
        self.timestamp = datetime.now()
        self.content = content
        self.memory_type = memory_type #episodic, semantic, flashbulb, procdural, etc.
        self.importance = max(0.0, min(1.0, importance)) # Ensure importance is between 0 and 1
        self.last_accessed = datetime.now()
        self.vector = None

        #cognitive properties 
        self.emotional_weight = 1.0
        self.associative_links = []   # List of MemoryItem IDs that are associated with this item

class vector_memory:
    def _get_embedding(self,  text: str) -> np.ndarray:
        ...

    def add_memory(self, memory: MemoryItem):
        ...
    
    def search(self, query: str, temporal_context: datetime = None, n_results: int = 5) -> List[MemoryItem]:
        ...

    def calculate_decay(self, timestamp: datetime) -> float:
        ...
    
    def time_decay(self, memory: MemoryItem, context_time: datetime) -> float:
        ...

    def consolidate_memories(self):
        ...
    
    def save_state(self, file_path: str):
        ...
    
    def load_state(self, file_path: str):
        ...
    
    