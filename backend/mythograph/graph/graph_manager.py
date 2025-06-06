from neo4j import GraphDatabase

NEO4J_URI ="bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "hardworking123"

class GraphManger:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def add_event(self, agent_id, action_description):
        query = """
        MATCH (a:Character {agent_id: $agent_id})
        CREATE (e:Event {description: $desc, timestamp()})
        CREATE (a)-[:PERFORMED] ->(e)
        """
        with self.driver.session() as session:
            session.run(query, agent_id=agent_id, desc=action_description)