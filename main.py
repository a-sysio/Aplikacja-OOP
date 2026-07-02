from karnety import KarnetStandard, KarnetPremium, KarnetStudencki
from osoby import Czlonek, Trener
from zajecia import Zajecia
from klub import Klub


def main():
    klub = Klub("FitClub Lodz")

    # tworzenie obiektow karnetow (rozne typy - beda uzyte polimorficznie)
    standard = KarnetStandard("K001", "Standard", 120.0)
    premium = KarnetPremium("K002", "Premium", 120.0, 60.0)
    studencki = KarnetStudencki("K003", "Studencki", 120.0)

    # czlonkowie - kazdy dostaje karnet przez konstruktor (agregacja)
    anna = Czlonek("M001", "Anna", "Nowak", "anna.nowak@example.com", premium)
    piotr = Czlonek("M002", "Piotr", "Kowalski", "piotr.k@example.com", standard)
    kasia = Czlonek("M003", "Katarzyna", "Wisniewska", "kasia.w@example.com", studencki)

    marek = Trener("T001", "Marek", "Zielinski", "marek.z@example.com", "trening silowy")
    ewa = Trener("T002", "Ewa", "Lewandowska", "ewa.l@example.com", "plywanie")

    for c in (anna, piotr, kasia):
        klub.dodaj_czlonka(c)
    for t in (marek, ewa):
        klub.dodaj_trenera(t)

    # zajecia z przypisanym trenerem, strefa i limitem miejsc
    obwodowy = Zajecia("Z001", "Trening obwodowy", marek, "silownia", 2, "pon 18:00")
    aqua = Zajecia("Z002", "Aqua aerobik", ewa, "basen", 10, "wt 19:00")
    klub.dodaj_zajecia(obwodowy)
    klub.dodaj_zajecia(aqua)

    # wplaty na konto czlonkow
    anna.doplac(200)
    piotr.doplac(120)
    kasia.doplac(100)

    # proby zapisow - czesc odmowna (brak miejsc lub brak dostepu w karnecie)
    print("=== Zapisy na zajecia ===")
    proby = [("M001", "Z001"), ("M002", "Z001"), ("M003", "Z001"),
             ("M001", "Z002"), ("M002", "Z002")]
    for id_czlonka, id_zajec in proby:
        ok = klub.zapisz_na_zajecia(id_czlonka, id_zajec)
        print(f"{id_czlonka} -> {id_zajec}: {'zapisano' if ok else 'odmowa'}")

    # pobranie miesiecznych skladek
    print("\n=== Rozliczenie skladek ===")
    for osoba_id, oplacono in klub.rozlicz_skladki().items():
        print(f"{osoba_id}: {'oplacono' if oplacono else 'brak srodkow'}")

    # zbiorczy raport klubu
    print("\n=== Raport ===")
    print(klub.raport())


if __name__ == "__main__":
    main()
