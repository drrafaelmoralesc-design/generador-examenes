import streamlit as st
import pandas as pd

archivo_cargado = st.file_uploader("Suba su archivo Excel", type=["xlsx"])

if archivo_cargado and st.button("🚀 Generar Código LaTeX"):
    df = pd.read_excel(archivo_cargado)
    
    # Limpieza extrema: elimina el carácter 0xB2 y cualquier otro símbolo extraño
    def limpiar_final(texto):
        texto = str(texto).replace("²", " al cuadrado").replace("³", " al cubo")
        return "".join(c for c in texto if c.isprintable())

    # Aplicar limpieza a todo el DataFrame
    df = df.applymap(limpiar_final)
    
    teoricas = df[df['Tipo'] == 'opcion_multiple']
    problemas = df[df['Tipo'] != 'opcion_multiple']
    
    # Generar código ultra-plano (sin comandos LaTeX complejos)
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
    codigo += "\\noindent \\textit{Nota: La revisión de exámenes se realizará en la fecha indicada.}\n"
    
    st.code(codigo, language="latex")
