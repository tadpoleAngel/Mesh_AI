from agents.base_agent import BaseAgent
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
import numpy as np


class DummyConstantModel:
    """ Always predicts zero. Used at very low knowledge levels. """
    def fit(self, X, y):
        pass

    def predict(self, X):
        return [0.0 for _ in X]


class NaiveDeltaModel:
    """ Predicts next value by extrapolating last delta. """
    def fit(self, X, y):
        self.y = y

    def predict(self, X_next):
        if len(self.y) < 2:
            return [self.y[-1] if self.y else 0.0 for _ in X_next]
        delta = self.y[-1] - self.y[-2]
        return [self.y[-1] + delta for _ in X_next]


class Charlie(BaseAgent):
    def __init__(self, name="Charlie"):
        super().__init__(name)
        self.memory = []  # list of (tick, value)
        self.max_knowledge = 15  # You may adjust this ceiling later
        self.model = DummyConstantModel()  # Start with a simple model
        self.configure_model()

    def observe(self, data):
        """
        Expecting data in the form {'tick': int, 'value': float}
        Stores data for future model training.
        """
        super().observe(data)
        if isinstance(data, dict) and 'tick' in data and 'value' in data:
            self.memory.append((data['tick'], data['value']))
        return data

    def configure_model(self):
        """
        Configure internal model based on current knowledge level.
        """
        level = self.knowledge_level

        if level <= 2:
            self.model = DummyConstantModel()
        elif level <= 4:
            self.model = NaiveDeltaModel()
        elif level <= 8:
            self.model = LinearRegression()
        elif level <= 12:
            self.model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
        else:
            self.model = make_pipeline(PolynomialFeatures(degree=3), LinearRegression())

    def history_depth(self):
        """
        Determines how many past data points to use based on knowledge level.
        """
        if self.knowledge_level <= 2:
            return 1
        elif self.knowledge_level <= 4:
            return 2
        elif self.knowledge_level <= 8:
            return 5
        elif self.knowledge_level <= 12:
            return 10
        else:
            return 20

    def predict_next(self):
        """
        Predicts the next tick value using the current model and memory.
        """
        usable_memory = self.memory[-self.history_depth():]
        if len(usable_memory) < 2:
            return 0.0

        X = np.array([[tick] for tick, _ in usable_memory])
        y = np.array([value for _, value in usable_memory])

        try:
            self.model.fit(X, y)
            next_tick = np.array([[usable_memory[-1][0] + 1]])
            prediction = self.model.predict(next_tick)[0]
        except Exception:
            prediction = 0.0

        return prediction

    def apply_knowledge_change(self, delta):
        """
        Override to reconfigure Charlie’s model when knowledge level changes.
        """
        super().apply_knowledge_change(delta)
        self.configure_model()

    def generate_message(self):
        """
        Charlie typically doesn’t send messages in early implementations.
        """
        return {
            "from": self.name,
            "content": None,
            "notes": f"Charlie is at knowledge level {self.knowledge_level}."
        }

    def generate_outbound_messages(self):
        """
        Optional messages to Alice and/or Bob.
        """
        return []
