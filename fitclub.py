from abc import ABC, abstractmethod


class Karnet(ABC):
    def __init__(self, karnet_id, nazwa, cena_bazowa):
        self.karnet_id = karnet_id
        self.nazwa = nazwa
        self._cena_bazowa = cena_bazowa

    @abstractmethod
    def miesieczna_oplata(self):
        ...

    @abstractmethod
    def zakres_dostepu(self):
        ...

    def __str__(self):
        return f"{self.nazwa} ({self.karnet_id}) - {self.miesieczna_oplata():.2f} zl/mc"


class KarnetStandard(Karnet):
    def miesieczna_oplata(self):
        return self._cena_bazowa

    def zakres_dostepu(self):
        return ["silownia", "cardio"]


class KarnetPremium(Karnet):
    def __init__(self, karnet_id, nazwa, cena_bazowa, oplata_basen):
        super().__init__(karnet_id, nazwa, cena_bazowa)
        self._oplata_basen = oplata_basen

    def miesieczna_oplata(self):
        return self._cena_bazowa + self._oplata_basen

    def zakres_dostepu(self):
        return ["silownia", "cardio", "basen", "sauna"]


class KarnetStudencki(Karnet):
    znizka = 0.5

    def miesieczna_oplata(self):
        return self._cena_bazowa * (1 - self.znizka)

    def zakres_dostepu(self):
        return ["silownia", "cardio"]


class Osoba(ABC):
    def __init__(self, osoba_id, imie, nazwisko, email):
        self.osoba_id = osoba_id
        self.imie = imie
        self.nazwisko = nazwisko
        self.email = email

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, wartosc):
        if "@" not in wartosc or "." not in wartosc:
            raise ValueError("Niepoprawny adres email")
        self._email = wartosc

    @property
    def pelne_imie(self):
        return f"{self.imie} {self.nazwisko}"

    @abstractmethod
    def rola(self):
        ...

    def opis(self):
        return f"[{self.rola()}] {self.pelne_imie} ({self.osoba_id})"


class Czlonek(Osoba):
    def __init__(self, osoba_id, imie, nazwisko, email, karnet):
        super().__init__(osoba_id, imie, nazwisko, email)
        self._karnet = karnet
        self._saldo = 0.0
        self._wejscia = []

    @property
    def karnet(self):
        return self._karnet

    @property
    def saldo(self):
        return self._saldo

    def zmien_karnet(self, karnet):
        self._karnet = karnet

    def doplac(self, kwota):
        if kwota <= 0:
            raise ValueError("Kwota musi byc dodatnia")
        self._saldo += kwota

    def pobierz_oplate(self):
        oplata = self._karnet.miesieczna_oplata()
        if self._saldo < oplata:
            return False
        self._saldo -= oplata
        return True

    def zarejestruj_wejscie(self, data):
        self._wejscia.append(data)

    def liczba_wejsc(self):
        return len(self._wejscia)

    def rola(self):
        return "Czlonek"

    def opis(self):
        return f"{super().opis()} - karnet: {self._karnet.nazwa}, saldo: {self._saldo:.2f} zl"


class Trener(Osoba):
    def __init__(self, osoba_id, imie, nazwisko, email, specjalizacja):
        super().__init__(osoba_id, imie, nazwisko, email)
        self.specjalizacja = specjalizacja

    def rola(self):
        return "Trener"

    def opis(self):
        return f"{super().opis()} - specjalizacja: {self.specjalizacja}"


class Zajecia:
    def __init__(self, zajecia_id, nazwa, trener, strefa, limit_miejsc, termin):
        self.zajecia_id = zajecia_id
        self.nazwa = nazwa
        self._trener = trener
        self.strefa = strefa
        self._limit_miejsc = limit_miejsc
        self.termin = termin
        self._zapisani = []

    @property
    def trener(self):
        return self._trener

    @property
    def wolne_miejsca(self):
        return self._limit_miejsc - len(self._zapisani)

    def zapisz(self, czlonek):
        if self.strefa not in czlonek.karnet.zakres_dostepu():
            return False
        if self.wolne_miejsca <= 0:
            return False
        if czlonek in self._zapisani:
            return False
        self._zapisani.append(czlonek)
        return True

    def wypisz(self, czlonek):
        if czlonek in self._zapisani:
            self._zapisani.remove(czlonek)
            return True
        return False

    def lista_uczestnikow(self):
        return list(self._zapisani)

    def __str__(self):
        return f"{self.nazwa} ({self.zajecia_id}) prow. {self._trener.pelne_imie}, {self.termin}, wolne: {self.wolne_miejsca}"


