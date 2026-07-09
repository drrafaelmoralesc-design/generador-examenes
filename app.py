import streamlit as st
import pandas as pd
import re

archivo_cargado = st.file_uploader("Suba su archivo Excel", type=["xlsx"])

if archivo_cargado and st.button("🚀 Generar Código LaTeX"):
    df = pd.read_excel(archivo_cargado)
    
    # Limpieza nivel experto: borra CUALQUIER cosa que no sea letra, número o puntuación básica
    def limpieza_extrema(texto):
        texto = str(texto)
        # Reemplazar símbolos matemáticos comunes por texto plano seguro
        texto = texto.replace("²", " al cuadrado").replace("³", " al cubo").replace("°", " grados")
        # Eliminar cualquier carácter que no sea ASCII (letras normales, números, puntuación básica)
        texto = re.sub(r'[^\x00-\x7F]+', '', texto)
        return texto

    # Aplicar la limpieza columna por columna
    for col in df.columns:
        df[col] = df[col].apply(limpieza_extrema)
    
    teoricas = df[df['Tipo'] == 'opcion_multiple']
    problemas = df[df['Tipo'] != 'opcion_multiple']
    
    # Generar código sin NINGUN comando especial (solo texto plano)
    codigo = "\\noindent \\textbf{INSTITUTO POLITÉCNICO NACIONAL} \\\\\n"
    codigo += "\\noindent \\textbf{CECyT Núm. 7 \"CUAUHTÉMOC\"} \\\\\n"
    codigo += "\\noindent \\textbf{ACADEMIA DE FÍSICA II} \\\\\n\n"
    codigo += "\\noindent Nombre: \\underline{\\hspace{6cm}} Boleta: \\underline{\\hspace{3cm}} Grupo: \\underline{\\hspace{2cm}}\n\n"
    codigo += "\\rule{\\linewidth}{0.5mm}\n\n"
    
    codigo += "\\noindent \\textbf{SECCIÓN I: TEORÍA}\n\n"
    for _, row in teoricas.iterrows():
        codigo += "\\noindent " + str(row['Enunciado']) + " \\\\\n"
        codigo += "a) " + str(row['Opción A']) + " b) " + str(row['Opción B']) + " c) " + str(row['Opción C']) + " d) " + str(row['Opción D']) + " \\\\\n\\vspace{0.2cm}\n"
    
    codigo += "\\newpage\n\\noindent \\textbf{SECCIÓN II: PROBLEMAS}\n\n"
    for _, row in problemas.iterrows():
        codigo += "\\noindent " + str(row['Enunciado']) + " \\\\\n\\vspace{3cm}\n"
    
    codigo += "\\vspace{\\fill}\n"
    codigo += "\\noindent \\textit{Nota: La revision de examenes se realizara en la fecha indicada.}\n"
    
    st.code(codigo, language="latex")
