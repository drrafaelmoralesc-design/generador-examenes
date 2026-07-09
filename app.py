import streamlit as st
import pandas as pd
import unicodedata

# Panel de configuración
st.sidebar.header("⚙️ Datos del Examen")
prof_resp = st.sidebar.text_input("Profesor Responsable", value="Dr. Rafael")
presi_acad = st.sidebar.text_input("Presidente de Academia", value="Ing. Nombre Presidente")
jefe_dept = st.sidebar.text_input("Jefe de Departamento", value="M. en C. Nombre Jefe")

archivo_cargado = st.file_uploader("Suba su archivo Excel", type=["xlsx"])

# Función de limpieza total
def limpiar_texto(texto):
    if pd.isna(texto):
        return ""
    # Normalizar caracteres extraños a texto plano ASCII
    txt = str(texto)
    # Reemplazo manual de símbolos problemáticos
    txt = txt.replace("²", " al cuadrado")
    txt = txt.replace("³", " al cubo")
    # Eliminar cualquier otro carácter raro no reconocido
    return "".join(c for c in unicodedata.normalize('NFKD', txt) if c.isprintable())

if archivo_cargado and st.button("🚀 Generar Código LaTeX Final"):
    df = pd.read_excel(archivo_cargado)
    # Aplicar limpieza a todas las columnas de texto
    for col in df.columns:
        df[col] = df[col].apply(limpiar_texto)
        
    teoricas = df[df['Tipo'] == 'opcion_multiple']
    problemas = df[df['Tipo'] != 'opcion_multiple']
    
    codigo_final = "\\begin{center}\n\\textbf{INSTITUTO POLITÉCNICO NACIONAL} \\\\\n"
    codigo_final += "\\textbf{CECyT Núm. 7 \"CUAUHTÉMOC\"} \\\\\n"
    codigo_final += "\\textbf{ACADEMIA DE FÍSICA II} \\\\\n\\end{center}\n"
    codigo_final += "\\noindent Nombre: \\hrulefill \\quad Boleta: \\underline{\\hspace{2cm}} \\quad Grupo: \\underline{\\hspace{1.5cm}}\n\n"
    codigo_final += "\\vspace{0.3cm}\n\\noindent \\textbf{SECCIÓN I: TEORÍA}\n\n"
    
    for _, row in teoricas.iterrows():
        codigo_final += "\\noindent " + str(row['Enunciado']) + " \\\\\n"
        codigo_final += "a) " + str(row['Opción A']) + " \\hfill b) " + str(row['Opción B']) + " \\hfill c) " + str(row['Opción C']) + " \\hfill d) " + str(row['Opción D']) + " \\\\\n\\vspace{0.3cm}\n"
    
    codigo_final += "\\vspace{\\fill}\n"
    codigo_final += "\\noindent \\begin{tabular}{p{5cm}p{5cm}p{5cm}}\n"
    codigo_final += prof_resp + " & " + presi_acad + " & " + jefe_dept + " \\\\\n"
    codigo_final += "Profesor Responsable & Presidente de Academia & Jefe de Departamento \\\\\n"
    codigo_final += "\\end{tabular}\n\n\\newpage\n"
    codigo_final += "\\noindent \\textbf{SECCIÓN II: PROBLEMAS}\n\n"
    
    for _, row in problemas.iterrows():
        codigo_final += "\\noindent " + str(row['Enunciado']) + " \\\\\n\\vspace{3cm}\n"
        
    codigo_final += "\\vspace{\\fill}\n"
    codigo_final += "\\noindent \\textit{Nota: La revisión de exámenes se realizará en la fecha y hora indicadas por la academia.}\n"
    
    st.code(codigo_final, language="latex")
