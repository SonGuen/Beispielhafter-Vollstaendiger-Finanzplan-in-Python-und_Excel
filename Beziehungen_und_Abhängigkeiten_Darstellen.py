from Import_Libraries import *

####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
'''
Diese Datei stellt die grafische Visualisierung der beziehungen aus dem multivariaten Fall zusammen.

'''
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################




### Laden der Dateien

file="C:/Users/soner/Desktop/Szenario_II_1_Monte_Carlo.csv"

df=pd.DataFrame(np.array((pd.read_csv(file))))

df_2_Endwert=pd.DataFrame()
df_2_Endwert["Endwert in €"]=df[20]

file_degradation="C:/Users/soner/OneDrive/04_Masterarbeit/99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Verteilung/Degradation_Monte.csv"
df_degredation=pd.read_csv(file_degradation)

file_Anschaffungsauszahlung="C:/Users/soner/OneDrive/04_Masterarbeit/99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Verteilung/Anschaffungsauszahlung_Monte.csv"
df_Anschaffungsauszahlung=pd.read_csv(file_Anschaffungsauszahlung)

file_Batteriepreis="C:/Users/soner/OneDrive/04_Masterarbeit/99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Verteilung/Batteriepreis_Monte.csv"
df_Batteriepreis=pd.read_csv(file_Batteriepreis)

file_Batteriepreissenkung="C:/Users/soner/OneDrive/04_Masterarbeit/99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Verteilung/Batteriepreissenkung_Monte.csv"
df_Batteriepreissenkung=pd.read_csv(file_Batteriepreissenkung)


file_Fremdkapitalzinssatz="C:/Users/soner/OneDrive/04_Masterarbeit/99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Verteilung/Fremdkapitalzinssatz_Monte_Bank.csv"
df_Fremdkapitalzinssatz=pd.read_csv(file_Fremdkapitalzinssatz)

file_Habenzinssatz="C:/Users/soner/OneDrive/04_Masterarbeit/99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Verteilung/Habenzinssatz_Monte.csv"
df_Habenzinssatz=pd.read_csv(file_Habenzinssatz)

file_Laufende_Auszahlung="C:/Users/soner/OneDrive/04_Masterarbeit/99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Verteilung/Laufende_Auszahlung_Monte.csv"
df_Laufende_Auszahlung=pd.read_csv(file_Laufende_Auszahlung)

file_Sollzins_KfW="C:/Users/soner/OneDrive/04_Masterarbeit/99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Verteilung/Sollzins_KfW_Monte.csv"
df_Sollzins_KfW=pd.read_csv(file_Sollzins_KfW)

file_Strompreis_1000000="C:/Users/soner/OneDrive/04_Masterarbeit//99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Verteilung/Strompreis_1000000.csv"
df_Strompreis_1000000=pd.read_csv(file_Strompreis_1000000)



### Zuweisen der Variablen auf eines
df_ONE = pd.DataFrame([df_2_Endwert["Endwert in €"][0:500],
                       df_degredation["0"][0:500],
                       df_Anschaffungsauszahlung["0"][0:500],
                       df_Batteriepreis["0"][0:500],
                       df_Batteriepreissenkung["0"][0:500],
                       df_Fremdkapitalzinssatz["0"][0:500],
                       df_Habenzinssatz["0"][0:500],
                       df_Laufende_Auszahlung["0"][0:500],
                       df_Sollzins_KfW["0"][0:500]]
                      )

df_ONE = df_ONE.reset_index()
df_ONE = df_ONE.transpose()
df_ONE = df_ONE.drop("index", axis=0)

A = df_Strompreis_1000000.drop("Unnamed: 0", axis=1).transpose().mean(axis=1)[0:500]
A = pd.DataFrame(A)[0].rename(9)
df_ONE = pd.concat([df_ONE.reset_index(), A.reset_index()], axis=1).drop("index", axis=1)
# df_Strompreis_1000000.drop("Unnamed: 0",axis=1).transpose().mean(axis=0)]

dict = {0: 'Endwert in €',
        1: 'Degradation in %',
        2: 'Anschaffungsauszahlung in €/kWp',
        3: 'Batteriepreis in €/kWp',
        4: 'Senkung der Anschaffung des Batteriepreises in %',
        5: 'Fremdkapitalzinssatz in %',
        6: 'Habenzinssatz in %',
        7: 'Laufende Auszahlung in €/kWp',
        8: 'Sollzinssatz vom KfW Kredit in %',
        9: 'Strompreis in €/kWh'}

# call rename () method
df_ONE.rename(columns=dict,
              inplace=True)
print(df_ONE.head())

###plotten der Datei
sns.pairplot(df_ONE)
g.fig.suptitle("Beziehungen aus den einzelnen Faktoren aus dem Multivariaten Fall", y=1.08)