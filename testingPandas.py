import pandas as pd
import streamlit as st
import plotly.express as px


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

        return excel, hojas  # Si todo sale bien devolvemos el excel y sus hojas
    except Exception as error:
        # Cualquier caso de error sera manejado aqui
        st.error(f"Error al cargar el archivo {archivo}: {error}")
        st.stop()


# Función para mostrar una tabla con los datos de la hoja
def mostrar_tabla(df, hoja):
    try:
        st.write(f"Datos de la hoja {hoja}", df)
    except Exception as error:
        st.error(f"Error al leer la hoja: {error}")


# Función para obtener el total de las ventas
def obtener_total_ventas(df):

    # Verificamos que la columna de VENTAS exista y que no este vacia
    if "VENTAS" in df.columns and not df["VENTAS"].empty:

        # Cambiamos la columna de las ventas a valores numeros, si estos no se pueden convertir, los haremos NaN, luego los convertiremos en 0, y todos los numeros seran de tipo int
        df["VENTAS"] = (
            pd.to_numeric(df["VENTAS"], errors="coerce").fillna(0).astype(int)
        )

        sum = df["VENTAS"].sum()  # Se hace la sumatoria y se retorna el total
        return sum
    else:
        return None


# Función para crear una grafica lineal
def crear_grafica_lineal(df, año):

    # Primero, establecemos los meses de la columna MES en mayusculas para mantener coherencia
    df["MES"] = df["MES"].str.upper()

    # Ahora establecemos la columna MES de tipo categorico, para que se interpreten de manera ordenada
    df["MES"] = pd.Categorical(
        df["MES"],
        categories=[
            "ENERO",
            "FEBRERO",
            "MARZO",
            "ABRIL",
            "MAYO",
            "JUNIO",
            "JULIO",
            "AGOSTO",
            "SEPTIEMBRE",
            "OCTUBRE",
            "NOVIEMBRE",
            "DICIEMBRE",
        ],
        ordered=True,
    )

    df = df.sort_values("MES")  # Se asegura que los meses este en el orden adecuado

    # Se devuelve la grafica lineal
    return px.line(df, x="MES", y="VENTAS", title=f"Ventas mensuales de {año}")


# FLUJO PRINCIPAL
achivo_excel_importado = st.file_uploader(
    "Ingrese el archivo Excel", type="xlsx"
)  # En este input se agrega el archivo excel

# Si el archivo fue agregado se mostrara la aplicación principal
if achivo_excel_importado:

    # Aqui guardamos el Excel completo en un objeto y extraemos sus hojas
    archivo_excel, hojas = cargar_archivo(achivo_excel_importado)

    # Luego creamos una sidebar con todas las hojas obtenidas
    hoja_seleccionada = st.sidebar.radio("Lista de vendedores", hojas)

    # Creamos un dataframe en la hoja seleccionada para luego mostrar la tabla, y ademas limpiamos cualquier espacio que las columnas tengan, para evitar futuros errores
    df = archivo_excel.parse(hoja_seleccionada)
    df.columns = df.columns.str.strip()

    # Obtenemos el total de ventas
    total_ventas_mensuales = obtener_total_ventas(df)

    # Pasamos el archivo excel y el nombre de la tabla por esta función para mostrar la tabla
    mostrar_tabla(df, hoja_seleccionada)

    # Ahora creamos una grafuca lineal de las ventas mensuales
    if "MES" in df.columns:
        fig = crear_grafica_lineal(df, "2024")
        st.plotly_chart(fig)
