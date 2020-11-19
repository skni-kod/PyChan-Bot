import re
class zad:
    def __init__(self,data):
        self.kappa = lambda h1, h2: h1 / (h1 - h2)  # Funkcja obliczająpca Kappa
        self.niep_kappa = lambda h1, h2, u_od_h: abs(-h2 / ((h1 - h2) ** 2)) * u_od_h + abs(h1 / ((h1 - h2) ** 2)) * u_od_h  # Funkcja obliczająca niepewność u(kappa)
        self.dane = str(data).split('\n')
        self.u_od_h = float(self.dane[0])
        self.wynik = ""
    def oblicz(self):
        for i in range(1, len(self.dane)):
            h1, h2 = map(int, self.dane[i].split())  # Zgarnij h1 i h2 z linii
            k = self.kappa(h1, h2)  # Oblicz kappa dla i-tego pomiaru
            niep = self.niep_kappa(h1, h2, self.u_od_h)  # Oblicz u(kappa)
            self.wynik += ("Kappa_{} = ({} +/- {})\n".format(i, k, niep))  # Zapis do zmiennej
        return self.wynik



