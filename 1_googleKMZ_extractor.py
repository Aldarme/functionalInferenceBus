

import os
import shutil
import pathlib

VERBOS = 1




if __name__ == '__main__':

    # Directory folders
    inPath = "/media/Stock/Projets/Serge__optimo_DataAnalyses/1_Datas/1_Data_optimo(RTTB)_horiginals/Google_Suivi_Bus/"
    outPath = "/media/Stock/Projets/Serge__optimo_DataAnalyses/1_Datas/2_Data_optimo_rename/"


    # Directory listing

    list_YearDirectories = os.listdir(inPath)
    if VERBOS :
        print("**********************************")
        print("List of years directories: ")
        print("**********************************")
        print(list_YearDirectories)
        print("\r\n")

    if VERBOS:
        print("**********************************")
        print("Directories of day per years:")
        print("**********************************")
        print("\r\n")

    for year in list_YearDirectories:
        yearPath = inPath + year

        if VERBOS:
            print(yearPath)  #years folders
        list_dayFolder = os.listdir(yearPath)

        if VERBOS:
            print(list_dayFolder)   #day folders
            print("\r\n")

        for day in list_dayFolder:
            dayPath = yearPath +'/'+ day

            if VERBOS:
                print(dayPath)  # day folders
            list_files = os.listdir(dayPath)

            if VERBOS:
                print(list_files)  # files
                print("\r\n")

            #copy/paste file to output dir. and rename
            for file in list_files:
                #keep only kmz file
                if pathlib.Path(file).suffix == ".kmz":
                    #get file name
                    cFile_name, cFile_extension = os.path.splitext(file)

                    #keep only wanted kmz file
                    if not cFile_name.__contains__(day):
                        if not cFile_name.__contains__("Hanover"):
                        
                            #print(file)
                            #print(dayPath+'/'+file)
                            #print(outPath+file)

                            # copy the current file to output directory
                            origin = dayPath+'/'+file
                            dest = outPath+file
                            shutil.copyfile(origin, dest)

                            #rename file (in output directory), with format: "dayFolder_kmzNbr.kmz"
                            os.rename(outPath+file, outPath+day+'_'+file)
