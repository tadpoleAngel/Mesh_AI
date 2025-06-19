import torch
import torch.nn as nn
import torch.optim as optim
import os
from agents.base_agent import BaseAgent


class SimpleRegressor(nn.Module):
    def __init__(self, input_dim=2, hidden_dim=16):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

    def forward(self, x):
        return self.net(x)


class Charlie(BaseAgent):
    def __init__(self, name, model_path="models/charlie.pkl", max_ticks=1000):
        super().__init__(name)
        self.model_path = model_path
        self.max_ticks = max_ticks
        self.model = SimpleRegressor()
        self.optimizer = optim.SGD(self.model.parameters(), lr=0.01)
        self.loss_fn = nn.MSELoss()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.last_reward = 0.0

        # Try to load model from disk if it exists
        if os.path.exists(model_path) and os.path.getsize(model_path) > 0:
            self.load_model(model_path)

    def observe(self, data):
        """
        Charlie receives Bob's memory buffer (a list of dicts with 'tick' and 'value').
        """
        # wrapped in a list because thats what the rest of the class expects
        self.latest_observation = [data.get("content", [])] if data else []

    def predict_next(self):
        if not hasattr(self, 'latest_observation') or self.latest_observation is None or len(self.latest_observation) == 0:
            return None

        tick_norm = self.latest_observation[-1]["tick"] / self.max_ticks
        tick_val = torch.tensor([[tick_norm, self.last_reward]], dtype=torch.float32).to(self.device)
        with torch.no_grad():
            prediction = self.model(tick_val).item()
        return prediction

    def train(self, actual_value, reward=None):
        if not self.latest_observation:
            return

        self.last_reward = reward if reward is not None else 0.0

        # Prepare training data from Bob's memory buffer
        X_list = []
        y_list = []
        for entry in self.latest_observation:
            tick_norm = entry["tick"] / self.max_ticks
            X_list.append([tick_norm, self.last_reward])
            y_list.append(entry["value"])

        X = torch.tensor(X_list, dtype=torch.float32).to(self.device)
        y = torch.tensor(y_list, dtype=torch.float32).unsqueeze(1).to(self.device)

        self.model.train()
        self.optimizer.zero_grad()
        predictions = self.model(X)
        loss = self.loss_fn(predictions, y)
        loss.backward()
        self.optimizer.step()


    def save_model(self, path=None):
        if path is None:
            path = self.model_path
        torch.save(self.model.state_dict(), path)

    def load_model(self, path=None):
        if path is None:
            path = self.model_path
        self.model.load_state_dict(torch.load(path, map_location=self.device))
