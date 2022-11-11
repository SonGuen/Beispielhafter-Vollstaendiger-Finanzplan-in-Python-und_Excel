from Import_Libraries import *

####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
'''
Achtung diese 3dimensionale Betrachtung des Strompreises über die Nutzungsdauer funktioniert ausschließliich über 
Jupiter aufgrund des Befehls -->% matplotlib notebook für die Interaktion der Grafik auf der Oberfläche
Diese Datei stellt die 3 dimensionale Abbildung des Strompreises mit dem Endwert sowie der Nutzungsdauer dar.
Da die unten aufgeführten Befehle ausschließlich der grafischen Visualisierung dienen wird nicht vertieft darauf eingegangen. 

'''
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################


df_Strompreis_up = pd.read_excel("C:/Users/soner/OneDrive/04_Masterarbeit/99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Variation_Strompreis.xlsx",sheet_name="Tabelle2")
df_Strompreis_down = pd.read_excel("C:/Users/soner/OneDrive/04_Masterarbeit/99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Variation_Strompreis.xlsx",sheet_name="Tabelle3")
#laden des Strompreises


### Erstellen einer leeren Abbildung mit Times New Roman und einer automatischen Größeneinstellung

#% matplotlib notebook
fig = plt.figure(figsize=(16, 8))
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
plt.rcParams["font.family"] = "Times New Roman"


### Erzuege ein leeres 3D Diagramm und füge die Daten des Strompreises ein.--> Markerie im Anschluss diese mit einem * bzw. einen Punkt.
### Spalte 1 bezeichnet die Nutzungsdauer
ax = fig.add_subplot(projection='3d')
ax.scatter(df_Strompreis_up["Spalte1"],
           df_Strompreis_up["Strompreis up"],
           df_Strompreis_up["Oberer Bereich Szenario II (1)"],
           color="#A42828", marker='o', label="Szenario II (1) Strompreis oberer Bereich in €/kWh")
ax.scatter(df_Strompreis_up["Spalte1"],
           df_Strompreis_up["Strompreis up"],
           df_Strompreis_up["Oberer Bereich Szenario II (2)"],
           color="#9F2525", marker='*', label="Szenario II (2) Strompreis oberer Bereich in €/kWh")

ax.scatter(df_Strompreis_down["Spalte1"],
           df_Strompreis_down["Strompreis down"],
           df_Strompreis_down["Unterer Bereich Szenario II (1)"],
           color="#3D9AD8", marker='o', label="Szenario II (1) Strompreis unterer Bereich in €/kWh")

ax.scatter(df_Strompreis_down["Spalte1"],
           df_Strompreis_down["Strompreis down"],
           df_Strompreis_down["Unterer Bereich Szenario II (2)"],
           color="#7696AC", marker='*', label="Szenario II (2) Strompreis unterer Bereich in €/kWh")

# ax.title("Obere und untere Bereich des Strompreises für die jeweilige Perioden")
### Definiere die X Achse genauer, somit kann die automatische Skalierung von Matplotlib aufgehoben werden
ax.xaxis.set_ticks(np.arange(0, 21, 1))


###Definiere die Achsen sowie die Datenbeschriftungen
ax.set_xlabel("Periode t")
ax.set_ylabel("Strompreis in €/kWh")
ax.set_zlabel("Bestandssalden sowie der Endwert bei t=20")
ax.set_title("Obere und untere Bereich des Strompreises für die jeweilige Periode",fontsize=18)
plt.legend(loc="upper left")

plt.show()
#plt.savefig('plot.png', dpi=750)