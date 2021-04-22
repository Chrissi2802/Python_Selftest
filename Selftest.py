#Überprüft alle Pythondateien in diesem Ordner

import os
import platform

#Betriebssystem herausfinden
if (platform.system().find("Windows") < 0):
    pythonbefehlsname = "python3"   #Linux oder Mac
else:
    pythonbefehlsname = "python"    #Windows

rueckgabewertio = 0
rueckgabewertnio = 1


def Dateiliste_erstellen(datei_ueberspringen):
    """Dateiliste erstellen, von allen Python-Dateien in diesem Ordner"""

    dateiliste = [datei for datei in os.listdir() if datei.endswith(".py")]
    
    #Falls Dateien übersprungen werden sollen, werden diese aus der Liste gelöscht
    n = 0
    while (n < len(dateiliste)):
        datei_loeschen = False
        for m in range(len(datei_ueberspringen)):
            if (datei_ueberspringen[m].find(dateiliste[n]) >= 0):
                datei_loeschen = True
        if (datei_loeschen == True):
            del(dateiliste[n])
        else:
            n += 1

    return dateiliste


def Dateiliste_durchlaufen(Funktion, datei_ueberspringen = []):
    """Durch die Dateiliste laufen und die übergebene Funktion ausführen"""

    dateiliste = Dateiliste_erstellen(datei_ueberspringen)
    for dateiname in dateiliste:
        zielname = Funktion.__name__ + " prüft " + dateiname
        print(zielname)
        rueckgabewert = Funktion(dateiname)
        assert (rueckgabewert == rueckgabewertio), "Fehler in: " + dateiname


def Codeprüfung_Asserts_vorhanden(datei):
    """Prüft ob in jeder Datei ein Testcode und assert vorhanden ist"""

    aktuelledatei = open(datei, "r")    #Datei zum lesen öffnen
    testcode = False
    rueckgabewert = rueckgabewertnio
    
    for zeile in aktuelledatei:
        if ("if" in zeile) and ("__name__" in zeile) and ("__main__" in zeile):
            testcode = True
        if (testcode == True):
            if ("assert" in zeile):
                rueckgabewert = rueckgabewertio
    aktuelledatei.close()
    
    if (rueckgabewert == rueckgabewertnio):
        if (testcode == False):
            print("Kein Testcode gefunden in", datei)
        else:
            print("Keine Asserts gefunden in", datei)

    return rueckgabewert


def Codeprüfung_Datei_irgendwo_importiert(datei):
    """Prüft ob alle Dateien irgendwo (in einer anderen Datei) importiert wurden"""
    
    dateibezeichnung, dateiendung = os.path.splitext(datei)
    dateiliste = Dateiliste_erstellen([])
    rueckgabewert = rueckgabewertnio

    for dateiname in dateiliste:
        aktuelledatei = open(dateiname, "r")    #Datei zum lesen öffnen
        for zeile in aktuelledatei:
            if ("import" in zeile) and (dateibezeichnung in zeile):
                rueckgabewert = rueckgabewertio
        aktuelledatei.close()

    if (rueckgabewert == rueckgabewertnio):
        print(datei, "wurde nirgendwo importiert")

    return rueckgabewert


def Codeprüfung_Main_Block(datei):
    """Führt von der aufgerufenen Datei, den kompletten Code aus. 
    Alles was in dieser Datei steht.
    Falls es eine main.py gibt, muss diese ausgeschlossen werden."""
    return os.system(pythonbefehlsname + " " + datei)


def Codeprüfung_Pyflakes(datei):
    """Pyflakes findet nicht verwendete Importe und nicht verwendete lokale Variablen (zusätzlich zu vielen anderen Programmfehlern)"""
    return os.system("pyflakes " + datei)


def Codeprüfung_Vulture(datei):
    """Vulture findet nicht benutzen Code"""
    return os.system("vulture " + datei + " --min-confidence 70")


def Selftest():
    """Das alles wird ausgeführt beim Selftest"""
    #main und aktuelle Datei überspringen
    ueberspringenmitaktuellerdatei = ["main.py", str(__file__)]

    ueberspringen = []
    
    Dateiliste_durchlaufen(Codeprüfung_Asserts_vorhanden, ueberspringenmitaktuellerdatei)
    Dateiliste_durchlaufen(Codeprüfung_Datei_irgendwo_importiert, ueberspringenmitaktuellerdatei)
    Dateiliste_durchlaufen(Codeprüfung_Main_Block, ueberspringenmitaktuellerdatei)
    Dateiliste_durchlaufen(Codeprüfung_Pyflakes, ueberspringen)
    Dateiliste_durchlaufen(Codeprüfung_Vulture, ueberspringen)


if (__name__ == "__main__"):
    Selftest()
    print("--------------------------------------------------")
    print("Alle Tests erfolgreich ausgeführt!")
    print("--------------------------------------------------")
