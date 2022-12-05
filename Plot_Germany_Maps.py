from Import_Libraries import *
#####-----------------------------Das Laden der Daten und Parameter für die grafische Visualisierung Anfang----------------------------------#######


path_1="/99_Sonstige_Rohdaten/"
path = "/99_Sonstige_Rohdaten/Global_Radiation_Germany_Monthly_Rohdaten/"
Liste ="/99_Sonstige_Rohdaten/Global_Radiation_Germany_Monthly_Rohdaten/"

folder_file = list()


###abfrage sollte die Datei nicht existieren dann werden die Rohdaten von DWD zusammengefasst
if not os.path.exists("/DWD_Deutschlandkarte/00_Auswertung/global_radiation_years.txt"):

    ###Liste die Dokumentnamen aus dem Ordner laufen und weise die auf einen Variablen zu
    for filename in os.listdir(path):
        folder_file.append(filename)


    ###entnahme der Inhalte aus der .txt Datei ab Zeile 28
    header_rows_information = 28
    header = {}

    row_iteration = 1
    ### zuweisung der Daten auf eine Variable
    start_point = 22
    with open(path + folder_file[0], 'rt') as files:
        for line in files:
            if row_iteration > start_point:
                if row_iteration < header_rows_information:
                    line = line.split(" ", 1)
                    header[line[0]] = float(line[1])
                else:
                    break
            row_iteration = row_iteration + 1


    ### Berechnung der einzelnen Pixel
    left = header['XLLCORNER']
    right = header['XLLCORNER'] + header['NCOLS'] * header['CELLSIZE']
    bottom = header['YLLCORNER']
    top = header['YLLCORNER'] + header['NROWS'] * header['CELLSIZE']
    map_extent = (left, right, bottom, top)

    ####Speichern der Auswertungen auf eine txt. Datei

    mean_global_radiation = (np.loadtxt(path + folder_file[0], skiprows=header_rows_information)) * 0
    Jan, Feb, Mar, Apr, Mai, Jun, Jul, Aug, Sep, Okt, Nov, Dez = [], [], [], [], [], [], [], [], [], [], [], []
    years_global_rad, years_global_radiation_with_nan = [], []
    global_radiation = (np.loadtxt(path + folder_file[0], skiprows=header_rows_information)) * 0

    for i in tqdm(range(0, len(folder_file))):


        ### Da -999 in den Daten enthalten sind, und diese das Farbschema verzerren, werden diese rausgefiltert mit nan werten (not available number)

        years_global_rad_tmp = (
            np.loadtxt(path + folder_file[i], skiprows=header_rows_information))  # laden eines Satzes aus einem Monat
        years_global_rad_tmp = np.where(np.array(years_global_rad_tmp) == -999, np.nan,
                                        np.array(years_global_rad_tmp))  # umwandeln der Daten von -999 in nan
        global_radiation = years_global_rad_tmp + global_radiation  # aufzählen der zahlen

        if int((folder_file[i].split("_")[-1].split(".")[0])[-2] + (folder_file[i].split("_")[-1].split(".")[0])[
            -1]) == 12:
            years_global_radiation_with_nan.append(
                global_radiation)  # zuweisen auf die variable noch kein Durchschnittswert gebildet sondern nur aufsummiert
            global_radiation = (np.loadtxt(path + folder_file[0],
                                           skiprows=header_rows_information)) * 0  # zurücksetzen der Jährlichen Daten


        ### speichern der Daten in Monaten zwischen 1991 bis 2021

        if int((folder_file[i].split("_")[-1].split(".")[0])[-2] + (folder_file[i].split("_")[-1].split(".")[0])[
            -1]) == 1:
            Jan.append(np.loadtxt(path + folder_file[i], skiprows=header_rows_information))

        if int((folder_file[i].split("_")[-1].split(".")[0])[-2] + (folder_file[i].split("_")[-1].split(".")[0])[
            -1]) == 2:
            Feb.append(np.loadtxt(path + folder_file[i], skiprows=header_rows_information))

        if int((folder_file[i].split("_")[-1].split(".")[0])[-2] + (folder_file[i].split("_")[-1].split(".")[0])[
            -1]) == 3:
            Mar.append(np.loadtxt(path + folder_file[i], skiprows=header_rows_information))

        if int((folder_file[i].split("_")[-1].split(".")[0])[-2] + (folder_file[i].split("_")[-1].split(".")[0])[
            -1]) == 4:
            Apr.append(np.loadtxt(path + folder_file[i], skiprows=header_rows_information))

        if int((folder_file[i].split("_")[-1].split(".")[0])[-2] + (folder_file[i].split("_")[-1].split(".")[0])[
            -1]) == 5:
            Mai.append(np.loadtxt(path + folder_file[i], skiprows=header_rows_information))

        if int((folder_file[i].split("_")[-1].split(".")[0])[-2] + (folder_file[i].split("_")[-1].split(".")[0])[
            -1]) == 6:
            Jun.append(np.loadtxt(path + folder_file[i], skiprows=header_rows_information))

        if int((folder_file[i].split("_")[-1].split(".")[0])[-2] + (folder_file[i].split("_")[-1].split(".")[0])[
            -1]) == 7:
            Jul.append(np.loadtxt(path + folder_file[i], skiprows=header_rows_information))

        if int((folder_file[i].split("_")[-1].split(".")[0])[-2] + (folder_file[i].split("_")[-1].split(".")[0])[
            -1]) == 8:
            Aug.append(np.loadtxt(path + folder_file[i], skiprows=header_rows_information))

        if int((folder_file[i].split("_")[-1].split(".")[0])[-2] + (folder_file[i].split("_")[-1].split(".")[0])[
            -1]) == 9:
            Sep.append(np.loadtxt(path + folder_file[i], skiprows=header_rows_information))

        if int((folder_file[i].split("_")[-1].split(".")[0])[-2] + (folder_file[i].split("_")[-1].split(".")[0])[
            -1]) == 10:
            Okt.append(np.loadtxt(path + folder_file[i], skiprows=header_rows_information))

        if int((folder_file[i].split("_")[-1].split(".")[0])[-2] + (folder_file[i].split("_")[-1].split(".")[0])[
            -1]) == 11:
            Nov.append(np.loadtxt(path + folder_file[i], skiprows=header_rows_information))

        if int((folder_file[i].split("_")[-1].split(".")[0])[-2] + (folder_file[i].split("_")[-1].split(".")[0])[
            -1]) == 12:
            Dez.append(np.loadtxt(path + folder_file[i], skiprows=header_rows_information))



    ### Gleiche umwandlung wie oben
    Dez = np.where(np.array(Dez) == -999, np.nan, np.array(Dez))
    Nov = np.where(np.array(Nov) == -999, np.nan, np.array(Nov))
    Okt = np.where(np.array(Okt) == -999, np.nan, np.array(Okt))
    Sep = np.where(np.array(Sep) == -999, np.nan, np.array(Sep))
    Aug = np.where(np.array(Aug) == -999, np.nan, np.array(Aug))
    Jul = np.where(np.array(Jul) == -999, np.nan, np.array(Jul))
    Jun = np.where(np.array(Jun) == -999, np.nan, np.array(Jun))
    Mai = np.where(np.array(Mai) == -999, np.nan, np.array(Mai))
    Apr = np.where(np.array(Apr) == -999, np.nan, np.array(Apr))
    Mar = np.where(np.array(Mar) == -999, np.nan, np.array(Mar))
    Feb = np.where(np.array(Feb) == -999, np.nan, np.array(Feb))
    Jan = np.where(np.array(Jan) == -999, np.nan, np.array(Jan))

    # Variablen Sichern und zwar binär, damit die dateien nicht so groß sind
    var_save = open(path_1 + "/00_Auswertung/" + "global_radiation_years.txt", "wb")
    pickle.dump(years_global_radiation_with_nan, var_save)
    var_save.close()

    var_save = open(path_1 + "/00_Auswertung/" + "Januar_30_Jahre.txt", "wb")
    pickle.dump(Jan, var_save)
    var_save.close()
    var_save = open(path_1 + "/00_Auswertung/" + "Feb_30_Jahre.txt", "wb")
    pickle.dump(Feb, var_save)
    var_save.close()
    var_save = open(path_1 + "/00_Auswertung/" + "März_30_Jahre.txt", "wb")
    pickle.dump(Mar, var_save)
    var_save.close()
    var_save = open(path_1 + "/00_Auswertung/" + "April_30_Jahre.txt", "wb")
    pickle.dump(Apr, var_save)
    var_save.close()
    var_save = open(path_1 + "/00_Auswertung/" + "Mai_30_Jahre.txt", "wb")
    pickle.dump(Mai, var_save)
    var_save.close()
    var_save = open(path_1 + "/00_Auswertung/" + "Juni_30_Jahre.txt", "wb")
    pickle.dump(Jun, var_save)
    var_save.close()
    var_save = open(path_1 + "/00_Auswertung/" + "Juli_30_Jahre.txt", "wb")
    pickle.dump(Jul, var_save)
    var_save.close()
    var_save = open(path_1 + "/00_Auswertung/" + "August_30_Jahre.txt", "wb")
    pickle.dump(Aug, var_save)
    var_save.close()
    var_save = open(path_1 + "/00_Auswertung/" + "September_30_Jahre.txt", "wb")
    pickle.dump(Sep, var_save)
    var_save.close()
    var_save = open(path_1 + "/00_Auswertung/" + "Oktober_30_Jahre.txt", "wb")
    pickle.dump(Okt, var_save)
    var_save.close()
    var_save = open(path_1 + "/00_Auswertung/" + "November_30_Jahre.txt", "wb")
    pickle.dump(Nov, var_save)
    var_save.close()
    var_save = open(path_1 + "/00_Auswertung/" + "Dezember_30_Jahre.txt", "wb")
    pickle.dump(Dez, var_save)
    var_save.close()


