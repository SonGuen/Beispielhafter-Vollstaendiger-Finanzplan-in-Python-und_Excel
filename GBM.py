


'''
Das Verfahren für die geometrisches brownsches Verfahren
-###- beschreibt die wichtigsten Funktionen
### Die unten angewendete Funtion ist auch im VOFI.py enthalten
'''


###laden der Bibliotheken udn dem VOFI wo das geometrische brownsche Verfahren hinterlegt ist
from Import_Libraries import *
from VOFI import Monte_Carlo_GBM as Monte_Carlo_GBM



##################-------Was wäre wenn t=1/2 ist siehe Kapitel 5 Zahlungsströme-------------------------------##################


###lese die Daten des Strompreises
df = pd.read_excel("./99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Energiepreis/preis_test.xlsx")

dt = 1 / 2
###Bestimme den diskreten Zeitschritt
P_0 = df.loc[len(df) - 1, "Strompreis"]


###Ermittlung der durchschnittliche Wachstumsrate --Beginn

Wachstumsrate = df.iloc[-1]["Strompreis"] / df.iloc[0]["Strompreis"]
Dauer = len(df["Strompreis"])

Durchschnittliche_Wachstumsrate = (Wachstumsrate ** (1 / Dauer) - 1)
####Ermittlung der durchschnittliche Wachstumsrate --Ende



###Ermittlung der Volatilität --Beginn
df["Preisdifferenz"] = 0.0

for i in range(len(df["Preisdifferenz"]) - 1):
    df.loc[i, "Preisdifferenz"] = df.loc[(i), "Strompreis"] / df.loc[(i + 1), "Strompreis"]

Vola = df["Preisdifferenz"].std()
###Ermittlung der Volatilität --Ende




###Definiere die Parameter S_T ist irrelevant,
S_T = []
Q_T = []


###definiere die Anzahl der Durchläufe und den Zeitraum
runs = 20 * 10 ** 3
Zeitraum = 43  # FÜr 20 Jahren da t=1/2 --> 20 Jahre sowie ein halbes Jahr für ende 2022, da der Start anfang 2023
### stattfindet wurde der erste Strompreis ende 2023 herangezogen, -->daher die 43 Perioden

### Dient der Wiederholbarkeit der Simulation mit gleichen Ergebnissen, Zufallsgenerator des Rechners fixiert sich dabei
### Die Zahl 42 begründet sich nach den Sinn des Lebens
np.random.seed(42)


### Durchlauf des geometrisch brownschen Bewegung und ZUweisung des Parameters
Q_T = Monte_Carlo_GBM(Zeitraum, S_T, dt, P_0, Durchschnittliche_Wachstumsrate, runs)
### Transporniert die Matrix für die grafische Darstellung
Q_T = pd.DataFrame(data=np.transpose(Q_T))




###  Grafische Darstellung der Auswertung ------Beginn
plt.figure(figsize=(17, 10))
plt.title("Allgemeiner geometrische Brownsche Bewegung \n mit 6 Szenarien und dem Mittelwert mit $t=1$")
plt.ylabel("Energiepreis $p_t$")
plt.xlabel("Jahre $t$")


date_range = pd.date_range(start='2022-06-30', end='2043-12-31', freq='6M')###definieren der Zeitachse jährlich
date_range_half = pd.date_range(start='2022-06-30', end='2043-12-31', freq='2Y')###definieren der Zeitachse jährlich

lines = []

###Entnahme der ersten sechs Szenarien
for i in range(np.shape(Q_T)[0]):
    lines += plt.plot(date_range, Q_T[:][i], "#B590BF", linestyle=":")
    if i == 5:
        break

###Ermittlung des Mittelwerts sowie Standardabweichung und Varianz der jeweiligen Simulationsläufe
Q_T = pd.DataFrame(data=np.transpose(Q_T))
Q_T = Q_T.assign(mean=Q_T.mean(axis=1))
Q_T = Q_T.assign(std=Q_T.std(axis=1))
Q_T = Q_T.assign(var=Q_T.var(axis=1))


###Plotten der Standardabweichung sowie des Mittelwertes
line_P, = plt.plot(date_range, Q_T["mean"] + Q_T["std"], "#8B8787")
line_M, = plt.plot(date_range, Q_T["mean"] - Q_T["std"], "#8B8787")
line_m, = plt.plot(date_range, Q_T["mean"], "#978181")

###Füllen der grau schraffierten Fläche
line_stabwa = plt.fill_between(date_range, Q_T["mean"] - Q_T["std"], Q_T["mean"] + Q_T["std"], facecolor="#E2DCDC")


####legende Beschreiben
plt.legend([lines[0], lines[1], lines[2], lines[3], lines[4], lines[5], line_P, line_m], \
           ["Szenario 1", "Szenario 2", "Szenario 3", "Szenario 4", "Szenario 5", "Szenario 6", "Standardabweichung",
            "Mittelwert"], \
           loc='upper left', frameon=False)

###Plotten der Grafik
plt.grid()
plt.xticks(date_range_half)
plt.show()
###  Grafische Darstellung der Auswertung ------Ende


#####---------------------Die Beschreibungen gelten auch für das untere Funktionsbaustein gilt für unten----------------------#############################
##################-------Was wäre wenn t=1 ist siehe Kapitel 5 Zahlungsströme-------------------------------##################



df = pd.read_excel("./99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Energiepreis/preis_test - Kopie.xlsx")

dt = 1

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

plt.figure(figsize=(17, 10))
plt.title("Allgemeiner geometrische Brownsche Bewegung \n mit 6 Szenarien und dem Mittelwert mit $t=1$")
plt.ylabel("Energiepreis $p_t$")
plt.xlabel("Jahre $t$")

# date_range=pd.to_datetime(pd.DataFrame([df.loc[len(df["Jahr"])-1,"Jahr"]+i for i in range(len(Q_T[:][0]))])[0],format="%Y")
date_range = pd.date_range(start='2022-06-30', end='2043-12-31', freq='6M')
date_range_half = pd.date_range(start='2022-06-30', end='2043-12-31', freq='2Y')

lines = []

for i in range(np.shape(Q_T)[0]):

    lines += plt.plot(date_range, Q_T[:][i], "#B590BF", linestyle=":")
    if i == 5:
        break

Q_T = pd.DataFrame(data=np.transpose(Q_T))
Q_T = Q_T.assign(mean=Q_T.mean(axis=1))
Q_T = Q_T.assign(std=Q_T.std(axis=1))
Q_T = Q_T.assign(var=Q_T.var(axis=1))

line_P, = plt.plot(date_range, Q_T["mean"] + Q_T["std"], "#8B8787")
line_M, = plt.plot(date_range, Q_T["mean"] - Q_T["std"], "#8B8787")
line_m, = plt.plot(date_range, Q_T["mean"], "#978181")
line_stabwa = plt.fill_between(date_range, Q_T["mean"] - Q_T["std"], Q_T["mean"] + Q_T["std"], facecolor="#E2DCDC")



plt.legend([lines[0], lines[1], lines[2], lines[3], lines[4], lines[5], line_P, line_m], \
           ["Szenario 1", "Szenario 2", "Szenario 3", "Szenario 4", "Szenario 5", "Szenario 6", "Standardabweichung",
            "Mittelwert"], \
           loc='upper left', frameon=False)
plt.grid()
plt.xticks(date_range_half)
plt.show()

