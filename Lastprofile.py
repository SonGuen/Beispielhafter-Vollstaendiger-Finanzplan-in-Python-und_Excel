from Import_Libraries import *


'''
´Die folgenden Befehle erstellen den Standardlastprofil für
eine Bäckerei mit einer Mitarbeiterzahl von 8 Personen aus
auf Basis der Trajektorie aus BDEW
die Kommentare zur Nachvollziehbarkeit des Codes sind mit -###- hinterlegt

'''


df_Verlauf = pd.read_excel(
    "Standardlastprofil.xlsx",
    sheet_name="Tabelle2")
df_Wichtig = pd.read_excel(
    "Standardlastprofil.xlsx",
    sheet_name=2)
### Laden der Standardlastprofile

Stromverbrauch_Baeckerei_Erwerbstätiger = np.array([7429, 6958, 6489, 6132, 5775, 5998, 6222, 6222]).mean()
###mittlerer Stromverbrauch
Zahl_der_Erwerbstätigen = 8.1

Stromprofil_Jahr_kWh = Zahl_der_Erwerbstätigen * Stromverbrauch_Baeckerei_Erwerbstätiger
###gesamter mittlerer Stromverbrauch

df_Verlauf = df_Verlauf[:-1]
###Entnahme der letzten reihe aus der Tabelle der Excel Datei aus dem zweiten Reiter



###Definiere die Jahreszeiten mit Sonntag, Samstag, Werktag und der Zeit

Sommerzeit = {"Werktag": df_Verlauf["Werktag_Sommer"],
              "Samstag": df_Verlauf["Samstag_Sommer"],
              "Sonntag": df_Verlauf["Sonntag_Sommer"],
              "Time": df_Verlauf["[W]"]}

Winterzeit = {"Werktag": df_Verlauf["Werktag_Winter"],
              "Samstag": df_Verlauf["Samstag_Winter"],
              "Sonntag": df_Verlauf["Sonntag_Winter"],
              "Time": df_Verlauf["[W]"]}

Übergangszeit = {"Werktag": df_Verlauf["Werktag_Übergangszeit"],
                 "Samstag": df_Verlauf["Samstag_Übergangszeit"],
                 "Sonntag": df_Verlauf["Sonntag_Übergangszeit"],
                 "Time": df_Verlauf["[W]"]}


###Definiere die Zeiträume der Jahrenszeiten

##Winterzeit 01.11.2021-20.03.2022

start = datetime(2021, 10, 31)
end = datetime(2022, 3, 20)

dates = [end - delta(days=x) for x in range(0, (end - start).days)]
Winterdaten = pd.Series(dates)  # wenn du index haben willst index=dates

##Sommerzeit 15.05.2022-14.09.2022


start = datetime(2022, 5, 14)
end = datetime(2022, 9, 14)

dates = [end - delta(days=x) for x in range(0, (end - start).days)]
Sommerdaten = pd.Series(dates)  # wenn du index haben willst index=dates

##Frühling 21.03.2022-14.05.2022


start = datetime(2022, 3, 20)
end = datetime(2022, 5, 14)

dates = [end - delta(days=x) for x in range(0, (end - start).days)]
Fruehlingsdaten = pd.Series(dates)  # wenn du index haben willst index=dates

##Herbst 15.09.2022-31.10.2022


start = datetime(2022, 9, 14)
end = datetime(2022, 10, 31)

dates = [end - delta(days=x) for x in range(0, (end - start).days)]
Herbstsdaten = pd.Series(dates)  # wenn du index haben willst index=dates


###Definiere die 15 minütige Taktung für die Jahreszeiten

day = 24
minutes = 24 * 60
minutes_15 = minutes / 15

Sommer = []
for Datum in (Sommerdaten):
    for i in range(int(minutes_15)):

        if i == 0:
            Sommer.append(Datum + delta(minutes=15))
        else:
            Sommer.append(Sommer[-1] + delta(minutes=15))

Fruehling = []
for Datum in (Fruehlingsdaten):
    for i in range(int(minutes_15)):

        if i == 0:
            Fruehling.append(Datum + delta(minutes=15))
        else:
            Fruehling.append(Fruehling[-1] + delta(minutes=15))

Herbst = []
for Datum in (Herbstsdaten):
    for i in range(int(minutes_15)):

        if i == 0:
            Herbst.append(Datum + delta(minutes=15))
        else:
            Herbst.append(Herbst[-1] + delta(minutes=15))