else:
    ##laden der Dateien von Januar bis Dezember aus den obigen Berechnungen und sicherungen sollten die bereits existieren

    for filename in os.listdir(Liste):
   #     i = i + 1
        folder_file.append(filename)

    header_rows_information = 28
    header = {}
    row_iteration = 1
    start_point = 22
    with open(Liste + folder_file[0], 'rt') as files:
        for line in files:
            if row_iteration > start_point:
                if row_iteration < header_rows_information:
                    line = line.split(" ", 1)
                    header[line[0]] = float(line[1])
                else:
                    break
            row_iteration = row_iteration + 1

    left = header['XLLCORNER']
    right = header['XLLCORNER'] + header['NCOLS'] * header['CELLSIZE']
    bottom = header['YLLCORNER']
    top = header['YLLCORNER'] + header['NROWS'] * header['CELLSIZE']
    map_extent = (left, right, bottom, top)

file = open("/00_Auswertung/global_radiation_years.txt", 'rb')
years_global_rad = pickle.load(file)
file.close()

file = open("/00_Auswertung/Januar_30_Jahre.txt", 'rb')
Januar = pickle.load(file)
file.close()
file = open("/00_Auswertung/Feb_30_Jahre.txt", 'rb')
Februar = pickle.load(file)
file.close()
file = open("/00_Auswertung/März_30_Jahre.txt", 'rb')
Maerz = pickle.load(file)
file.close()
file = open("/00_Auswertung/April_30_Jahre.txt", 'rb')
April = pickle.load(file)
file.close()
file = open("/00_Auswertung/Mai_30_Jahre.txt", 'rb')
Mai = pickle.load(file)
file.close()
file = open("/00_Auswertung/Juni_30_Jahre.txt", 'rb')
Juni = pickle.load(file)
file.close()
file = open("/00_Auswertung/Juli_30_Jahre.txt", 'rb')
Juli = pickle.load(file)
file.close()
file = open("/00_Auswertung/August_30_Jahre.txt", 'rb')
August = pickle.load(file)
file.close()
file = open("/00_Auswertung/September_30_Jahre.txt", 'rb')
September = pickle.load(file)
file.close()
file = open("/00_Auswertung/Oktober_30_Jahre.txt", 'rb')
Oktober = pickle.load(file)
file.close()
file = open("/00_Auswertung/November_30_Jahre.txt", 'rb')
November = pickle.load(file)
file.close()
file = open("/00_Auswertung/Dezember_30_Jahre.txt", 'rb')
Dezember = pickle.load(file)
file.close()
#####-----------------------------Das Laden der Daten und Parameter für die grafische Visualisierung Ende----------------------------------#######




mean_radiation_in_years = years_global_rad * 0
sum_years=years_global_rad[0]*0
for i in range(np.shape(years_global_rad)[0]):
    mean_radiation_in_years.append(years_global_rad[
                                       i] / 12)  # (np.shape(years_global_rad))[0])#jährlich durchschnittlicher Wert da oben nicht aufsummiert hätte durch 12 teilen müssen da oben summe in jahren
    sum_years=years_global_rad[i]+sum_years

##mittlere Jahressumme
mean_sum_years=sum_years/np.shape(years_global_rad)[0]

#df=pd.read_csv("C:/Users/soner/Desktop/Mappe1.csv",sep=";")


########################################################Grafische Darlegung der Deutschlandkarte#########################################
plt.figure()
#plt.scatter(df["Latitude"],df["Longitude"])
plt.imshow(mean_sum_years, extent=map_extent)
clb=plt.colorbar()
clb.ax.set_title("$ \mathrm{Wh/m^2}$")
plt.set_cmap('jet')
plt.axis(False)
plt.title("Mittlere Jahressumme der Globalstrahlung"+"\n"+"in Deutschland zwischen 1991-2021")

plt.show()

########################################################Grafische Darlegung der Deutschlandkarte#########################################
