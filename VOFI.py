from Import_Libraries import *

####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
'''
In dieser Datei werden die einzelnen Funktionen aufgeführt die entwickelt worden sind. Im 
speziellen handelt es sich um das VOFI sowie dem geometrisch brownschen Bewegung.
Zusätzlich wird ein Rundungsbefehl "round_down" aufgeführt für die Gewerbesteuer aufgeführt. (Line  ca .286) 
Diese entspricht den den Flussdiagrammen bzw. Ablaufdiagrammen von  
(Grob (2006), S. 121 (ISBN 978-3-8006-3276-3)), 
(Trost/ Fox (2017)), Müller (2019) S. 384, (DOI: 10.1515/9783110517163-020),  
(Grob (2006), S. 351 ff. (ISBN: 978-3-8006-3276-3)),
(Götze (2008), S. 140 f.  (ISBN: 10.1007/978-3-540-78873-7))
'''
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################

#Ermittlung des Ein- bzw. Auszahlungsüberschüsse
def EZUE(EZÜ,
         Umsatzsteuer_auf_Eigenverbrauch,
         Auszahlung_BoS_Versicherung_Wartung,
         Ersparnis_Eigenverbrauch_in_Euro,
         EEG_Foerderung_Gesamt,
         Batteriepreis, Batteriepreisenkung,
         Wechselrichterpreis, Wechselrichtersenkung,
         t):
    if t == 10:
        Batteriepreis_berechnung = -Batteriepreis * Batteriepreisenkung

    else:
        Batteriepreis_berechnung = 0

    if t == 12:
        Wechselrichterpreis_berechnung = -Wechselrichterpreis * ((1 - Wechselrichtersenkung) ** t)

    else:
        Wechselrichterpreis_berechnung = 0

    EZÜ.append(Umsatzsteuer_auf_Eigenverbrauch[t] + Auszahlung_BoS_Versicherung_Wartung[t] + \
               Ersparnis_Eigenverbrauch_in_Euro[t] + EEG_Foerderung_Gesamt[t] + \
               Batteriepreis_berechnung + Wechselrichterpreis_berechnung)


         
# Init 
def Anschaffungsauszahlung(Szenario, Auszahlung_aus_der_Szenario, Szenario_Batterie, Batterie):
    Auszahlung = []
    KfW_Kredit_Ende = []
    Aufnahme_KfW = []

    Auszahlung.append(-(Auszahlung_aus_der_Szenario * Szenario + Batterie * Szenario_Batterie))
    Aufnahme_KfW.append((Auszahlung_aus_der_Szenario * Szenario + Batterie * Szenario_Batterie))

    Aufnahme = [0]
    Sollzins_Kredit = [0]
    Tilgung_Kredit = [0]

    Anlage = [0]
    Habenzins = [0]
    Auflösung = [0]

    EZÜ = [-(Auszahlung_aus_der_Szenario * Szenario + Batterie * Szenario_Batterie)]
    Steuer = [0]
    Festgeldkonto = [0]
    Kontokorrentkredit = [0]

    KfW_Kredit_Ende.append(-(Auszahlung_aus_der_Szenario * Szenario + Batterie * Szenario_Batterie))

    Endwert = []
    Endwert.append(-(Auszahlung_aus_der_Szenario * Szenario + Batterie * Szenario_Batterie))

    return Auszahlung, Aufnahme_KfW, Anlage, Auflösung, Steuer, EZÜ, Aufnahme, \
           KfW_Kredit_Ende, Festgeldkonto, Kontokorrentkredit, Sollzins_Kredit, \
           Habenzins, Tilgung_Kredit, Endwert


