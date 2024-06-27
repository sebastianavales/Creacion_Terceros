import pandas as pd
import glob
import sys


### Importación de Archivos
print("[1] Importación de archivos:")
all_files1 = glob.glob('01. Input/01. Nuevos/*.XLSX')
# Lista para almacenar los DataFrames de los archivos en la ruta
dataframes = []
# Cargar cada archivo en un DataFrame y agregarlo a la lista
for archivo in all_files1:
    try:
        df = pd.read_excel(archivo)
        dataframes.append(df)
        
        print(f"[1] Se ha importado el archivo {archivo}.")

    except FileNotFoundError:
        print(f"[Error] El archivo {archivo} no se encontró.")
        input("Presiona Enter para salir...")
        sys.exit()
        
    except Exception as e:
        print(f"[Error] Se produjo un error al leer el archivo {archivo}: {e}")
        input("Presiona Enter para salir...")
        sys.exit()

# Concatenar los DataFrames en uno solo (Archivo para consultar terceros)
concatenado = pd.concat(dataframes, ignore_index=True)

print("[2] Archivos concatenados.")

### Listado Nits Nuevos
# Listado de Terceros nuevos
nits_nuevos = concatenado.loc[pd.notnull(concatenado['Identificación Fiscal'])]
nits_nuevos = nits_nuevos[['Identificación Fiscal']]
nits_nuevos.to_csv('02. Output/01.NITS_NUEVOS.csv', index=False, encoding='utf-16-le')

print("[3] Listado de NITS nuevos generado en la carpeta 'Output'.")
input("Presiona Enter para salir...")