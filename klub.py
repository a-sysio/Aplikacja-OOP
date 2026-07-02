# Klasa Klub to warstwa zarzadzajaca - trzyma rejestry i obsluguje operacje na calym systemie.
# Jedna odpowiedzialnosc: koordynacja, a nie logika pojedynczego karnetu czy zajec.
class Klub:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        # KOMPOZYCJA + DOSTEP PRZEZ ID: rejestry jako slowniki {id: obiekt}
        self._czlonkowie = {}
        self._trenerzy = {}
        self._zajecia = {}

    def dodaj_czlonka(self, czlonek):
        self._czlonkowie[czlonek.osoba_id] = czlonek

    def dodaj_trenera(self, trener):
        self._trenerzy[trener.osoba_id] = trener

    def dodaj_zajecia(self, zajecia):
        self._zajecia[zajecia.zajecia_id] = zajecia

    # operacja na dwoch obiektach odszukanych po ID
    def zapisz_na_zajecia(self, id_czlonka, id_zajec):
        czlonek = self._czlonkowie.get(id_czlonka)
        zajecia = self._zajecia.get(id_zajec)
        if czlonek is None or zajecia is None:
            return False
        return zajecia.zapisz(czlonek)

    # probuje pobrac skladke od kazdego czlonka; wynik: {id: czy_oplacono}
    def rozlicz_skladki(self):
        wynik = {}
        for czlonek in self._czlonkowie.values():
            wynik[czlonek.osoba_id] = czlonek.pobierz_oplate()
        return wynik

    # POLIMORFIZM: sumuje oplaty roznych typow karnetow przez wspolna metode
    def przychod_miesieczny(self):
        return sum(c.karnet.miesieczna_oplata() for c in self._czlonkowie.values())

    def lista_osob(self):
        return list(self._czlonkowie.values()) + list(self._trenerzy.values())

    # POLIMORFIZM: dla kazdej osoby wolamy opis(), ktory dziala inaczej dla czlonka i trenera
    def raport(self):
        linie = [f"Klub: {self.nazwa}", "Osoby:"]
        for osoba in self.lista_osob():
            linie.append("  " + osoba.opis())
        linie.append("Zajecia:")
        for z in self._zajecia.values():
            linie.append("  " + str(z))
        linie.append(f"Prognozowany przychod miesieczny: {self.przychod_miesieczny():.2f} zl")
        return "\n".join(linie)