Winter = []
for Datum in (Winterdaten):
    for i in range(int(minutes_15)):

        if i == 0:
            Winter.append(Datum + delta(minutes=15))
        else:
            Winter.append(Winter[-1] + delta(minutes=15))


###Prüfung ob alles stimmig ist
print(np.shape(Winter)[0] + np.shape(Sommer)[0] + np.shape(Herbst)[0] + np.shape(Fruehling)[0])



###Definiere eine Tabelle und erstelle eine Spalte Zeit
Winter = pd.DataFrame(Winter)
Winterzeit = pd.DataFrame(Winterzeit)
Winter = Winter.rename(columns={0: "Zeit"})

Sommer = pd.DataFrame(Sommer)
Sommerzeit = pd.DataFrame(Sommerzeit)
Sommer = Sommer.rename(columns={0: "Zeit"})

Herbst = pd.DataFrame(Herbst)
Herbst = Herbst.rename(columns={0: "Zeit"})

Fruehling = pd.DataFrame(Fruehling)
Fruehling = Fruehling.rename(columns={0: "Zeit"})

Übergangszeit = pd.DataFrame(Übergangszeit)


###Sortiere die Daten aus dem Typ Zeit
Winter = Winter.sort_values(by=["Zeit"], ignore_index=True)
Sommer = Sommer.sort_values(by=["Zeit"], ignore_index=True)
Herbst = Herbst.sort_values(by=["Zeit"], ignore_index=True)
Fruehling = Fruehling.sort_values(by=["Zeit"], ignore_index=True)


### Weiße die Daten zu, wenn die Tage gleichen und die Jahreszeiten (Verheiraten der Daten 15 minütiger Taktung
### und Stromverbrauch 15 minütiger Taktung

Sommer["kWh"] = 0
timer = 0
for index, Zeiten in tqdm(enumerate((Sommer["Zeit"]))):

    if Zeiten.day_name() == "Saturday":
        Sommer.loc[index, "kWh"] = Sommerzeit.loc[timer, "Samstag"]

    if Zeiten.day_name() == "Sunday":
        Sommer.loc[index, "kWh"] = Sommerzeit.loc[timer, "Sonntag"]

    if Zeiten.day_name() != "Sunday" and Zeiten.day_name() != "Saturday":
        Sommer.loc[index, "kWh"] = Sommerzeit.loc[timer, "Werktag"]

    timer = timer + 1
    if timer == len(Sommerzeit["Time"]):
        timer = 0

Herbst["kWh"] = 0
timer = 0
for index, Zeiten in tqdm(enumerate((Herbst["Zeit"]))):

    if Zeiten.day_name() == "Saturday":
        Herbst.loc[index, "kWh"] = Übergangszeit.loc[timer, "Samstag"]

    if Zeiten.day_name() == "Sunday":
        Herbst.loc[index, "kWh"] = Übergangszeit.loc[timer, "Sonntag"]

    if Zeiten.day_name() != "Sunday" and Zeiten.day_name() != "Saturday":
        Herbst.loc[index, "kWh"] = Übergangszeit.loc[timer, "Werktag"]

    timer = timer + 1
    if timer == len(Übergangszeit["Time"]):
        timer = 0

Fruehling["kWh"] = 0
timer = 0
for index, Zeiten in tqdm(enumerate((Fruehling["Zeit"]))):

    if Zeiten.day_name() == "Saturday":
        Fruehling.loc[index, "kWh"] = Übergangszeit.loc[timer, "Samstag"]

    if Zeiten.day_name() == "Sunday":
        Fruehling.loc[index, "kWh"] = Übergangszeit.loc[timer, "Sonntag"]

    if Zeiten.day_name() != "Sunday" and Zeiten.day_name() != "Saturday":
        Fruehling.loc[index, "kWh"] = Übergangszeit.loc[timer, "Werktag"]

    timer = timer + 1
    if timer == len(Übergangszeit["Time"]):
        timer = 0

Winter["kWh"] = 0
timer = 0
for index, Zeiten in tqdm(enumerate((Winter["Zeit"]))):

    if Zeiten.day_name() == "Saturday":
        Winter.loc[index, "kWh"] = Winterzeit.loc[timer, "Samstag"]

    if Zeiten.day_name() == "Sunday":
        Winter.loc[index, "kWh"] = Winterzeit.loc[timer, "Sonntag"]

    if Zeiten.day_name() != "Sunday" and Zeiten.day_name() != "Saturday":
        Winter.loc[index, "kWh"] = Winterzeit.loc[timer, "Werktag"]

    timer = timer + 1
    if timer == len(Übergangszeit["Time"]):
        timer = 0



