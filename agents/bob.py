from agents.base_agent import BaseAgent

class Bob(BaseAgent):
    def __init__(self, name="Bob"):
        super().__init__(name)
        self.database = []  # Store data from Alice and previous ticks

    def observe(self, data):
        """
        Bob receives structured data from Alice:
        {'tick': int, 'value': float, 'notes': Optional[str]}
        Stores and may optionally preprocess before forwarding to Charlie.
        """
        super().observe(data)
        if isinstance(data, dict) and 'tick' in data and 'value' in data:
            self.database.append(data)
        return data

    def generate_message(self):
        """
        Packages data for Charlie.
        Adds extra computation like a moving average.
        """
        message_data = {
            "from": self.name,
            "content": None,
            "notes": None
        }

        if self.database:
            latest = self.database[-1]
            recent_values = [entry['value'] for entry in self.database[-3:]]
            avg = sum(recent_values) / len(recent_values)

            message_data["content"] = {
                "tick": latest["tick"],
                "value": latest["value"],
                "moving_avg": avg
            }
            message_data["notes"] = f"3-tick average computed by Bob."

        return message_data

    def generate_outbound_messages(self):
        """
        Sends a message to Charlie. Only 1 recipient at this stage.
        """
        return [("Charlie", self.generate_message())]
