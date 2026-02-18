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

# --------------------------------------------------
# ¿Todos los pisos tienen misma cantidad?
# --------------------------------------------------

misma_cantidad_pisos = st.radio(
    "¿Todos los pisos tienen la misma cantidad de apartamentos?",
    ["Sí", "No"]
)

if misma_cantidad_pisos == "Sí":

    # --------------------------------------------------
    # ¿Secuencia normal o tipología especial?
    # --------------------------------------------------

    misma_secuencia = st.radio(
        "¿Todos los apartamentos del piso tienen secuencia consecutiva normal? (ej: 201,202,203...)",
        ["Sí", "No"]
    )

    if misma_secuencia == "Sí":
        aptos_por_piso = st.number_input("¿Cuántos apartamentos por piso?", min_value=1, value=4)

        for piso in range(1, pisos+1):
            for num in range(1, aptos_por_piso+1):
                apto = int(f"{piso}{str(num).zfill(2)}")
                apartamentos.append(apto)

    else:
        secuencia = st.text_input(
            "Escribe la secuencia usando 'x' como número de piso (ej: x01,x02,x03,x15,x16)"
        )

        if secuencia:
            patrones = [s.strip() for s in secuencia.split(',')]

            for piso in range(1, pisos+1):
                for patron in patrones:
                    if 'x' in patron:
                        apto = patron.replace('x', str(piso))
                        apartamentos.append(int(apto))

# --------------------------------------------------
# Si NO todos los pisos tienen misma cantidad
# --------------------------------------------------

else:

    diferentes = st.text_input(
        "¿Qué pisos son diferentes? (ej: 3,5,6)"
    )

    pisos_diferentes = []

    if diferentes:
        pisos_diferentes = [
            int(x.strip()) for x in diferentes.split(',')
            if x.strip().isdigit()
        ]

    # Primero definimos modelo base
    misma_secuencia = st.radio(
        "Para los pisos normales, ¿usan secuencia consecutiva normal?",
        ["Sí", "No"]
    )

    aptos_base = []

    if misma_secuencia == "Sí":
        aptos_por_piso = st.number_input(
            "¿Cuántos apartamentos tienen los pisos normales?",
            min_value=1,
            value=4
        )

        for piso in range(1, pisos+1):
            if piso not in pisos_diferentes:
                for num in range(1, aptos_por_piso+1):
                    apto = int(f"{piso}{str(num).zfill(2)}")
                    apartamentos.append(apto)

    else:
        secuencia = st.text_input(
            "Secuencia base usando x (ej: x01,x02,x15,x16)"
        )

        if secuencia:
            patrones = [s.strip() for s in secuencia.split(',')]

            for piso in range(1, pisos+1):
                if piso not in pisos_diferentes:
                    for patron in patrones:
                        apto = patron.replace('x', str(piso))
                        apartamentos.append(int(apto))

    # Ahora pedimos manual los pisos diferentes
    for piso in pisos_diferentes:
        entrada = st.text_input(f"Escriba los apartamentos del piso {piso} (ej: 301,305,310)")

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
