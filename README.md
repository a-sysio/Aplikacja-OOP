# FitClub — system zarządzania klubem sportowym

## Temat aplikacji

Aplikacja konsolowa modelująca działanie klubu sportowego (siłownia + basen). Klub prowadzi rejestr członków i trenerów, oferuje różne rodzaje karnetów oraz organizuje zajęcia grupowe. Członek posiada karnet, który określa zakres dostępu do stref (siłownia, cardio, basen, sauna) oraz wysokość miesięcznej opłaty. Zapisy na zajęcia są weryfikowane pod kątem uprawnień karnetu, limitu miejsc i duplikatów. Klub potrafi rozliczyć składki oraz wygenerować raport.

Uruchomienie:

```bash
python main.py
```

## Lista klas

### `Karnet` (klasa abstrakcyjna) — `karnety.py`
Kontrakt dla wszystkich rodzajów karnetów.
- Właściwości: `karnet_id`, `nazwa`, `_cena_bazowa`
- Metody: `miesieczna_oplata()` (abstrakcyjna), `zakres_dostepu()` (abstrakcyjna), `__str__()`

### `KarnetStandard`, `KarnetPremium`, `KarnetStudencki` — `karnety.py`
Konkretne rodzaje karnetów. Każdy inaczej liczy opłatę i udostępnia inne strefy (Premium dodaje opłatę za basen i dostęp do basenu/sauny, Studencki nalicza 50% zniżki).
- Metody: `miesieczna_oplata()`, `zakres_dostepu()`

### `Osoba` (klasa abstrakcyjna) — `osoby.py`
Wspólna baza dla osób w systemie. Waliduje adres e-mail.
- Właściwości: `osoba_id`, `imie`, `nazwisko`, `email` (walidowane), `pelne_imie`
- Metody: `rola()` (abstrakcyjna), `opis()`

### `Czlonek` — `osoby.py`
Członek klubu z karnetem, saldem i historią wejść.
- Właściwości: `karnet`, `saldo` (tylko do odczytu), `_wejscia`
- Metody: `zmien_karnet()`, `doplac()`, `pobierz_oplate()`, `zarejestruj_wejscie()`, `liczba_wejsc()`, `rola()`, `opis()`

### `Trener` — `osoby.py`
Trener prowadzący zajęcia.
- Właściwości: `specjalizacja`
- Metody: `rola()`, `opis()`

### `Zajecia` — `zajecia.py`
Pojedyncze zajęcia prowadzone przez trenera, z listą zapisanych członków.
- Właściwości: `zajecia_id`, `nazwa`, `trener`, `strefa`, `termin`, `wolne_miejsca`, `_zapisani`
- Metody: `zapisz()`, `wypisz()`, `lista_uczestnikow()`, `__str__()`

### `Klub` — `klub.py`
Warstwa zarządzająca: przechowuje rejestry i obsługuje operacje na całym systemie.
- Właściwości: `nazwa`, rejestry `_czlonkowie`, `_trenerzy`, `_zajecia`
- Metody: `dodaj_czlonka()`, `dodaj_trenera()`, `dodaj_zajecia()`, `zapisz_na_zajecia()`, `rozlicz_skladki()`, `przychod_miesieczny()`, `lista_osob()`, `raport()`

## Relacje między klasami

- **Agregacja**: `Czlonek` ma `Karnet` przekazany w konstruktorze — karnet istnieje niezależnie od członka i może być współdzielony między obiektami.
- **Asocjacja przez właściwość / konstruktor**: `Zajecia` mają przypisanego `Trenera` (przekazanego w konstruktorze).
- **Kolekcja (wiele-do-wielu)**: `Zajecia` przechowują listę zapisanych obiektów `Czlonek`; jeden członek może być na wielu zajęciach.
- **Kompozycja + dostęp przez ID**: `Klub` tworzy i posiada rejestry (`dict`) członków, trenerów i zajęć, adresowane po identyfikatorze; operacje takie jak `zapisz_na_zajecia()` odwołują się do obiektów po ID.
- **Reguła między relacjami**: przy zapisie `Zajecia` odpytują `Karnet` członka o `zakres_dostepu()`, łącząc trzy klasy w jednej operacji.

## Cztery zasady OOP

- **Enkapsulacja**: `Czlonek._saldo` i `_wejscia` są ukryte, a zmieniane wyłącznie przez `doplac()` / `pobierz_oplate()` (z walidacją kwoty). `Osoba.email` ma setter sprawdzający poprawność adresu. Stan zajęć (`_zapisani`, `_limit_miejsc`) modyfikowany tylko metodami `zapisz()` / `wypisz()`.
- **Dziedziczenie**: `Osoba` → `Czlonek`, `Trener` oraz `Karnet` → `KarnetStandard`, `KarnetPremium`, `KarnetStudencki`.
- **Polimorfizm**: `Klub.raport()` iteruje po liście `Osoba` i wywołuje `opis()`, który zachowuje się inaczej dla członka i trenera. Analogicznie `miesieczna_oplata()` i `zakres_dostepu()` dają różny wynik dla różnych typów karnetów wywoływanych przez wspólny typ `Karnet`.
- **Abstrakcja**: `Karnet` i `Osoba` to klasy abstrakcyjne (`ABC`) z metodami `@abstractmethod` — definiują kontrakt bez implementacji, którego muszą dopełnić klasy szczegółowe.

## Struktura plików

```
fitclub/
├── karnety.py   # Karnet (abstrakcyjna) + 3 rodzaje karnetów
├── osoby.py     # Osoba (abstrakcyjna) + Czlonek, Trener
├── zajecia.py   # Zajecia
├── klub.py      # Klub (warstwa zarządzająca)
├── main.py      # przykładowe uruchomienie
└── README.md
```

AI użyłem przy:
- Zredagowaniu moich notatek do README.md
- Wykrywaniu błędów w kodzie
- Propozycji udoskonaleniu cześci kodu (np. klasy)
- Dodawaniu komentarzy do kodu dla przejrzystości i łatwiejszej orientacji
