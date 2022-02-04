import sys
import getpass
import cx_Oracle
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import datetime
from distutils.debug import DEBUG
from SQL_main_app import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_21_3")

hostname = 'admlab2.cs.put.poznan.pl'
servicename = 'dblab02_students.cs.put.poznan.pl'

# pwd = getpass.getpass('Hasło:\n')


cnxn = cx_Oracle.connect(user='inf145220', password='inf145220', dsn='%s/%s' % (hostname, servicename), encoding="UTF-8")
cursor = cnxn.cursor()

class CardWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('pokaz_karta.ui', self)


class SelectWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('search_window.ui', self)


class SQLappWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('SQL_main_app.ui', self)
        # self.setupUi(self)

        self.dyr_butt.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.piel_butt.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.lek_butt.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.d_backtomain.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.p_backtomain.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.l_backtomain.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        self.tabWidget.currentChanged.connect(self.deactivate_buttons)
        self.tabWidget_2.currentChanged.connect(self.deactivate_buttons)
        self.tabWidget_3.currentChanged.connect(self.deactivate_buttons)

        # dyrektor
        self.d_add.clicked.connect(self.add_as_dyrektor)
        self.d_edit.clicked.connect(self.modify_as_dyrektor)
        self.d_search.clicked.connect(self.search_as_dyrektor)

        self.d_piel_gMod_butt.clicked.connect(self.load_data_dyrektor)
        self.d_lek_gMod_butt.clicked.connect(self.load_data_dyrektor)
        self.d_sal_gMod_butt.clicked.connect(self.load_data_dyrektor)

        # pielegniarka
        self.p_add.clicked.connect(self.add_as_piel)
        self.p_delete.clicked.connect(self.del_as_piel)
        self.p_edit.clicked.connect(self.modify_as_piel)
        self.p_search.clicked.connect(self.search_as_piel)

        self.p_pac_gMod_butt.clicked.connect(self.load_data_piel)
        self.p_bed_gMod_butt.clicked.connect(self.load_data_piel)
        self.p_assign_gMod_butt.clicked.connect(self.load_data_piel)

        # lekarz
        self.l_add.clicked.connect(self.add_as_lek)
        self.l_delete.clicked.connect(self.del_as_lekarz)
        self.l_edit.clicked.connect(self.modify_as_lekarz)
        self.l_search.clicked.connect(self.search_as_lekarz)

        self.l_klc_gMod_butt.clicked.connect(self.load_data_lekarz)
        self.l_appoin_gMod_butt.clicked.connect(self.load_data_lekarz)
        self.l_oper_gMod_butt.clicked.connect(self.load_data_lekarz)
        self.l_chor_gMod_butt.clicked.connect(self.load_data_lekarz)

        self.d_show_all.clicked.connect(
            lambda: self.show_all(self.tabWidget.tabText(self.tabWidget.currentIndex())))
        self.p_show_all.clicked.connect(
            lambda: self.show_all(self.tabWidget_2.tabText(self.tabWidget_2.currentIndex())))
        self.l_show_all.clicked.connect(
            lambda: self.show_all(self.tabWidget_3.tabText(self.tabWidget_3.currentIndex())))

        self.p_pac_gKLC_butt.clicked.connect(self.show_karta)
        self.l_klc_gKLC_butt.clicked.connect(self.show_karta)

    def deactivate_buttons(self):
        if self.stackedWidget.currentIndex() == 1:
            self.d_add.setEnabled(True)
            self.d_search.setEnabled(True)
            self.d_delete.setEnabled(True)
            self.d_edit.setEnabled(True)
            if self.tabWidget.currentIndex() == 0:
                self.d_delete.setEnabled(False)
            elif self.tabWidget.currentIndex() == 1:
                self.d_delete.setEnabled(False)
                self.d_edit.setEnabled(False)
            elif self.tabWidget.currentIndex() == 2:
                self.d_add.setEnabled(False)
                self.d_search.setEnabled(False)
                self.d_delete.setEnabled(False)
        elif self.stackedWidget.currentIndex() == 2:
            self.p_add.setEnabled(True)
            self.p_search.setEnabled(True)
            self.p_delete.setEnabled(True)
            self.p_edit.setEnabled(True)
            if self.tabWidget_2.currentIndex() == 2:
                self.p_add.setEnabled(False)
                self.p_delete.setEnabled(False)
                self.p_search.setEnabled(False)
            elif self.tabWidget_2.currentIndex() == 3:
                self.p_add.setEnabled(False)
                self.p_search.setEnabled(False)
            elif self.tabWidget_2.currentIndex() == 1 or self.tabWidget_2.currentIndex() == 0:
                self.p_delete.setEnabled(False)
                self.p_edit.setEnabled(False)
            elif self.tabWidget_2.currentIndex() == 4:
                self.p_add.setEnabled(False)
                self.p_search.setEnabled(False)
                self.p_delete.setEnabled(False)
                self.p_edit.setEnabled(False)
        elif self.stackedWidget.currentIndex() == 3:
            self.l_add.setEnabled(True)
            self.l_search.setEnabled(True)
            self.l_delete.setEnabled(True)
            self.l_edit.setEnabled(True)
            if self.tabWidget_3.currentIndex() == 4:
                self.l_add.setEnabled(False)
                self.l_delete.setEnabled(False)
            elif self.tabWidget_3.currentIndex() == 3:
                self.l_add.setEnabled(False)
                self.l_delete.setEnabled(False)
                self.l_edit.setEnabled(False)
            elif self.tabWidget_3.currentIndex() in (1, 2):
                self.l_edit.setEnabled(False)
            elif self.tabWidget_3.currentIndex() == 5:
                self.l_delete.setEnabled(False)
                self.l_edit.setEnabled(False)
            elif self.tabWidget_3.currentIndex() == 6:
                self.l_add.setEnabled(False)
                self.l_search.setEnabled(False)
                self.l_delete.setEnabled(False)
                self.l_edit.setEnabled(False)

    def add_as_dyrektor(self):
        if self.tabWidget.currentIndex() == 0:
            imie = self.d_piel_gM_imie_edit.text().upper()
            nazwisko = self.d_piel_gM_nazw_edit.text().upper()

            insert_pracownik = """INSERT INTO pracownik VALUES (DEFAULT, :imie, :nazwisko, :zatrudniony)"""
            cursor.prepare(insert_pracownik)

            cursor.execute(None,
                           imie=imie,
                           nazwisko=nazwisko,
                           zatrudniony=datetime.datetime.now()
                           )
            insert_pielegniarka = 'INSERT INTO pielegniarka VALUES ((SELECT max(id_prac) FROM pracownik), '') '
            cursor.execute(insert_pielegniarka)
            print("dodałem pielegniarke")
        if self.tabWidget.currentIndex() == 1:
            imie = self.d_lek_gM_imie_edit.text().upper()
            nazwisko = self.d_lek_gM_nazw_edit.text().upper()
            specjal = self.d_lek_gM_spec_edit.text().upper()

            insert_pracownik = """INSERT INTO pracownik VALUES (DEFAULT, :imie, :nazwisko, :zatrudniony)"""
            cursor.prepare(insert_pracownik)

            cursor.execute(None,
                           imie=imie,
                           nazwisko=nazwisko,
                           zatrudniony=datetime.datetime.now()
                           )

            insert_lekarz = (
                'INSERT INTO lekarz VALUES ((SELECT max(id_prac) FROM pracownik), :SPECJALIZACJA, (SELECT min(id_sali) FROM sala WHERE typ in \'gabinet lekarski\'))')
            cursor.execute(insert_lekarz, [specjal])

            print("dodałem lekarza")

    def load_data_dyrektor(self):
        # TODO zrobić funkcje zeby wyswietlalo sie okno o pustym polu
        if self.tabWidget.currentIndex() == 0:
            found = False
            id_prac = self.d_piel_gMod_idpiel_edit.text()
            imie = ""
            nazwisko = ""
            # select po id_prac
            # wprowadz otrzymany wynik do imienia i nazwiska
            # /błąd jak nie ma takiego rekordu/
            cursor.execute(
                "SELECT pielegniarka.id_prac, imie, nazwisko, zatrudniony, id_sali FROM pielegniarka join pracownik on pracownik.id_prac = pielegniarka.id_prac")
            for item in cursor:
                if str(item[0]) == id_prac:
                    item = tuple(map(str, item))
                    imie, nazwisko = item[1], item[2]
                    found = True
                    break
            if not found:
                print("nie ma takiego pracownika")
                # error messagebox
            else:
                self.d_piel_gM_imie_edit.setText(imie)
                self.d_piel_gM_nazw_edit.setText(nazwisko)

                print("laduje piel")
        if self.tabWidget.currentIndex() == 2:
            found = False
            typ = ""
            id_sali = self.d_sal_gMod_idsali_edit.text()
            # select po id_sali
            # wprowadz otrzymany wynik do pól
            # /błąd jak nie ma takiego rekordu/

            cursor.execute(
                "SELECT id_sali, typ FROM sala")
            for item in cursor:
                if str(item[0]) == id_sali:
                    item = tuple(map(str, item))
                    typ = item[1]
                    found = True
                    break
            if not found:
                print("nie ma takiej sali")
            else:
                self.d_sal_gM_type_combo.setCurrentIndex(self.d_sal_gM_type_combo.findText(typ))
                print("laduje sale")

    def modify_as_dyrektor(self):
        if self.tabWidget.currentIndex() == 0:
            id_prac = self.d_piel_gMod_idpiel_edit.text()
            imie = self.d_piel_gM_imie_edit.text().upper()
            nazwisko = self.d_piel_gM_nazw_edit.text().upper()
            # sprawdz czy istnieje

            update_nazwisko = 'UPDATE pielegniarka SET nazwisko = :naz WHERE id_prac = :id'

            cursor.execute(update_nazwisko, [nazwisko, id_prac])
            cursor.execute("COMMIT")
            print("modify piel")
        if self.tabWidget.currentIndex() == 2:
            id_sali = self.d_sal_gMod_idsali_edit.text()
            typ_sali = self.d_sal_gM_type_combo.currentText()
            # sprawdz czy istnieje sala po id_sali

            updateSala = ('UPDATE sala SET typ = :typp WHERE id_sali = :id_salii')
            cursor.execute(updateSala, [typ_sali, id_sali])
            cursor.execute("COMMIT")
            print("modify sala")

    def search_as_dyrektor(self):
        if self.tabWidget.currentIndex() == 0:
            imie = self.d_piel_gM_imie_edit.text().upper()
            nazwisko = self.d_piel_gM_nazw_edit.text().upper()
            # jezeli nic nie ma daj bład
            # select * from cos tam where imie = cos nazwisko = cos
            self.window = SelectWidget()
            self.window.tabela.setColumnCount(4)
            self.window.tabela.setRowCount(10)
            self.window.tabela.setHorizontalHeaderLabels(["Imie", "Nazwisko", "Zatrudniony", "Nr sali"])
            occur = False
            cursor.execute(
                "SELECT imie, nazwisko, zatrudniony, id_sali FROM pielegniarka join pracownik on pracownik.id_prac = pielegniarka.id_prac")

            tablerow = 0
            for item in cursor:
                item = tuple(map(str, item))
                if imie != '':
                    if imie == item[0]:
                        occur = True
                    else:
                        occur = False
                        continue
                if nazwisko != '':
                    if nazwisko == item[1]:
                        occur = True
                    else:
                        occur = False
                        continue

                if occur:
                    for i in range(4):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1

            print("search piel")
        if self.tabWidget.currentIndex() == 1:
            imie = self.d_lek_gM_imie_edit.text().upper()
            nazwisko = self.d_lek_gM_nazw_edit.text().upper()
            specjal = self.d_lek_gM_spec_edit.text().upper()
            self.window = SelectWidget()
            self.window.tabela.setColumnCount(5)
            self.window.tabela.setRowCount(10)
            self.window.tabela.setHorizontalHeaderLabels(["Imie", "Nazwisko", "Zatrudniony", "Nr sali", "Specjalizacja"])
            occur = False
            cursor.execute(
                "SELECT imie, nazwisko, zatrudniony, id_sali as nr_sali, specjalizacja  FROM pracownik join lekarz on pracownik.id_prac = lekarz.id_prac")

            tablerow = 0
            for item in cursor:
                item = tuple(map(str, item))
                if imie != '':
                    if imie == item[0]:
                        occur = True
                    else:
                        occur = False
                        continue
                if nazwisko != '':
                    if nazwisko == item[1]:
                        occur = True
                    else:
                        occur = False
                        continue
                if specjal != '':
                    if specjal == item[2]:
                        occur = True
                    else:
                        occur = False
                        continue
                if occur:
                    for i in range(5):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1
            print("search lek")

    def add_as_piel(self):
        if self.tabWidget_2.currentIndex() == 0:
            imie = self.p_pac_gM_imie_edit.text().upper()
            nazwisko = self.p_pac_gM_nazw_edit.text().upper()
            pesel = self.p_pac_gM_pesel_edit.text()
            data_uro_r = self.p_pac_gM_date_dedit.date().year()
            data_uro_m = self.p_pac_gM_date_dedit.date().month()
            data_uro_d = self.p_pac_gM_date_dedit.date().day()

            # sprawdz czy nie ma o tym samym peselu

            insert_pacjent = """INSERT INTO pacjent VALUES (:pesel, :imie, :nazwisko, :data_ur)"""
            cursor.prepare(insert_pacjent)

            cursor.execute(None,
                           pesel=pesel,
                           imie=imie,
                           nazwisko=nazwisko,
                           data_ur=datetime.date(data_uro_r, data_uro_m, data_uro_d)
                           )

            print("dodaj pacjent")
        if self.tabWidget_2.currentIndex() == 1:
            imie_o = self.p_odw_gM_imie_edit.text().upper()
            nazwisko_o = self.p_odw_gM_nazw_edit.text().upper()
            pesel_o = self.p_odw_gM_peselO_edit.text()
            pesel = self.p_odw_gM_pesel_edit.text()
            st_pok = self.p_odw_gM_pokr_combo.currentText()

            insert_pracownik = """INSERT INTO odwiedziny VALUES (:data_odw, :pesel_odw, :pesel, :imie_odw, :nazwisko_odw, :st_pokr)"""
            cursor.prepare(insert_pracownik)

            cursor.execute(None,
                           data_odw=datetime.datetime.now(),
                           pesel=pesel,
                           pesel_odw=pesel_o,
                           imie_odw=imie_o,
                           nazwisko_odw=nazwisko_o,
                           st_pokr=st_pok
                           )
            print("dodaj odwiedziny")

    def del_as_piel(self):
        if self.tabWidget_2.currentIndex() == 3:
            id_prac = self.p_assign_gU_idpiel_edit.text()
            # jezeli puste info
            # jezeli istenieje ok jezeli nie to powiadom

            update_pielegniarka = 'UPDATE pielegniarka SET id_sali = :id_salii WHERE id_prac = :id'

            cursor.execute(update_pielegniarka, ["", id_prac])
            cursor.execute("COMMIT")
            print("usun przypisanie do sali")

    def load_data_piel(self):
        if self.tabWidget_2.currentIndex() == 2:
            found = False
            id_sali, pesel, usytuowanie, respirator = "", "", "", ""
            id_lozka = self.p_bed_gMod_idbed_edit.text()
            # jezeli puste notyfikacja
            # select po unikat
            cursor.execute(
                "SELECT id_lozka, id_sali, pesel, usytuowanie, respirator FROM lozko")
            for item in cursor:
                if str(item[0]) == id_lozka:
                    item = tuple(map(str, item))
                    id_sali, pesel, usytuowanie, respirator = item[1], item[2], item[3], item[4]
                    found = True
                    break
            if not found:
                print("nie ma takiego pracownika")
                # error messagebox
            else:
                self.p_bed_gM_plc_combo.setCurrentIndex(self.p_bed_gM_plc_combo.findText(usytuowanie))
                self.p_bed_gM_res_combo.setCurrentIndex(self.p_bed_gM_res_combo.findText(respirator))
                self.p_bed_gM_idsali_edit.setText(id_sali)
                self.p_bed_gM_pesel_edit.setText(pesel)
                print("zaladuj lozko")
        if self.tabWidget_2.currentIndex() == 3:
            found = False
            id_sali = ""
            id_prac = self.p_assign_gMod_idpiel_edit.text()
            # jezeli puste notify
            # select po unikat
            cursor.execute(
                "SELECT pielegniarka.id_prac, id_sali FROM pielegniarka join pracownik on pracownik.id_prac = pielegniarka.id_prac")
            for item in cursor:
                if str(item[0]) == id_prac:
                    item = tuple(map(str, item))
                    id_sali = item[1]
                    found = True
                    break
            if not found:
                print("nie ma takiego pracownika")
                # error messagebox
            else:
                self.p_assign_gM_idsali_edit.setText(id_sali)
                print("zaladuj przypis")

    def modify_as_piel(self):
        if self.tabWidget_2.currentIndex() == 2:
            id_lozka = self.p_bed_gMod_idbed_edit.text()
            # jezeli puste notyfikacja
            # select po unikat
            polozenie = self.p_bed_gM_plc_combo.currentText()
            resp = self.p_bed_gM_res_combo.currentText()
            id_sali = self.p_bed_gM_idsali_edit.text()
            pesel = self.p_bed_gM_pesel_edit.text()
            # update

            update_lozko = ('UPDATE lozko SET pesel = :psl WHERE id_lozka = :id')
            cursor.execute(update_lozko, [pesel, id_lozka])
            cursor.execute("COMMIT")
            print("update lozko")
        if self.tabWidget_2.currentIndex() == 3:
            id_prac = self.p_assign_gMod_idpiel_edit.text()
            # jezeli puste notify
            # select po unikat
            id_sali = self.p_assign_gM_idsali_edit.text()
            # sprawdz czy sala istnieje jak nie error message
            update_pielegniarka = 'UPDATE pielegniarka SET id_sali = :id_salii WHERE id_prac = :id'

            cursor.execute(update_pielegniarka, [id_sali, id_prac])
            cursor.execute("COMMIT")
            print("update przypis")

    def search_as_piel(self):
        if self.tabWidget_2.currentIndex() == 0:
            # jezeli puste notyfikacja
            imie = self.p_pac_gM_imie_edit.text().upper()
            nazwisko = self.p_pac_gM_nazw_edit.text().upper()
            pesel = self.p_pac_gM_pesel_edit.text().upper()
            data = self.p_pac_gM_date_dedit.date().toString("yyyy-MM-dd")
            # select po tym co nie jest null
            self.window = SelectWidget()
            self.window.tabela.setColumnCount(4)
            self.window.tabela.setRowCount(10)
            self.window.tabela.setHorizontalHeaderLabels(["PESEL", "Imie", "Nazwisko", "Data urodzenia"])
            occur = False

            cursor.execute(
                 "SELECT p.* FROM pacjent p")

            tablerow = 0
            for item in cursor:
                item = tuple(map(str, item))
                if pesel != '':
                    if pesel == item[0]:
                        occur = True
                    else:
                        occur = False
                        continue
                if imie != '':
                    if imie == item[1]:
                        occur = True
                    else:
                        occur = False
                        continue
                if nazwisko != '':
                    if nazwisko == item[2]:
                        occur = True
                    else:
                        occur = False
                        continue

                if occur:
                    for i in range(4):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1
            print("szukaj pacjent")
        if self.tabWidget_2.currentIndex() == 1:
            imie_o = self.p_odw_gM_imie_edit.text()
            nazwisko_o = self.p_odw_gM_nazw_edit.text()
            pesel_o = self.p_odw_gM_peselO_edit.text()
            pesel = self.p_odw_gM_pesel_edit.text()
            st_pok = self.p_odw_gM_pokr_combo.currentText()
            # select po tym co nie jest null
            self.window = SelectWidget()
            self.window.tabela.setColumnCount(6)
            self.window.tabela.setRowCount(50)
            self.window.tabela.setHorizontalHeaderLabels(["Imie", "Nazwisko", "Imie odwiedzajacego", "Nazwisko odwiedzajacego", "Stopien pokrewienstwa",
                     "Data odwiedzin"])
            occur = False
            cursor.execute(
                "SELECT imie, nazwisko, imie_odw, nazwisko_odw, st_pokrewienstwa, data_odw FROM odwiedziny o join pacjent p on p.pesel = o.pesel")

            tablerow = 0
            for item in cursor:
                item = tuple(map(str, item))
                if imie_o != '':
                    if imie_o == item[2]:
                        occur = True
                    else:
                        occur = False
                        continue
                if nazwisko_o != '':
                    if nazwisko_o == item[3]:
                        occur = True
                    else:
                        occur = False
                        continue

                if occur:
                    for i in range(6):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1
            print("szukaj odwiedz")

    def add_as_lek(self):
        if self.tabWidget_3.currentIndex() == 0:
            pesel = self.l_klc_gM_pesel_edit.text()
            nazwa_chor = self.l_klc_gM_idchor_edit.text().upper()
            nazwa_leku = self.l_klc_gM_idlek_edit.text().upper()
            stan = self.l_klc_gM_stan_txt_edit.toPlainText()

            # insert

            insert_KARTA = """INSERT INTO karta_lecz_chor VALUES (DEFAULT, :pesel, (SELECT id_choroby from choroba WHERE nazwa in :nazwa_c), :d_zdiag, (SELECT id_leku from leki WHERE nazwa in :nazwa_l), :data_wpisu, :stan)"""
            cursor.prepare(insert_KARTA)

            cursor.execute(None,
                           pesel=pesel,
                           nazwa_c=nazwa_leku,
                           d_zdiag=datetime.date.today(),
                           nazwa_l=nazwa_chor,
                           data_wpisu=datetime.date.today(),
                           stan=stan
                           )

            print("dodaje karte")
        if self.tabWidget_3.currentIndex() == 1:
            imie_l = self.l_appoin_gM_imielek_edit.text().upper()
            nazwisko_l = self.l_appoin_gM_nazwlek_edit.text().upper()
            pesel = self.l_appoin_gM_pesel_edit.text()
            data_wizyt_r = self.l_appoin_gM_dateofappoin_dedit.date().year()
            data_wizyt_m = self.l_appoin_gM_dateofappoin_dedit.date().month()
            data_wizyt_d = self.l_appoin_gM_dateofappoin_dedit.date().day()

            insert_pracownik = """INSERT INTO wizyta VALUES (DEFAULT, :data_wizyty, (SELECT id_prac FROM pracownik WHERE imie in :imie_l and nazwisko in :nazwisko_l),  :pesel)"""
            cursor.prepare(insert_pracownik)
            cursor.execute(None,
                           data_wizyty=datetime.date(data_wizyt_r, data_wizyt_m, data_wizyt_d),
                           imie_l=imie_l,
                           nazwisko_l=nazwisko_l,
                           pesel=pesel
                           )

            print("dodaje wizyte")
        if self.tabWidget_3.currentIndex() == 2:  # operacja
            nazwa_oper = self.l_oper_gM_nazwa_edit.text().upper()
            pesel_p = self.l_oper_gM_pesel_edit.text()
            imie_lek = self.l_oper_gM_imielek_edit.text().upper()
            nazwisko_lek = self.l_oper_gM_nazwilek_edit.text().upper()
            nazwa_chor = self.l_oper_gM_idchor_edit.text().upper()
            id_sali = self.l_oper_gM_idsali_edit.text()
            data_oper = self.l_oper_gM_date_dedit.date().toString("yyyy-MM-dd")
            czas = self.l_oper_gM_time_spinbox.value()

            # id choroby = nazwa?
            # insert

            insert_pracownik = """INSERT INTO operacja VALUES (DEFAULT, :data_op, :nazwa_op, :dl_trwania, :pesel, (SELECT id_choroby FROM choroba WHERE nazwa in :nazwa_c), (SELECT id_prac FROM pracownik WHERE imie in :imie_l and nazwisko in :nazwisko_l), :id_sali )"""
            cursor.prepare(insert_pracownik)

            cursor.execute(None,
                           data_op=datetime.datetime.now(),
                           nazwa_op=nazwa_oper,
                           dl_trwania=czas,
                           pesel=pesel_p,
                           nazwa_c=nazwa_chor,
                           imie_l=imie_lek,
                           nazwisko_l=nazwisko_lek,
                           id_sali=id_sali
                           )

            print("dodaje operacje")
        if self.tabWidget_3.currentIndex() == 5:
            imie = self.p_pac_gM_imie_edit_3.text().upper()
            nazwisko = self.p_pac_gM_nazw_edit_3.text().upper()
            pesel = self.p_pac_gM_pesel_edit_3.text()
            data_uro_r = self.p_pac_gM_date_dedit.date().year()
            data_uro_m = self.p_pac_gM_date_dedit.date().month()
            data_uro_d = self.p_pac_gM_date_dedit.date().day()
            # sprawdz czy nie ma o tym samym peselu

            insert_pacjent = """INSERT INTO pacjent VALUES (:pesel, :imie, :nazwisko, :data_ur)"""
            cursor.prepare(insert_pacjent)

            cursor.execute(None,
                           pesel=pesel,
                           imie=imie,
                           nazwisko=nazwisko,
                           data_ur=datetime.date(data_uro_r, data_uro_m, data_uro_d)
                           )

            print("dodaje pacjent")

    def del_as_lekarz(self):
        if self.tabWidget_3.currentIndex() == 0:
            nr_karty = self.l_klc_gU_nrkart_edit.text()
            # sprawdz czy istnieje
            # delete

            delete_karta = 'DELETE FROM karta_lecz_chor WHERE nr_karty in :karta'
            cursor.execute(delete_karta, [nr_karty])
            cursor.execute("COMMIT")
            print("usun karte")
        if self.tabWidget_3.currentIndex() == 1:
            id_wizyty = self.l_appoin_gU_idlek_edit.text()
            # jak jedno puste błąd
            # sprawdz czy istnieje
            # delete

            delete_wizyta = 'DELETE FROM wizyta where id_wizyty in :id_w'
            cursor.execute(delete_wizyta, [id_wizyty])
            cursor.execute("COMMIT")
            print("usun wizyte")
        if self.tabWidget_3.currentIndex() == 2:
            id_operacji = self.l_oper_gU_idoper_edit.text()
            # sprawdz czy istnieje
            # delete

            delete_operacja = 'DELETE FROM operacja where id_operacji in :id_op'
            cursor.execute(delete_operacja, [id_operacji])
            cursor.execute("COMMIT")
            print("usun operacje")

    def load_data_lekarz(self):
        if self.tabWidget_3.currentIndex() == 0:
            # select jezeli jest
            found = False
            pesel, nazwa_c, nazwa_l, stan = "", "", "", ""
            nr_karty = self.l_klc_gMod_nrkart_edit.text()

            cursor.execute(
                "SELECT nr_karty, k.pesel, c.nazwa, stan, l.nazwa FROM choroba c join karta_lecz_chor k on c.id_choroby = k.id_choroby join leki l on k.id_leku = l.id_leku")
            for item in cursor:
                if str(item[0]) == nr_karty:
                    item = tuple(map(str, item))
                    pesel, nazwa_c, stan, nazwa_l = item[1], item[2], item[3], item[4]
                    found = True
                    break
            if not found:
                print("nie ma takiej karty")
                # error messagebox
            else:
                self.l_klc_gM_pesel_edit.setText(pesel)
                self.l_klc_gM_idchor_edit.setText(nazwa_c)
                self.l_klc_gM_idlek_edit.setText(nazwa_l)
                self.l_klc_gM_stan_txt_edit.setPlainText(stan)
                print("ładuj karte")
        if self.tabWidget_3.currentIndex() == 4:
            found = False
            nazwa_c, uleczal = "", ""
            id_choroby = self.l_chor_gMod_idchor_edit.text()

            cursor.execute("SELECT id_choroby, nazwa, uleczalnosc FROM choroba")
            for item in cursor:
                if str(item[0]) == id_choroby:
                    item = tuple(map(str, item))
                    nazwa_c, uleczal = item[1], item[2]
                    found = True
                    break
            if not found:
                print("nie ma takiego pracownika")
                # error messagebox
            else:
                self.l_chor_gM_nazwa_edit.setText(nazwa_c)
                self.l_chor_gM_ulecz_combo.setCurrentIndex(self.l_chor_gM_ulecz_combo.findText(uleczal))
                print("ładuj choroba")

    def modify_as_lekarz(self):
        if self.tabWidget_3.currentIndex() == 0:
            nr_karty = self.l_klc_gMod_nrkart_edit.text()

            pesel = self.l_klc_gM_pesel_edit.text()
            id_choroby = self.l_klc_gM_idchor_edit.text()
            id_leku = self.l_klc_gM_idlek_edit.text()
            stan = self.l_klc_gM_stan_txt_edit.toPlainText()
            # update

            update_karta = 'UPDATE karta_lecz_chor SET stan = :stann where nr_karty in :karta'
            cursor.execute(update_karta, [stan, nr_karty])
            cursor.execute("COMMIT")
            print("edytuj karte")
        if self.tabWidget_3.currentIndex() == 4:
            id_choroby = self.l_chor_gMod_idchor_edit.text()

            uleczal = self.l_chor_gM_ulecz_combo.currentText()

            update_choroba = ('UPDATE choroba SET uleczalnosc = :ulecz WHERE id_choroby = :id')
            cursor.execute(update_choroba, [uleczal, id_choroby])
            cursor.execute("COMMIT")
            print("edytuj choroba")

    def search_as_lekarz(self):
        if self.tabWidget_3.currentIndex() == 0:
            pesel = self.l_klc_gM_pesel_edit.text()
            id_choroby = self.l_klc_gM_idchor_edit.text()
            id_leku = self.l_klc_gM_idlek_edit.text()
            # select
            print("szukam karte")
        if self.tabWidget_3.currentIndex() == 1:
            id_lekarz = self.l_appoin_gM_idlek_edit.text()
            pesel = self.l_appoin_gM_pesel_edit.text()
            data_wizyt = self.l_appoin_gM_dateofappoin_dedit.date().toString("yyyy-MM-dd")
            # select
            print("szukam wizyte")
        if self.tabWidget_3.currentIndex() == 2:
            nazwa_oper = self.l_oper_gM_nazwa_edit.text()
            pesel_p = self.l_oper_gM_pesel_edit.text()
            id_lekarz = self.l_oper_gM_idlek_edit.text()
            id_choroby = self.l_oper_gM_idchor_edit.text()
            id_sali = self.l_oper_gM_idsali_edit.text()
            data_oper = self.l_oper_gM_date_dedit.date().toString("yyyy-MM-dd")
            czas = self.l_oper_gM_time_spinbox.value()

            # select
            print("szukam operacje")
        if self.tabWidget_3.currentIndex() == 3:
            nazwa_lek = self.l_leki_gM_nazwa_edit.text()
            na_rec = self.l_leki_gM_rec_combo.currentText()
            # select
            print("szukam leki")
        if self.tabWidget_3.currentIndex() == 4:
            nazwa_chor = self.l_chor_gM_nazwa_edit.text()
            ulecz = self.l_chor_gM_ulecz_combo.currentText()
            # select
            print("szukam choroba")
        if self.tabWidget_3.currentIndex() == 5:
            imie = self.p_pac_gM_imie_edit_3.text()
            nazwisko = self.p_pac_gM_nazw_edit_3.text()
            pesel = self.p_pac_gM_pesel_edit_3.text()
            data = self.p_pac_gM_date_dedit_3.date().toString("yyyy-MM-dd")
            # select po tym co nie jest null
            print("szukam pacjent")

    def show_all(self, name):
        self.window = SelectWidget()
        self.window.wynik_label.setText(name)
        if self.stackedWidget.currentIndex() == 1:
            if self.tabWidget.currentIndex() == 0:
                self.window.tabela.setColumnCount(4)
                self.window.tabela.setRowCount(50)
                self.window.tabela.setHorizontalHeaderLabels(["Imie", "Nazwisko", "Zatrudniony", "Nr sali"])

                cursor.execute(
                    "SELECT imie, nazwisko, zatrudniony, id_sali FROM pielegniarka join pracownik on pracownik.id_prac = pielegniarka.id_prac")

                tablerow = 0
                for item in cursor:
                    item = tuple(map(str, item))
                    for i in range(4):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1

            if self.tabWidget.currentIndex() == 1:
                self.window.tabela.setColumnCount(5)
                self.window.tabela.setRowCount(50)
                self.window.tabela.setHorizontalHeaderLabels(
                    ["Imie", "Nazwisko", "Zatrudniony", "Nr sali", "Specjalizacja"])

                cursor.execute(
                    "SELECT imie, nazwisko, zatrudniony, id_sali as nr_sali, specjalizacja  FROM pracownik join lekarz on pracownik.id_prac = lekarz.id_prac")

                tablerow = 0
                for item in cursor:
                    item = tuple(map(str, item))
                    for i in range(5):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1

            if self.tabWidget.currentIndex() == 2:
                self.window.tabela.setColumnCount(3)
                self.window.tabela.setRowCount(50)
                self.window.tabela.setHorizontalHeaderLabels(["Nr sali", "Typ sali", "Liczba lozek"])

                cursor.execute(
                    "SELECT s.*, nvl((select count(id_sali) from lozko group by lozko.id_sali having id_sali = s.id_sali  ),0) as liczba_lozek FROM sala s")

                tablerow = 0
                for item in cursor:
                    item = tuple(map(str, item))
                    for i in range(3):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1

        if self.stackedWidget.currentIndex() == 2:
            if self.tabWidget_2.currentIndex() == 0:
                self.window.tabela.setColumnCount(4)
                self.window.tabela.setRowCount(50)
                self.window.tabela.setHorizontalHeaderLabels(["PESEL", "Imie", "Nazwisko", "Data urodzenia"])

                cursor.execute(
                    "SELECT p.* FROM pacjent p")

                tablerow = 0
                for item in cursor:
                    item = tuple(map(str, item))
                    for i in range(4):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1
            if self.tabWidget_2.currentIndex() == 1:
                self.window.tabela.setColumnCount(6)
                self.window.tabela.setRowCount(50)
                self.window.tabela.setHorizontalHeaderLabels(
                    ["Imie", "Nazwisko", "Imie odwiedzajacego", "Nazwisko odwiedzajacego", "Stopien pokrewienstwa",
                     "Data odwiedzin"])

                cursor.execute(
                    "SELECT imie, nazwisko, imie_odw, nazwisko_odw, st_pokrewienstwa, data_odw FROM odwiedziny o join pacjent p on p.pesel = o.pesel")

                tablerow = 0
                for item in cursor:
                    item = tuple(map(str, item))
                    for i in range(6):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1
            if self.tabWidget_2.currentIndex() == 2:

                self.window.tabela.setColumnCount(6)
                self.window.tabela.setRowCount(50)
                self.window.tabela.setHorizontalHeaderLabels(
                    ["Pacjent", "Id lozka", "Id sali", "PESEL", "Usytuowanie", "Respirator"])

                cursor.execute(
                    "SELECT  imie ||' '|| nazwisko as pacjent, l.* FROM lozko l right join pacjent p on l.pesel = p.pesel")

                tablerow = 0
                for item in cursor:
                    item = tuple(map(str, item))
                    for i in range(6):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1
            if self.tabWidget_2.currentIndex() == 3:

                self.window.tabela.setColumnCount(4)
                self.window.tabela.setRowCount(50)
                self.window.tabela.setHorizontalHeaderLabels(["Id prac", "Imie", "Nazwisko", "Id sali"])

                cursor.execute(
                    "SELECT pielegniarka.id_prac, imie, nazwisko, id_sali FROM pielegniarka join pracownik on pracownik.id_prac = pielegniarka.id_prac")

                tablerow = 0
                for item in cursor:
                    item = tuple(map(str, item))
                    for i in range(4):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1
            if self.tabWidget_2.currentIndex() == 4:

                self.window.tabela.setColumnCount(3)
                self.window.tabela.setRowCount(50)
                self.window.tabela.setHorizontalHeaderLabels(["Nr sali", "Typ sali", "Liczba lozek"])

                cursor.execute(
                    "SELECT s.*, nvl((select count(id_sali) from lozko group by lozko.id_sali having id_sali = s.id_sali  ),0) as liczba_lozek FROM sala s")

                tablerow = 0
                for item in cursor:
                    item = tuple(map(str, item))
                    for i in range(3):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1
        if self.stackedWidget.currentIndex() == 3:
            if self.tabWidget_3.currentIndex() == 0:
                self.window.tabela.setColumnCount(7)
                self.window.tabela.setRowCount(50)
                self.window.tabela.setHorizontalHeaderLabels(
                    ["Nr karty", "Choroba", "Uleczalnosc", "Stan", "Data wpisu", "Lek", "Data zdiag"])

                cursor.execute(
                    "SELECT nr_karty, c.nazwa as choroba, uleczalnosc, stan, data_wpisu, l.nazwa as lek,  d_zdiag FROM choroba c join karta_lecz_chor k on c.id_choroby = k.id_choroby join leki l on k.id_leku = l.id_leku")

                tablerow = 0
                for item in cursor:
                    item = tuple(map(str, item))
                    for i in range(7):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1
            if self.tabWidget_3.currentIndex() == 1:

                self.window.tabela.setColumnCount(5)
                self.window.tabela.setRowCount(50)
                self.window.tabela.setHorizontalHeaderLabels(["Id wizyty", "Pacjent", "PESEL", "Lekarz", "Data wizyty"])

                cursor.execute(
                    "SELECT id_wizyty, p.imie ||' '|| p.nazwisko as pacjent, w.pesel, l.imie ||' '|| l.nazwisko as lekarz,data_wizyty FROM (pracownik l join wizyta w on l.id_prac = w.id_prac) join pacjent p on w.pesel = p.pesel")

                tablerow = 0
                for item in cursor:
                    item = tuple(map(str, item))
                    for i in range(5):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1
            if self.tabWidget_3.currentIndex() == 2:
                self.window.tabela.setColumnCount(6)
                self.window.tabela.setRowCount(50)
                self.window.tabela.setHorizontalHeaderLabels(
                    ["Id operacji", "Choroba", "Nazwa operacja", "Data operacji", "Lekarz", "Czas trwania operacji"])

                cursor.execute(
                    "SELECT id_operacji, nazwa, nazwa_operacji, data_operacji, imie || ' ' || nazwisko as lekarz, długość_trwania || ' minut' as czas_trwania_operacji FROM choroba c join operacja o on c.id_choroby = o.id_choroby join pracownik p on o.id_prac = p.id_prac")

                tablerow = 0
                for item in cursor:
                    item = tuple(map(str, item))
                    for i in range(6):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1
            if self.tabWidget_3.currentIndex() == 3:
                self.window.tabela.setColumnCount(3)
                self.window.tabela.setRowCount(50)
                self.window.tabela.setHorizontalHeaderLabels(["Id leku", "Nazwa leku", "Czy na recepte"])

                cursor.execute(
                    "SELECT * FROM leki")

                tablerow = 0
                for item in cursor:
                    item = tuple(map(str, item))
                    for i in range(3):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1
            if self.tabWidget_3.currentIndex() == 4:

                self.window.tabela.setColumnCount(3)
                self.window.tabela.setRowCount(50)
                self.window.tabela.setHorizontalHeaderLabels(["Id choroby", "Nazwa choroby", "Uleczalność"])

                cursor.execute(
                    "SELECT * FROM choroba")

                tablerow = 0
                for item in cursor:
                    item = tuple(map(str, item))
                    for i in range(3):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1
            if self.tabWidget_3.currentIndex() == 5:
                self.window.tabela.setColumnCount(4)
                self.window.tabela.setRowCount(50)
                self.window.tabela.setHorizontalHeaderLabels(["PESEL", "Imie", "Nazwisko", "Data urodzenia"])

                cursor.execute(
                    "SELECT p.* FROM pacjent p")

                tablerow = 0
                for item in cursor:
                    item = tuple(map(str, item))
                    for i in range(4):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1
            if self.tabWidget_3.currentIndex() == 6:
                self.window.tabela.setColumnCount(3)
                self.window.tabela.setRowCount(50)
                self.window.tabela.setHorizontalHeaderLabels(["Nr sali", "Typ sali", "Liczba łóżek"])

                cursor.execute(
                    "SELECT s.*, nvl((select count(id_sali) from lozko group by lozko.id_sali having id_sali = s.id_sali  ),0) as liczba_lozek FROM sala s")

                tablerow = 0
                for item in cursor:
                    item = tuple(map(str, item))
                    for i in range(3):
                        self.window.tabela.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                    tablerow += 1
        self.window.show()

    def show_karta(self):
        self.wine = CardWidget()
        if self.stackedWidget.currentIndex() == 3 or self.stackedWidget.currentIndex() == 2:
            pesel = ""
            if self.stackedWidget.currentIndex() == 3:
                pesel = self.l_klc_gKLC_pesel_edit.text()

            if self.stackedWidget.currentIndex() == 2:
                pesel = self.p_pac_gKLC_pesel_edit.text()

            self.window.tabela_pacjent.setColumnCount(4)
            self.window.tabela_pacjent.setRowCount(2)
            self.window.tabela_pacjent.setHorizontalHeaderLabels(["PESEL", "Imie", "Nazwisko", "Data urodzenia"])

            select_cos = ("SELECT * FROM pacjent WHERE pesel in :pesel")
            cursor.execute(select_cos, ["", pesel])
            tablerow = 0
            for item in cursor:
                item = tuple(map(str, item))
                for i in range(4):
                    self.window.tabela_pacjent.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                tablerow += 1

            self.window.tabela_karta.setColumnCount(8)
            self.window.tabela_karta.setRowCount(20)
            self.window.tabela_karta.setHorizontalHeaderLabels(["Nr karty", "PESEL", "Choroba", "Uleczalność", "Stan", "data_wpisu", "lek", "Data_zdiag"])

            select_cos = ("SELECT nr_karty, pesel, c.nazwa, uleczalnosc, stan, data_wpisu, l.nazwa,  d_zdiag FROM choroba c join karta_lecz_chor k on c.id_choroby = k.id_choroby join leki l on k.id_leku = l.id_leku where pesel in :pes")
            cursor.execute(select_cos, ["", pesel])
            tablerow = 0
            for item in cursor:
                item = tuple(map(str, item))
                for i in range(8):
                    self.window.tabela_pacjent.setItem(tablerow, i, QtWidgets.QTableWidgetItem(item[i]))
                tablerow += 1
        self.wine.show()
        print("gówno")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = SQLappWindow()
    win.show()

    sys.exit(app.exec_())
