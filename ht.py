# CT60A0201 Ohjelmoinnin perusteet 2016 ohjelmien otsikkotiedot.
# Tekijä: Annika Vieraankivi
# Opiskelijanumero: 0506688
# Päivämäärä: 19.12.2016
# Yhteistyö ja 1lähteet, nimi ja yhteistyön muoto: -
# HUOM! KAIKKI KURSSIN TEHTÄVÄT OVAT HENKILÖKOHTAISIA!
######################################################################
import svgwrite

class saa: #Määritellään luokka
    pvm = ""
    sade = ""
    ka = ""
    minimi = ""
    maksimi = ""

def valikko(): #Tulostetaan valikko
    print("Säätietojen käsittely")
    print("*******************************************************")
    print("1) Lataa kaupungin säätiedot tiedostosta")
    print("2) Laske keskiarvo kuukauden lämpötiloista")
    print("3) Laske kuukauden lämpötilojen minimi ja maksimi")
    print("4) Tallenna kuukauden tiedot tiedostoon")
    print("5) Piirrä graafi kuukauden lämpötiloista kaupungissa")
    print("6) Lataa toiset säätiedot ja piirrä vertailugraafi")
    print("0) Lopeta")
    valinta = int(input("Valintasi: "))
    return valinta

def tallenna(kaupunki,ka,minimi,maksimi): #Tallennetaan tiedostoon
    nimi = input("Anna tiedostonimi: ")
    tiedosto2 = open(nimi, "w", encoding="utf-8")
    tiedosto2.write("Kuukauden säätilasto kaupungissa " + kaupunki + "\n")
    tiedosto2.write("*******************************************************" + "\n")
    tiedosto2.write("Kuukauden lämpötilan keskiarvo: " + str(ka) + " celsiusastetta. \n")
    tiedosto2.write("Kuukauden lämpötilan minimi: " + str(minimi) + " celsiusastetta. \n")
    tiedosto2.write("Kuukauden lämpötilan maksimi: " + str(maksimi) + " celsiusastetta. \n")
    tiedosto2.write("*******************************************************")
    tiedosto2.close()
    print("Tallennus onnistui.")

def lataa_tiedostosta():
    try: 
        lista = []
        nimi = input("Anna tiedostonimi: ")
        if nimi == "lappeenranta.csv":
            tiedosto = open("lappeenranta.csv", "r", encoding="utf-8")
        elif nimi == "kouvola.csv":
            tiedosto = open("kouvola.csv", "r", encoding="utf-8")
        while True:
            rivi = tiedosto.readline()
            if rivi == "":
                break
            s = saa()
            rivi = rivi.split(";")
            s.pvm = rivi[0]
            s.sade = rivi[1]
            s.ka = rivi[2]
            s.minimi = rivi[3]
            s.maksimi = rivi[4]
            lista.append(s)     #Tallennetaan säätiedot listaan
        lista.remove(lista[0]) #Poistetaan otsikkotiedot listasta
        tiedosto.close()
        kaupunki = nimi.strip(".csv") 
        kaupunki = kaupunki.capitalize()
        print("Tiedoston luku onnistui.")
        return lista,kaupunki
    except FileNotFoundError: #Virheen varalta
        print("Tiedostoa ei löydy.")

def keskiarvon_laskeminen(lista):
    asteet = 0
    päivät = 0
    s = saa()
    for s in lista:
        asteet = asteet + float(s.ka)
        päivät = päivät + 1
    ka = round(asteet/päivät,1)
    print("Kuukauden lämpötilan keskiarvo: ",ka)
    return ka

def minimi_maksimi(lista):
    pienimmät = []
    suurimmat = []
    s = saa()
    for s in lista:
        pienimmät.append(float(s.minimi))
    for s in lista:
        suurimmat.append(float(s.maksimi))
    minimi = min(pienimmät)
    maksimi = max(suurimmat)
    print("Kuukauden lämpötilan minimi: ", minimi)
    print("Kuukauden lämpötilan maksimi: ", maksimi)
    return minimi,maksimi

