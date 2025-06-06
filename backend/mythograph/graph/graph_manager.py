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

    def get_recent_events(self, agent_id=None, limit=5):
        if agent_id:
            query="""
            MATCH (a:Character {agent_id: $agent_id})-[PERFORMED]->(e:Event)
            RETURN e.description As description
            ORDER BY e.timestamp DESC LIMIT $LIMIT
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