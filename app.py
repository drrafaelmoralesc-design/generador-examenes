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

# Mostrar simulación de los campos del alumno construyendo el HTML de forma segura
html_alumno = (
    '<div style="border: 1px solid #ccc; padding: 15px; border-radius: 5px; background-color: #f9f9f9; margin-bottom: 25px;">'
    '<table style="width: 100%; border-collapse: collapse;">'
    '<tr>'
    '<td style="width: 50%;"><b>Nombre del Alumno:</b> _____________________________________</td>'
    '<td style="width: 25%;"><b>Boleta:</b> ______________</td>'
    '<td style="width: 25%;"><b>Grupo:</b> _________</td>'
    '</tr>'
    '<tr>'
    f'<td><b>Unidad de Aprendizaje:</b> {academia}</td>'
    f'<td><b>Ciclo Escolar:</b> {ciclo}</td>'
    '<td><b>Calificación:</b> ______</td>'
    '</tr>'
    '<tr>'
    f'<td colspan="3"><b>Tipo de Evaluación:</b> {evaluacion} &nbsp;&nbsp;&nbsp;&nbsp; <b>Fecha:</b> {fecha} &nbsp;&nbsp;&nbsp;&nbsp; <b>{tipo_examen}</b></td>'
    '</tr>'
    '</table>'
    '</div>'
)

st.markdown(html_alumno, unsafe_allow_html=True)

# Sección de Carga de Archivos
st.header("📊 Carga de Reactivos")
archivo_cargado = st.file_uploader("Suba el archivo de Excel con el banco de preguntas (.xlsx)", type=["xlsx"])

if archivo_cargado is not None:
    try:
        df = pd.read_excel(archivo_cargado)
        st.success("¡Archivo de reactivos cargado exitosamente!")
        
        st.subheader("📝 Selección de Reactivos para el Examen")
        st.write("Seleccione las preguntas que desea incluir en la versión final:")
        
        df['Seleccionar'] = False
        tabla_edicion = st.data_editor(
            df,
            column_config={
                "Seleccionar": st.column_config.CheckboxColumn(
                    "¿Incluir?",
                    help="Marque la casilla para agregar esta pregunta",
                    default=False,
                )
            },
            disabled=["Tema", "Tipo", "Enunciado", "Opción A", "Opción B", "Opción C", "Opción D"],
            hide_index=True,
        )
        
        if st.button("🚀 Generar Código LaTeX (Formato Oficio Oficial)"):
            preguntas_seleccionadas = tabla_edicion[tabla_edicion['Seleccionar'] == True]
            
            if len(preguntas_seleccionadas) == 0:
                st.warning("Por favor, seleccione al menos una pregunta de la lista.")
            else:
                st.subheader("📄 Código LaTeX Listo para Copiar")
                
                # Formato ultra compatible para importación directa en LyX
                codigo_previa = (
                    "\\documentclass[11pt,spanish]{article}\n"
                    "\\usepackage[utf8]{inputenc}\n"
                    "\\usepackage{babel}\n"
                    "\\usepackage[letterpaper,margin=1.5cm]{geometry}\n"
                    "\\usepackage{shortlst}\n"
                    "\\usepackage{enumitem}\n\n"
                    "\\begin{document}\n\n"
                    "\\begin{center}\n"
                    "    {\\Large \\textbf{INSTITUTO POLITÉCNICO NACIONAL}} \\\\\n"
                    "    {\\large \\textbf{CENTRO DE ESTUDIOS CIENTÍFICOS Y TECNOLÓGICOS NÚM. 7 \"CUAUHTÉMOC\"}} \\\\\n"
                    "    \\textbf{SUBDIRECCIÓN ACADÉMICA} \\\\\n"
                    "    \\vspace{0.3cm}\n"
                    f"    \\textbf{{UNIDAD DE APRENDIZAJE:}} {academia} \\quad \\textbf{{CICLO:}} {ciclo} \\\\\n"
                    f"    \\textbf{{{evaluacion}}} \\quad \\textbf{{{tipo_examen}}}\n"
                    "\\end{center}\n\n"
                    "\\vspace{0.2cm}\n"
                    "\\noindent\\textbf{Nombre del Alumno:} \\hrulefill \\, \\textbf{Boleta:} \\underline{\\hspace{2.5cm}} \\, \\textbf{Grupo:} \\underline{\\hspace{1.5cm}} \\\\\n"
                    f"\\noindent\\textbf{{Fecha:}} {fecha} \\quad \\textbf{{Horario:}} {horario} \\quad \\textbf{{Calificación:}} \\underline{{\\hspace{{1.5cm}}}}\n\n"
                    "\\vspace{0.5cm}\n"
                    "\\noindent\\rule{\\linewidth}{0.5mm}\n\n"
                    "\\begin{enumerate}[label=\\arabic*.-]\n"
                )
                
                for idx, row in preguntas_seleccionadas.iterrows():
                    codigo_previa += f"\n    \\item {row['Enunciado']}"
                    if row['Tipo'] == 'opcion_multiple':
                        # Se cambia piletters por un entorno estándar de letras (a, b, c, d)
                        codigo_previa += (
                            f"\n    \\begin{{enumerate}}[label=\\alph*)] \n"
                            f"        \\item {row['Opción A']} \n"
                            f"        \\item {row['Opción B']} \n"
                            f"        \\item {row['Opción C']} \n"
                            f"        \\item {row['Opción D']} \n"
                            f"    \\end{{enumerate}}"
                        )
                
                codigo_previa += (
                    "\n\\end{enumerate}\n\n"
                    "\\vspace{1.5cm}\n"
                    "\\begin{center}\n"
                    "\\begin{tabular}{cc}\n"
                    "   \\rule{5cm}{0.2mm} & \\rule{5cm}{0.2mm} \\\\\n"
                    "   Presidente de Academia & Jefa de Departamento \\\\\n"
                    "\\end{tabular}\n"
                    "\\end{center}\n\n"
                    "\\end{document}\n"
                )
                
                st.code(codigo_previa, language="latex")
                st.success("¡Código LaTeX estructurado con éxito nativo! Listo para importar en LyX.")
                
    except Exception as e:
        st.error(f"Hubo un problema al procesar el archivo de Excel: {e}")
else:
    st.info("Esperando el archivo de Excel para desplegar el banco de reactivos.")