def vertailugraafi(lista):
    lämpötilat2 = []
    lista2 = []
    lämpötilat = []
    s = saa()
    nimi2 = input("Anna vertailtavat säätiedot sisältävän tiedoston nimi: ")
    tiedosto2 = open(nimi2, "r", encoding="utf-8")
    while True: #Ladataan vertailtavan kaupungin tiedot
            rivi = tiedosto2.readline()
            if rivi == "":
                break
            s = saa()
            rivi = rivi.split(";")
            s.pvm = rivi[0]
            s.sade = rivi[1]
            s.ka = rivi[2]
            s.minimi = rivi[3]
            s.maksimi = rivi[4]
            lista2.append(s)
    lista2.remove(lista2[0])
    tiedosto2.close()
    nimi = input("Anna svg-tiedoston nimi: ")
    kuva = svgwrite.Drawing(nimi,size=('600px','600px'))
    kuva.add(kuva.rect((0,0),(600,600),fill='white'))
    for i in range(1,6): #Luodaan diagrammin pohja
        y = i*100
        kuva.add(kuva.line((0,y),(600,y),stroke='black'))
        teksti = (-y/10)+30
        kuva.add(kuva.text(teksti,(0,y-3),fill='green'))
    kuvapisteet2 = open("kuvapisteet.csv","w")
    for s in lista:
        lämpötilat.append(float(s.ka))
    for i in range(0,len(lämpötilat)-1): #Alkuperäisen kaupungin käyrä
        x1 = i*20
        arvo = float(lämpötilat[i])
        y1 = (30-arvo)*10
        kuvapisteet2.write(str(int(y1)) + ",")
        x2 = (i+1)*20
        a = i+1
        arvo2 = float(lämpötilat[a])
        y2 = (30-arvo2)*10
        kuva.add(kuva.line((x1,y1),(x2,y2),stroke='red'))
    kuvapisteet2.write(str(int(y2)))
    kuvapisteet2.write("\n")

    for s in lista2:
        lämpötilat2.append(float(s.ka))
    for i in range(0,len(lämpötilat2)-1): #Vertailtavan kaupungin käyrä
        x1 = i*20
        arvo = float(lämpötilat2[i])
        y1 = (30-arvo)*10
        kuvapisteet2.write(str(int(y1)) + ",") #Lisätään kuvapisteet tiedostoon
        x2 = (i+1)*20
        a = i+1
        arvo2 = float(lämpötilat2[a])
        y2 = (30-arvo2)*10
        kuva.add(kuva.line((x1,y1),(x2,y2),stroke='blue'))
    kuvapisteet2.write(str(int(y2))) #Lisätään viimeinen kuvapiste tiedostoon
    kuvapisteet2.close()
    kuva.save()
    print("Svg- ja csv- tiedostojen kirjoitus onnistui.")
  
def graafi(lista):
    lämpötilat = [] #Määritetään lista, johon tallennetaan keskilämpötilat
    nimi = input("Anna svg-tiedoston nimi: ")
    s = saa()
    for s in lista:
        lämpötilat.append(float(s.ka))
    kuva = svgwrite.Drawing(nimi,size=('600px','600px')) 
    kuva.add(kuva.rect((0,0),(600,600),fill='white'))
    for i in range(1,6): #Tehdään diagrammille pohja
        y = i*100
        kuva.add(kuva.line((0,y),(600,y),stroke='black'))
        teksti = (-y/10)+30
        kuva.add(kuva.text(teksti,(0,y-3),fill='green'))
    kuvapisteet = open("kuvapisteet.csv","w")
    for i in range(0,len(lämpötilat)-1): #Tehdään lämpötilakäyrä
        x1 = i*20
        arvo = float(lämpötilat[i])
        y1 = (30-arvo)*10
        kuvapisteet.write(str(int(y1)) + ",") #Tallennetaan kuvapisteet tiedostoon
        x2 = (i+1)*20
        a = i+1
        arvo2 = float(lämpötilat[a])
        y2 = (30-arvo2)*10
        kuva.add(kuva.line((x1,y1),(x2,y2),stroke='red'))
    kuvapisteet.write(str(int(y2)))
    kuva.save()
    kuvapisteet.close()
    print("Svg- ja csv- tiedostojen kirjoitus onnistui.")
    
    
def paaohjelma():
    while True:
        valinta = valikko()
        if valinta == 1:
            lista,kaupunki = lataa_tiedostosta()
        elif valinta == 2:
            ka = keskiarvon_laskeminen(lista)
        elif valinta == 3:
            minimi,maksimi = minimi_maksimi(lista)
        elif valinta == 4:
            tallenna(kaupunki,ka,minimi,maksimi)
        elif valinta == 5:
            graafi(lista)
        elif valinta == 6:
            vertailugraafi(lista)
        elif valinta == 0:
            print("Kiitos ohjelman käytöstä!")
            break
paaohjelma()
    
######################################################################
# eof