def Bestandssaldo(KfW_Kredit_Ende,
                  Kontokorrentkredit,
                  Festgeldkonto,
                  Anlage, Aufnahme, Auflösung,
                  Endwert,
                  t):
    KfW_Kredit_Ende.append(KfW_Kredit_Ende[t - 1] - Tilgung_KfW[t])
    Festgeldkonto.append(Festgeldkonto[t - 1] - Anlage[t] - Auflösung[t])
    if Kontokorrentkredit[t - 1] - Tilgung_Kredit[t] - Aufnahme[t] > 0:
        Kontokorrentkredit.append(0)
    else:
        Kontokorrentkredit.append(Kontokorrentkredit[t - 1] - Tilgung_Kredit[t] - Aufnahme[t])

    Endwert.append(KfW_Kredit_Ende[t] + Festgeldkonto[t] + Kontokorrentkredit[t])


         
### Berechnung der Ein- Auszahlungen
def Nebenrechnung_Strom(Ersparnis_durch_Eigenverbrauch, Netzeinspeisung_in_kWh, Stromabnahme_vom_Netz,
                        Ersparnis_Eigenverbrauch_in_Euro,
                        EEG_Foerderung_Gesamt,
                        Nutzungsdauer,
                        Strompreis_mit_Inflation, Strompreis,
                        EEG_Vergütung,
                        Degredation, Inflation, Abzug_EEG_2024,
                        Umsatzsteuer_auf_Eigenverbrauch, Umsatzsteuer,
                        Auszahlung_BoS_Versicherung_Wartung):
    Stromverbrauch_in_kWh = 51865.3125  # Stromverbrauch konstant

    Ersparnis_durch_Eigenverbrauch = (Stromverbrauch_in_kWh - Stromabnahme_vom_Netz - Netzeinspeisung_in_kWh)

    for t in range(0, Nutzungsdauer):
        EEG_Vergütung.append(np.power(1 - Abzug_EEG_2024, 2) * EEG_Vergütung[t])

        Strompreis_mit_Inflation.append((1 + Inflation) * Strompreis[t])

        Ersparnis_Eigenverbrauch_in_Euro.append(Ersparnis_durch_Eigenverbrauch * Strompreis_mit_Inflation[t])
        EEG_Foerderung_Gesamt.append(Netzeinspeisung_in_kWh * EEG_Vergütung[t])

        Auszahlung_BoS_Versicherung_Wartung.append((Auszahlung_BoS_Versicherung_Wartung[t]) * (1 + Inflation))

        Umsatzsteuer_auf_Eigenverbrauch.append(-Ersparnis_Eigenverbrauch_in_Euro[t] * Umsatzsteuer)

        Stromabnahme_vom_Netz = ((1 + Degredation) * Stromabnahme_vom_Netz)
        Netzeinspeisung_in_kWh = ((1 - Degredation) * Netzeinspeisung_in_kWh)
        Ersparnis_durch_Eigenverbrauch = (Stromverbrauch_in_kWh - Stromabnahme_vom_Netz - Netzeinspeisung_in_kWh)

    Umsatzsteuer_auf_Eigenverbrauch = [0] + Umsatzsteuer_auf_Eigenverbrauch
    Ersparnis_Eigenverbrauch_in_Euro = [0] + Ersparnis_Eigenverbrauch_in_Euro
    EEG_Foerderung_Gesamt = [0] + EEG_Foerderung_Gesamt

    return Auszahlung_BoS_Versicherung_Wartung, Umsatzsteuer_auf_Eigenverbrauch, \
           Ersparnis_Eigenverbrauch_in_Euro, EEG_Foerderung_Gesamt


#Berechnung des Abschreibung mit Sonderabschreibung nach §7 Gewstg
def AFA(Auszahlung, Nutzungsdauer):
    Sonder_AfA_0_2 = 0.2
    Laufzeit_Sonder_AfA = 5

    for t in range(1, Nutzungsdauer + 1):
        if t <= 5:
            AfA.append(Auszahlung[0] / (Nutzungsdauer))
            Sonder_AfA.append(Auszahlung[0] * Sonder_AfA_0_2 / Laufzeit_Sonder_AfA)

            if t == 5:
                Neue_Abschreibung = -Auszahlung[0] + np.sum(Sonder_AfA) + np.sum(AfA)
                Restnutzungsdauer = Nutzungsdauer - t

        if t >= 6:
            AfA.append(-Neue_Abschreibung / (Restnutzungsdauer))
            Sonder_AfA.append(0)

    return AfA, Sonder_AfA

