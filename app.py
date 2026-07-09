import streamlit as st
import pandas as pd

# Panel de configuración y carga (se mantiene igual)
st.sidebar.header("⚙️ Datos del Examen")
prof_resp = st.sidebar.text_input("Profesor Responsable", value="Dr. Rafael")
presi_acad = st.sidebar.text_input("Presidente de Academia", value="Ing. Nombre Presidente")
jefe_dept = st.sidebar.text_input("Jefe de Departamento", value="M. en C. Nombre Jefe")

archivo_cargado = st.file_uploader("Suba su archivo Excel", type=["xlsx"])

if archivo_cargado and st.button("🚀 Generar Código LaTeX Final"):
    df = pd.read_excel(archivo_cargado)
    teoricas = df[df['Tipo'] == 'opcion_multiple']
    problemas = df[df['Tipo'] != 'opcion_multiple']
    
    # ESTRUCTURA MAESTRA DE LaTeX
    codigo_final = (
        "% --- ENCABEZADO OFICIAL ---\n"
        "\\begin{center}\n"
        "\\textbf{INSTITUTO POLITÉCNICO NACIONAL} \\\\\n"
        "\\textbf{CECyT Núm. 7 \"CUAUHTÉMOC\"} \\\\\n"
        "\\textbf{ACADEMIA DE FÍSICA II} \\\\\n"
        "\\end{center}\n"
        "\\noindent Nombre: \\hrulefill \\quad Boleta: \\underline{\\hspace{2cm}} \\quad Grupo: \\underline{\\hspace{1.5cm}}\n\n"
        "\\vspace{0.3cm}\n"
        "% --- PÁGINA 1: TEORÍA Y FIRMAS AL FINAL ---\n"
        "\\noindent \\textbf{SECCIÓN I: TEORÍA}\n\n"
    )
    
    for _, row in teoricas.iterrows():
        codigo_final += f"\\noindent {row['Enunciado']} \\\\\n"
        codigo_final += f"a) {row['Opción A']} \\hfill b) {row['Opción B']} \\hfill c) {row['Opción C']} \\hfill d) {row['Opción D']} \\\\\n\\vspace{0.3cm}\n"
    
    codigo_final += (
        "\\vspace{\\fill}\n"
        "% --- FIRMAS PÁGINA 1 ---\n"
        "\\noindent \\begin{tabular}{p{5cm}p{5cm}p{5cm}}\n"
        f"{prof_resp} & {presi_acad} & {jefe_dept} \\\\\n"
        "Profesor Responsable & Presidente de Academia & Jefe de Departamento \\\\\n"
        "\\end{tabular}\n\n"
        "\\newpage\n"
        "% --- PÁGINA 2: PROBLEMAS Y LEYENDA ---\n"
        "\\noindent \\textbf{SECCIÓN II: PROBLEMAS}\n\n"
    )
    
    for _, row in problemas.iterrows():
        codigo_final += f"\\noindent {row['Enunciado']} \\\\\n\\vspace{3cm}\n"
        
    codigo_final += (
        "\\vspace{\\fill}\n"
        "\\noindent \\textit{Nota: La revisión de exámenes se realizará en la fecha y hora indicadas por la academia.}\n"
    )
    
    st.code(codigo_final, language="latex")
