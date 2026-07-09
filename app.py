import streamlit as st
import pandas as pd

# Configuración de la página en modo centrado
st.set_page_config(page_title="Generador de Exámenes - IPN CECyT 7", layout="centered")

# Encabezado centrado institucional en la web
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

# Panel de Configuración de Datos del Examen
st.sidebar.header("⚙️ Datos del Encabezado")
ciclo = st.sidebar.text_input("Ciclo Escolar", value="2026-2")
evaluacion = st.sidebar.text_input("Evaluación", value="Evaluación por ETS (Extraordinario)")
academia = st.sidebar.text_input("Academia / Unidad", value="Física II")
fecha = st.sidebar.text_input("Fecha de Aplicación", value="Julio 2026")
horario = st.sidebar.text_input("Horario", value="10:00 AM")
tipo_examen = st.sidebar.selectbox("Tipo de Examen", ["Tipo A", "Tipo B"])

# Datos de Firmas Personalizables
st.sidebar.header("✍️ Firmas del Examen")
prof_resp = st.sidebar.text_input("Profesor Responsable", value="Dr. Rafael")
presi_acad = st.sidebar.text_input("Presidente de Academia", value="Ing. Nombre Presidente")
jefe_dept = st.sidebar.text_input("Jefe de Departamento", value="M. en C. Nombre Jefe")

# Función para limpiar texto y convertir caracteres como ² o ³ a modo matemático nativo
def limpiar_texto_latex(texto):
    if pd.isna(texto):
        return ""
    txt = str(texto)
    # Reemplazar superíndices de texto por modo matemático compatible con LyX
    txt = txt.replace("²", "$^2$")
    txt = txt.replace("³", "$^3$")
    return txt

# Sección de Carga de Archivos
st.header("📊 Carga de Reactivos")
archivo_cargado = st.file_uploader("Suba el archivo de Excel (.xlsx)", type=["xlsx"])

