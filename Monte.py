import time
import locale #für die Währung aus dem Plot für die Häufigkeitsverteilung

import matplotlib.pyplot as plt
from Import_Libraries import *
import seaborn as sns


def Erwartungswert(werte, Gewichtungen):
    werte = np.asarray(werte)
    Gewichtungen = np.asarray(Gewichtungen)
    return (werte * Gewichtungen).sum() / Gewichtungen.sum()

font = FontProperties()
font.set_name('Times New Roman')


def compute_histogram_bins(data, desired_bin_size):###Funktion für die erstellung der Spannweite
    min_val = np.min(data)
    max_val = np.max(data)
    min_boundary = -1.0 * (min_val % desired_bin_size - min_val)
    max_boundary = max_val - max_val % desired_bin_size + desired_bin_size
    n_bins = int((max_boundary - min_boundary) / desired_bin_size) + 1
    bins = np.linspace(min_boundary, max_boundary, n_bins)
    return bins


file="C:/Users/soner/OneDrive/04_Masterarbeit/99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Szenario_II_2_Monte_Carlo.csv"
file="C:/Users/soner/Desktop/Szenario_II_2_Monte_Carlo.csv"

df=pd.DataFrame(np.array((pd.read_csv(file))))

df_2_Endwert=pd.DataFrame()
df_2_Endwert["Endwert in €"]=df[20]

locale.setlocale( locale.LC_ALL, '')


wunsch=1000

ax=sns.histplot(data=df_2_Endwert["Endwert in €"],bins=compute_histogram_bins(df_2_Endwert["Endwert in €"],wunsch),kde=True,color="grey",label="Häufigkeiten mit einer Spannweite von 1.000 €")


x,y=np.histogram(df_2_Endwert["Endwert in €"],bins=compute_histogram_bins(df_2_Endwert["Endwert in €"],1000))
wahrscheinlichkeiten=np.float64(x/np.sum(x))


ax.axvline(10289.16, color='red', linestyle="-", label='Basisszenario {}'.format(locale.currency(10289.16)), linewidth=2)
plt.xticks(compute_histogram_bins(df_2_Endwert["Endwert in €"],10000*5),fontsize=12)



###zweite y achse (in Excel heißt es sekundärdarstellung...)
ax2=plt.twinx()
ax2=sns.ecdfplot(data=df_2_Endwert["Endwert in €"],ax=ax2)
ax2.set_ylabel('Wahrscheinlichkeit',fontsize=12)


plt.xlabel("Endwert in €",fontsize=12)
ax.set_ylabel("Häufigkeit",fontsize=12)
plt.title("Häufigkeitsverteilung von Szenario II (2)",fontsize=16)
ax.legend(loc="upper right",fontsize=12)

print(locale.currency(Erwartungswert(np.delete(y, np.where(y==0)),wahrscheinlichkeiten)))
#plt.savefig("C:/Users/soner/Desktop/Szenario_II_2_Monte_Calo.png",dpi=750)
plt.show()


#################################--------------------------------------------------------------------------###############
file="C:/Users/soner/OneDrive/04_Masterarbeit/99_Abgabe_Masterarbeit_Soner_Günaydin/00_Wirtschaftliche_Auswertung/Szenario_II_1_Monte_Carlo.csv"
file="C:/Users/soner/Desktop/Szenario_II_1_Monte_Carlo.csv"


df=pd.DataFrame(np.array((pd.read_csv(file))))

df_2_Endwert=pd.DataFrame()
df_2_Endwert["Endwert in €"]=df[20]

locale.setlocale( locale.LC_ALL, '')



wunsch=1000

ax=sns.histplot(data=df_2_Endwert["Endwert in €"],bins=compute_histogram_bins(df_2_Endwert["Endwert in €"],wunsch),kde=True,color="grey",label="Häufigkeiten mit einer Spannweite von 1.000 €")#7500


ax.axvline(23742.42, color='r', linestyle="-", label='Basisszenario {}'.format(locale.currency(23742.42)), linewidth=2)
plt.xticks(compute_histogram_bins(df_2_Endwert["Endwert in €"],10000*5),fontsize=12)


ax2=plt.twinx()
ax2=sns.ecdfplot(data=df_2_Endwert["Endwert in €"],ax=ax2)
ax2.set_ylabel('Wahrscheinlichkeit',fontsize=12)

plt.xlabel("Endwert in €",fontsize=12)
ax.set_ylabel("Häufigkeit",fontsize=12)
plt.title("Häufigkeitsverteilung von Szenario II (1)",fontsize=16)
ax.legend(loc="upper right",fontsize=12)


#plt.savefig("C:/Users/soner/Desktop/Szenario_II_1_Monte_Calo.png",dpi=750)
plt.show()



x,y=np.histogram(df_2_Endwert["Endwert in €"],bins=compute_histogram_bins(df_2_Endwert["Endwert in €"],1000))
wahrscheinlichkeiten=np.float64(x/np.sum(x))
print(Erwartungswert(np.delete(y, np.where(y==0)),wahrscheinlichkeiten))



####Sollzins_KfW_Monte=[]
##for i in range(0,runs):Sollzins_KfW_Monte.append(np.random.triangular(0.0465,0.0538,0.1143))#np.random.uniform(0.0465,0.1143,runs) <--effizinetere alternative
##pd.DataFrame(Sollzins_KfW_Monte).to_csv("C:/Users/soner/Desktop/Sollzins_KfW_Monte_Triangular.csv")
####