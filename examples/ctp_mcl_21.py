"""
CTP Minimal Control Law (MCL-21)
--------------------------------

Status: Frozen, Non-Normative
Scope: Illustrative control-law core for Cognitive Transport Protocol (CTP v1.0)

This file provides a minimal, self-contained illustration of the core control
dynamics underlying CTP. It is intentionally compact and omits engineering
concerns such as smoothing, persistence, instrumentation, or integration
scaffolding.

Semantics:
- Bandwidth (B) is finite and exogenous
- Precision (Pi) increases under overload and is saturating
- Distress (D) integrates precision-weighted overload
- Truncation is a regime switch triggered by accumulated distress
- Recovery is exponential and resets acute precision

This artifact is NOT a production implementation and MUST NOT be used
directly in deployed systems.

Canonical role: conceptual anchor only.
"""
import math

class CTP:
    def __init__(self, B=10, a=0.12, k=1.5):
        self.B = B          # bandwidth
        self.Pi = 1.0       # precision
        self.D = 0.0        # accumulated distress
        self.a = a          # precision growth rate
        self.k = k          # truncation gain
        self.R = False      # recovery state
        self.D0 = 0.0       # distress at truncation
        self.t = 0          # recovery time index

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
            self.t