###Definiere die Feiertage

Neujahr = datetime(2022, 1, 1)  # nicht notwendig da in Urlaub fällt
Erscheinungsfest = datetime(2022, 1, 6)  # nicht notwendig da in Urlaub fällt
Karfreitag = datetime(2022, 4, 15)
Ostermontag = datetime(2022, 4, 18)
Tag_der_Arbiet = datetime(2022, 5, 1)
Himmelfahrt = datetime(2022, 5, 26)
Pfingsmontag = datetime(2022, 6, 6)
Fronleichnam = datetime(2022, 6, 16)
Tag_der_deutschen_Einheit = datetime(2022, 10, 3)
Allerheiligen = datetime(2022, 11, 1)
Erster_Weihnachten = datetime(2022, 12, 25)
Zweiter_Weihnachten = datetime(2022, 12, 26)

###Definiere die Urlaubszeiträume

Urlaub_bis = datetime(2022, 1, 16)
Urlaub_von = datetime(2022, 1, 1)

Urlaub_bis_2 = datetime(2022, 8, 11)
Urlaub_von_2 = datetime(2022, 8, 1)


###Ermittle aus den bestimmten Zeiträumen den Mittelwert siehe Kapitel 5.1
Mittel = []

Mittel.append(Übergangszeit[Übergangszeit["Time"] >= datetime.strptime('20:00', '%H:%M').time()]["Werktag"].mean())
Mittel.append(Übergangszeit[Übergangszeit["Time"] >= datetime.strptime('20:00', '%H:%M').time()]["Samstag"].mean())
Mittel.append(Übergangszeit[Übergangszeit["Time"] >= datetime.strptime('20:00', '%H:%M').time()]["Sonntag"].mean())

Mittel.append(Winterzeit[Winterzeit["Time"] >= datetime.strptime('20:00', '%H:%M').time()]["Werktag"].mean())
Mittel.append(Winterzeit[Winterzeit["Time"] >= datetime.strptime('20:00', '%H:%M').time()]["Samstag"].mean())
Mittel.append(Winterzeit[Winterzeit["Time"] >= datetime.strptime('20:00', '%H:%M').time()]["Sonntag"].mean())

Mittel.append(Sommerzeit[Sommerzeit["Time"] >= datetime.strptime('20:00', '%H:%M').time()]["Werktag"].mean())
Mittel.append(Sommerzeit[Sommerzeit["Time"] >= datetime.strptime('20:00', '%H:%M').time()]["Samstag"].mean())
Mittel.append(Sommerzeit[Sommerzeit["Time"] >= datetime.strptime('20:00', '%H:%M').time()]["Sonntag"].mean())

Mittelwert_zwischen_20_24 = np.mean(Mittel)



###Vereine die einzelnen Jahreszeiten

Jahresbetrachtung = [Winter, Fruehling, Sommer, Herbst]

###Passe die Jahre auf ein gemeinsames an
Jahresbetrachtung = pd.concat(Jahresbetrachtung, ignore_index=True)
Jahresbetrachtung.update(
    Jahresbetrachtung[(Jahresbetrachtung["Zeit"] < datetime(2022, 1, 1))]["Zeit"] + pd.offsets.DateOffset(years=1))
Jahresbetrachtung = Jahresbetrachtung.sort_values(by=["Zeit"], ignore_index=True)


###betrachte Zwischenfazit
print(Jahresbetrachtung.info())


