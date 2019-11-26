"""
File name: oblicz_30.py
Author: Jakub Szatkowski
Date created: 04/12/2016
Python Version: 3.5
License: MiT
"""

import matplotlib.pyplot as plt
import numpy as np
import math
import pylab
from io import StringIO

licz_a = lambda x, y: (len(x) * sum(x * y) - sum(x) * sum(y)) / (
            len(x) * sum(x ** 2) - sum(x) ** 2)
licz_b = lambda x, y: (sum(y) * sum(x ** 2) - sum(x) * sum(x * y)) / (
            len(x) * sum(x ** 2) - sum(x) ** 2)
estymator = lambda x, y, a, b: np.sqrt(
    (sum(y ** 2) - a * sum(x * y) - b * sum(y)) / (len(x) - 2))
niepewnosc_a = lambda x, y, estymator: estymator * np.sqrt(
    len(x) / (len(x) * sum(x ** 2) - sum(x) ** 2))
niepewnosc_b = lambda x, y, estymator: estymator * np.sqrt(
    sum(x ** 2) / (len(x) * sum(x ** 2) - sum(x) ** 2))
ugamma = lambda R0, uR0, a, ua: np.sqrt(
    (1 / R0 * ua) ** 2 + (-a / R0 ** 2 * uR0) ** 2)

# Obliczenie niepewnosci
ut = (1) / np.sqrt(3)
ur = (0.01) / np.sqrt(3)


def oblicz30(input_data):
    # Czytanie danych z pliku
    #with open("dane_30.txt") as f:
    #    data = np.loadtxt(f)
    f = StringIO(input_data)
    data = np.loadtxt(f)
    t = data[:, 0]
    r = data[:, 1]

    # Pierwszy wykres
    plt.figure(1)
    plt.subplot(121)
    a = licz_a(t, r)
    b = licz_b(t, r)
    est = estymator(t, r, a, b)
    ua = niepewnosc_a(t, r, est)
    ub = niepewnosc_b(t, r, est)
    xa = np.arange(0, 100, 0.01)
    ya = a * xa + b

    plt.errorbar(t, r, xerr=ut, yerr=ur, fmt='none')
    plt.plot(xa, ya)

    pylab.xlim([0, 100])

    plt.title('Wykres zaleznosci R(T)')
    plt.xlabel('$T [\degree C]$')
    plt.ylabel('$R [\Omega]$')

    plt.subplot(122)
    plt.errorbar(t, r, xerr=ut, yerr=ur, fmt='none')
    plt.plot(xa, ya)

    pylab.xlim([65, 71])
    pylab.ylim([120, 130])

    plt.title('Zblizenie wykresu')
    plt.xlabel('$T [\degree C]$')
    plt.ylabel('$R [\Omega]$')

    # Obliczenie wspolczynnika temeperaturowego
    R0 = b
    gamma = a / R0
    uGamma = ugamma(R0, ur, a, ua)

    wynik = ["Niepewność termometru: u(T) = %f oC\n" % ut,
             "Niepewność ohmomierza: u(R) = %f Ohm\n" % ur,
             "Współczynnik kierunkowy prostej: a = (%f +/- %f) Ohm/oC\n" % (
             a, ua),
             "Współczynnik kierunkowy prostej: b = (%f +/- %f) Ohm\n" % (
             b, ub),
             "Temperaturowy wspolczynnik rezystancji: gamma = (%f +/- %f) 1/oC\n" % (
                 gamma, uGamma),
             "Obliczony R0: R0 = (%f +/- %f) Ohm" % (R0, ub)]

    plt.savefig('foo.png')
    plt.clf()
    plt.cla()
    plt.close()
    return "".join(wynik)


# plt.show()
