from ..llm.model_interface import LLMInterface

class NarrativePlanner:
    def __init__(self):
        self.llm = LLMInterface()
        self.plans = {}

    def generate_plan(self, agent, goal, conflict, theme):
        """Create an IPOCL-style plan for a given character."""
        prompt = (
            f"Generate a narrative plan for character {agent.name} "
            f"with goal '{goal}', conflict '{conflict}', and theme '{theme}' "
            f"using the IPOCL planning framework."
        )
        plan = self.llm.generate_response(prompt)
        self.plans[agent.agent_id] = plan
        return plan

    def evaluate_plan(self, agent, story_context):
        """Evaluate plan alignment with current story context."""
        plan = self.plans.get(agent.agent_id, "")
        prompt = (
            f"Given the current story context: '{story_context}', "
            f"does this plan align: '{plan}'?"
        )
        alignment = self.llm.generate_response(prompt)
        return alignment.strip().lower().startswith("yes")
