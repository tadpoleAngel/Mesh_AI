class BaseAgent:
    def __init__(self, name):
        self.name = name
        self.knowledge_level = 10  # Start at grade 10 equivalent
        self.message_inbox = []
        self.outbound_messages = []

    def observe(self, data):
        """
        Process observed input (may be overridden by Alice).
        """
        self.latest_observation = data
        return data

    def receive_message(self, message):
        """
        Store incoming message.
        """
        self.message_inbox.append(message)

    def generate_message(self):
        """
        Optional: Format message for another agent (overridden by Alice/Bob).
        """
        return {
            "from": self.name,
            "content": self.latest_observation if hasattr(self, 'latest_observation') else None,
            "notes": None
        }

    def generate_outbound_messages(self):
        """
        Override to send messages to other agents (up to 2).
        Returns list of tuples: (recipient_name, message_dict)
        """
        return []

    def predict_next(self):
        """
        Placeholder for Charlie’s prediction logic.
        """
        return None

    def propose_knowledge_changes(self):
        """
        Decide how to alter the knowledge level of other agents.
        Must return dict: {target_agent_name: delta, ...}
        """
        return {}

    def apply_knowledge_change(self, delta):
        """
        Apply a change to this agent's knowledge level.
        """
        self.knowledge_level += delta
        self.knowledge_level = max(0, self.knowledge_level)  # Prevent negative knowledge
