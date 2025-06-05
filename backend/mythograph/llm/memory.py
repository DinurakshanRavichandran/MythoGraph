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
    def __init__(self, max_capacity=1000, decay_factor=0.95):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = faiss.IndexFlatL2(384)
        self.memory_buffer = deque(maxlen=max_capacity)
        self.decayfactor = decay_factor
        self.importance_threshold = 0.2

        #Temportal context tracking 
        self.time_scale = 1.0 # = realtime, > 1.0 = compressed time


    def _get_embedding(self,  text: str) -> np.ndarray:
        return self.model.encode(text, convert_to_tensor=False)

    def add_memory(self, memory: MemoryItem):
        #calculate dynamic improtance based on decay
        memory.importance = self._caculate_decay(memory.timestamp)

        #Add to Faiss index if semantically important
        if memory.importance > self.importance_threshold:
            embedding = self._get_embedding(memory.content)
            self.index.add(np.array([embedding]))

        self.memory_buffer.append(memory)
    
    def search(self, query: str, temporal_context: datetime = None, n_results: int = 5) -> List[MemoryItem]:
        #Semantic search
        query_embed = self._get_embedding(query)
        _, indices = self.index.search(np.array(np.array([query_embed]), n_results))

        #Temporal relevance
        results = []
        for idx in indices[0]:
            if idx < len(self.memory_buffer)
                mem = self.memeory_buffer[idx]
                time_weight = self._time_decay(mem, temporal_context)
                relevance = (0.6 * mem.importance + 0.3 * time_weight + 0.1 * mem.emotional_weight)
                results.append((relevance,mem))

        #sort by combined relevance
        return [mem for _, mem in heapq.nlargest(n_results, results)]


    def calculate_decay(self, timestamp: datetime) -> float:
        time_diff = (datetime.now() - timestamp).total_seconds()
        return np.exp(-self.decayfactor * time_diff/3600) #3600
    
    def time_decay(self, memory: MemoryItem, context_time: datetime) -> float:
        if not context_time:
            return 1.0
        time_diff = (context_time - memory.timestamp).total_seconds()
        return 1/ (1 + np.sqrt(time_diff / 3600))


    def consolidate_memories(self):
        ...
    
    def save_state(self, file_path: str):
        ...
    
    def load_state(self, file_path: str):
        ...
    
    