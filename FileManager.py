from os import listdir
import os
import re


import pandas as pd


from SQLManager import SqlManager


class FileManager():
    def execute_scripts(source: int, manager: SqlManager):
        if source == 1:
            category = "Articulos"
        if source == 2:
            category = "Proveedores"
        directory = "Output/"
        os.mkdir(directory)
        output_file1 = directory + "/SICCH.dbo."+category+"_CumplieronReglas.xlsx"
        output_file2 = directory + "/SICCH.dbo."+category+"_NoCumplieronReglas.xlsx"
        files = listdir("./Scripts/"+category)
        writer_cumplen = pd.ExcelWriter(output_file1)
        writer_no_cumplen = pd.ExcelWriter(output_file2)

        for file in files:
            script_dir = ("./Scripts/" + category + "/" + file)
            script = open(script_dir, "r")
            comandos = script.read()
            df = manager.ejecutar_query(comandos)

            nombre_excel = re.sub("[0-9]+_[0-9]_", '', file)
            if (re.search("NoCumplenReglas.sql", nombre_excel)):
                nombre_excel = nombre_excel.rstrip("_NoCumplenReglas.sql")
                df.to_excel(writer_no_cumplen, sheet_name=nombre_excel)
            if (re.search("CumplenReglas.sql", nombre_excel)):
                nombre_excel = nombre_excel.rstrip("_NoCumplenReglas.sql")
                df.to_excel(writer_cumplen, sheet_name=nombre_excel)
