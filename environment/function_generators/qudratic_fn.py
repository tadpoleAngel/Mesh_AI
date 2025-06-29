class QuadraticFunction:
    def __init__(self, a=1.0, b=0.0, c=0.0):
        self.a = a
        self.b = b
        self.c = c

    def get_value(self, tick):
        return self.a * tick**2 + self.b * tick + self.c