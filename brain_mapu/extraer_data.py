import re
from unidecode import unidecode
import json
import pymupdf
import os
import sys

# Agregar el directorio raíz al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



def clean_mapudungun(text):
    # Normaliza acentos y caracteres especiales
    text = unidecode(text).lower()

    # Elimina caracteres extraños pero mantiene espacios
    text = re.sub(r'[^a-zñü\s]', '', text)

    # Reemplaza saltos de línea y tabulaciones con espacios
    text = text.replace('\n', ' ').replace('\t', ' ')

    # Elimina espacios adicionales
    text = re.sub(r'\s+', ' ', text).strip()    

    return text




def pdf_to_json(pdf_path):
    # Usa PyMuPDF para extraer texto con coordenadas
    doc = pymupdf.open(pdf_path)
    all_text = []


    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        #print(span["text"])
                        texto = clean_mapudungun(span["text"])
                        # Acumula todo el texto en una lista
                        all_text.append(texto)

    combined_text = " ".join(all_text).strip()

    file_name = os.path.splitext(os.path.basename(pdf_path))[0]
    #print(file_name)
    
    structured_data = {file_name: combined_text}

    return structured_data


# Lista de archivos PDF
pdf_files = ["data_pdf/Diccionario_mapudungun.pdf", "data_pdf/Diccionario-mapudungun-espanol-espanol-mapudungun.pdf"]



# Diccionario para almacenar todos los datos
all_data = []




for pdf_file in pdf_files:
    data = pdf_to_json(pdf_file)
    all_data.append(data)



# Extraer el texto entre "alfabeto y numeros" y "glosario"
def extract_text_between_keywords(text, start_keyword, end_keyword):
    pattern = re.compile(rf'{start_keyword}(.*?){end_keyword}', re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return ""


def seleccionar_texto():
    # ---------------- Diccionario_mapudungun --------
    alfabeto = extract_text_between_keywords(all_data[0]['Diccionario_mapudungun'], "u alfabeto", "glosario etimologico originario  palabra chilena")

    glosario_etimologico_originario = extract_text_between_keywords(all_data[0]['Diccionario_mapudungun'], start_keyword="significado original significado actual", end_keyword="kultrun instrumento musical")

    conceptos_basicos = extract_text_between_keywords(all_data[0]['Diccionario_mapudungun'], start_keyword="agradecer pedir y hasta sanar enfermedades   conceptos basicos", end_keyword="el cuerpo humano  u la cabeza")

    cuerpo_humano = extract_text_between_keywords(all_data[0]['Diccionario_mapudungun'],start_keyword="el cuerpo humano  u", end_keyword="willodmawe nimin que se enrolla sobre")

    familia_relaciones_comunidad = extract_text_between_keywords(all_data[0]['Diccionario_mapudungun'], start_keyword="familia relaciones y comunidad  u familia y relaciones abuela", end_keyword="saludos y primeros contactos")

    saludos_primeros_contactos = extract_text_between_keywords(all_data[0]['Diccionario_mapudungun'], start_keyword="u saludo despedida preguntas y respuestas", end_keyword="hombre y mujer representados en tejido textil makun")

    ambito_hogar = extract_text_between_keywords(all_data[0]['Diccionario_mapudungun'], start_keyword="el ambito  del hogar  u", end_keyword="aliwen arbol que esta plantado")

    verbos_acciones_adjetivos_emociones = extract_text_between_keywords(all_data[0]['Diccionario_mapudungun'], start_keyword="adjetivos y emociones  u", end_keyword="persona buena kumeche persona")

    ceremonias_fiestas_musica_juegos = extract_text_between_keywords(all_data[0]['Diccionario_mapudungun'], start_keyword="ceremonias fiestas  musica juegos  u", end_keyword="anumka representacion de una planta")

    naturaleza = extract_text_between_keywords(all_data[0]['Diccionario_mapudungun'], start_keyword="con fines medicos y decorativos", end_keyword="wangulen espiritu femenino presente en la mitologia mapuche")


    comunicacion_basica = extract_text_between_keywords(all_data[0]['Diccionario_mapudungun'], start_keyword="listado de frases   de comunicacion basica", end_keyword="bibliografia armengol")


    # ----------------  Diccionario-mapudungun-espanol-espanol-mapudungun --------


    structured_data = [
                    "Diccionario_mapudungun",
                       {
                        "alfabeto": alfabeto,
                        "glosario_etimologico_originario":glosario_etimologico_originario,
                        "conceptos_basicos": conceptos_basicos,
                        "cuerpo_humano": cuerpo_humano,
                        "familia_relaciones_comunidad": familia_relaciones_comunidad,
                        "saludos_primeros_contactos": saludos_primeros_contactos,
                        "ambito_hogar": ambito_hogar,
                        "verbos_acciones_adjetivos_emociones": verbos_acciones_adjetivos_emociones,
                        "ceremonias_fiestas_musica_juegos":ceremonias_fiestas_musica_juegos,
                        "naturaleza": naturaleza,
                        "comunicacion_basica": comunicacion_basica
                        },
                    "Diccionario-mapudungun-espanol-espanol-mapudungun",
                        {
                            "proximamente":"..."
                        }
                    ]
                    
    
    nombre_archivo = "mapuche_data_selected.json"
    ruta_final = f"D:/LLLIT/Code-W11/PY/api_data_mapu/brain_mapu/json_data/{nombre_archivo}"

    # Guardar los datos en un archivo JSON
    with open(ruta_final, "w", encoding="utf-8") as f:
        json.dump(structured_data, f, ensure_ascii=False, indent=4)
        print(f"Datos guardados correctamente en {ruta_final}")



#print(all_data)


if __name__ == "__main__":

    try:

        seleccionar_texto()

        nombre_archivo = "mapuche_data.json"
        ruta_final = f"D:/LLLIT/Code-W11/PY/api_data_mapu/brain_mapu/json_data/{nombre_archivo}"


        # Guardar los datos en un archivo JSON
        with open(ruta_final, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
            print(f"Datos guardados correctamente en {ruta_final}")
    except:
        print("Error")

