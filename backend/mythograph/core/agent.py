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
        """Perceive relationships and events from the graph."""
        relationships = self.graph.get_relationships(self.agent_id)
        events = self.graph.get_recent_events(self.agent_id)
        self.memory.append({"relationships": relationships, "events": events})
        return relationships, events

    def decide_action(self):
        """Use LLM to decide action based on internal state and world."""
        context = self.perceive_world()
        prompt = (
            f"As {self.name}, with goals: {self.goals}, beliefs: {self.beliefs}, "
            f"personality: {self.personality_vector.tolist()}, and context: {context}, "
            f"what action should you take next?"
        )
        action = self.llm.generate_response(prompt)
        return action

    def execute_action(self, action):
        """Execute and log the decided action."""
        self.graph.add_event(self.agent_id, action)
        self.memory.append({"action": action})

    def update_beliefs(self, new_beliefs):
        """Update beliefs with new observations."""
        self.beliefs.update(new_beliefs)