class Klub:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self._czlonkowie = {}
        self._trenerzy = {}
        self._zajecia = {}

    def dodaj_czlonka(self, czlonek):
        self._czlonkowie[czlonek.osoba_id] = czlonek

    def dodaj_trenera(self, trener):
        self._trenerzy[trener.osoba_id] = trener

    def dodaj_zajecia(self, zajecia):
        self._zajecia[zajecia.zajecia_id] = zajecia

    def zapisz_na_zajecia(self, id_czlonka, id_zajec):
        czlonek = self._czlonkowie.get(id_czlonka)
        zajecia = self._zajecia.get(id_zajec)
        if czlonek is None or zajecia is None:
            return False
        return zajecia.zapisz(czlonek)

    def rozlicz_skladki(self):
        wynik = {}
        for czlonek in self._czlonkowie.values():
            wynik[czlonek.osoba_id] = czlonek.pobierz_oplate()
        return wynik

    def przychod_miesieczny(self):
        return sum(c.karnet.miesieczna_oplata() for c in self._czlonkowie.values())

    def lista_osob(self):
        return list(self._czlonkowie.values()) + list(self._trenerzy.values())

    def raport(self):
        linie = [f"Klub: {self.nazwa}", "Osoby:"]
        for osoba in self.lista_osob():
            linie.append("  " + osoba.opis())
        linie.append("Zajecia:")
        for z in self._zajecia.values():
            linie.append("  " + str(z))
        linie.append(f"Prognozowany przychod miesieczny: {self.przychod_miesieczny():.2f} zl")
        return "\n".join(linie)


def main():
    klub = Klub("FitClub Lodz")

    standard = KarnetStandard("K001", "Standard", 120.0)
    premium = KarnetPremium("K002", "Premium", 120.0, 60.0)
    studencki = KarnetStudencki("K003", "Studencki", 120.0)

    anna = Czlonek("M001", "Anna", "Nowak", "anna.nowak@example.com", premium)
    piotr = Czlonek("M002", "Piotr", "Kowalski", "piotr.k@example.com", standard)
    kasia = Czlonek("M003", "Katarzyna", "Wisniewska", "kasia.w@example.com", studencki)

    marek = Trener("T001", "Marek", "Zielinski", "marek.z@example.com", "trening silowy")
    ewa = Trener("T002", "Ewa", "Lewandowska", "ewa.l@example.com", "plywanie")

    for c in (anna, piotr, kasia):
        klub.dodaj_czlonka(c)
    for t in (marek, ewa):
        klub.dodaj_trenera(t)

    obwodowy = Zajecia("Z001", "Trening obwodowy", marek, "silownia", 2, "pon 18:00")
    aqua = Zajecia("Z002", "Aqua aerobik", ewa, "basen", 10, "wt 19:00")
    klub.dodaj_zajecia(obwodowy)
    klub.dodaj_zajecia(aqua)

    anna.doplac(200)
    piotr.doplac(120)
    kasia.doplac(100)

    print("=== Zapisy na zajecia ===")
    proby = [("M001", "Z001"), ("M002", "Z001"), ("M003", "Z001"),
             ("M001", "Z002"), ("M002", "Z002")]
    for id_czlonka, id_zajec in proby:
        ok = klub.zapisz_na_zajecia(id_czlonka, id_zajec)
        print(f"{id_czlonka} -> {id_zajec}: {'zapisano' if ok else 'odmowa'}")

    print("\n=== Rozliczenie skladek ===")
    for osoba_id, oplacono in klub.rozlicz_skladki().items():
        print(f"{osoba_id}: {'oplacono' if oplacono else 'brak srodkow'}")

    print("\n=== Raport ===")
    print(klub.raport())


if __name__ == "__main__":
    main()
