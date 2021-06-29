from math import degrees, radians, pi
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import newton, brentq
from constants import g, rho


class Bazooka:
    def __init__(self, m, r, C, alpha, x0, y0, v0=None, T=None, Tw=None, To=None, z=None, H=None):
        self.m = m
        self.r = r
        self.C = C
        self.alpha = radians(alpha)
        self.x0 = x0
        self.y0 = y0
        self.v0 = v0
        self.T = T
        self.Tw = Tw
        self.To = To
        self.H = H
        self.z = z
        self.mu = 0.5 * self.C * rho * (pi * self.r ** 2) / self.m
        self.timeIntervals = 1000

    def model(self, t, vec, p=None):
        x, y, vx, vy = vec
        v = np.sqrt(vx**2 + vy**2)
        return np.array([vx, vy, -self.mu * vx * v, -self.mu * vy * v - g])

    def solveWithKnownV0(self, t):
        vec0 = [self.x0, self.y0, self.v0x, self.v0y]
        result = odeint(lambda vec, t: self.model(t, vec), vec0, t)
        return result[:, 0], result[:, 1], result[:, 2], result[:, 3]

    def calculateV0(self, knownField, v0Guess):
        return brentq(
            lambda v: getattr(
                Bazooka(m=self.m, r=self.r, C=self.C, alpha=degrees(self.alpha),
                        x0=self.x0, y0=self.y0, v0=v).solve(), knownField
            ) - getattr(self, knownField), 1e-6, v0Guess
        )

    def solve(self, v0Guess=None):
        knownField = next(field for field in [
                          "v0", "T", "Tw", "To", "H", "z"] if getattr(self, field) != None)
        if (knownField != "v0"):
            optimalV0 = True
            foundV0 = None
            while True:
                try:
                    foundV0 = self.calculateV0(knownField, v0Guess)
                except ValueError:
                    optimalV0 = False
                    v0Guess += 1
                else:
                    if (not optimalV0):
                        print(f"Warn: use v0 guess = {v0Guess} instead!")
                        optimalV0 = True

                    break

            self.v0 = foundV0

        self.setV0Components()
        self.setLiftTime()
        self.setTotalTime()
        self.setFallTime()
        self.setMaxHeight()
        self.setRange()

        return self

    def getSolution(self):
        t = np.linspace(0, self.T, self.timeIntervals)
        return self.solveWithKnownV0(t)

    def setV0Components(self):
        self.v0x = self.v0 * np.cos(self.alpha)
        self.v0y = self.v0 * np.sin(self.alpha)

    def setLiftTime(self):
        if self.Tw == None:
            self.Tw = newton(
                lambda t: self.solveWithKnownV0([0, t])[3][1], 0)
        if (self.Tw < 0):
            self.Tw = 0

    def setTotalTime(self):
        if self.T == None:
            self.T = newton(lambda t: self.solveWithKnownV0(
                [0, t])[1][1], 2 * self.Tw)
        if (self.T < 0):
            self.T = 0

    def setFallTime(self):
        if self.To == None:
            self.To = self.T - self.Tw
        if (self.To < 0):
            self.To = 0

    def setMaxHeight(self):
        if self.H == None:
            self.H = self.solveWithKnownV0([0, self.Tw])[1][1]

    def setRange(self):
        if self.z == None:
            t = np.linspace(0, self.T, self.timeIntervals)
            x, y, _, _ = self.solveWithKnownV0(t)

            self.z = x[-1]

    def getInfo(self):
        print(f"Bazooka where \u03b1 = {round(degrees(self.alpha), 2)}\u00b0")
        print(f"v0: {round(3.6 * self.v0, 2)} km/h")
        print(f"Tw: {round(self.Tw, 2)} s")
        print(f"To: {round(self.To, 2)} s")
        print(f"T: {round(self.T, 2)} s")
        print(f"z: {round(self.z, 2)} m")
        print(f"H: {round(self.H, 2)} m")
        print()
