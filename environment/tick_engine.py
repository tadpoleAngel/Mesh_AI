class TickEngine:
    def __init__(self, function_generator):
        """
        Wraps around a function generator that defines the evolving pattern.
        The generator should have a method: get_value(tick: int) -> float
        """
        self.function_generator = function_generator
        self.tick = -1  # Initialized before first tick

    def advance(self):
        """
        Move to the next tick and return the corresponding value.
        """
        self.tick += 1
        return self.function_generator.get_value(self.tick)

    def peek_next(self):
        """
        Peek the value for the next tick without advancing.
        """
        return self.function_generator.get_value(self.tick + 1)

    def get_tick(self):
        return self.tick
