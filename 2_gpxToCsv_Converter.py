#########################################################################
#
# This file have to extract few data from given GPX file to aggregate them
# into a CSV file.
#
# GPX file are obtain, Thanks a webScrapper: AltScrapper, that convert
# KMZ (google file) into GPX file. After that, the google ELEVATION API
# is used to add the missing information of elevation to each GPS point.
# Then, those GPX file are used to be grabed and only extract wanted
# informations to create a usable csv file.
#########################################################################


import os
import xml.etree.ElementTree as ET
import csv
from time import perf_counter
from time import sleep

#Storing directory
directory = "/home/promet/Documents/optimo/1_Data_optimo_gpx/"

#time
#timeList = []

#List all gpx files
inputFiles = sorted( filter( lambda x: os.path.isfile(os.path.join(directory, x)), os.listdir(directory) ) )
outputFiles = []
for file in inputFiles:
    outputFiles.append(file.split('.')[0]  + '.csv') #create list of futur csv files

nbrOfFiles = len(inputFiles)

#For each file
for i in range(0, len(inputFiles)):

    #Analyse time performance
    #timeInit = perf_counter()

    #verbose
    print(inputFiles[i], "file {}/{}".format(i, nbrOfFiles))

    try:

        #Read gpx file as XML files
        xmlparse = ET.parse(directory+inputFiles[i])    # Pass the path of the xml document
        root = xmlparse.getroot()                           # get the parent tag
        root.attrib                                         # get the tags attributes

    except:
        print("#######################ERROR Parsing XML#######################")
        continue


    #xml needed informations
    cols = ["line", "state", "date", "hour", "latitude", "longitude", "elevation", "lastStop", "destination", "early", "late"]
    rows = []

    try:

        #access waipoint information from xml file
        for wpt in root:
            wpt_attrib = wpt.attrib     #dict of wpt marker: Latitude & Longitude
            row = []

            for j in wpt:
                row.append(j.text)     #list[3] of wpt marker: elevation, name, description

            if len(row) < 3:
                continue

            stgList = row[2].split("<br/>")


            #kill exeption file
            exceptKeyword = ["Véhicule sans SAE."]

            if len(stgList) > 1:                                #len(stgList) = 1, containing URL
                if exceptKeyword[0] in stgList:
                    continue

            #print(stgList)
            #create list of variable containing selected datas
            line_v = stgList[4][8:]
            etat_v = stgList[2][7:]
            date_v = stgList[0][7:]
            hour_v = stgList[1][8:]
            lat_v = wpt_attrib["lat"]
            long_v = wpt_attrib["lon"]
            ele_v = row[0]
            lastStop_v = stgList[6][16:]
            nextStop_v = stgList[5][14:]

            time = stgList[10].split(":")
            if len(time[1]) == 7:
                time[1] = time[1][1:2] + "." + time[1][-2:]
            if len(time[1]) == 7:
                time[1] = time[1][1:3] + "." + time[1][-2:]

            if time[0] == "Avance ":
                avance_v = time[1][0:]
                retard_v = 0.0
            if time[0] == "Retard ":
                retard_v = time[1][0:]
                avance_v = 0.0

            #create a list containing wanted informations
            row = [ line_v,
                    etat_v,
                    date_v,
                    hour_v,
                    lat_v,
                    long_v,
                    ele_v,
                    lastStop_v,
                    nextStop_v,
                    avance_v,
                    retard_v
                    ]

            #insert current row
            rows.append(row)

        #Write CSV file with datas of the current file

        #file name
        filename = "/home/promet/Documents/optimo/csv_data/" + outputFiles[i]

        #write the csv file
        with open(filename, 'w') as csvfile:
            csvWriter = csv.writer(csvfile)
            csvWriter.writerow(cols)
            csvWriter.writerows(rows)

        #Analyse time performance
    #    timeEnd = perf_counter()

    #    timeList.append(timeEnd - timeInit)

    #print(timeList)

    except:
        print("#####################AN ERROR OCCUR###################")
        print(stgList)
        print(row)
