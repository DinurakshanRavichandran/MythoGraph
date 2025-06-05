from ..llm.model_interface import LLMInterface

class NarrativePlanner:
    def __init__(self):
        self.llm = LLMInterface()
        self.plans = {} # Store character plans

    def gererate_plan(self, agent, goal, conflict, theme):
        """Generate a plan for a character using IPOCL (Intent-driven Partial Order Casual Link)."""
        prompt = f"Generate a narrative plan for {agent.name} with goal '{goal}', '{conflict}', and theme '{theme}' using IPOCL framework."
        plan = self.llm.generate_response(prompt)
        self.plans[agent.agent_id] = plan
        return plan
    