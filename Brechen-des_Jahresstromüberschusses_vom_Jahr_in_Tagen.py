from Import_Libraries import *




df=pd.read_json("C:/users/soner/Desktop/Vid/tmy_47.598_9.551_2005_2020.json")
df_rel=pd.DataFrame(df["outputs"]["tmy_hourly"])
Global_radiation=df_rel["G(h)"].sum()
df_one=df_rel["G(h)"]/Global_radiation

Speicherkapazitaet=2003.2
df_new=pd.DataFrame(data=df_rel["time(UTC)"])
df_new=df_new.assign(Speicherkapaztiät_in_kWh=(df_one*Speicherkapazitaet))
plt.plot(df_new["Speicherkapaztiät_in_kWh"])
df_new["Uhrzeit_richtig"]=pd.to_datetime(df_new["time(UTC)"],format='%Y%m%d:%H%M')#%I:%M%p
df_new["Uhrzeit_richtig"].sort_values(ascending=True)

df_new["Stunde"]=df_new["Uhrzeit_richtig"].dt.strftime("%H")
df_new["Monat"]=df_new["Uhrzeit_richtig"].dt.strftime("%m")

df_new

#Januar
Januar=df_new[(df_new["Monat"] == "01")]
#Februar
Februar=df_new[(df_new["Monat"] == "02")]
#März
Maerz=df_new[(df_new["Monat"] == "03")]
#April
April=df_new[(df_new["Monat"] == "04")]
#Mai
Mai=df_new[(df_new["Monat"] == "05")]
#Juni
Juni=df_new[(df_new["Monat"] == "06")]
#Juli
Juli=df_new[(df_new["Monat"] == "07")]
#August
August=df_new[(df_new["Monat"] == "08")]
#September
September=df_new[(df_new["Monat"] == "09")]
#Oktober
Oktober=df_new[(df_new["Monat"] == "10")]
#November
November=df_new[(df_new["Monat"] == "11")]
#Dezember
Dezember=df_new[(df_new["Monat"] == "12")]


font = FontProperties()
font.set_name('Arial')

plt.figure(figsize=(124,24))
plt.rcParams.update({'font.size': 28})

plt.subplot(261,title="Monat: Januar")
plt.plot(Januar["Stunde"][0:24],Januar["Speicherkapaztiät_in_kWh"][0:24],label="Stromüberschuss")
plt.ylabel("Stromüberschuss in kWh")
plt.xlabel("Zeit in Stunden")

plt.subplot(262,title="Monat: Februar")
plt.plot(Februar["Stunde"][0:24],Februar["Speicherkapaztiät_in_kWh"][0:24],label="Stromüberschuss")
plt.ylabel("Stromüberschuss in kWh")
plt.xlabel("Zeit in Stunden")

plt.subplot(263,title="Monat: März")
plt.plot(Maerz["Stunde"][0:24],Maerz["Speicherkapaztiät_in_kWh"][0:24],label="Stromüberschuss")
plt.ylabel("Stromüberschuss in kWh")
plt.xlabel("Zeit in Stunden")

plt.subplot(264,title="Monat: April")
plt.plot(April["Stunde"][0:24],April["Speicherkapaztiät_in_kWh"][0:24],label="Stromüberschuss")
plt.ylabel("Stromüberschuss in kWh")
plt.xlabel("Zeit in Stunden")


plt.figure(figsize=(124,24))
plt.rcParams.update({'font.size': 28})

plt.subplot(271,title="Monat: Mai")
plt.plot(Mai["Stunde"][0:24],Mai["Speicherkapaztiät_in_kWh"][0:24],label="Stromüberschuss")


plt.subplot(272,title="Monat: Juni")
plt.plot(Juni["Stunde"][0:24],Juni["Speicherkapaztiät_in_kWh"][0:24],label="Stromüberschuss")


plt.subplot(273,title="Monat: Juli")
plt.plot(Juli["Stunde"][0:24],Juli["Speicherkapaztiät_in_kWh"][0:24],label="Stromüberschuss")


plt.subplot(274,title="Monat: August")
plt.plot(August["Stunde"][0:24],August["Speicherkapaztiät_in_kWh"][0:24],label="Stromüberschuss für einen Tag im Monat")


plt.figure(figsize=(124,24))
plt.rcParams.update({'font.size': 28})

plt.subplot(281,title="Monat: September")
plt.plot(September["Stunde"][0:24],September["Speicherkapaztiät_in_kWh"][0:24],label="Stromüberschuss für einen Tag im Monat")

plt.subplot(282,title="Monat: Oktober")
plt.plot(Oktober["Stunde"][0:24],Oktober["Speicherkapaztiät_in_kWh"][0:24],label="Stromüberschuss für einen Tag im Monat")


plt.subplot(283,title="Monat: November")
plt.plot(November["Stunde"][0:24],November["Speicherkapaztiät_in_kWh"][0:24],label="Stromüberschuss für einen Tag im Monat")

plt.subplot(284,title="Monat: Dezember")
plt.plot(Dezember["Stunde"][0:24],Dezember["Speicherkapaztiät_in_kWh"][0:24],label="Stromüberschuss für einen Tag im Monat")

plt.rcParams["legend.loc"]="lower right"
plt.legend()
