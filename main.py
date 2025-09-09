from fastapi import FastAPI
from pydantic import BaseModel
from functions.pdf_loader import load_pdf_text
from functions.pdf_cleaner import clean_pdf_text
from functions.section_detecter import detect_section

app = FastAPI(title="PDF Tarifas API", version="1.0")

PDF_PATH = "sample_pdfs/pdf1.pdf"
MAIN_KEYWORDS = ["Servicios de comunicación", "Servicios de paquetería", "Servicios digitales", "Servicios de marketing, libros y publicaciones periódicas", "Servicios complementarios", "Servicios prestados en oficinas", "Filatelia"]

# Cargar PDF al iniciar la API
pdf_text = load_pdf_text(PDF_PATH)
#pdf_text = clean_pdf_text(pdf_text)
data = detect_section(pdf_text, MAIN_KEYWORDS)
#results = pdf_text
@app.post("/filter")

def filter_pdf():
    """
    Filtra el PDF por palabra principal y sub-palabra
    """
    return {"results": data}

@app.get("/pvp")
def get_sorted_pvp():
    pvp_items = []

    # Recorre data → categorías → secciones → items
    for category, sections in data.items():
        for section, items in sections.items():
            for item in items:
                if isinstance(item, dict) and "pvp" in item and category.lower() == "servicios de paquetería":
                    pvp_items.append({
                        **item,
                        "categoria": category,
                        "seccion": section
                    })

    # Ordena la lista por pvp de menor a mayor
    #sorted_items = sorted(pvp_items, key=lambda x: x["pvp"])
    sorted_items = pvp_items
    if sorted_items:
        return {"pvp_ordenados": sorted_items}
    else:
        return {"message": "No se encontraron precios con PVP"}
