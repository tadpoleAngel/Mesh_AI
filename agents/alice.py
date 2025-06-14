from agents.base_agent import BaseAgent

class Alice(BaseAgent):
    def __init__(self, name="Alice"):
        super().__init__(name)
        self.data_stream = []     # Full list of data points from the simulation
        self.tick_pointer = 0     # Current index into the simulation

    def load_simulation_data(self, data_sequence):
        """
        Load or reset the full simulation data.
        Expected format: list of dicts with keys 'tick' and 'value'
        """
        self.data_stream = data_sequence
        self.tick_pointer = 0

    def observe(self, _):
        """
        Alice retrieves the next piece of simulation data.
        She does not observe input from the environment like Bob/Charlie.
        """
        if self.tick_pointer < len(self.data_stream):
            data = self.data_stream[self.tick_pointer]
            self.latest_observation = data
            self.tick_pointer += 1
            return data
        else:
            self.latest_observation = None
            return None

    def generate_message(self):
        """
        Alice decides what to send to Bob.
        She may distort data or adjust notes based on her knowledge level.
        """
        message = {
            "from": self.name,
            "content": None,
            "notes": None
        }

        if hasattr(self, 'latest_observation') and self.latest_observation:
            data = self.latest_observation.copy()

            if self.knowledge_level < 5:
                data["value"] += 0.5  # simulate imprecision or bias
                message["notes"] = "Note: estimated due to low precision equipment."
            else:
                message["notes"] = "High-confidence measurement."

            message["content"] = data

        return message

    def generate_outbound_messages(self):
        """
        Send data to Bob only.
        """
        return [("Bob", self.generate_message())]