if archivo_cargado is not None:
    try:
        df = pd.read_excel(archivo_cargado)
        st.success("¡Archivo de reactivos cargado exitosamente!")
        
        st.subheader("📝 Selección de Reactivos")
        df['Seleccionar'] = False
        tabla_edicion = st.data_editor(
            df,
            column_config={
                "Seleccionar": st.column_config.CheckboxColumn("¿Incluir?", default=False)
            },
            disabled=["Tema", "Tipo", "Enunciado", "Opción A", "Opción B", "Opción C", "Opción D"],
            hide_index=True,
        )
        
        if st.button("🚀 Generar Código LaTeX (Formato Oficial con Logos)"):
            seleccionadas = tabla_edicion[tabla_edicion['Seleccionar'] == True]
            
            if len(seleccionadas) == 0:
                st.warning("Por favor, seleccione reactivos.")
            else:
                st.subheader("📄 Código LaTeX Listo para LyX")
                
                # Separar los reactivos por tipo
                teoricas = seleccionadas[seleccionadas['Tipo'] == 'opcion_multiple']
                problemas = seleccionadas[seleccionadas['Tipo'] != 'opcion_multiple']
                
                # Encabezado oficial para recuadro ERT de LyX
                codigo_final = (
                    "\\noindent\n"
                    "\\begin{tabular}{@{}p{2.2cm}cp{2.2cm}@{}}\n"
                    "   \\raisebox{-0.3\\totalheight}{\\includegraphics[width=2.0cm]{logo_ipn}} &\n"
                    "   \\begin{center}\n"
                    "       {\\large \\textbf{INSTITUTO POLITÉCNICO NACIONAL}} \\\\\n"
                    "       {\\small \\textbf{CENTRO DE ESTUDIOS CIENTÍFICOS Y TECNOLÓGICOS NÚM. 7 \"CUAUHTÉMOC\"}} \\\\\n"
                    "       \\textbf{\\footnotesize SUBDIRECCIÓN ACADÉMICA} \\\\\n"
                    "       \\vspace{0.1cm}\n"
                    f"       \\textbf{{\\footnotesize UNIDAD DE APRENDIZAJE:}} {{\\footnotesize {academia}}} \\quad \\textbf{{\\footnotesize CICLO:}} {{\\footnotesize {ciclo}}} \\\\\n"
                    f"       \\textbf{{\\footnotesize {evaluacion}}} \\quad \\textbf{{\\footnotesize {tipo_examen}}}\n"
                    "   \\end{center} &\n"
                    "   \\raisebox{-0.3\\totalheight}{\\includegraphics[width=2.0cm]{logo_cecyt7}} \\\\\n"
                    "\\end{tabular}\n\n"
                    "\\vspace{0.1cm}\n"
                    "\\noindent\\textbf{Nombre del Alumno:} \\hrulefill \\, \\textbf{Boleta:} \\underline{\\hspace{2.5cm}} \\, \\textbf{Grupo:} \\underline{\\hspace{1.5cm}} \\\\\n"
                    f"\\noindent\\textbf{{Fecha:}} {fecha} \\quad \\textbf{{Horario:}} {horario} \\quad \\textbf{{Calificación:}} \\underline{{\\hspace{{1.5cm}}}}\n\n"
                    "\\vspace{0.3cm}\n"
                    "\\noindent\\rule{\\linewidth}{0.5mm}\n\n"
                    "\\vspace{0.2cm}\n"
                    "\\noindent \\textbf{SECCIÓN I: PREGUNTAS DE OPCIÓN MÚLTIPLE (TEORÍA)}\\\\\n"
                    "\\vspace{0.4cm}\n"
                )
                
                # Renderizar teóricas aplicando la limpieza de caracteres
                num = 1
                for idx, row in teoricas.iterrows():
                    enunciado = limpiar_texto_latex(row['Enunciado']).replace(f"{num}.-", "").strip()
                    op_a = limpiar_texto_latex(row['Opción A'])
                    op_b = limpiar_texto_latex(row['Opción B'])
                    op_c = limpiar_texto_latex(row['Opción C'])
                    op_d = limpiar_texto_latex(row['Opción D'])
                    
                    codigo_final += f"\\noindent \\textbf{{{num}.-}} {enunciado} \\\\\n"
                    codigo_final += f"\\noindent a) {op_a} \\hfill b) {op_b} \\hfill c) {op_c} \\hfill d) {op_d} \\\\\n"
                    codigo_final += "\\vspace{0.5cm}\n"
                    num += 1
                
                # Forzar salto a la Página 2 para los problemas numéricos limpiando caracteres
                if len(problemas) > 0:
                    codigo_final += (
                        "\\newpage\n"
                        "\\noindent \\textbf{SECCIÓN II: PROBLEMAS NUMÉRICOS (DESARROLLO)}\\\\\n"
                        "\\vspace{0.4cm}\n"
                    )
                    
                    for idx, row in problemas.iterrows():
                        enunciado_prob = limpiar_texto_latex(row['Enunciado']).strip()
                        if enunciado_prob.startswith(f"{num}"):
                            enunciado_prob = enunciado_prob.split(".-", 1)[-1].strip()
                        codigo_final += f"\\noindent \\textbf{{{num}.-}} {enunciado_prob} \\\\\n"
                        codigo_final += "\\vspace{3.5cm} % Espacio en blanco para desarrollo\n"
                        num += 1
                
                # Bloque Oficial de Tres Firmas perfectamente distribuidas
                codigo_final += (
                    "\\vspace{\\fill}\n"
                    "\\begin{center}\n"
                    "\\small\n"
                    "\\begin{tabular}{ccc}\n"
                    "   \\rule{4.5cm}{0.2mm} & \\rule{4.5cm}{0.2mm} & \\rule{4.5cm}{0.2mm} \\\\\n"
                    f"   {prof_resp} & {presi_acad} & {jefe_dept} \\\\\n"
                    "   Profesor Responsable & Presidente de Academia & Jefe de Departamento \\\\\n"
                    "\\end{tabular}\n"
                    "\\end{center}\n"
                )
                
                st.code(codigo_final, language="latex")
                st.success("¡Código LaTeX maestro optimizado y libre de errores de caracteres!")
                
    except Exception as e:
        st.error(f"Error al procesar: {e}")
else:
    st.info("Esperando el archivo de Excel para desplegar el banco de reactivos.")
