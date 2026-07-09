import streamlit as st
import pandas as pd

# Configuración de la página en modo centrado
st.set_page_config(page_title="Generador de Exámenes - IPN CECyT 7", layout="centered")

# Encabezado centrado con HTML
st.markdown(
    """
    <div style="text-align: center;">
        <h2 style="margin-bottom: 0;">INSTITUTO POLITÉCNICO NACIONAL</h2>
        <h3 style="margin-top: 0; margin-bottom: 5px;">CENTRO DE ESTUDIOS CIENTÍFICOS Y TECNOLÓGICOS NÚM. 7 "CUAUHTÉMOC"</h3>
        <p style="font-size: 1.1em; font-weight: bold; margin-top: 0;">SUBDIRECCIÓN ACADÉMICA • DEPARTAMENTO DE UNIDADES DE APRENDIZAJE TRASVERSALES</p>
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown("---")

# Panel de Configuración de Datos del Examen (Barra Lateral Izquierda)
st.sidebar.header("⚙️ Datos del Encabezado")
ciclo = st.sidebar.text_input("Ciclo Escolar", value="2026-2")
evaluacion = st.sidebar.text_input("Evaluación", value="Evaluación por ETS (Extraordinario)")
academia = st.sidebar.text_input("Academia / Unidad", value="Física II")
fecha = st.sidebar.text_input("Fecha de Aplicación", value="Julio 2026")
horario = st.sidebar.text_input("Horario", value="10:00 AM")
tipo_examen = st.sidebar.selectbox("Tipo de Examen", ["Tipo A", "Tipo B"])

# Mostrar simulación de los campos del alumno en la página principal
st.markdown(
    f"""
    <div style="border: 1px solid #ccc; padding: 15px; border-radius: 5px; background-color: #f9f9f9; margin-bottom: 25px;">
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="width: 50%;"><b>Nombre del Alumno:</b> _____________________________________</td>
                <td style="width: 25%;"><b>Boleta:</b> ______________</td>
                <td style="width: 25%;"><b>Grupo:</b> _________</td>
            </tr>
            <tr>
                <td><b>Unidad de Aprendizaje:</b> {academia}</td>
                <td><b>Ciclo Escolar:</b> {ciclo}</td>
                <td><b>
