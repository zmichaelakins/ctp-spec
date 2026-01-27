"""
Regulator v3.0 — Non-Normative Reference Implementation
Cognitive Transport Protocol (CTP) v1.0

Illustrative only. Not a compliance definition.
See the CTP v1.0 Technical Standard Specification for normative requirements.
"""
import time, math, random


# Core params – tune per "user"

B_base = 1.0 # baseline bandwidth

Pi_base = 1.2 # baseline precision weighting

kappa = 0.7 # truncation reset strength (0–1)

overload_threshold = 1.2

dt = 0.1 # sim step (seconds)


def recovery_half_life(Pi, B):

    return (math.log(2) / 2) * (Pi / max(0.1, B))


# State init

t = E = D = 0.0

B = B_base

Pi = Pi_base

in_overload = False

last_trunc = -999


print("t | B_eff | E | D_felt | action | rec t½")


random.seed(42) # for reproducible demo


while t < 60:

    B_eff = B / Pi

    load = random.gauss(1.2, 0.4)

    if 10 < t < 20 or 35 < t < 45:

        load *= 2.5 # overload bursts


    excess = max(0, load - B_eff)

    E += excess * dt

    D += Pi * E * dt

    D_felt = math.sqrt(D)


    if E > overload_threshold * B_eff and not in_overload:

        in_overload = True

        print(f"{t:4.1f}| {B_eff:5.2f}| {E:5.2f}| {D_felt:6.2f}| **TRUNCATE** | -")

        E *= (1 - kappa)

        last_trunc = t

        in_overload = False


    B = B_base * (1 - 0.005 * t + 0.3 * math.sin(t / 5))

    Pi = Pi_base * (1 + 0.4 * (E / B_eff))


    half_life = recovery_half_life(Pi, B)


    if t % 5 < dt:

        action = "recovery" if t - last_trunc < 5 else "steady"

        print(f"{t:4.1f}| {B_eff:5.2f}| {E:5.2f}| {D_felt:6.2f}| {action:8} | {half_life:4.1f}s")


    t += dt

    # time.sleep(0.01) # uncomment for real-time feel


print(f"\nFinal felt distress: {D_felt:.2f}")

print("Early truncation → fast recovery → equilibrium.")

