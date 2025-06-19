import matplotlib.pyplot as plt
from IPython.display import display, clear_output

class LivePlotter:
    def __init__(self):
        self.ticks = []
        self.predictions = []
        self.actuals = []
        self.errors = []
        self.knowledge_levels = {"Alice": [], "Bob": [], "Charlie": []}

        plt.ion()
        self.fig, self.axs = plt.subplots(3, 1, figsize=(8, 10))
        self.fig.tight_layout(pad=4.0)

    def update(self, tick, pred, actual, error, knowledge_dict):
        self.ticks.append(tick)
        self.predictions.append(pred)
        self.actuals.append(actual)
        self.errors.append(error)
        for name in self.knowledge_levels:
            self.knowledge_levels[name].append(knowledge_dict[name])

        self.axs[0].clear()
        self.axs[0].plot(self.ticks, self.actuals, label="Actual", color='green')
        self.axs[0].plot(self.ticks, self.predictions, label="Predicted", color='blue')
        self.axs[0].set_title("Charlie's Prediction vs Actual")
        self.axs[0].legend()

        self.axs[1].clear()
        self.axs[1].plot(self.ticks, self.errors, label="Error", color='red')
        self.axs[1].set_title("Prediction Error")

        self.axs[2].clear()
        for name, values in self.knowledge_levels.items():
            self.axs[2].plot(self.ticks, values, label=name)
        self.axs[2].set_title("Knowledge Levels")
        self.axs[2].legend()

        plt.pause(0.01)