##Berechnung des Zinssatzes vom KfW Kredit
def Kredit(Aufnahme_KfW, Fremdkapitalzins_KfW, Tilgungsbeginn, Tilgungjahr, Typ, Auszahlung, Nutzungsdauer):
    Sollzins_KfW = []
    Tilgung_KfW = []
    Rate = []
    Restschuld = []

    for q in range(Typ):
        Tilgung_KfW.append(0)
        Sollzins_KfW.append(Aufnahme_KfW[0] * Fremdkapitalzins_KfW / Tilgungsbeginn)
        Rate.append(Tilgung_KfW[q] + Sollzins_KfW[q])

        Restschuld.append(Aufnahme_KfW[0])

    for q in range(Typ, Tilgungsbeginn * Nutzungsdauer):
        Tilgung_KfW.append(Aufnahme_KfW[0] / (Tilgungsbeginn * Tilgungjahr))
        Sollzins_KfW.append(Restschuld[q - 1] * Fremdkapitalzins_KfW / Tilgungsbeginn)

        Rate.append(Tilgung_KfW[q] + Sollzins_KfW[q])
        Restschuld.append(Restschuld[q - 1] - Tilgung_KfW[q])

    Sollzins_KfW = -np.sum(np.reshape(Sollzins_KfW, (Nutzungsdauer, -1)), axis=1)
    Tilgung_KfW = -np.sum(np.reshape(Tilgung_KfW, (Nutzungsdauer, -1)), axis=1)
    Restschuld = np.sum(np.reshape(Restschuld, (Nutzungsdauer, -1)), axis=1)

    Sollzins_KfW = list(Sollzins_KfW)
    Tilgung_KfW = list(Tilgung_KfW)

    Sollzins_KfW = [0] + Sollzins_KfW
    Tilgung_KfW = [0] + Tilgung_KfW
    return Sollzins_KfW, Tilgung_KfW, Restschuld


##Körperschaftsteuer mit Soli sowie Gewerbesteuer mit Hebesatz; in dieser Funktion wird auch der Sollzins vom KfW sowie der Fremdkapitalzins und Habenzinssatz ermittelt
def Ertragssteuer(Auszahlung, Aufnahme,
                  AfA, Sonder_AfA,
                  Sollzins_Kredit, Sollzins_KfW, Habenszins, Haben,
                  EZÜ,
                  Nutzungsdauer,
                  Szenario, Gewerbe, Körperschaft, t):
    if Kontokorrentkredit[t - 1] < 0:
        Sollzins_Kredit.append(Kontokorrentkredit[t - 1] * Fremdkapitalzins)

    else:
        Sollzins_Kredit.append(0)

    if Festgeldkonto[t - 1] >= 1.0:
        Habenzins.append(Festgeldkonto[t - 1] * Haben)

    else:
        Habenzins.append(0)

    Gewerbebetrag = 0
    Körperschatbetrag = 0

    ##Gewerbe

    if Szenario < 10.0:
        Gewerbebetrag = 0

    else:
        Gewerbebetrag = (round_down((EZÜ[t] + Sollzins_Kredit[t] + Sollzins_KfW[t] \
                                     + Habenzins[t] - (Sollzins_KfW[t] + Sollzins_Kredit[t]) * 0.25), -2) * Gewerbe)

    # Körperschaft

    Körperschatbetrag = (EZÜ[t] + AfA[t] + Sonder_AfA[t] + Sollzins_KfW[t] + Sollzins_Kredit[t] + Habenzins[
        t]) * Körperschaft
    Steuer.append(-(Gewerbebetrag + Körperschatbetrag))


         
 
