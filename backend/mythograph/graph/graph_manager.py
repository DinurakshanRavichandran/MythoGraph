from neo4j import GraphDatabase

NEO4J_URI ="bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "hardworking123"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_URI, NEO4J_PASSWORD))

def add_character_travel(character_name, location_name):
    query = """ 
    MERGE (c:character {name: $character})
    MERGE (l:location {name: $location})
    MERGE (c)-[TRAVELED_TO]->(l)
    """
    with driver.session() as session:
        session.run(query, character=character_name, location=location_name)
    print("f Added: {character_name} traveled to {location_name}")

if __name__ == "__main__":
    add_character_travel("Elandor", "Ashen Vale")
    add_character_travel("Nyra", "Crimson Peaks")

    driver.close()