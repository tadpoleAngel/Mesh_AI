# File: agents/bob.py

from agents.base_agent import BaseAgent

class Bob(BaseAgent):
    def __init__(self, name, memory_size=20):
        super().__init__(name)
        self.memory_size = memory_size
        self.memory = []  # Holds recent observations from Alice

    def observe(self, data):
        """
        Bob receives data from Alice and stores it in memory (rolling buffer).
        Data includes both raw value and commentary.
        """
        if data is not None:
            self.memory.append(data)
            if len(self.memory) > self.memory_size:
                self.memory.pop(0)
            self.latest_observation = data  # For messaging or tracking
        return data

    def generate_message(self):
        """
        Packages recent memory into a message for Charlie.
        """
        return {
            "from": self.name,
            "content": self.memory.copy(),  # Send the buffer, not just latest
            "notes": f"Memory of last {len(self.memory)} ticks."
        }

    def generate_outbound_messages(self):
        """
        Bob may send up to two messages. Currently unused.
        """
        return []

    def propose_knowledge_changes(self):
        """
        Currently neutral; does not attempt to change other agents.
        """
        return {}

