import pandas as pd
import numpy as np
import re
import warnings
from unicodedata import normalize

# Desactivar los avisos
warnings.filterwarnings("ignore")

try:
    ### Importación Archivo Detalle y Homologaciones
    print("[1] Importación de recursos:")
    # Archivo detalle
    detalle = pd.read_csv('01. Input/02. Creacion Terceros/Creacion de terceros.csv', sep=";", dtype=str)
    detalle = detalle.replace({np.nan: ''})
    print("[1] Archivo detalle importado.")
    # Tablas homologación Pais y Municipio
    pais = pd.read_excel('01. Input/Ubicacion.xlsx', sheet_name='Pais', dtype=str)
    municipio = pd.read_excel('01. Input/Ubicacion.xlsx', sheet_name='Municipio', dtype=str)
    print("[1] Archivo ubicación importado.")
    # Tabla empleados
    empleados = pd.read_csv('01. Input/Empleados.csv', sep=";", dtype=str)
    print("[1] Archivo empleados importado.")

    ### Reemplazar dos o más espacios por un solo espacio en todas las columnas
    detalle.replace(regex=r'\s{2,}', value=' ', inplace=True)

    print("[2] Dos o más espacios reemplazados.")

    ### Eliminar caracteres especiales
    # Lista de columnas a tratar
    columnas_especificas = ['Acreedor', 'Nombre', 'País', 'Región', 'Calle', 'Conc.búsq.', 'Gr.cuentas', 'Tipo NIF', \
                            'Teléfono', 'Tel. Mo.', 'Fax']

    # Función para quitar tildes y otros
    def quitar_caracteres_tildes(texto):
        # Utiliza una expresión regular para quitar tildes y otros
        return re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", texto), 0, re.I)
    # Aplica la función solo a las columnas específicas
    detalle[columnas_especificas] = detalle[columnas_especificas].astype(str).applymap(quitar_caracteres_tildes)

    # Función para quitar caracteres especiales
    def quitar_caracteres_especiales(texto):
        # Utiliza una expresión regular para quitar caracteres no alfanuméricos
        return re.sub(r'[^A-Za-z0-9]+', ' ', str(texto))
    # Aplica la función solo a las columnas específicas
    detalle[columnas_especificas] = detalle[columnas_especificas].astype(str).applymap(quitar_caracteres_especiales)

    print("[3] Caracteres especiales eliminados.")
    
    ### Transformar Tipo NIF
   # Función para determinar el Tipo NIF según caracteristicas del NIF
    def determinar_tipo_nif(NIF, Tipo_NIF):
        nif = str(NIF)
        tipo_nif = str(Tipo_NIF)
        largo = len(nif)
        inicia = nif[0]

        # Tipo 11
        if tipo_nif == '11':  
            if largo == 8 and inicia in ['1','2','3','4','5','6','7']:
                return 11
            elif largo == 9 and inicia in ['1','2','3','4','5','6','9']:
                return 11
            elif largo == 10 and inicia in ['1']:
                return 11
            elif largo == 11 and inicia in ['1']:
                return 11
            
        # Tipo 12   
        elif tipo_nif == '12':
            if largo == 7 and inicia in ['1','2','8']:
                return 12
            elif largo == 8 and inicia in ['1', '3', '4', '5']:
                return 12
            elif largo == 9 and inicia in ['1']:
                return 12
            elif largo == 10 and inicia in ['1']:
                return 12
            elif largo == 11 and inicia in ['1']:
                return 12
        
        # Tipo 13
        elif tipo_nif == '13':  
            if largo == 6 and inicia in ['1','2','3','4','5','6','7','8','9']:
                return 13
            elif largo == 7 and inicia in ['1','2','3','4','5','6','7','8','9']:
                return 13
            elif largo == 8 and inicia in ['1','2','3','4','5','6','7','8','9']:
                return 13
            elif largo == 10 and inicia in ['1','2']:
                return 13
        
        # Tipo 22
        elif tipo_nif == '22':
            if nif.isdigit():
                if largo == 6 and inicia in ['1','2','3','4','5','6','7','8','9']:
                    return 22
                elif largo == 7 and inicia in ['1','2','3','4','5','6','7','8','9']:
                    return 22
                elif largo == 8 and inicia in ['1','2','3','4','5','6','7','8','9']:
                    return 22

        # Tipo 31
        elif tipo_nif == '31':
            if largo == 10 and inicia in ['8','9']:
                return 31
        
        # Tipo 41
        elif tipo_nif == '41':
            if nif.isdigit():
                if largo == 5 and inicia in ['1','2','3','4','5','6','7','8','9']:
                    return 41
                elif largo == 6 and inicia in ['1','2','3','4','5','6','7','8','9']:
                    return 41
                elif largo == 7 and inicia in ['1','2','3','4','5','6','7','8','9']:
                    return 41
                elif largo == 8 and inicia in ['1','2','3','4','5','6','7','8','9']:
                    return 41
                elif largo == 9 and inicia in ['1','2','3','4','5','6','7','8','9']:
                    return 41
                elif largo == 10 and inicia in ['0','1','2','3','5']:
                    return 41
                elif largo == 11 and inicia in ['1']:
                    return 41
            elif any(caracter.isalpha() for caracter in nif):
                if largo == 5:
                    return 41
                elif largo == 6:
                    return 41
                elif largo == 7:
                    return 41
                elif largo == 8:
                    return 41
                elif largo == 9:
                    return 41
                elif largo == 10:
                    return 41
                elif largo == 11:
                    return 41

        # Tipo 42
        elif tipo_nif == '42':
            return 42

        # Tipo 47
        elif tipo_nif == '47':
            if largo == 6 and inicia in ['5','6','7','8','9']:
                return 47
            elif largo == 7 and inicia in ['1','2','3','4','5','6','7','8','9']:
                return 47
            elif largo == 8 and inicia in ['1']:
                return 47
            elif largo == 9 and inicia in ['9']:
                return 47
            elif largo == 10 and inicia in ['5']:
                return 47
            elif largo == 11 and inicia in ['0']:
                return 47
            elif largo == 12 and inicia in ['1']:
                return 47
            elif largo == 13 and inicia in ['4']:
                return 47
            elif largo == 15 and inicia in ['1','2','3','7','8','9']:
                return 47

        # Tipo 48
        elif tipo_nif == '48':
            if largo == 6 and inicia in ['5','6','7','8','9']:
                return 48
            elif largo == 7 and inicia in ['1','2','3','4','5','6']:
                return 48
            elif largo == 8 and inicia in ['2','4','7']:
                return 48
            elif largo == 9 and inicia in ['5','6']:
                return 48
        
        return "I"

    # Columna Tipo NIF
    detalle['Tipo NIF'] = detalle.apply(lambda row: pd.Series(determinar_tipo_nif(row['N.I.F.1'], row['Tipo NIF'])), axis=1)

    # Función para determinar el Tipo NIF según caracteristicas del NIF (2da Validación)
    def determinar_tipo_nif_2(NIF, Tipo_NIF):
        nif = str(NIF)
        tipo_nif = str(Tipo_NIF)
        largo = len(nif)
        inicia = nif[0]

        if tipo_nif == 'I':

        # Tipo 11
            if largo == 9 and inicia in ['1','2','3','4','5','6']:
                return 11
            elif largo == 11 and inicia in ['1']:
                return 11
            
        # Tipo 13
            if largo == 6 and inicia in ['1','2','3','4','5','6','7','8','9']:
                return 13
            elif largo == 7 and inicia in ['1','2','3','4','5','6','7','8','9']:
                return 13
            elif largo == 8 and inicia in ['1','2','3','4','5','6','7','8','9']:
                return 13
            elif largo == 10 and inicia in ['1','2']:
                return 13
            
        # Tipo 31
            if largo == 10 and inicia in ['8','9']:
                return 31
        
        # Tipo 47
            if largo == 10 and inicia in ['5']:
                return 47
            elif largo == 11 and inicia in ['0']:
                return 47
            elif largo == 12 and inicia in ['1']:
                return 47
            elif largo == 13 and inicia in ['4']:
                return 47
            elif largo == 15 and inicia in ['1','2','3','7','8','9']:
                return 47
        
        return Tipo_NIF

    # Columna Tipo NIF (2da Validación)
    detalle['Tipo NIF'] = detalle.apply(lambda row: pd.Series(determinar_tipo_nif_2(row['N.I.F.1'], row['Tipo NIF'])), axis=1)

    ### Tratar columna NIF y extraer DV
    # Columna Identificación
    detalle['Identificación(STCD1) (CHAR/000030)'] = np.select(
        [detalle['Tipo NIF'] != 31],
        [detalle['N.I.F.1']],   
        default=detalle['N.I.F.1'].str[:-1]
    )

    # Columna Digito Verificación
    detalle['Dígito Verificación(CODVER) (CHAR/000002)'] = np.select(
        [detalle['Tipo NIF'] == 31],
        [detalle['N.I.F.1'].str[-1]],
        default=""
    )

    print("[4] Columna NIF tratada.")

    ### Separación de Nombres y Apellidos
    # Función para separar nombres y apellidos persona natural
    def separar_nombres_apellidos(nombre_completo, tipo_persona):

        if tipo_persona != 31:

            nombre_completo = nombre_completo.replace(' de ', ' de_')
            nombre_completo = nombre_completo.replace(' DE ', ' DE_')
            nombre_completo = nombre_completo.replace(' De ', ' De_')

            nombre_completo = nombre_completo.replace(' d ', ' d_')
            nombre_completo = nombre_completo.replace(' D ', ' D_')

            nombre_completo = nombre_completo.replace(' mc ', ' mc_')
            nombre_completo = nombre_completo.replace(' MC ', ' MC_')
            nombre_completo = nombre_completo.replace(' Mc ', ' Mc_')

            nombre_completo = nombre_completo.replace(' del ', ' del_')
            nombre_completo = nombre_completo.replace(' DEL ', ' DEL_')
            nombre_completo = nombre_completo.replace(' Del ', ' Del_')

            nombre_completo = nombre_completo.replace(' de la ', ' de_la_')
            nombre_completo = nombre_completo.replace(' DE LA ', ' DE_LA_')
            nombre_completo = nombre_completo.replace(' De La ', ' De_La_')
            nombre_completo = nombre_completo.replace(' De la ', ' De_la_')
            nombre_completo = nombre_completo.replace(' de_la ', ' de_la_')
            nombre_completo = nombre_completo.replace(' DE_LA ', ' DE_LA_')
            nombre_completo = nombre_completo.replace(' De_La ', ' De_La_')
            nombre_completo = nombre_completo.replace(' De_la ', ' De_la_')

            nombre_completo = nombre_completo.replace(' de las ', ' de_las_')
            nombre_completo = nombre_completo.replace(' DE LAS ', ' DE_LAS_')
            nombre_completo = nombre_completo.replace(' De Las ', ' De_Las_')
            nombre_completo = nombre_completo.replace(' De las ', ' De_las_')
            nombre_completo = nombre_completo.replace(' de_las ', ' de_las_')
            nombre_completo = nombre_completo.replace(' DE_LAS ', ' DE_LAS_')
            nombre_completo = nombre_completo.replace(' De_Las ', ' De_Las_')
            nombre_completo = nombre_completo.replace(' De_las ', ' De_las_')
            
            nombre_completo = nombre_completo.replace(' de los ', ' de_los_')
            nombre_completo = nombre_completo.replace(' DE LOS ', ' DE_LOS_')
            nombre_completo = nombre_completo.replace(' De Los ', ' De_Los_')
            nombre_completo = nombre_completo.replace(' De los ', ' De_los_')
            nombre_completo = nombre_completo.replace(' de_los ', ' de_los_')
            nombre_completo = nombre_completo.replace(' DE_LOS ', ' DE_LOS_')
            nombre_completo = nombre_completo.replace(' De_Los ', ' De_Los_')
            nombre_completo = nombre_completo.replace(' De_los ', ' De_los_')

            # Doble espacio
            nombre_completo = nombre_completo.replace(' de  la ', ' de_la_')
            nombre_completo = nombre_completo.replace(' DE  LA ', ' DE_LA_')
            nombre_completo = nombre_completo.replace(' De  La ', ' De_La_')
            nombre_completo = nombre_completo.replace(' De  la ', ' De_la_')


            nombre_completo = nombre_completo.replace(' de  las ', ' de_las_')
            nombre_completo = nombre_completo.replace(' DE  LAS ', ' DE_LAS_')
            nombre_completo = nombre_completo.replace(' De  Las ', ' De_Las_')
            nombre_completo = nombre_completo.replace(' De  las ', ' De_las_')


            nombre_completo = nombre_completo.replace(' de  los ', ' de_los_')
            nombre_completo = nombre_completo.replace(' DE  LOS ', ' DE_LOS_')
            nombre_completo = nombre_completo.replace(' De  Los ', ' De_Los_')
            nombre_completo = nombre_completo.replace(' De  los ', ' De_los_')

            # Cubrir errores
            nombre_completo = nombre_completo.replace(' de lo ', ' de_lo_')
            nombre_completo = nombre_completo.replace(' DE LO ', ' DE_LO_')
            nombre_completo = nombre_completo.replace(' De Lo ', ' De_Lo_')
            nombre_completo = nombre_completo.replace(' De lo ', ' De_lo_')
            nombre_completo = nombre_completo.replace(' de_lo ', ' de_lo_')
            nombre_completo = nombre_completo.replace(' DE_LO ', ' DE_LO_')
            nombre_completo = nombre_completo.replace(' De_Lo ', ' De_Lo_')
            nombre_completo = nombre_completo.replace(' De_lo ', ' De_lo_')

            nombre_completo = nombre_completo.replace(' del la ', ' del_la_')
            nombre_completo = nombre_completo.replace(' DEL LA ', ' DEL_LA_')
            nombre_completo = nombre_completo.replace(' Del La ', ' Del_La_')
            nombre_completo = nombre_completo.replace(' Del la ', ' Del_la_')
            nombre_completo = nombre_completo.replace(' del_la ', ' del_la_')
            nombre_completo = nombre_completo.replace(' DEL_LA ', ' DEL_LA_')
            nombre_completo = nombre_completo.replace(' Del_La ', ' Del_La_')
            nombre_completo = nombre_completo.replace(' Del_la ', ' Del_la_')

            nombre_completo = nombre_completo.replace(' del las ', ' del_las_')
            nombre_completo = nombre_completo.replace(' DEL LAS ', ' DEL_LAS_')
            nombre_completo = nombre_completo.replace(' Del Las ', ' Del_Las_')
            nombre_completo = nombre_completo.replace(' Del las ', ' Del_las_')
            nombre_completo = nombre_completo.replace(' del_las ', ' del_las_')
            nombre_completo = nombre_completo.replace(' DEL_LAS ', ' DEL_LAS_')
            nombre_completo = nombre_completo.replace(' Del_Las ', ' Del_Las_')
            nombre_completo = nombre_completo.replace(' Del_las ', ' Del_las_')

            nombre_completo = nombre_completo.replace(' del los ', ' del_los_')
            nombre_completo = nombre_completo.replace(' DEL LOS ', ' DEL_LOS_')
            nombre_completo = nombre_completo.replace(' Del Los ', ' Del_Los_')
            nombre_completo = nombre_completo.replace(' Del los ', ' Del_los_')
            nombre_completo = nombre_completo.replace(' del_los ', ' del_los_')
            nombre_completo = nombre_completo.replace(' DEL_LOS ', ' DEL_LOS_')
            nombre_completo = nombre_completo.replace(' Del_Los ', ' Del_Los_')
            nombre_completo = nombre_completo.replace(' Del_los ', ' Del_los_')

            # Doble espacio
            nombre_completo = nombre_completo.replace(' de  lo ', ' de_lo_')
            nombre_completo = nombre_completo.replace(' DE  LO ', ' DE_LO_')
            nombre_completo = nombre_completo.replace(' De  Lo ', ' De_Lo_')
            nombre_completo = nombre_completo.replace(' De  lo ', ' De_lo_')

            nombre_completo = nombre_completo.replace(' del  la ', ' del_la_')
            nombre_completo = nombre_completo.replace(' DEL  LA ', ' DEL_LA_')
            nombre_completo = nombre_completo.replace(' Del  La ', ' Del_La_')
            nombre_completo = nombre_completo.replace(' Del  la ', ' Del_la_')

            nombre_completo = nombre_completo.replace(' del  las ', ' del_las_')
            nombre_completo = nombre_completo.replace(' DEL  LAS ', ' DEL_LAS_')
            nombre_completo = nombre_completo.replace(' Del  Las ', ' Del_Las_')
            nombre_completo = nombre_completo.replace(' Del  las ', ' Del_las_')

            nombre_completo = nombre_completo.replace(' del  los ', ' del_los_')
            nombre_completo = nombre_completo.replace(' DEL  LOS ', ' DEL_LOS_')
            nombre_completo = nombre_completo.replace(' Del  Los ', ' Del_Los_')
            nombre_completo = nombre_completo.replace(' Del  los ', ' Del_los_')

            # Separar nombres y apellidos
            partes = nombre_completo.split()

            # Inicializar las variables
            nombre1, nombre2, apellido1, apellido2 = '', '', '', ''

            # 
            if len(partes) == 1:
                nombre1 = partes[0]

            # 
            if len(partes) == 2:
                nombre1 = partes[0]
                apellido1 = partes[-1]

            # 
            if len(partes) == 3:
                nombre1 = partes[0]
                apellido1 = partes[-2]
                apellido2 = partes[-1]

            # 
            if len(partes) >= 4:
                nombre1 = partes[0]
                nombre2 = partes[1]
                apellido1 = partes[-2]
                apellido2 = partes[-1]

            return nombre1, nombre2, apellido1, apellido2

        else:

            return '', '', '', ''
        
    # Columnas Nombres y Apellidos
    detalle[['Nombre 1(NAME1) (CHAR/000060)', 'Nombre 2(NAME2) (CHAR/000060)', 'Apellido 1(APEL1) (CHAR/000060)', 'Apellido 2(APEL2) (CHAR/000060)']] = detalle.apply(lambda row: pd.Series(separar_nombres_apellidos(row['Nombre'], row['Tipo NIF'])), axis=1)
    detalle[['Nombre 1(NAME1) (CHAR/000060)', 'Nombre 2(NAME2) (CHAR/000060)', 'Apellido 1(APEL1) (CHAR/000060)', 'Apellido 2(APEL2) (CHAR/000060)']] = detalle[['Nombre 1(NAME1) (CHAR/000060)', 'Nombre 2(NAME2) (CHAR/000060)', 'Apellido 1(APEL1) (CHAR/000060)', 'Apellido 2(APEL2) (CHAR/000060)']].applymap(lambda x: x.replace('_', ' '))
    # Columna Razón Social
    detalle['Razón Social(RAZSC) (CHAR/000100)'] = np.select(
        [detalle['Tipo NIF'] == 31],
        [detalle['Nombre']],
        default=""
    )

    print("[5] Columna Nombre tratada.")

    ### Homologación de Municipio y Pais DIAN
    detalle = pd.merge(detalle, municipio, left_on=['Región','Población'], right_on=['Código Departamento','Municipio / Ciudad'], how='left')
    detalle = pd.merge(detalle, pais, left_on='País', right_on='País SAP', how='left')

    detalle['Calle'] = np.select(
        [detalle['País DIAN'] != "169"],
        [""],
        default=detalle['Calle']
    )

    detalle['Región'] = np.select(
        [detalle['País DIAN'] != "169"],
        [""],
        default=detalle['Región']
    )

    detalle['Código Municipio'] = np.select(
        [detalle['País DIAN'] != "169"],
        [""],
        default=detalle['Código Municipio']
    )

    print("[6] Columnas Ubicación homologadas.")

    ### Eliminación de Letras en Teléfono, Móvil y FAX
    detalle['Teléfono'] = detalle['Teléfono'].replace(regex=r'[^0-9]', value='')
    detalle['Teléfono'] = np.select(
        [detalle['Teléfono'].str.len() <= 5],
        [""],
        default=detalle['Teléfono']   
    )
    detalle['Tel. Mo.'] = detalle['Tel. Mo.'].replace(regex=r'[^0-9]', value='')
    detalle['Tel. Mo.'] = np.select(
        [detalle['Tel. Mo.'].str.len() <= 5],
        [""],
        default=detalle['Tel. Mo.']   
    )
    detalle['Fax'] = detalle['Fax'].replace(regex=r'[^0-9]', value='')
    detalle['Fax'] = np.select(
        [detalle['Fax'].str.len() <= 5],
        [""],
        default=detalle['Fax']   
    )

    print("[7] Letras en teléfono, móvil y FAX eliminadas.")

    ### Verificación Empleados
    # Verificar si el registro se encuentra en la base de datos de empleados
    detalle['Empleado(ISEMP) (CHAR/000001)'] = np.select(
        [detalle['N.I.F.1'].isin(empleados['Empleado GH']) == True],
        ["X"],
        default=""
    )

    print("[8] Empleados verificados.")

    ### Generación de columnas restantes (Vacías)
    detalle['Tercero del Exterior(ISTEREXT) (CHAR/000001)'] = ""
    detalle['Identificación(STCD1_U) (CHAR/000030)'] = ""
    detalle['Tipo de N.I.F.(STCDT_U) (CHAR/000002)'] = ""
    detalle['Fecha(DATCR) (DATS/000008)'] = ""
    detalle['Usuario(USRCR) (CHAR/000012)'] = ""
    detalle['Fecha(DATMD) (DATS/000008)'] = ""
    detalle['Usuario(USRMD) (CHAR/000012)'] = ""

    ### Estructura final de plantilla
    # Selección de las columnas necesarias para la plantilla
    plantilla = detalle[['Identificación(STCD1) (CHAR/000030)', 'Tipo NIF', 'Dígito Verificación(CODVER) (CHAR/000002)',\
                        'Nombre 1(NAME1) (CHAR/000060)', 'Nombre 2(NAME2) (CHAR/000060)', 'Apellido 1(APEL1) (CHAR/000060)',\
                        'Apellido 2(APEL2) (CHAR/000060)', 'Razón Social(RAZSC) (CHAR/000100)', 'Calle', 'Región',\
                        'Código Municipio', 'País DIAN', 'Correo electrónico', 'Teléfono', 'Tel. Mo.', 'Fax',\
                        'Empleado(ISEMP) (CHAR/000001)', 'Tercero del Exterior(ISTEREXT) (CHAR/000001)', 'Identificación(STCD1_U) (CHAR/000030)',\
                        'Tipo de N.I.F.(STCDT_U) (CHAR/000002)', 'Fecha(DATCR) (DATS/000008)', 'Usuario(USRCR) (CHAR/000012)',\
                        'Fecha(DATMD) (DATS/000008)', 'Usuario(USRMD) (CHAR/000012)']]
    # Cambio de nombre de las columnas a formato de la plantilla
    plantilla = plantilla.rename(columns={'Tipo NIF': 'Tipo de N.I.F.(STCDT) (CHAR/000002)',
                                        'Calle': 'Dirección(ADRNR) (CHAR/000060)',
                                        'Región': 'Población(REGIO) (CHAR/000035)',
                                        'Código Municipio': 'Población(ORT01) (CHAR/000035)',
                                        'País DIAN': 'Población(LAND1) (CHAR/000035)',
                                        'Correo electrónico': 'Correo electr.(SMTPADR) (CHAR/000241)',
                                        'Teléfono': 'Teléfono 1(TELF1) (CHAR/000016)',
                                        'Tel. Mo.': 'Teléfono móvil(MOB_NUMBER) (CHAR/000030)',
                                        'Fax': 'Fax(FAX_NUMBER) (CHAR/000030)',
                                        })


    ### Eliminar registros duplicados
    # Calcula la cantidad de celdas diferentes de vacío y diferentes de nulo por fila
    plantilla['Cantidad_de_Datos'] = ((plantilla.notna()) & (plantilla.ne(""))).sum(axis=1)
    # Ordena el DataFrame por la cantidad de datos en orden descendente
    plantilla = plantilla.sort_values(by='Cantidad_de_Datos', ascending=False)
    resultado = plantilla.copy()
    # Elimina todos los duplicados y conserva el que tiene más datos (el primero en orden descendente)
    resultado = resultado.drop_duplicates(subset=['Identificación(STCD1) (CHAR/000030)'], keep='first')
    # Reinicia los índices después de eliminar filas
    resultado = resultado.reset_index(drop=True)
    # Elimina las columnas temporales creadas
    resultado = resultado.drop(['Cantidad_de_Datos'], axis=1)

    print("[9] Duplicados eliminados.")

    ### Exportar la plantilla
    resultado.to_csv('02. Output/02.PLANTILLA.csv', sep=';', encoding='utf-16-le', index=False)

    print("Plantilla generada en la carpeta 'Output'.")

except Exception as e:
    print(f"[Error] Se produjo un error durante la ejecución: {e}")

# Restaurar la configuración de los avisos al estado original al final del script
warnings.filterwarnings("default")

input("Presiona Enter para salir...")