import pandas as pd
import streamlit as st

# Función para cargar el archivo excel
def cargar_archivo(archivo):
    try:
        # Leemos el archivo y lo guardamos junto con sus hojas
        excel = pd.ExcelFile(archivo)
        hojas = excel.sheet_names

        # Si no existen hojas validas, mostramos un error
        if not hojas:
            st.error("El archivo no tiene hojas validas.")
            st.stop()
        # Si todo sale bien devolvemos el excel y sus hojas
        return excel, hojas
    except Exception as error:
        # Cualquier caso de error sera manejado aqui
        st.error(f"Error al cargar el archivo {archivo}: {error}")
        st.stop()
    
# Función para mostrar una tabla con los datos de la hoja
def mostrar_tabla(excel, hoja):
    try:
        # Creamos un dataframe en la hoja seleccionada para luego mostrar la tabla
        df = excel.parse(hoja)

        # df_styled = df.style.format({"PORCENTAJE": "{:.2%}"})
        
        st.write(f"Esta es la tabla de la hoja: {hoja}",df)
    except Exception as error:
        st.error(f"Error al leer la hoja: {error}")


# En este input se agrega el archivo excel
achivo_excel_importado = st.file_uploader("Ingrese el archivo Excel", type="xlsx")

# Si el archivo fue agregado se mostrara la aplicación principal
if achivo_excel_importado:
    
    # Aqui guardamos el Excel completo en un objeto y extraemos sus hojas
    archivo_excel, hojas = cargar_archivo(achivo_excel_importado)

    # Luego creamos una sidebar con todas las hojas obtenidas
    hoja_seleccionada = st.sidebar.radio("Lista de vendedores", hojas)
    
    # Pasamos el archivo excel y el nombre de la tabla por esta función para mostrar la tabla
    mostrar_tabla(archivo_excel, hoja_seleccionada)