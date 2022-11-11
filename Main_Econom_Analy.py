import pandas as pd

from Import_Libraries import *
from VOFI import *

'''
Achtung, der univariate Fall wurde für die angenommenen Parameter bewusst nicht automatisiert, diese 
müssen in Abhängigkeit der Szenario angepasst werden

'''

if __name__ == "__main__":

    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    '''
    Ermittlung der geometrischen brownschen Bewegung für den Strompreis für die kommenden 20 Jahren.
    '''
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    df = pd.read_excel(
        "C:/Users/soner/OneDrive/04_Masterarbeit/99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Energiepreis/preis_test.xlsx")

    dt = 1 / 2

    P_0 = df.loc[len(df) - 1, "Strompreis"]

    Wachstumsrate = df.iloc[-1]["Strompreis"] / df.iloc[0]["Strompreis"]
    Dauer = len(df["Strompreis"])

    Durchschnittliche_Wachstumsrate = (Wachstumsrate ** (1 / Dauer) - 1)

    df["Preisdifferenz"] = 0.0

    for i in range(len(df["Preisdifferenz"]) - 1):
        df.loc[i, "Preisdifferenz"] = df.loc[(i), "Strompreis"] / df.loc[(i + 1), "Strompreis"]

    Vola = df["Preisdifferenz"].std()

    S_T = []
    Q_T = []

    runs = 20 * 10 ** 3  # 10**5
    Zeitraum = 43  # 20
    np.random.seed(42)

    Q_T = Monte_Carlo_GBM(Zeitraum, S_T, dt, P_0, Durchschnittliche_Wachstumsrate, runs)
    Q_T = pd.DataFrame(data=np.transpose(Q_T))
    alpha = 0.025
    Q_T = Q_T.assign(Q_T_lower=Q_T.quantile(alpha, axis=1))
    Q_T = Q_T.assign(Q_T_upper=Q_T.quantile(1 - alpha, axis=1))
    Q_T = Q_T.assign(Q_T_Mean=Q_T.mean(axis=1))
    Q_T.drop(Q_T.index[[0, 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 43]],
             inplace=True)




    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    '''
    Festlegung der einzelnen Spannweiten der Parameter mit 100 Teilschritten mithilfe des linspace FUnktion 
    --> linearen gleichmäßigen Raum 
    '''
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    Strompreis_Ranges_Test = pd.DataFrame()
    Strompreis_Ranges_Test = pd.DataFrame(
        [-Q_T.quantile(0.05, axis=1) + Q_T.mean(axis=1), Q_T.quantile(0.95, axis=1) - Q_T.mean(axis=1)])
    # Strompreis_Ranges_Test=pd.DataFrame([-Q_T.std(axis=1)+Q_T.mean(axis=1),Q_T.std(axis=1)+Q_T.mean(axis=1)])
    Strompreis_Ranges_Test = Strompreis_Ranges_Test.T
    RANGE_STRP_PREIS = []
    tmp_a = 0
    tmp_b = 0
    for i in range(0, len(Strompreis_Ranges_Test)):
        for q in range(np.shape(Strompreis_Ranges_Test)[1]):
            if q == 0:
                tmp_a = Strompreis_Ranges_Test.loc[i, 0]
        if q > 0:
            tmp_b = Strompreis_Ranges_Test.loc[i, 1]

            RANGE_STRP_PREIS.append(np.linspace(tmp_a, tmp_b, 20))
        #pd.DataFrame(Strompreis_Ranges_Test).to_excel("C:/Users/soner/Desktop/RANGE_STRP_PREIS.xlsx")



    Degredation_Range = np.linspace(0.004, 0.007, 100)
    Degredation_Range = list(Degredation_Range)
    #pd.DataFrame(Degredation_Range).to_excel("C:/Users/soner/Desktop/Univariate_Sensitivität/" \
    #                                         "Degredation_Range.xlsx",
    #                                         index=False)  ### zum abspeichern, der resultierenden Parameter

    Fremdkapitalzins_Range = np.linspace(0.0799, 0.1399, 100)
    Fremdkapitalzins_Range = list(Fremdkapitalzins_Range)
    #pd.DataFrame(Fremdkapitalzins_Range).to_excel("C:/Users/soner/Desktop/Univariate_Sensitivität/" \
    #                                              "Fremdkapitalzins_Range.xlsx",
    #                                              index=False)  ### zum abspeichern, der resultierenden Parameter

    Inflation_Range = np.linspace(0.0, 0.1, 100)
    Inflation_Range = list(Inflation_Range)
    #pd.DataFrame(Inflation_Range).to_excel("C:/Users/soner/Desktop/Univariate_Sensitivität/" \
    #                                       "Inflation_Range.xlsx",
    #                                       index=False)  ### zum abspeichern, der resultierenden Parameter

    Sollzins_KfW_Range = np.linspace(0.0465, 0.1143, 100)
    Sollzins_KfW_Range = list(Sollzins_KfW_Range)
    #pd.DataFrame(Sollzins_KfW_Range).to_excel("C:/Users/soner/Desktop/Univariate_Sensitivität/" \
    #                                          "Sollzins_KfW_Range.xlsx",
    #                                          index=False)  ### zum abspeichern, der resultierenden Parameter

    # Einspeisevergütung_Range=np.linspace(0.0,0.0818365444375388,100)
    # Einspeisevergütung_Range=list(Einspeisevergütung_Range)
    # pd.DataFrame(Einspeisevergütung_Range).to_excel("C:/Users/soner/Desktop/Univariate_Sensitivität/"\
    #                                                         "Einspeisevergütung_Range.xlsx",index=False) #zum abspeichern, der resultierenden Parameter

    Batteriepreisenkung_Range = np.linspace(0.4, 0.5, 100)
    #Batteriepreisenkung_Range = list(Batteriepreisenkung_Range)
    #pd.DataFrame(Batteriepreisenkung_Range).to_excel("C:/Users/soner/Desktop/Univariate_Sensitivität/" \
    #                                                "Batteriepreisenkung_Range.xlsx",
    #                                                index=False)  # zum abspeichern, der resultierenden Parameter

    Auszahlung_aus_der_Szenario_Range = np.linspace(1201.12 * (1 - 0.07), 1201.12 * (1 + 0.07), 100)
    #Auszahlung_aus_der_Szenario_Range = list(Auszahlung_aus_der_Szenario_Range)
    #pd.DataFrame(Auszahlung_aus_der_Szenario_Range).to_excel("C:/Users/soner/Desktop/Univariate_Sensitivität/" \
    #                                                         "Auszahlung_aus_der_Szenario_Range.xlsx",
    #                                                         index=False)  # zum abspeichern, der resultierenden
    # Parameter

    Batteriepreis_Range = np.linspace(1200, 2200, 100)
    Batteriepreis_Range = list(Batteriepreis_Range)
    #pd.DataFrame(Batteriepreis_Range).to_excel("C:/Users/soner/Desktop/Univariate_Sensitivität/" \
    #                                           "Batteriepreis_Range.xlsx",
    #                                           index=False)  # zum abspeichern, der resultierenden Parameter

    Anschaffung_Szenario_II = 1201.12408
    Auszahlung_BoS_Versicherung_Wartung_Range = np.linspace(Anschaffung_Szenario_II * 0.015, 30.1, 100)
    Auszahlung_BoS_Versicherung_Wartung_Range = list(Auszahlung_BoS_Versicherung_Wartung_Range)
    #pd.DataFrame(Auszahlung_BoS_Versicherung_Wartung_Range).to_excel("C:/Users/soner/Desktop/Univariate_Sensitivität/" \
    #                                                                 "Auszahlung_BoS_Versicherung_Wartung_Range.xlsx",
    #                                                                 index=False)  # zum abspeichern, der resultierenden Parameter

    Habenzins_Range = np.linspace(0, 0.0237, 100)
    Habenzins_Range = list(Habenzins_Range)
    #pd.DataFrame(Habenzins_Range).to_excel("C:/Users/soner/Desktop/Univariate_Sensitivität/" \
    #                                       "Habenzins_Range.xlsx",
     #                                      index=False)  # zum abspeichern, der resultierenden Parameter

    Strompreis_Range = np.linspace(min_Quantil_Strompreis, max_Quantil_Strompreis, 100)
    #Strompreis_Range = list(Strompreis_Range)

    #pd.DataFrame(Strompreis_Range).to_excel("C:/Users/soner/Desktop/Univariate_Sensitivität/" \
    #                                        "Strompreis_Range.xlsx",
    #                                        index=False)  # zum abspeichern, der resultierenden Parameter

    # pd.DataFrame(Strompreis_upper).to_excel("C:/Users/soner/Desktop/Univariate_Sensitivität/"\
    #                                                        "Strompreis_upper.xlsx",index=False) #zum abspeichern, der resultierenden Parameter


    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    '''
    Achtung, der univariate Fall wurde für die angenommenen Parameter bewusst nicht automatisiert, diese 
    müssen in Abhängigkeit der Szenario angepasst werden. Es wurde manuell ausgeführt, da sichergestellt werden solle
    dass die Berechnungen auch zutreffend sind.
    
    In den kommentierten Flächen "#" werden die Spannweiten einzelner Faktoren dargelegt.
    Der unten aufgeführte Quellcode führt das VOFI durch. Das VOFI ist in einzelne Funktionen gegliedert, damit 
    ein Übersicht sowie schnellere Fehlerfindung stattfinden konnte. Das Finanzierungssaldo konnte entsprechend nicht 
    angewendet werden, da der tabellarischer Aufbau nicht direkt ersichtlich ist. 
    In der Python Datei VOFI.py wird eine Funktion aufgeführt, welche den tabellarische Aufbau ausgibt, 
    jedoch ist diese lediglich der Vollständigkeit implementiert worden.
    Ein Verwendung für diese Arbeit hat die Funktion "printing_VOFI" nicht 
    stattgefunden.
    
    Die einzelnen Funktion werden hier nicht näher erläutert, da dies 1x1 dem Logik des Excel Dokument 
    "VOFI (version 1).xlsm" darstellt. 
    
    Nur ist wichtig zu erwähnen, dass der Sollzinssatz sowie der Habenzinssatz in der Ertragssteuerberechnung 
    ermittelt werden, da diese nach dem aufgeführten Logik im Excel-Dokument zuerst in Anspruch genommen wird.
    Die sonstigen Funktionen spiegeln die Fragmente wie im VOFI ab. 
    '''
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################


    ### Beginn des VOFIS ab hier
    Endwert_der_Szenarien = []

    for i in tqdm(range(len(Strompreis_Range))):


        ### ANFANG --------- Initialisierung der Eingangsdaten


        Szenario = 16.09  # 8.05 oder 16.09
        Nutzungsdauer = 20  # Wirtschafltiche Nutzungsdauer
        Tilgungsbeginn = 4  # Tilgung KfW
        Typ = 12  # Resutlierend aus vierteljährlicher Zahlung mit dem Beginn nach t=3 -->4*3
        Tilgungjahr = 17  # Anzahl der Jahre, die getilt werden

        Abzug_EEG_2024 = 0.01  # Abzug der Vergütung zweimal pro Jahr
        Umsatzsteuer = 0.19  # Umsatzsteuer

        Gewerbe = (3.55 * 3.5) / 100  # Gewerbesteuer
        Körperschaft = 15 * (1 + 0.055) / 100  # Körperschaftsteuer

        Steuer = []
        Ersparnis_durch_Eigenverbrauch = []
        Strompreis_mit_Inflation = []  # Definition der Variable zum t=0
        Ersparnis_Eigenverbrauch_in_Euro = []  # Definition der Variable zum t=0
        EEG_Foerderung_Gesamt = []  # Definition der Variable zum t=0
        Netzeinspeisung_Geld = []  # Definition der Variable zum t=0
        Umsatzsteuer_auf_Eigenverbrauch = []  # Definition der Variable zum t=0

        # Auszahlung_aus_der_Szenario=Auszahlung_aus_der_Szenario_Range[i]
        Auszahlung_aus_der_Szenario = 1201.12408  # Summe ;Szenario II 1201.12408 pro kWp  #Szenario I 1282.2316

        # Batterie=Batteriepreis_Range[i]
        Batterie = 0  # der Preis der Batterie  bei <5 1200
        # Szenario II 2 1750
        # Szenario II 1 0

        Szenario_Batterie = 0  # aus Szenarien
        # Szenario II 2 3.84
        # Szenario II 1 0

        Batteriepreisenkung = 0.45  # Senkung der Batterie nach t=10
        # Batteriepreisenkung=Batteriepreisenkung_Range[i]

        Fremdkapitalzins_KfW = 0.0538  # KfW Zins
        # Fremdkapitalzins_KfW=Sollzins_KfW_Range[i]
        path="C:/Users/soner/OneDrive/04_Masterarbeit/99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Energiepreis/Mappe1.xlsx"
        Strompreis=list(((np.array(pd.read_excel(path,header=None)).reshape(-1))))

        ######für Strompreis kommentiert dann werden Strompreis_upper und Strompreis_lower auf den Strompreis verwiesen
        # Strompreis=list(Strompreis_Ranges_Test[q])

        Auszahlung_BoS_Versicherung_Wartung = [-Szenario * 30.1]  # Definition der Variable zum t=0 t=1
        # Auszahlung_BoS_Versicherung_Wartung=[-Auszahlung_BoS_Versicherung_Wartung_Range[i]*Szenario]
        # 30.1 v ## Szenario I 34.9

        Stromabnahme_vom_Netz = 39443.50365  # variable in Abhängigkeit der entnommenen  ####siehe Excel liste
        # Szenario II 2 39611.2446
        # Szenario II 1 39443.50365

        Netzeinspeisung_in_kWh = 1891.497262  # variable in Abhängigkeit der entnommenen
        # Szenario II 2 1872.79772
        # Szenario II 1 1891.497262

        EEG_Vergütung = [0.0818365444375388]  # EEG-Vergütung zum t=1 ab t=2 siehe funktion
        # EEG_Vergütung=[Einspeisevergütung_Range[i]]
        # 0.0818365444375388 v 0.086

        Degredation = 0.005  # konstante Abnutzung
        # Degredation=Degredation_Range[i]

        Inflation = 0.02  # Inflation
        # Inflation=Inflation_Range[i]

        Haben = 0.017
        # Haben=Habenzins_Range[i]

        Fremdkapitalzins = 0.0799  # Fremdkapitalzins
        # Fremdkapitalzins=Fremdkapitalzins_Range[i]

        Batteriepreis = Batterie * Szenario_Batterie  # Preis der Batterie
        Wechselrichterpreis = 142.15968 * Szenario  # 16=>142.15968
        Wechselrichtersenkung = 0.02  # nach t=12 Senkung des Wechselrichters

        AfA = [0]
        Sonder_AfA = [0]

        ### ENDE --------- Initialisierung der Eingangsdaten


        ### Initialiserung des Parameter aus dem VOFI
        Auszahlung, Aufnahme_KfW, Anlage, Auflösung, Steuer, EZÜ, Aufnahme, \
        KfW_Kredit_Ende, Festgeldkonto, Kontokorrentkredit, Sollzins_Kredit, \
        Habenzins, Tilgung_Kredit, Endwert = Anschaffungsauszahlung(Szenario, Auszahlung_aus_der_Szenario,
                                                                    Szenario_Batterie, Batterie)

        ### KfW Darlehen berechnen aus dem VOFI
        Sollzins_KfW, Tilgung_KfW, Restschuld = Kredit(Aufnahme_KfW, Fremdkapitalzins_KfW \
                                                       , Tilgungsbeginn, Tilgungjahr, Typ \
                                                       , Auszahlung, Nutzungsdauer)

        ### Berechnen der AFA und Sonderafa für die Ertragsteuer aus dem VOFI
        AfA, Sonder_AfA = AFA(Auszahlung, Nutzungsdauer)


        ### Berechnen der Nebenrechnung aus dem VOFI
        Auszahlung_BoS_Versicherung_Wartung, Umsatzsteuer_auf_Eigenverbrauch, \
        Ersparnis_Eigenverbrauch_in_Euro, EEG_Foerderung_Gesamt, Netzeinspeisung_Geld = Nebenrechnung_Strom( \
            Ersparnis_durch_Eigenverbrauch, Netzeinspeisung_in_kWh, Stromabnahme_vom_Netz,
            Ersparnis_Eigenverbrauch_in_Euro,
            EEG_Foerderung_Gesamt, Netzeinspeisung_Geld,
            Nutzungsdauer,
            Strompreis_mit_Inflation, Strompreis,
            EEG_Vergütung,
            Degredation, Inflation, Abzug_EEG_2024,
            Umsatzsteuer_auf_Eigenverbrauch, Umsatzsteuer,
            Auszahlung_BoS_Versicherung_Wartung)


        ### Durchführung des VOFI's ab dem Zeitpunkt t=1
        for t in range(1, Nutzungsdauer + 1):
            EZUE(EZÜ,
                 Umsatzsteuer_auf_Eigenverbrauch,
                 Auszahlung_BoS_Versicherung_Wartung,
                 Ersparnis_Eigenverbrauch_in_Euro,
                 Netzeinspeisung_Geld,
                 EEG_Foerderung_Gesamt,
                 Batteriepreis, Batteriepreisenkung,
                 Wechselrichterpreis, Wechselrichtersenkung,
                 t)

            Ertragssteuer(Auszahlung, Aufnahme,
                          AfA, Sonder_AfA,
                          Sollzins_Kredit, Sollzins_KfW, Habenzins, Haben,
                          EZÜ,
                          Nutzungsdauer,
                          Szenario, Gewerbe, Körperschaft, t)

            Kontokorrent(EZÜ, Steuer,
                         Tilgung_KfW, Sollzins_KfW,
                         Sollzins_Kredit, Tilgung_Kredit,
                         Habenzins, Festgeldkonto,
                         Aufnahme, Fremdkapitalzins, Kontokorrentkredit,
                         t)

            Geldanlage(Anlage, EZÜ,
                       Steuer,
                       Sollzins_KfW, Sollzins_Kredit,
                       Habenzins, Haben, Festgeldkonto, Auflösung,
                       Tilgung_KfW, Tilgung_Kredit, Kontokorrentkredit, t)

            Bestandssaldo(KfW_Kredit_Ende,
                          Kontokorrentkredit,
                          Festgeldkonto,
                          Anlage, Aufnahme, Auflösung,
                          Endwert,
                          t)
        Endwert_der_Szenarien.append(Endwert)

    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    '''
    Analog für den multivariaten Fall
    '''
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################


    # -------------------------------------

    df = pd.read_excel(
        "C:/Users/soner/OneDrive/04_Masterarbeit/99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Energiepreis/preis_test.xlsx")

    dt = 1 / 2

    P_0 = df.loc[len(df) - 1, "Strompreis"]

    Wachstumsrate = df.iloc[-1]["Strompreis"] / df.iloc[0]["Strompreis"]
    Dauer = len(df["Strompreis"])

    Durchschnittliche_Wachstumsrate = (Wachstumsrate ** (1 / Dauer) - 1)

    df["Preisdifferenz"] = 0.0

    for i in range(len(df["Preisdifferenz"]) - 1):
        df.loc[i, "Preisdifferenz"] = df.loc[(i), "Strompreis"] / df.loc[(i + 1), "Strompreis"]

    Vola = df["Preisdifferenz"].std()

    S_T = []
    Q_T = []

    runs = 10 ** 5  # 10**5
    Zeitraum = 43  # 20
    np.random.seed(42)###Zufälliger Stichwert

    Q_T = Monte_Carlo_GBM(Zeitraum, S_T, dt, P_0, Durchschnittliche_Wachstumsrate, runs)
    Q_T = pd.DataFrame(data=np.transpose(Q_T))
    Q_T.drop(Q_T.index[[0, 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 43]],
             inplace=True)

    #pd.DataFrame(Q_T).to_csv("C:/Users/soner/Desktop/Strompreis_1000000.csv")
    # Strompreise_Range=np.reshape([Strompreis_lower,Strompreis_upper],(-1))#wenn konstant über die Zeiträume betrachtet werden soll

    np.random.seed(42)

    Habenzinssatz_Monte = []
    for i in range(0, runs): Habenzinssatz_Monte.append(np.random.uniform(0, 0.0237, 1)[0])
    #pd.DataFrame(Habenzinssatz_Monte).to_csv("C:/Users/soner/Desktop/Habenzinssatz_Monte.csv")

    Fremdkapitalzinssatz_Monte_Bank = []
    for i in range(0, runs): Fremdkapitalzinssatz_Monte_Bank.append(np.random.uniform(0.0799, 0.1399, 1)[0])
    #pd.DataFrame(Fremdkapitalzinssatz_Monte_Bank).to_csv("C:/Users/soner/Desktop/Fremdkapitalzinssatz_Monte_Bank.csv")
    Anschaffungsauszahlung_Monte = []
    for i in range(0, runs): Anschaffungsauszahlung_Monte.append(
        np.random.uniform((1 - 0.07) * 1201.12, (1 + 0.07) * 1201.12, 1)[0])
    #pd.DataFrame(Anschaffungsauszahlung_Monte).to_csv("C:/Users/soner/Desktop/Anschaffungsauszahlung_Monte.csv")

    Batteriepreis_Monte = []
    for i in range(0, runs): Batteriepreis_Monte.append(np.random.uniform(1200, 2200, 1)[0])
    #pd.DataFrame(Batteriepreis_Monte).to_csv("C:/Users/soner/Desktop/Batteriepreis_Monte.csv")

    Batteriepreissenkung_Monte = []
    for i in range(0, runs): Batteriepreissenkung_Monte.append(np.random.uniform(0.4, 0.5, 1)[0])
    #pd.DataFrame(Batteriepreissenkung_Monte).to_csv("C:/Users/soner/Desktop/Batteriepreissenkung_Monte.csv")

    Laufende_Auszahlung_Monte = []
    for i in range(0, runs): Laufende_Auszahlung_Monte.append(np.random.uniform(1201.12 * 0.015, 30.1, 1)[0])
    #pd.DataFrame(Laufende_Auszahlung_Monte).to_csv("C:/Users/soner/Desktop/Laufende_Auszahlung_Monte.csv")

    Sollzins_KfW_Monte = []
    for i in range(0, runs): Sollzins_KfW_Monte.append(
        np.random.uniform(0.0465, 0.1143, 1)[0])  # np.random.uniform(0.0465,0.1143,runs) <--effizinetere alternative
    #pd.DataFrame(Sollzins_KfW_Monte).to_csv("C:/Users/soner/Desktop/Sollzins_KfW_Monte.csv")

    Degradation_Monte = []
    for i in range(0, runs): Degradation_Monte.append(np.random.uniform(0.004, 0.007, 1)[0])
    #pd.DataFrame(Degradation_Monte).to_csv("C:/Users/soner/Desktop/Degradation_Monte.csv")

    Endwert_der_Szenarien = []
    Szenariosa = 1
    for i in tqdm(range(runs)):###Laufe die defnierten RUNS

        ### ANFANG --------- Initialisierung der Eingangsdaten
        Szenario = 16.09  # 8.05 oder 16.09
        Nutzungsdauer = 20  # Wirtschafltiche Nutzungsdauer
        Tilgungsbeginn = 4  # Tilgung KfW
        Typ = 12  # Resutlierend aus vierteljährlicher Zahlung mit dem Beginn nach t=3 -->4*3
        Tilgungjahr = 17  # Anzahl der Jahre, die getilt werden

        Abzug_EEG_2024 = 0.01  # Abzug der Vergütung zweimal pro Jahr
        Umsatzsteuer = 0.19  # Umsatzsteuer

        Gewerbe = (3.55 * 3.5) / 100  # Gewerbesteuer
        Körperschaft = 15 * (1 + 0.055) / 100  # Körperschaftsteuer

        Steuer = []
        Ersparnis_durch_Eigenverbrauch = []
        Strompreis_mit_Inflation = []  # Definition der Variable zum t=0
        Ersparnis_Eigenverbrauch_in_Euro = []  # Definition der Variable zum t=0
        EEG_Foerderung_Gesamt = []  # Definition der Variable zum t=0
        Umsatzsteuer_auf_Eigenverbrauch = []  # Definition der Variable zum t=0

        Auszahlung_aus_der_Szenario = Anschaffungsauszahlung_Monte[i]
        Auszahlung_BoS_Versicherung_Wartung = [-Szenario * Laufende_Auszahlung_Monte[i]]

        if Szenariosa == 2:
            Batterie = Batteriepreis_Monte[i]
            Batteriepreisenkung = Batteriepreissenkung_Monte[i]
            Stromabnahme_vom_Netz = 39611.2446  # variable in Abhängigkeit der entnommenen  ####siehe Excel liste
            Netzeinspeisung_in_kWh = 1872.79772  # variable in Abhängigkeit der entnommenen
            Szenario_Batterie = 3.84  # aus Szenarien

        else:
            Batteriepreisenkung = 0
            Batterie = 0
            Szenario_Batterie = 0
            Stromabnahme_vom_Netz = 39443.50365
            Netzeinspeisung_in_kWh = 1891.497262

        Fremdkapitalzins_KfW = Sollzins_KfW_Monte[i]
        Strompreis = list(Q_T[i])

        EEG_Vergütung = [0.0818365444375388]  # EEG-Vergütung zum t=1 ab t=2 siehe funktion
        Degredation = Degradation_Monte[i]

        Inflation = 0.02  # Inflation
        Haben = Habenzinssatz_Monte[i]
        Fremdkapitalzins = Fremdkapitalzinssatz_Monte_Bank[i]

        Batteriepreis = Batterie * Szenario_Batterie  # Preis der Batterie
        Wechselrichterpreis = 142.15968 * Szenario  # 16=>142.15968
        Wechselrichtersenkung = 0.02  # nach t=12 Senkung des Wechselrichters

        AfA = [0]
        Sonder_AfA = [0]
        ### Ende  --------- Initialisierung der Eingangsdaten



        ### Beginn des VOFIS

        Auszahlung, Aufnahme_KfW, Anlage, Auflösung, Steuer, EZÜ, Aufnahme, \
        KfW_Kredit_Ende, Festgeldkonto, Kontokorrentkredit, Sollzins_Kredit, \
        Habenzins, Tilgung_Kredit, Endwert = Anschaffungsauszahlung(Szenario, Auszahlung_aus_der_Szenario,
                                                                    Szenario_Batterie, Batterie)

        Sollzins_KfW, Tilgung_KfW, Restschuld = Kredit(Aufnahme_KfW, Fremdkapitalzins_KfW \
                                                       , Tilgungsbeginn, Tilgungjahr, Typ \
                                                       , Auszahlung, Nutzungsdauer)

        AfA, Sonder_AfA = AFA(Auszahlung, Nutzungsdauer)

        Auszahlung_BoS_Versicherung_Wartung, Umsatzsteuer_auf_Eigenverbrauch, \
        Ersparnis_Eigenverbrauch_in_Euro, EEG_Foerderung_Gesamt = Nebenrechnung_Strom( \
            Ersparnis_durch_Eigenverbrauch, Netzeinspeisung_in_kWh, Stromabnahme_vom_Netz,
            Ersparnis_Eigenverbrauch_in_Euro,
            EEG_Foerderung_Gesamt,
            Nutzungsdauer,
            Strompreis_mit_Inflation, Strompreis,
            EEG_Vergütung,
            Degredation, Inflation, Abzug_EEG_2024,
            Umsatzsteuer_auf_Eigenverbrauch, Umsatzsteuer,
            Auszahlung_BoS_Versicherung_Wartung)

        for t in range(1, Nutzungsdauer + 1):

            if t != 1:
                Inflation = 0.02

            else:
                Inflation = 0.07

            EZUE(EZÜ,
                 Umsatzsteuer_auf_Eigenverbrauch,
                 Auszahlung_BoS_Versicherung_Wartung,
                 Ersparnis_Eigenverbrauch_in_Euro,
                 EEG_Foerderung_Gesamt,
                 Batteriepreis, Batteriepreisenkung,
                 Wechselrichterpreis, Wechselrichtersenkung,
                 t)

            Ertragssteuer(Auszahlung, Aufnahme,
                          AfA, Sonder_AfA,
                          Sollzins_Kredit, Sollzins_KfW, Habenzins, Haben,
                          EZÜ,
                          Nutzungsdauer,
                          Szenario, Gewerbe, Körperschaft, t)

            Kontokorrent(EZÜ, Steuer,
                         Tilgung_KfW, Sollzins_KfW,
                         Sollzins_Kredit, Tilgung_Kredit,
                         Habenzins, Festgeldkonto,
                         Aufnahme, Fremdkapitalzins, Kontokorrentkredit,
                         t)

            Geldanlage(Anlage, EZÜ,
                       Steuer,
                       Sollzins_KfW, Sollzins_Kredit,
                       Habenzins, Haben, Festgeldkonto, Auflösung,
                       Tilgung_KfW, Tilgung_Kredit, Kontokorrentkredit, t)

            Bestandssaldo(KfW_Kredit_Ende,
                          Kontokorrentkredit,
                          Festgeldkonto,
                          Anlage, Aufnahme, Auflösung,
                          Endwert,
                          t)
        Endwert_der_Szenarien.append(Endwert)

        ''' Zum sichern des VOFI's
        save_name = "VOFI_"+str(runs)
        printering.printing_VOFI(save_name, 
                                 EZÜ, Steuer, Aufnahme_KfW, Sollzins_KfW, Tilgung_KfW, 
                                 Aufnahme, Sollzins_Kredit, Tilgung_Kredit, Anlage, 
                                 Habenzins, 
                                 Auflösung, 
                                 Kontokorrentkredit, 
                                 Festgeldkonto, 
                                 KfW_Kredit_Ende, 
                                 Endwert)
        '''