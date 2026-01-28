import math

class CTP:
    def __init__(self, B=10, a=0.12, k=1.5):
        self.B = B
        self.Pi = 1.0
        self.D = 0.0
        self.a = a
        self.k = k
        self.R = False
        self.D0 = 0.0
        self.t = 0

    def t_half(self):
        return (math.log(2) / 2) * (self.Pi / self.B)

    def thresh(self):
        return self.k * self.B * self.Pi

    def step(self, load):
        if self.R:
            self.D = self.D0 * 2 ** (-self.t / max(self.t_half(), 1e-9))
            self.t += 1
            if self.D < 0.1:
                self.R = False
                self.Pi = 1.0
            return "RECOVER", self.Pi, self.D

        E = max(0.0, load - self.B)
        self.Pi *= 1 + self.a * (E / max(self.B, 1e-9))
        self.Pi = max(0.1, min(self.Pi, 3.0))
        self.D += self.Pi * E

        if self.D > self.thresh():
            self.R = True
            self.D0 = self.D
            self.t = 0
            return "TRUNCATE", self.Pi, self.D

        return "NORMAL", self.Pi, self.D