#Bankguthaben die Überschussrechnung
def Geldanlage(Anlage, EZÜ,
               Steuer,
               Sollzins_KfW, Sollzins_Kredit,
               Habenzins, Haben, Festgeldkonto, Auflösung,
               Tilgung_KfW, Tilgung_Kredit, Kontokorrentkredit, t):
    if EZÜ[t] + Steuer[t] + Sollzins_Kredit[t] + Sollzins_KfW[t] + Tilgung_KfW[t] + Habenzins[t] + Tilgung_Kredit[
        t] > 0 and Kontokorrentkredit[t - 1] <= 0:

        Anlage.append(-(EZÜ[t] + Steuer[t] + Sollzins_Kredit[t] + Sollzins_KfW[t] + Tilgung_KfW[t] + Habenzins[t] +
                        Tilgung_Kredit[t]))

    elif EZÜ[t] + Steuer[t] + Sollzins_Kredit[t] + Sollzins_KfW[t] + Tilgung_KfW[t] + Habenzins[t] + Tilgung_Kredit[
        t] > 0 and Kontokorrentkredit[t - 1] > 0 and \
            EZÜ[t] + Steuer[t] + Sollzins_Kredit[t] + Sollzins_KfW[t] + Tilgung_KfW[t] + Habenzins[t] + Tilgung_Kredit[
        t] > Kontokorrentkredit[t - 1]:

        Anlage.append(-(EZÜ[t] + Steuer[t] + Sollzins_Kredit[t] + Sollzins_KfW[t] + Tilgung_KfW[t] + Habenzins[t]) -
                      Tilgung_Kredit[t] - Kontokorrentkredit[t - 1])

    else:
        Anlage.append(0)

    if EZÜ[t] + Steuer[t] + Sollzins_KfW[t] + Sollzins_Kredit[t] + Tilgung_KfW[t] + Habenzins[t] < 0 and Festgeldkonto[
        t - 1] >= 0 and \
            EZÜ[t] + Steuer[t] + Sollzins_KfW[t] + Sollzins_Kredit[t] + Tilgung_KfW[t] + Habenzins[t] > -Festgeldkonto[
        t - 1]:

        Auflösung.append(-(EZÜ[t] + Steuer[t] + Sollzins_KfW[t] + Sollzins_Kredit[t] + Tilgung_KfW[t] + Habenzins[t]))

    elif EZÜ[t] + Steuer[t] + Sollzins_Kredit[t] + Sollzins_KfW[t] + Tilgung_KfW[t] + Habenzins[t] < 0 and \
            Festgeldkonto[t - 1] >= 0 and \
            EZÜ[t] + Steuer[t] + Sollzins_Kredit[t] + Sollzins_KfW[t] + Tilgung_KfW[t] + Habenzins[t] < -1 * \
            Festgeldkonto[t - 1]:

        Auflösung.append(Festgeldkonto[t - 1])
    else:
        Auflösung.append(0)


#Fremdkapitalrechnung Unterschussrechnung
def Kontokorrent(EZÜ, Steuer,
                 Tilgung_KfW, Sollzins_KfW,
                 Sollzins_Kredit, Tilgung_Kredit,
                 Habenzins, Festgeldkonto,
                 Aufnahme, Fremdkapitalzins, Kontokorrentkredit,
                 t):
    if EZÜ[t] + Steuer[t] + Tilgung_KfW[t] + Sollzins_KfW[t] + Habenzins[t] + Sollzins_Kredit[t] + Festgeldkonto[
        t - 1] < 0:

        Aufnahme.append(-(EZÜ[t] + Steuer[t] + Tilgung_KfW[t] + Sollzins_KfW[t] + Habenzins[t] + Sollzins_Kredit[t] +
                          Festgeldkonto[t - 1]))

    else:
        Aufnahme.append(0)

    if -(EZÜ[t] + Steuer[t] + Tilgung_KfW[t] + Sollzins_KfW[t] + Sollzins_Kredit[t] + Festgeldkonto[t - 1]) < 0:
        Tilgung_Kredit.append(0)
    elif Kontokorrentkredit[t - 1] < 0:
        if Aufnahme[t] == 0:
            if EZÜ[t] + Steuer[t] + Tilgung_KfW[t] + Sollzins_KfW[t] + Sollzins_Kredit[t] + Festgeldkonto[t - 1] > 0:
                Tilgung_Kredit.append(-(
                            EZÜ[t] + Steuer[t] + Tilgung_KfW[t] + Sollzins_KfW[t] + Sollzins_Kredit[t] + Festgeldkonto[
                        t - 1]))
            else:
                Tilgung_Kredit.append(0)
        else:
            Tilgung_Kredit.append(0)
    else:
        Tilgung_Kredit.append(0)


