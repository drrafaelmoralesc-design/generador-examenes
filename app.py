import streamlit as st
import pandas as pd

# Configuración de la página en modo centrado
st.set_page_config(page_title="Generador de Exámenes - IPN CECyT 7", layout="centered")

# Encabezado centrado institucional
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
        
        if st.button("🚀 Generar Código LaTeX (Formato Oficial)"):
            seleccionadas = tabla_edicion[tabla_edicion['Seleccionar'] == True]
            
            if len(seleccionadas) == 0:
                st.warning("Por favor, seleccione reactivos.")
            else:
                st.subheader("📄 Código LaTeX Listo para LyX")
                
                # Separar los reactivos por tipo
                teoricas = seleccionadas[seleccionadas['Tipo'] == 'opcion_multiple']
                problemas = seleccionadas[seleccionadas['Tipo'] != 'opcion_multiple']
                
                # Construcción del examen plano para recuadro ERT
                codigo_final = (
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
                    "\\vspace{0.3cm}\n"
                    "\\noindent\\rule{\\linewidth}{0.5mm}\n\n"
                    "\\vspace{0.2cm}\n"
                    "\\noindent \\textbf{SECCIÓN I: PREGUNTAS DE OPCIÓN MÚLTIPLE (TEORÍA)}\\\\\n"
                    "\\vspace{0.2cm}\n"
                )
                
                # Renderizar teóricas (Página 1) con opciones en una sola línea
                num = 1
                for idx, row in teoricas.iterrows():
                    codigo_final += f"\\noindent {num}.- {row['Enunciado']} \\\\\n"
                    codigo_final += f"\\noindent a) {row['Opción A']} \\quad b) {row['Opción B']} \\quad c) {row['Opción C']} \\quad d) {row['Opción D']} \\\\\n"
                    codigo_final += "\\vspace{0.4cm}\n"
                    num += 1
                
                # Forzar salto a la Página 2 para los problemas numéricos
                codigo_final += (
                    "\\newpage\n"
                    "\\noindent \\textbf{SECCIÓN II: PROBLEMAS NUMÉRICOS (DESARROLLO)}\\\\\n"
                    "\\vspace{0.2cm}\n"
                )
                
                for idx, row in problemas.iterrows():
                    codigo_final += f"\\noindent {num}.- {row['Enunciado']} \\\\\n"
                    codigo_final += "\\vspace{2.5cm} % Espacio libre para desarrollo numérico\n"
                    num += 1
                
                # Bloque Oficial de Tres Firmas con nombres de la barra lateral
                codigo_final += (
                    "\\vspace{\\fill}\n"
                    "\\begin{center}\n"
                    "\\small\n"
                    "\\begin{tabular}{ccc}\n"
                    f"   \\rule{4.5cm}{0.2mm} & \\rule{4.5cm}{0.2mm} & \\rule{4.5cm}{0.2mm} \\\\\n"
                    f"   {prof_resp} & {presi_acad} & {jefe_dept} \\\\\n"
                    "   Profesor Responsable & Presidente de Academia & Jefe de Departamento \\\\\n"
                    "\\end{tabular}\n"
                    "\\end{center}\n"
                )
                
                st.code(codigo_final, language="latex")
                st.success("¡Código corregido con éxito estructural!")
                
    except Exception as e:
        st.error(f"Error al procesar: {e}")
