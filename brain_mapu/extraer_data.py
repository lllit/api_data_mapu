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


#print(all_data[0]['Diccionario_mapudungun'])



if __name__ == "__main__":

    try:
        ruta_final = "D:/LLLIT/Code-W11/PY/api_data_mapu/brain_mapu/json_data/mapuche_data.json"


        # Guardar los datos en un archivo JSON
        with open(ruta_final, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
            print(f"Datos guardados correctamente en {ruta_final}")
    except:
        print("Error")

