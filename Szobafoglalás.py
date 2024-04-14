from abc import ABC
from datetime import datetime, timedelta
import random


class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar


class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar):
        super().__init__(szobaszam, ar)
        self.agyak_szama = 1
        self.letszam = 1


class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar):
        super().__init__(szobaszam, ar)
        self.agyak_szama = 2
        self.letszam = 2


class Szalloda:
    def __init__(self, nev, csillagok_szama, szobak):
        self.nev = nev
        self.csillagok_szama = csillagok_szama
        self.szobak = szobak
        self.foglalasok = []

    def foglal(self, szoba, datum):
        if datum.date() >= datetime.now().date() and not any(f.datum.date() == datum.date() and f.szoba == szoba for f
                                                             in self.foglalasok):
            self.foglalasok.append(Foglalas(szoba, datum))
            return szoba.ar
        else:
            return "\nA foglalás sikertelen. A szoba már foglalt ezen a dátumon."

    def lemond(self, szobaszam, datum):
        szobaszam = int(szobaszam)
        szoba = next((s for s in self.szobak if s.szobaszam == szobaszam), None)
        if szoba:
            foglalasok = [f for f in self.foglalasok if f.szoba == szoba and f.datum.date() == datum.date()]
            if foglalasok:
                for foglalas in foglalasok:
                    self.foglalasok.remove(foglalas)
                return "\nA foglalás lemondva."
        return "\nA foglalás nem létezik."

    def listaz(self):
        foglalasok = sorted(self.foglalasok, key=lambda f: (f.szoba.szobaszam, f.datum))
        foglalasok_listazva = []
        for foglalas in foglalasok:
            if foglalas.datum.date() >= datetime.now().date():
                foglalasok_listazva.append(f"{foglalas.szoba.szobaszam}. "
                                           f"szoba foglalt {foglalas.datum.strftime('%Y-%m-%d')} dátumra")
        return foglalasok_listazva


class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum


def main():
    szobak = [EgyagyasSzoba(1, 10000), KetagyasSzoba(2, 15000), EgyagyasSzoba(3, 10000)]
    szalloda = Szalloda("Hotel Gyula", 3, szobak)
    for i in range(5):
        szoba = random.choice(szobak)
        datum = datetime.now() + timedelta(days=random.randint(0, 10))
        while any(f.szoba == szoba and f.datum == datum for f in szalloda.foglalasok):
            szoba = random.choice(szobak)
            datum = datetime.now() + timedelta(days=random.randint(1, 10))
        szalloda.foglalasok.append(Foglalas(szoba, datum))

    while True:
        print("\nÜdvözöljük a Hotel Gyula foglalási rendszerében!")
        print("Kérem válasszon az alábbi menüpontok közül:")
        print("1. Szobafoglalás")
        print("2. Foglalás lemondása")
        print("3. Foglalások listája")
        print("4. Kilépés")

        valasztas = input("Válassz egy lehetőséget: ")

        if valasztas == "1":
            print("\nVálasztható szobatípusok:")
            for szoba in szobak:
                szoba_tipus = 'Egyágyas' if isinstance(szoba, EgyagyasSzoba) else 'Kétágyas'
                print(f"Szobaszám: {szoba.szobaszam}, Típus: {szoba_tipus}")
            while True:
                szobaszam = int(input("Add meg a lefoglalni kívánt szoba számát: "))
                szoba = next((szoba for szoba in szobak if szoba.szobaszam == szobaszam), None)
                if szoba is not None:
                    break
                else:
                    print("A megadott szobaszám nem létezik. Kérlek, próbáld újra.")
            while True:
                try:
                    datum = datetime.strptime(input("Add meg a dátumot (YYYY-MM-DD formátumban): "), "%Y-%m-%d")
                    if datum.date() < datetime.now().date() and datum.date() != datetime.now().date():
                        print("A dátum régebbi mint a mai. Kérlek, add meg újra a dátumot.")
                    else:
                        break
                except ValueError:
                    print("Hibás dátum formátum. Kérlek, add meg újra a dátumot.")
            szoba = next((szoba for szoba in szobak if szoba.szobaszam == szobaszam), None)
            if szoba and all(foglalas.szoba != szoba or foglalas.datum != datum for foglalas in szalloda.foglalasok):
                foglalas_eredmeny = szalloda.foglal(szoba, datum)
                if foglalas_eredmeny != "\nA foglalás sikertelen. A szoba már foglalt ezen a dátumon.":
                    print(f"\nA foglalás sikeres. \nA foglalás ára: {foglalas_eredmeny} Ft.")
                else:
                    print(foglalas_eredmeny)

        elif valasztas == "2":
            while True:
                szobaszam = int(input("Add meg a törölni kíván foglalás szoba számát: "))
                szoba = next((szoba for szoba in szobak if szoba.szobaszam == szobaszam), None)
                if szoba is not None:
                    break
                else:
                    print("A megadott szobaszám nem létezik. Kérlek, próbáld újra.")
            while True:
                try:
                    datum = datetime.strptime(input("Add meg a dátumot (YYYY-MM-DD formátumban): "), "%Y-%m-%d")
                    if datum.date() < datetime.now().date():
                        print("A dátum régebbi mint a mai. Kérlek, add meg újra a dátumot.")
                    else:
                        break
                except ValueError:
                    print("Hibás dátum formátum. Kérlek, add meg újra a dátumot.")
            if szoba:
                print(szalloda.lemond(szoba.szobaszam, datum))
            else:
                print("\nA foglalás nem létezik.")

        elif valasztas == "3":
            reservations = szalloda.listaz()
            if reservations:
                print("\nAz alábbi foglalások vannak rögzítve:")
                for reservation in reservations:
                    print(reservation)
            else:
                print("\nNincs foglalt szoba")

        elif valasztas == "4":
            break
        else:
            print("\nNincs ilyen lehetőség.")


if __name__ == "__main__":
    main()
