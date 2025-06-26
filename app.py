import streamlit as st
from docxtpl import DocxTemplate
import tempfile
import os
import time
from docx import Document
from docxcompose.composer import Composer

def generar_documento(template_path, consecutivo_inicial, apartamentos):
    consecutivo = consecutivo_inicial
    temp_files = []

    # Generar cada documento individual
    for apto in apartamentos:
        doc = DocxTemplate(template_path)
        doc.render({'consecutivo': consecutivo, 'apto': apto})

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        doc.save(temp_file.name)
        temp_files.append(temp_file.name)
        consecutivo += 1

    # Crear documento base con el primero
    master = Document(temp_files[0])
    composer = Composer(master)

    # Agregar los demás documentos con docxcompose para evitar hojas en blanco
    for temp_file in temp_files[1:]:
        sub_doc = Document(temp_file)
        composer.append(sub_doc)

    output = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    composer.save(output.name)

    # Limpiar archivos temporales
    time.sleep(1)
    for f in temp_files:
        try:
            os.remove(f)
        except PermissionError:
            pass

    return output.name

# --- Interfaz Streamlit ---

st.title("Generador de Declaraciones RETIE")

st.markdown("""
Sube tu plantilla Word con los campos `{{consecutivo}}` y `{{apto}}`. El sistema generará copias exactas de la plantilla por apartamento, cambiando solo los valores.
""")

plantilla = st.file_uploader("Sube la plantilla .docx", type="docx")
consecutivo_inicial = st.number_input("Consecutivo inicial", min_value=1, value=1300)

pisos = st.number_input("¿Cuántos pisos tiene el edificio?", min_value=1, value=5)
misma_cantidad = st.radio("¿Todos los pisos tienen la misma cantidad de apartamentos?", ["Sí", "No"])

apartamentos = []

if misma_cantidad == "Sí":
    aptos_por_piso = st.number_input("¿Cuántos apartamentos por piso?", min_value=1, value=4)
    for piso in range(1, pisos+1):
        for num in range(1, aptos_por_piso+1):
            apto = int(f"{piso}{str(num).zfill(2)}")
            apartamentos.append(apto)

elif misma_cantidad == "No":
    primer_diferente = st.radio("¿Solo el primer piso es diferente?", ["Sí", "No"])

    if primer_diferente == "Sí":
        primer_piso = st.text_input("Apartamentos del primer piso (ej: 101, 102, 103)")
        resto = st.number_input("¿Cuántos apartamentos por piso (excepto el primero)?", min_value=1, value=4)
        if primer_piso:
            aptos_p1 = [int(x.strip()) for x in primer_piso.split(',') if x.strip().isdigit()]
            apartamentos.extend(aptos_p1)
            for piso in range(2, pisos+1):
                for num in range(1, resto+1):
                    apto = int(f"{piso}{str(num).zfill(2)}")
                    apartamentos.append(apto)

    else:
        st.markdown("**Define los apartamentos por piso:**")
        for piso in range(1, pisos+1):
            entrada = st.text_input(f"Piso {piso}", key=f"piso_{piso}")
            if entrada:
                partes = []
                for val in entrada.split(','):
                    val = val.strip()
                    if '-' in val:
                        ini, fin = val.split('-')
                        partes.extend(range(int(ini), int(fin)+1))
                    elif val.isdigit():
                        partes.append(int(val))
                apartamentos.extend(partes)

if plantilla and apartamentos:
    if st.button("Generar documento"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(plantilla.read())
            tmp.flush()
            doc_path = generar_documento(tmp.name, consecutivo_inicial, apartamentos)

        with open(doc_path, "rb") as f:
            st.download_button(
                label="📥 Descargar documento final",
                data=f,
                file_name="Declaraciones_Final.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
