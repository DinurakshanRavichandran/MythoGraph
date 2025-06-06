from neo4j import GraphDatabase
from ..graph.schema import NODE_TYPES, RELATIONSHIP_TYPES

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "hardworking123"

class GraphManager:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def add_event(self, agent_id, action_description):
        query = """
        MATCH (a:Character {agent_id: $agent_id})
        CREATE (e:Event {description: $desc, timestamp: timestamp()})
        CREATE (a)-[:PERFORMED]->(e)
        """
        with self.driver.session() as session:
            session.run(query, agent_id=agent_id, desc=action_description)

    def get_recent_events(self, agent_id=None, limit=5):
        if agent_id:
            query = """
            MATCH (a:Character {agent_id: $agent_id})-[:PERFORMED]->(e:Event)
            RETURN e.description AS description
            ORDER BY e.timestamp DESC LIMIT $limit
            """
            params = {"agent_id": agent_id, "limit": limit}
        else:
            query = """
            MATCH (e:Event)
            RETURN e.description AS description
            ORDER BY e.timestamp DESC LIMIT $limit
            """
            params = {"limit": limit}

        with self.driver.session() as session:
            result = session.run(query, **params)
            return [{"description": record["description"]} for record in result]

    def get_relationships(self, agent_id):
        query = """
        MATCH (a:Character {agent_id: $agent_id})-[r]->(b)
        RETURN type(r) AS relationship, b.name AS target
        """
        with self.driver.session() as session:
            result = session.run(query, agent_id=agent_id)
            return [{"relationship": record["relationship"], "target": record["target"]} for record in result]

    def add_character_travel(self, character_name, location_name):
        query = """ 
        MERGE (c:Character {name: $character})
        MERGE (l:Location {name: $location})
        MERGE (c)-[:TRAVELED_TO]->(l)
        """
        with self.driver.session() as session:
            session.run(query, character=character_name, location=location_name)
        print(f"Added: {character_name} traveled to {location_name}")

    def create_character(self, agent_id, name):
        query = """
        MERGE (c:Character {agent_id: $agent_id})
        ON CREATE SET c.name = $name
        """
        with self.driver.session() as session:
            session.run(query, agent_id=agent_id, name=name)
