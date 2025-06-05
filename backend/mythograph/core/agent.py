import numpy as np
from ..llm.model_interface import LLMInterface
from ..graph.graph_manager import GraphManager

class StoryAgent:
    def __init__(self, agent_id, name, goals, beliefs, personality_vector):
        self.agent_id = agent_id
        self.name = name
        self.goals = goals
        self.beliefs = beliefs
        self.personality_vector = np.array(personality_vector)
        self.memory = []
        self.llm = LLMInterface()
        self.graph = GraphManager()

    def perceive_world(self):
        """Perceive the world by querying the Narrative Knowledge Graph."""
        relationships = self.graph_relationships(self.agent_id)
        events = self.graph.get_recent_events()
        self.memory.append({"relationships": relationships, "events": events})
        return relationships, events
    
    def decide_action(self):
        """Decide an action based on goals, beliefs, and personality using LLM and RL."""
        context = self.perceive_world()
        prompt = f"Agent {self.name} with goals {self.goals}, beliefs {self.beliefs}, and personality {self.personality_vector} perceives {context}. What action should they take?"
        action = self.llm.generate_response(prompt)
        return action
    
    def execute_action(self, action):
        """Execute the action and update the graph."""
        self.graph.add_event(self.agent_id, action)
        self.memory.append({"action": action})

    def update_beliefs(self, new_beliefs):
        """Update beliefs based on new information."""
        self.beliefs.update(new_beliefs)