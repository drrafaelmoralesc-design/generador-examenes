import streamlit as st
import pandas as pd

st.sidebar.header("⚙️ Datos del Examen")
prof_resp = st.sidebar.text_input("Profesor Responsable", value="Dr. Rafael")
presi_acad = st.sidebar.text_input("Presidente de Academia", value="Ing. Nombre Presidente")
jefe_dept = st.sidebar.text_input("Jefe de Departamento", value="M. en C. Nombre Jefe")

archivo_cargado = st.file_uploader("Suba su archivo Excel", type=["xlsx"])

if archivo_cargado and st.button("🚀 Generar Código LaTeX"):
    df = pd.read_excel(archivo_cargado)
    teoricas = df[df['Tipo'] == 'opcion_multiple']
    problemas = df[df['Tipo'] != 'opcion_multiple']
    
    # ESTRUCTURA BLINDADA: Todo se trata como texto puro para evitar errores de secuencia
    codigo_final = "\\begin{center}\n\\textbf{INSTITUTO POLITÉCNICO NACIONAL} \\\\\n"
    codigo_final += "\\textbf{CECyT Núm. 7 \"CUAUHTÉMOC\"} \\\\\n"
    codigo_final += "\\textbf{ACADEMIA DE FÍSICA II} \\\\\n\\end{center}\n"
    codigo_final += "\\noindent Nombre: \\hrulefill \\quad Boleta: \\underline{\\hspace{2cm}} \\quad Grupo: \\underline{\\hspace{1.5cm}}\n\n"
    codigo_final += "\\vspace{0.3cm}\n\\noindent \\textbf{SECCIÓN I: TEORÍA}\n\n"
    
    for _, row in teoricas.iterrows():
        # Usamos \text{} para que LaTeX no intente leer los caracteres raros como comandos
        codigo_final += "\\noindent \\text{" + str(row['Enunciado']) + "} \\\\\n"
        codigo_final += "a) \\text{" + str(row['Opción A']) + "} \\hfill b) \\text{" + str(row['Opción B']) + "} \\hfill c) \\text{" + str(row['Opción C']) + "} \\hfill d) \\text{" + str(row['Opción D']) + "} \\\\\n\\vspace{0.3cm}\n"
    
    codigo_final += "\\vspace{\\fill}\n"
    codigo_final += "\\noindent \\begin{tabular}{p{5cm}p{5cm}p{5cm}}\n"
    codigo_final += prof_resp + " & " + presi_acad + " & " + jefe_dept + " \\\\\n"
    codigo_final += "Profesor Responsable & Presidente de Academia & Jefe de Departamento \\\\\n"
    codigo_final += "\\end{tabular}\n\n\\newpage\n"
    codigo_final += "\\noindent \\textbf{SECCIÓN II: PROBLEMAS}\n\n"
    
    for _, row in problemas.iterrows():
        codigo_final += "\\noindent \\text{" + str(row['Enunciado']) + "} \\\\\n\\vspace{3cm}\n"
        
    codigo_final += "\\vspace{\\fill}\n"
    codigo_final += "\\noindent \\textit{Nota: La revisión de exámenes se realizará en la fecha y hora indicadas por la academia.}\n"
    
    st.code(codigo_final, language="latex")
