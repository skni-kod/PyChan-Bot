from io import StringIO

import matplotlib.pyplot as plt
import numpy as np

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


def oblicz22(input_data):
    # Czytanie danych z pliku
    f = StringIO(input_data)
    data = np.loadtxt(f)

    # Pobranie kolumn
    T = data[:, 0]
    E = data[:, 1]

    delta_T = 1
    delta_E = 0.01

    u_T = delta_T / np.sqrt(3)
    u_E = delta_E / np.sqrt(3)

    a = licz_a(T, E)
    b = licz_b(T, E)
    est = estymator(T, E, a, b)
    u_a = niepewnosc_a(T, E, est)
    u_b = niepewnosc_b(T, E, est)

    xa = np.arange(0, 90, 0.01)
    ya = a * xa + b

    plt.figure(1)
    plt.errorbar(T, E, xerr=u_T, yerr=u_E, fmt='.')
    plt.plot(xa, ya, '-', linewidth=0.5)
    plt.title('Wykres $\\varepsilon(T)$', fontsize=26)
    plt.xlabel('$T [\\degree C]$', fontsize=18)
    plt.ylabel('$\\varepsilon [mV]$', fontsize=18)
    ax = plt.gca()
    ax.set_aspect(aspect='auto')

    plt.savefig('foo.png', dpi=600)
    plt.clf()
    plt.cla()
    plt.close()

    wynik = ["u(T) = %f [oC]\n" % u_T, "u(E) = %f [mV]\n" % u_E,
             "a = ({} +/- {}) [mV/oC]\n".format(a, u_a),
             "b = ({} +/- {}) [mV]\n".format(b, u_b),
             "Estymator wynosi: %f\n" % est]

    return "".join(wynik)