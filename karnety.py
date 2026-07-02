from abc import ABC, abstractmethod


# ABSTRAKCJA: klasa abstrakcyjna - definiuje wspolny kontrakt dla wszystkich karnetow.
# Nie mozna utworzyc obiektu Karnet bezposrednio - trzeba uzyc klasy potomnej.
class Karnet(ABC):
    def __init__(self, karnet_id, nazwa, cena_bazowa):
        self.karnet_id = karnet_id                # identyfikator karnetu
        self.nazwa = nazwa
        self._cena_bazowa = cena_bazowa           # ENKAPSULACJA: pole chronione (podkreslnik)

    # metoda abstrakcyjna - kazda klasa potomna MUSI ja wlasciwie zaimplementowac
    @abstractmethod
    def miesieczna_oplata(self):
        ...

    @abstractmethod
    def zakres_dostepu(self):
        ...

    def __str__(self):
        return f"{self.nazwa} ({self.karnet_id}) - {self.miesieczna_oplata():.2f} zl/mc"


# DZIEDZICZENIE: KarnetStandard "jest rodzajem" Karnetu.
class KarnetStandard(Karnet):
    # POLIMORFIZM: wlasna wersja metody - oplata rowna cenie bazowej
    def miesieczna_oplata(self):
        return self._cena_bazowa

    def zakres_dostepu(self):
        return ["silownia", "cardio"]


class KarnetPremium(Karnet):
    def __init__(self, karnet_id, nazwa, cena_bazowa, oplata_basen):
        super().__init__(karnet_id, nazwa, cena_bazowa)   # wywolanie konstruktora klasy bazowej
        self._oplata_basen = oplata_basen                 # dodatkowe pole tylko dla Premium

    # POLIMORFIZM: Premium dolicza oplate za basen
    def miesieczna_oplata(self):
        return self._cena_bazowa + self._oplata_basen

    # szerszy dostep niz Standard - dodatkowo basen i sauna
    def zakres_dostepu(self):
        return ["silownia", "cardio", "basen", "sauna"]


class KarnetStudencki(Karnet):
    znizka = 0.5   # pole klasowe - wspolne dla wszystkich karnetow studenckich

    # POLIMORFIZM: karnet studencki nalicza 50% znizki
    def miesieczna_oplata(self):
        return self._cena_bazowa * (1 - self.znizka)

    def zakres_dostepu(self):
        return ["silownia", "cardio"]
