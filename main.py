from datetime import datetime, timedelta
from enum import Enum
from prettytable import PrettyTable
import random
from colorama import Fore, Style

ADD_MEG_A_KOLCSONZO_NEVET = "Add meg a kölcsönző nevét: "
ADD_MEG_A_BICIKLI_ID_T = "Add meg a bicikli ID-t: "
ADD_MEG_A_KOLCSONZES_IDT = "Add meg a kölcsönzés ID-t: "
ERVENYTELEN_VALASZTAS = "Érvénytelen választás. Kérlek, válassz újra."
KOLCSONOZES_LEMONDVA = "Kölcsönzés lemondva."
SIKERES_KOLCSONZES = "Kölcsönzés sikeresen létrehozva."
ERVENYTELEN_DATUM = "Érvénytelen dátum! A biciklit csak a jövőben lehet kölcsönözni."
NINCS_MEG_A_KOLCSONZES = "A megadott kölcsönzés nem található vagy már lejárt."
NINCS_MEG_A_BICIKLI = "A megadott bicikli nem található vagy már kölcsönözve van."
HIBAS_ID_FORMATUM = "Hibás ID formátum. Kérlek, próbáld újra."
HIBAS_DATUM_FORMATUM = "Hibás dátum formátum. Kérlek, próbáld újra."
NINCS_ELEG_BICIKLI = "Nincs elég szabad bicikli a kölcsönzéshez."
KOLCSONZES_DATUM_STR = "Add meg a kölcsönzés dátumát (YYYY-MM-DD, üresen hagyva a mai dátum lesz): "


class Allapot(Enum):
    SZABAD = "Szabad"
    KOLCSONZES_ALATT = "Kölcsönzés alatt"


class Bicikli:
    bicikli_id_counter = 1
    biciklik = []

    def __init__(self, ar, allapot=Allapot.SZABAD):
        self.bicikli_id = Bicikli.bicikli_id_counter
        Bicikli.bicikli_id_counter += 1
        self.ar = ar
        self.allapot = allapot
        Bicikli.biciklik.append(self)

    @classmethod
    def listazas(cls):
        table = PrettyTable()
        table.field_names = ["Bicikli ID", "Bicikli típus", "Ár", "Állapot"]

        for bicikli in cls.biciklik:
            table.add_row([bicikli.bicikli_id, bicikli.tipus, bicikli.ar, bicikli.allapot.value])

        print(table)


class OrszagutiBicikli(Bicikli):
    tipus = "Országúti"


class HegyiBicikli(Bicikli):
    tipus = "Hegyi"


class BMXBicikli(Bicikli):
    tipus = "BMX"


class ElektromosBicikli(Bicikli):
    tipus = "Elektromos"


class Kolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.biciklik = []
        self.kolcsonzesek = []

    def bicikli_hozzaadasa(self, bicikli):
        self.biciklik.append(bicikli)

    def teszt_kolcsonzes(self, darab):
        teszt_nevek = ["Teszt Elek", "Végh Béla", "Cserepes Virág"]

        szabad_biciklik = [b for b in self.biciklik if b.allapot == Allapot.SZABAD]

        for _ in range(darab):
            if not szabad_biciklik:
                print_hiba(NINCS_ELEG_BICIKLI)
                break

            random.shuffle(szabad_biciklik)
            bicikli = szabad_biciklik.pop(0)

            datum = datetime.now().date() + timedelta(days=random.randint(1, 10))
            nev = random.choice(teszt_nevek)
            kolcsonzes = Kolcsonzes(bicikli, datum, nev)
            bicikli.allapot = Allapot.KOLCSONZES_ALATT
            self.kolcsonzesek.append(kolcsonzes)

    def biciklik_listazasa(self):
        Bicikli.listazas()

    def datum_bekerese(self):
        while True:
            datum_str = input(KOLCSONZES_DATUM_STR)
            if not datum_str:
                return datetime.now().date()
            try:
                datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
                if datum >= datetime.now().date():
                    return datum
                else:
                    print_hiba(ERVENYTELEN_DATUM)
            except ValueError:
                print_hiba(HIBAS_DATUM_FORMATUM)

    def bicikli_id_bekerese(self):
        Bicikli.listazas()
        while True:
            bicikli_id = input(ADD_MEG_A_BICIKLI_ID_T)
            try:
                bicikli_id = int(bicikli_id)
                bicikli = next((b for b in self.biciklik if b.bicikli_id == bicikli_id and b.allapot == Allapot.SZABAD),
                               None)
                if bicikli:
                    return bicikli_id
                else:
                    print_hiba(NINCS_MEG_A_BICIKLI)
            except ValueError:
                print_hiba(HIBAS_ID_FORMATUM)

    def kolcsonzes_id_bekerese(self):
        self.kolcsonzesek_listazasa()
        while True:
            kolcsonzes_id = input(ADD_MEG_A_KOLCSONZES_IDT)
            try:
                kolcsonzes_id = int(kolcsonzes_id)
                kolcsonzes = next((k for k in self.kolcsonzesek if
                                   k.kolcsonzes_id == kolcsonzes_id and k.datum >= datetime.now().date()), None)
                if kolcsonzes:
                    return kolcsonzes_id
                else:
                    print_hiba(NINCS_MEG_A_KOLCSONZES)
            except ValueError:
                print_hiba(HIBAS_ID_FORMATUM)

    def kolcsonzes_letrehozasa(self):
        szabad_biciklik = [b for b in self.biciklik if b.allapot == Allapot.SZABAD]

        if not szabad_biciklik:
            print_hiba(NINCS_ELEG_BICIKLI)
            return

        kolcsonzo_nev = input(ADD_MEG_A_KOLCSONZO_NEVET)

        while True:
            bicikli_id = self.bicikli_id_bekerese()
            datum = self.datum_bekerese()

            bicikli = next((b for b in self.biciklik if b.bicikli_id == bicikli_id and b.allapot == Allapot.SZABAD),
                           None)
            if bicikli:
                kolcsonzes = Kolcsonzes(bicikli, datum, kolcsonzo_nev)
                bicikli.allapot = Allapot.KOLCSONZES_ALATT
                self.kolcsonzesek.append(kolcsonzes)
                print_ok(SIKERES_KOLCSONZES)
                break
            else:
                print_hiba(NINCS_MEG_A_BICIKLI)

    def kolcsonzes_lemondasa(self):
        kolcsonzes_id = self.kolcsonzes_id_bekerese()
        while True:
            try:
                kolcsonzes_id = int(kolcsonzes_id)
                kolcsonzes = next((k for k in self.kolcsonzesek if
                                   k.kolcsonzes_id == kolcsonzes_id and k.datum >= datetime.now().date()), None)
                if kolcsonzes:
                    kolcsonzes.bicikli.allapot = Allapot.SZABAD
                    self.kolcsonzesek.remove(kolcsonzes)
                    print_ok(KOLCSONOZES_LEMONDVA)
                    break
                else:
                    print_hiba(NINCS_MEG_A_KOLCSONZES)
            except ValueError:
                print_hiba(HIBAS_ID_FORMATUM)

    def kolcsonzesek_listazasa(self):
        table = PrettyTable()
        table.field_names = ["ID", "Bicikli típus", "Bicikli ID", "Kölcsönzés dátuma", "Kölcsönző név"]

        for kolcsonzes in self.kolcsonzesek:
            table.add_row(
                [kolcsonzes.kolcsonzes_id, kolcsonzes.bicikli.tipus, kolcsonzes.bicikli.bicikli_id, kolcsonzes.datum,
                 kolcsonzes.kolcsonzo_nev])

        print(table)


class Kolcsonzes:
    kolcsonzes_id_counter = 1

    def __init__(self, bicikli, datum, kolcsonzo_nev):
        self.kolcsonzes_id = Kolcsonzes.kolcsonzes_id_counter
        Kolcsonzes.kolcsonzes_id_counter += 1
        self.bicikli = bicikli
        self.datum = datum
        self.kolcsonzo_nev = kolcsonzo_nev


def print_hiba(message):
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")


def print_ok(message):
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")


kolcsonzo = Kolcsonzo("BikeRent")

kolcsonzo.bicikli_hozzaadasa(OrszagutiBicikli(100))
kolcsonzo.bicikli_hozzaadasa(OrszagutiBicikli(100))
kolcsonzo.bicikli_hozzaadasa(OrszagutiBicikli(100))
kolcsonzo.bicikli_hozzaadasa(HegyiBicikli(150))
kolcsonzo.bicikli_hozzaadasa(HegyiBicikli(150))
kolcsonzo.bicikli_hozzaadasa(HegyiBicikli(150))
kolcsonzo.bicikli_hozzaadasa(BMXBicikli(120))
kolcsonzo.bicikli_hozzaadasa(BMXBicikli(120))
kolcsonzo.bicikli_hozzaadasa(BMXBicikli(120))
kolcsonzo.bicikli_hozzaadasa(ElektromosBicikli(200))
kolcsonzo.teszt_kolcsonzes(5)

menu_items = ["Kölcsönzés", "Kölcsönzés lemondása", "Kölcsönzések listázása", "Biciklik listázása", "Kilépés"]

while True:
    print("\nVálassz műveletet:")
    for i, item in enumerate(menu_items):
        print(f"{i + 1}. {item}")

    try:
        selected_item = int(input("Válassz (1-5): "))
        if 1 <= selected_item <= len(menu_items):
            selected_item -= 1
        else:
            print_hiba(ERVENYTELEN_VALASZTAS)
            continue
    except ValueError:
        print_hiba(ERVENYTELEN_VALASZTAS)
        continue

    if selected_item == 0:
        kolcsonzo.kolcsonzes_letrehozasa()
    elif selected_item == 1:
        kolcsonzo.kolcsonzes_lemondasa()
    elif selected_item == 2:
        kolcsonzo.kolcsonzesek_listazasa()
    elif selected_item == 3:
        kolcsonzo.biciklik_listazasa()
    elif selected_item == 4:
        break
