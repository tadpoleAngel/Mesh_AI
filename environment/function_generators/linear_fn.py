class LinearFunction:
    def __init__(self, slope=1.0, intercept=0.0):
        self.slope = slope
        self.intercept = intercept

    def get_value(self, tick):
        return self.slope * tick + self.intercept