###Weiße die festgelgten Feiertage und Urlaubstage zu
for i in range(len(Jahresbetrachtung)):
    if Jahresbetrachtung.loc[i, "Zeit"] >= pd.Timestamp(Karfreitag) and \
            Jahresbetrachtung.loc[i, "Zeit"] < pd.Timestamp(Karfreitag + delta(1)):
        Jahresbetrachtung.loc[i, "kWh"] = Mittelwert_zwischen_20_24

    if Jahresbetrachtung.loc[i, "Zeit"] >= pd.Timestamp(Ostermontag) and \
            Jahresbetrachtung.loc[i, "Zeit"] < pd.Timestamp(Ostermontag + delta(1)):
        Jahresbetrachtung.loc[i, "kWh"] = Mittelwert_zwischen_20_24

    if Jahresbetrachtung.loc[i, "Zeit"] >= pd.Timestamp(Tag_der_Arbiet) and \
            Jahresbetrachtung.loc[i, "Zeit"] < pd.Timestamp(Tag_der_Arbiet + delta(1)):
        Jahresbetrachtung.loc[i, "kWh"] = Mittelwert_zwischen_20_24

    if Jahresbetrachtung.loc[i, "Zeit"] >= pd.Timestamp(Himmelfahrt) and \
            Jahresbetrachtung.loc[i, "Zeit"] < pd.Timestamp(Himmelfahrt + delta(1)):
        Jahresbetrachtung.loc[i, "kWh"] = Mittelwert_zwischen_20_24

    if Jahresbetrachtung.loc[i, "Zeit"] >= pd.Timestamp(Pfingsmontag) and \
            Jahresbetrachtung.loc[i, "Zeit"] < pd.Timestamp(Pfingsmontag + delta(1)):
        Jahresbetrachtung.loc[i, "kWh"] = Mittelwert_zwischen_20_24

    if Jahresbetrachtung.loc[i, "Zeit"] >= pd.Timestamp(Fronleichnam) and \
            Jahresbetrachtung.loc[i, "Zeit"] < pd.Timestamp(Fronleichnam + delta(1)):
        Jahresbetrachtung.loc[i, "kWh"] = Mittelwert_zwischen_20_24

    if Jahresbetrachtung.loc[i, "Zeit"] >= pd.Timestamp(Tag_der_deutschen_Einheit) and \
            Jahresbetrachtung.loc[i, "Zeit"] < pd.Timestamp(Tag_der_deutschen_Einheit + delta(1)):
        Jahresbetrachtung.loc[i, "kWh"] = Mittelwert_zwischen_20_24

    if Jahresbetrachtung.loc[i, "Zeit"] >= pd.Timestamp(Allerheiligen) and \
            Jahresbetrachtung.loc[i, "Zeit"] < pd.Timestamp(Allerheiligen + delta(1)):
        Jahresbetrachtung.loc[i, "kWh"] = Mittelwert_zwischen_20_24

    if Jahresbetrachtung.loc[i, "Zeit"] >= pd.Timestamp(Erster_Weihnachten) and \
            Jahresbetrachtung.loc[i, "Zeit"] < pd.Timestamp(Erster_Weihnachten + delta(1)):
        Jahresbetrachtung.loc[i, "kWh"] = Mittelwert_zwischen_20_24

    if Jahresbetrachtung.loc[i, "Zeit"] >= pd.Timestamp(Zweiter_Weihnachten) and \
            Jahresbetrachtung.loc[i, "Zeit"] < pd.Timestamp(Zweiter_Weihnachten + delta(1)):
        Jahresbetrachtung.loc[i, "kWh"] = Mittelwert_zwischen_20_24

    if Jahresbetrachtung.loc[i, "Zeit"] >= pd.Timestamp(Urlaub_von) and \
            Jahresbetrachtung.loc[i, "Zeit"] <= pd.Timestamp(Urlaub_bis):
        Jahresbetrachtung.loc[i, "kWh"] = 0.0

    if Jahresbetrachtung.loc[i, "Zeit"] >= pd.Timestamp(Urlaub_von_2) and \
            Jahresbetrachtung.loc[i, "Zeit"] <= pd.Timestamp(Urlaub_bis_2):
        Jahresbetrachtung.loc[i, "kWh"] = 0.0


###Füge die Stromverbrauche auf die Jahresbetrachtung und speichere dies ab und fasse beim ersten diese in stündlicher Taktung
Jahresbetrachtung.assign(Verhältnis_kWh=lambda x: (x["kWh"]/sum(Jahresbetrachtung["kWh"]))*Stromprofil_Jahr_kWh)\
.resample("H",on="Zeit")["Verhältnis_kWh"].sum().to_excel("Auswertung_Lastverlauf_stündlich.xlsx",
                                         sheet_name='Jahresbetrachtung',index=False,
                                         header=["Verhältnis_kWh_Stündlich"])

###abspeichern in 15 minütiger taktung
Jahresbetrachtung.assign(Verhältnis_kWh=lambda x: (x["kWh"]/sum(Jahresbetrachtung["kWh"]))*Stromprofil_Jahr_kWh)\
.to_excel("Auswertung_Lastprofil.xlsx",
                                         sheet_name='Jahresbetrachtung',index=False,
                                         header=["Zeit","kWh","Verhältnis_kWh"])
