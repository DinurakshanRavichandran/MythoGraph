# mythograph/core/agent.py

import uuid
import random
from datetime import datetime
from mythograph.llm.model_interface import call_llm
from mythograph.llm.memory import Memory
from mythograph.graph.graph_manager import GraphManager

class StoryAgent:
    def __init__(self, name, personality, goals, beliefs, graph: GraphManager):
        self.id = str(uuid.uuid4())
        self.name = name
        self.personality = personality  # Dict: {"openness": 0.7, "neuroticism": 0.3, ...}
        self.goals = goals              # List of strings
        self.beliefs = beliefs          # List of facts or opinions
        self.memory = Memory(self.name)
        self.graph = graph

        # Register character in the graph
        self.graph.add_character(self.name, self.personality, self.goals)

    def perceive(self, event_description: str):
        """Ingest an event and update memory and beliefs."""
        timestamp = datetime.now().isoformat()
        self.memory.store(event_description, timestamp)
        self.beliefs.append(f"Perceived event: {event_description}")

    def choose_action(self, context: str) -> str:
        """
        Decide on an action based on current goals, personality, and context.
        Uses LLM to suggest a next move.
        """
        prompt = self._generate_decision_prompt(context)
        response = call_llm(prompt)
        action = self._parse_action_from_response(response)
        return action

    def act(self, context: str):
        """Perform an action and update the graph and memory."""
        action = self.choose_action(context)
        timestamp = datetime.now().isoformat()

        # Log to memory
        self.memory.store(f"Action taken: {action}", timestamp)

        # Update graph
        self.graph.add_event(actor=self.name, description=action)

        return action

    def _generate_decision_prompt(self, context: str) -> str:
        prompt = f"""
You are {self.name}, a character in a dynamic, evolving mythic story world.

Your personality traits: {self.personality}
Your goals: {self.goals}
Your current beliefs: {self.beliefs[-3:]}  # Only recent beliefs

Context of the story right now:
{context}

Based on your goals and personality, what do you do next? Respond with a single, well-formed action.
"""
        return prompt.strip()

    def _parse_action_from_response(self, response: str) -> str:
        # Optionally parse LLM output if it's in structured format
        return response.strip()

    def summarize_self(self):
        return {
            "id": self.id,
            "name": self.name,
            "goals": self.goals,
            "beliefs": self.beliefs[-5:],  # recent
            "personality": self.personality,
        }
