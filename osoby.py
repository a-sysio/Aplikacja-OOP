from abc import ABC, abstractmethod


# ABSTRAKCJA: wspolna klasa bazowa dla osob w systemie (czlonek, trener).
class Osoba(ABC):
    def __init__(self, osoba_id, imie, nazwisko, email):
        self.osoba_id = osoba_id      # identyfikator osoby
        self.imie = imie
        self.nazwisko = nazwisko
        self.email = email            # przypisanie przechodzi przez setter ponizej (walidacja)

    # ENKAPSULACJA: email dostepny przez property, ale zmieniany tylko z walidacja
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, wartosc):
        if "@" not in wartosc or "." not in wartosc:
            raise ValueError("Niepoprawny adres email")
        self._email = wartosc

    # property tylko do odczytu - laczy imie i nazwisko
    @property
    def pelne_imie(self):
        return f"{self.imie} {self.nazwisko}"

    # metoda abstrakcyjna - kazda osoba musi okreslic swoja role
    @abstractmethod
    def rola(self):
        ...

    def opis(self):
        return f"[{self.rola()}] {self.pelne_imie} ({self.osoba_id})"


# DZIEDZICZENIE: Czlonek "jest rodzajem" Osoby.
class Czlonek(Osoba):
    def __init__(self, osoba_id, imie, nazwisko, email, karnet):
        super().__init__(osoba_id, imie, nazwisko, email)
        # AGREGACJA: czlonek MA karnet przekazany z zewnatrz (relacja miedzy klasami)
        self._karnet = karnet
        self._saldo = 0.0        # ENKAPSULACJA: saldo ukryte, zmieniane tylko metodami
        self._wejscia = []       # KOLEKCJA: historia wejsc czlonka

    @property
    def karnet(self):
        return self._karnet

    @property
    def saldo(self):
        return self._saldo

    def zmien_karnet(self, karnet):
        self._karnet = karnet

    # walidacja chroni przed ujemna wplata
    def doplac(self, kwota):
        if kwota <= 0:
            raise ValueError("Kwota musi byc dodatnia")
        self._saldo += kwota

    # pobiera oplate wg karnetu; zwraca False gdy brakuje srodkow
    def pobierz_oplate(self):
        oplata = self._karnet.miesieczna_oplata()   # POLIMORFIZM: rozny wynik dla roznych karnetow
        if self._saldo < oplata:
            return False
        self._saldo -= oplata
        return True

    def zarejestruj_wejscie(self, data):
        self._wejscia.append(data)

    def liczba_wejsc(self):
        return len(self._wejscia)

    # POLIMORFIZM: wlasna definicja roli
    def rola(self):
        return "Czlonek"

    # POLIMORFIZM: rozszerza opis z klasy bazowej o dane czlonka
    def opis(self):
        return f"{super().opis()} - karnet: {self._karnet.nazwa}, saldo: {self._saldo:.2f} zl"


# DZIEDZICZENIE: Trener rowniez "jest rodzajem" Osoby, ale ma inne dane niz Czlonek.
class Trener(Osoba):
    def __init__(self, osoba_id, imie, nazwisko, email, specjalizacja):
        super().__init__(osoba_id, imie, nazwisko, email)
        self.specjalizacja = specjalizacja

    def rola(self):
        return "Trener"

    def opis(self):
        return f"{super().opis()} - specjalizacja: {self.specjalizacja}"