def round_down(n, decimals=0):###Zum Abrunden der Gewerbesteuer
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier



#Geometrisch Brownsche Bewegung
def Monte_Carlo_GBM(Zeitraum, S_T, dt, P_0, Durchschnittliche_Wachstumsrate, runs):
    np.random.seed(42)

    for b in tqdm(range(runs)):  # monte
        tmp = np.ones(Zeitraum + 1) * P_0

        for i in range(Zeitraum):  # gbm
            tmp[i + 1] = tmp[i] + tmp[i] \
                         * (Durchschnittliche_Wachstumsrate * dt + Vola * np.random.standard_normal() * np.sqrt(dt))

        S_T.append(tmp)
        tmp = []

    return S_T

#Ausrucken des VOFI's in ein Excel sheet
class printering():
    @staticmethod
    def printing_VOFI(save_name,
                      EZÜ, Steuer, Aufnahme_KfW, Sollzins_KfW, Tilgung_KfW,
                      Aufnahme, Sollzins_Kredit, Tilgung_Kredit, Anlage,
                      Habenzins,
                      Auflösung,
                      Kontokorrentkredit,
                      Festgeldkonto,
                      KfW_Kredit_Ende,
                      Endwert):
        Spalte_Text = ["EZÜ", "Ertragsteuer", \
                       "Aufnahme KfW", "Sollzins KfW", "Tilgung KfW", \
                       "Aufnahme", "Tilgung", "Sollzins", \
                       "Anlage", "Habenzins", "Auflösung", \
                       "Saldo", \
                       "Kontokorrentkredit", "Festgeldkonto", "KfW Kredit", "Endwert"]
        counter = 0
        df = pd.DataFrame(np.transpose(Spalte_Text))

        Saldo = np.add(
            np.add(
            np.add(
            np.add(
            np.add(
            np.add(
            # np.add(\
            np.add(
            np.add(
            np.add(
            np.add(
                    EZÜ, Steuer),
                    Aufnahme_KfW), Sollzins_KfW), Tilgung_KfW),
                    Aufnahme),
                    Sollzins_Kredit),
                    Tilgung_Kredit),
                    Anlage), Habenzins), Auflösung)

        Saldo = np.add(np.ones(len(EZÜ)) * EZÜ[0], Saldo)
        Saldo[0] = 0
        df_2 = pd.DataFrame(
            [EZÜ,
             Steuer,
             Aufnahme_KfW,
             Sollzins_KfW,
             Tilgung_KfW,
             Aufnahme,
             Sollzins_Kredit,
             Tilgung_Kredit,
             Anlage,
             Habenzins,
             Auflösung,
             Saldo,
             Kontokorrentkredit,
             Festgeldkonto,
             KfW_Kredit_Ende,
             Endwert])
        df[0].rename("Periode t", inplace=True)
        with pd.ExcelWriter( + save_name + str(counter) + "_.xlsx",
                            engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
            df_2.to_excel(writer, index=False, startcol=1)
        printing_VOFI.counter += 1
