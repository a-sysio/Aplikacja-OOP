# Klasa Zajecia laczy trenera z lista zapisanych czlonkow.
# Jedna odpowiedzialnosc: pilnowanie regul zapisu (dostep, limit, duplikaty).
class Zajecia:
    def __init__(self, zajecia_id, nazwa, trener, strefa, limit_miejsc, termin):
        self.zajecia_id = zajecia_id
        self.nazwa = nazwa
        self._trener = trener            # ASOCJACJA: zajecia maja przypisanego trenera
        self.strefa = strefa             # np. "silownia" albo "basen"
        self._limit_miejsc = limit_miejsc
        self.termin = termin
        self._zapisani = []              # KOLEKCJA (wiele-do-wielu): lista zapisanych czlonkow

    @property
    def trener(self):
        return self._trener

    # liczba wolnych miejsc obliczana na biezaco
    @property
    def wolne_miejsca(self):
        return self._limit_miejsc - len(self._zapisani)

    # reguly zapisu - zwraca True gdy sie udalo, False gdy odmowa
    def zapisz(self, czlonek):
        # POLIMORFIZM: pytamy karnet czlonka o zakres dostepu (rozny dla roznych karnetow)
        if self.strefa not in czlonek.karnet.zakres_dostepu():
            return False
        if self.wolne_miejsca <= 0:            # brak miejsc
            return False
        if czlonek in self._zapisani:          # juz zapisany
            return False
        self._zapisani.append(czlonek)
        return True

    def wypisz(self, czlonek):
        if czlonek in self._zapisani:
            self._zapisani.remove(czlonek)
            return True
        return False

    # zwraca kopie listy, zeby nie dalo sie zmienic oryginalu z zewnatrz
    def lista_uczestnikow(self):
        return list(self._zapisani)

    def __str__(self):
        return f"{self.nazwa} ({self.zajecia_id}) prow. {self._trener.pelne_imie}, {self.termin}, wolne: {self.wolne_miejsca}"
