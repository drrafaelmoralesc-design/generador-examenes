import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Generador de Exámenes - IPN", layout="wide")

# Encabezado Institucional
st.image("https://www.ipn.mx/assets/files/main/img/template/logo-ipn.png", width=90)
st.title("INSTITUTO POLITÉCNICO NACIONAL")
st.subheader("CENTRO DE ESTUDIOS CIENTÍFICOS Y TECNOLÓGICOS NÚM. 7 'CUAUHTÉMOC'")

st.markdown("---")

# Panel de Configuración de Datos del Examen
st.sidebar.header("⚙️ Datos del Encabezado")
ciclo = st.sidebar.text_input("Ciclo Escolar", value="2026-2")
evaluacion = st.sidebar.selectbox("Evaluación", ["Evaluación por ETS (Extraordinario)", "Examen Parcial", "Examen Extraordinario"])
fecha = st.sidebar.text_input("Fecha de Aplicación", value="Julio 2026")
horario = st.sidebar.text_input("Horario", value="10:00 AM")
tipo_examen = st.sidebar.selectbox("Tipo de Examen", ["Tipo A", "Tipo B"])

# Sección de Carga de Archivos
st.header("📊 Carga de Reactivos")
archivo_cargado = st.file_uploader("Suba el archivo de Excel con el banco de preguntas (.xlsx)", type=["xlsx"])

if archivo_cargado is not None:
    try:
        df = pd.read_excel(archivo_cargado)
        st.success("¡Archivo de reactivos cargado exitosamente!")
        
        st.subheader("📝 Selección de Reactivos para el Examen")
        st.write("Seleccione las preguntas que desea incluir en la versión de LaTeX:")
        
        df['Seleccionar'] = False
        tabla_edicion = st.data_editor(
            df,
            column_config={
                "Seleccionar": st.column_config.CheckboxColumn(
                    "¿Incluir?",
                    help="Marque la casilla para agregar esta pregunta al examen",
                    default=False,
                )
            },
            disabled=["Tema", "Tipo", "Enunciado", "Opción A", "Opción B", "Opción C", "Opción D"],
            hide_index=True,
        )
        
        if st.button("🚀 Generar Código LaTeX para Formato Oficio"):
            preguntas_seleccionadas = tabla_edicion[tabla_edicion['Seleccionar'] == True]
            
            if len(preguntas_seleccionadas) == 0:
                st.warning("Por favor, seleccione al menos una pregunta de la lista.")
            else:
                st.subheader("📄 Vista Previa del Código Estructurado (Formato Oficio)")
                
                codigo_previa = f"""
% --- ENCABEZADO INSTITUCIONAL ---
\\textbf{{INSTITUTO POLITÉCNICO NACIONAL}} \\\\
\\textbf{{CECyT Núm. 7 "Cuauhtémoc"}} \\\\
\\text{{Ciclo Escolar: {ciclo}}} \\quad \\text{{Evaluación: {evaluacion}}} \\\\
\\text{{Fecha: {fecha}}} \\quad \\text{{Horario: {horario}}} \\quad \\textbf{{{tipo_examen}}} \\\\
\\rule{{\\linewidth}}{{0.5mm}}

% --- PREGUNTAS SELECCIONADAS ({len(preguntas_seleccionadas)} reactivos) ---
"""
                for idx, row in preguntas_seleccionadas.iterrows():
                    codigo_previa += f"\n\\item {row['Enunciado']}"
                    if row['Tipo'] == 'opcion_multiple':
                        codigo_previa += f"\n   A) {row['Opción A']}   B) {row['Opción B']}   C) {row['Opción C']}   D) {row['Opción D']}"
                
                st.code(codigo_previa, language="latex")
                st.success("Estructura base generada. ¡Listo para compilar en su plantilla profesional!")
                
    except Exception as e:
        st.error(f"Hubo un problema al procesar el archivo de Excel: {e}")
else:
    st.info("Esperando el archivo de Excel para desplegar el banco de reactivos.")
