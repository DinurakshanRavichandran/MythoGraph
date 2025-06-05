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
    
    def evaluate_plan(self, agent, story_context):
        """Evaluate if the plan aligns with the current story context."""
        plan = self.plans.get(agent.agent_id, "")
        prompt = f"Does the plan '{plan}' align with story context'{story_context}'?"
        alignment = self.llm.gererate_response(prompt)
        return alignment.lower().startswith("yes")