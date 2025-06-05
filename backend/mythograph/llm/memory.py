from datetime import datetime
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import json
import heapq
from collections import deque
import faiss

class MemoryItem:
    def __init__(self, content: str, memory_type: str, importance: float = 0.5):
        self.timestamp = datetime.now()
        self.content = content
        self.memory_type = memory_type  # episodic, semantic, flashbulb, procedural, etc.
        self.importance = max(0.0, min(1.0, importance))  # Ensure importance is between 0 and 1
        self.last_accessed = datetime.now()
        self.vector = None
        self.id = id(self)  # Unique ID for associative links

        # Cognitive properties
        self.emotional_weight = 1.0
        self.associative_links = []  # List of MemoryItem IDs that are associated with this item

class vector_memory:
    def __init__(self, max_capacity=1000, decay_factor=0.95):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = faiss.IndexFlatL2(384)  # 384 is the dimension of 'all-MiniLM-L6-v2'
        self.memory_buffer = deque(maxlen=max_capacity)
        self.decay_factor = decay_factor
        self.importance_threshold = 0.2
        self.id_to_memory = {}  # Map FAISS index to MemoryItem for safe retrieval

        # Temporal context tracking
        self.time_scale = 1.0  # = realtime, > 1.0 = compressed time
        self.index_counter = 0  # Track FAISS indices

    def _get_embedding(self, text: str) -> np.ndarray:
        return self.model.encode(text, convert_to_tensor=False)

    def add_memory(self, memory: MemoryItem):
        # Calculate dynamic importance based on decay
        memory.importance = self.calculate_decay(memory.timestamp)

        # Add to FAISS index if semantically important
        if memory.importance > self.importance_threshold:
            embedding = self._get_embedding(memory.content)
            self.index.add(np.array([embedding]))
            memory.vector = embedding
            self.id_to_memory[self.index_counter] = memory
            self.index_counter += 1

        self.memory_buffer.append(memory)

    def search(self, query: str, temporal_context: datetime = None, n_results: int = 5) -> List[MemoryItem]:
        # Semantic search
        query_embed = self._get_embedding(query)
        _, indices = self.index.search(np.array([query_embed]), n_results)

        # Temporal relevance
        results = []
        for idx in indices[0]:
            if idx in self.id_to_memory:
                mem = self.id_to_memory[idx]
                time_weight = self.time_decay(mem, temporal_context)
                relevance = (0.6 * mem.importance + 0.3 * time_weight + 0.1 * mem.emotional_weight)
                results.append((relevance, mem))

        # Sort by combined relevance
        return [mem for _, mem in heapq.nlargest(min(n_results, len(results)), results)]

    def calculate_decay(self, timestamp: datetime) -> float:
        time_diff = (datetime.now() - timestamp).total_seconds() / self.time_scale
        return np.exp(-self.decay_factor * time_diff / 3600)  # Decay over hours

    def time_decay(self, memory: MemoryItem, context_time: datetime) -> float:
        if not context_time:
            return 1.0
        time_diff = (context_time - memory.timestamp).total_seconds() / self.time_scale
        return 1 / (1 + np.sqrt(max(time_diff, 1e-6) / 3600))  # Avoid division by zero

    def consolidate_memories(self):
        """Neuro-symbolic memory consolidation process"""
        if not self.memory_buffer:
            return

        # Cluster similar memories
        embeddings = np.array([self._get_embedding(m.content) for m in self.memory_buffer])
        k = max(1, len(self.memory_buffer) // 10)
        centroids, assignments = faiss.Kmeans(d=384, k=k, niter=20).train(embeddings)

        # Strengthen important clusters
        for cluster_id in set(assignments):
            cluster_memories = [m for m, c in zip(self.memory_buffer, assignments) if c == cluster_id]
            if len(cluster_memories) > 3:
                for mem in cluster_memories:
                    mem.importance = min(1.0, mem.importance * 1.2)
                    # Link memories in the same cluster
                    for other_mem in cluster_memories:
                        if other_mem.id != mem.id and other_mem.id not in mem.associative_links:
                            mem.associative_links.append(other_mem.id)

    def save_state(self, file_path: str):
        state = {
            'memories': [{
                'content': m.content,
                'type': m.memory_type,
                'timestamp': m.timestamp.isoformat(),
                'importance': m.importance,
                'emotional_weight': m.emotional_weight,
                'associative_links': m.associative_links
            } for m in self.memory_buffer]
        }
        with open(file_path, 'w') as f:
            json.dump(state, f, indent=2)

    def load_state(self, file_path: str):
        with open(file_path, 'r') as f:
            state = json.load(f)
            self.memory_buffer = deque(maxlen=self.memory_buffer.maxlen)
            self.index = faiss.IndexFlatL2(384)
            self.index_counter = 0
            self.id_to_memory = {}
            for m in state['memories']:
                memory = MemoryItem(
                    content=m['content'],
                    memory_type=m['type'],
                    importance=m['importance']
                )
                memory.timestamp = datetime.fromisoformat(m['timestamp'])
                memory.emotional_weight = m['emotional_weight']
                memory.associative_links = m.get('associative_links', [])
                self.add_memory(memory)