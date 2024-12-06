import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Analisis de ventas")
st.subheader("GRUPO ALIPAR 2024")

archivo_cargado = st.file_uploader("Sube tu archivo en excel", type=["xlsx"])
ventas_totales = None

if archivo_cargado:
    vendedor = [
        "Alirio Parra",
        "Ivan Sepulveda",
        "Jorge Parra",
        "Julian Lozano",
        "Liliana Solano",
        "Luis Solano",
        "Mafe Solano",
        "Ramiro Miranda",
        "Raul Niebles",
    ]
    excel_file = pd.ExcelFile(archivo_cargado)
    sheet_names = excel_file.sheet_names
    filtro = st.sidebar.radio("Filtro por vendedor", sheet_names)
    df = pd.read_excel(archivo_cargado, sheet_name=filtro)
    if filtro == sheet_names[0]:  # consolidado 2024
        st.subheader("Resumen de ventas 2024")
        df["VENTAS"] = pd.to_numeric(df["VENTAS"], errors="coerce").astype(int)
        venta_anual = pd.to_numeric(df["VENTAS"], errors="coerce").sum()
        st.write(f"Las ventas del año 2024 fueron {venta_anual}")
        fig = px.line(df, x="MES", y="VENTAS", title="Ventas Mensuales en 2024")

        columna1, columna2 = st.columns([2, 1])  # alineacion
        with columna2:
            st.plotly_chart(fig)
        with columna1:
            st.write(df)

        if "PORCENTAJE" in df.columns and "MES" in df.columns:
            df = df.dropna(subset=["PORCENTAJE", "MES"])  # grafico de pastel
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=df["MES"],
                        values=df["PORCENTAJE"],
                        hoverinfo="label+percent",
                        textinfo="none",
                    )
                ]
            )
            fig.update_layout(
                title="Grafico del porcentaje de ventas",
                showlegend=True,
                margin={"t": 40, "l": 40, "r": 40},
                height=500,
            )
            st.plotly_chart(fig)
        fig = px.bar(
            df,
            x="MES",
            y=["DISTEXTIL", "ALIPAR"],
            labels={"DISTEXTIL": "DISTEXTIL", "ALIPAR": "ALIPAR"},
            title="Grafico de ventas por mes",
        )
        if isinstance(fig, dict):
            fig = px.bar(
                df,
                x="MES",
                y=["DISTEXTIL", "ALIPAR"],
                labels={"DISTEXTIL": "DISTEXTIL", "ALIPAR": "ALIPAR"},
                title="Ventas por Mes",
            )
        df_melted = df.melt(
            id_vars=["MES"],
            value_vars=["DISTEXTIL", "ALIPAR"],
            var_name="Empresa",
            value_name="Ventas",
        )
        df_melted["Empresa"] = df_melted["Empresa"].map(
            {"DISTEXTIL": "DISTEXTIL", "ALIPAR": "ALIPAR"}
        )
        st.plotly_chart(fig)
    else:
        st.subheader(f"Ventas de {filtro} 2024")
        st.write(df)

        if "VENTAS" in df.columns:
            st.subheader(
                f"Promedio de ventas {filtro} 2024"
            )  # promedio de venta por vendedor
            df["VENTAS"] = pd.to_numeric(df["VENTAS"], errors="coerce").astype(int)
            ventas_totales = pd.to_numeric(df["VENTAS"], errors="coerce").mean()
        if "PORCENTAJE" in df.columns and "MES" in df.columns:
            df = df.dropna(subset=["PORCENTAJE", "MES"])  # grafico de pastel
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=df["MES"],
                        values=df["PORCENTAJE"],
                        hoverinfo="label+percent",
                        textinfo="none",
                    )
                ]
            )
            fig.update_layout(
                title="Grafico del porcentaje de ventas",
                showlegend=True,
                margin={"t": 40, "l": 40, "r": 40},
                height=500,
            )
            columna1, columna2 = st.columns([2, 1])  # alineacion
            with columna1:
                st.plotly_chart(fig)
            with columna2:
                st.write(
                    f"El promedio de ventas del vendedor {filtro} para el año 2024 fue de {ventas_totales}"
                )

        if (
            "MES" in df.columns and "DISTEXTIL" in df.columns and "ALIPAR" in df.columns
        ):  # ventas por mes
            df = df.dropna(subset=["MES", "DISTEXTIL", "ALIPAR"])
            df["MES"] = df["MES"].astype(str)
            df["DISTEXTIL"] = pd.to_numeric(df["DISTEXTIL"], errors="coerce")
            df["ALIPAR"] = pd.to_numeric(df["ALIPAR"], errors="coerce")
            df["VENTAS"] = pd.to_numeric(df["VENTAS"], errors="coerce")
            st.subheader("Ventas por mes")
            fig = px.bar(
                df,
                x="MES",
                y=["DISTEXTIL", "ALIPAR"],
                labels={"DISTEXTIL": "DISTEXTIL", "ALIPAR": "ALIPAR"},
                title="Grafico de ventas por mes",
            )
            if isinstance(fig, dict):
                fig = px.bar(
                    df,
                    x="MES",
                    y=["DISTEXTIL", "ALIPAR"],
                    labels={"DISTEXTIL": "DISTEXTIL", "ALIPAR": "ALIPAR"},
                    title="Ventas por Mes",
                )
            df_melted = df.melt(
                id_vars=["MES"],
                value_vars=["DISTEXTIL", "ALIPAR"],
                var_name="Empresa",
                value_name="Ventas",
            )
            df_melted["Empresa"] = df_melted["Empresa"].map(
                {"DISTEXTIL": "DISTEXTIL", "ALIPAR": "ALIPAR"}
            )
            colores = {"DISTEXTIL": "darkslateblue", "ALIPAR": "darkred"}
            fig.update_layout(
                yaxis_title="Ventas", xaxis_title="Mes", legend_title="Empresa"
            )
            columna_izq, columna_der = st.columns(2)  # alineacion
            columna_izq.write(df)
            columna_der.plotly_chart(fig, use_container_width=True)
        if "META" in df.columns:
            st.subheader(f"Cumplimiento de proyección de {filtro}")  # proyeccion
            proyeccion = df["META"].iloc[0]
            cumplimiento = proyeccion - ventas_totales
        if cumplimiento <= 0:
            st.success(
                f"El vendedor {filtro} cumplio con la meta propuesta, Supero la meta por {cumplimiento}"
            )
        else:
            st.error(
                f"El vendedor {filtro}no cumplio con la meta propuesta. Le faltaron ${abs(cumplimiento)}"
            )
