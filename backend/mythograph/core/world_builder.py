from ..graph.vector_store import VectorStore

class WorldBuilder:
    def __init__(self):
        self.vector_store = VectorStore()

    def generate_map(self):
        """Create procedural map structure."""
        map_data = {
            "regions": ["Forest of Eld", "Mountains of Zor", "Plains of Vyr"],
            "connections": [
                ("Forest of Eld", "Mountains of Zor"),
                ("Mountains of Zor", "Plains of Vyr")
            ]
        }
        self.vector_store.store("map", map_data)
        return map_data

    def generate_culture(self):
        """Create a cultural structure with lore."""
        culture = {
            "name": "Eldrin",
            "religion": "Cult of the Sky Serpent",
            "magic_system": "Rune-based elemental magic",
            "values": ["Honor", "Balance", "Sacrifice"]
        }
        self.vector_store.store("culture", culture)
        return culture

    def get_lore(self, entity):
        """Retrieve lore for a specific entity."""
        return self.vector_store.retrieve(f"lore_{entity}")
