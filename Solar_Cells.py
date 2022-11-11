#import pvlib.pvsystem
'''

die grafische Visualisierung des Solarmoduls mit Temperaturverschiebung
-###- werden die wesentlichsten Begriffe kommentiert
'''

### laden der Bibliotheken
from Import_Libraries import *

#als funktion definiert ohne input oder output
def plot_Solar_cells():

    ###der der Solarmoduldaten aus der Datenbank
    CEC_Mod = pvlib.pvsystem.retrieve_sam("CECMod")
    ##umstellen der Daten als einen Typ: Dictionary
    parameters=dict(CEC_Mod["Aavid_Solar_ASMS_270P"])

    ###betrachte die Fälle Temperatur mit zum Beispiel Temperatur 65 °C mit 1000 W/m^2
    cases = [
        (1000, 25),
        (1000, 45),
        (1000, 65),
        (1000, 85),
    ]

    ###Beschreibe die Fälle
    conditions = pd.DataFrame(cases, columns=['Geff', 'Tcell'])

    ###weise die Daten zu und berechne die parameter
    IL, I0, Rs, Rsh, nNsVth = pvsystem.calcparams_desoto(
        conditions['Geff'],
        conditions['Tcell'],
        alpha_sc=parameters['alpha_sc'],
        a_ref=parameters['a_ref'],
        I_L_ref=parameters['I_L_ref'],
        I_o_ref=parameters['I_o_ref'],
        R_sh_ref=parameters['R_sh_ref'],
        R_s=parameters['R_s'],
        EgRef=1.121,
        dEgdT=-0.0002677
    )

    ### berechne ein solarzelle
    curve_info = pvsystem.singlediode(
        photocurrent=IL,
        saturation_current=I0,
        resistance_series=Rs,
        resistance_shunt=Rsh,
        nNsVth=nNsVth,
        ivcurve_pnts=250,
        method='lambertw'
    )


    ###erstelle ein leere Grafik
    plt.figure()

    ###weise die Eigenschaften zu und plotte
    for i, case in conditions.iterrows():
        label = (
            "$W_{eff}$ " + f"{case['Geff']} $W/m^2$\n"
            "$T_{cell}$ " + f"{case['Tcell']} $\\degree C$"
        )
        #plotte die grafik mit den daten
        plt.plot(curve_info['v'][i], curve_info['i'][i], label=label)
        v_mp = curve_info['v_mp'][i]
        i_mp = curve_info['i_mp'][i]
        plt.plot([v_mp], [i_mp], ls='', marker='o', c='k')
    plt.legend()
    plt.grid()
    ###achsten und titelbeschriften sowie ausgabe
    plt.xlabel('Spannung in $V$')
    plt.ylabel('Strom in $A$')
    plt.title('Verlaufskurve unterschiedlicher Temperaturen mit dem maximalen Arbeitspunkt \n  Firma Aavid Solar \n  Typ "PV Module ASMS-270P"')
    plt.show()

###main funktion für den Aufruf der Funktion
if __name__ == "__main__":

    plot_Solar_cells()