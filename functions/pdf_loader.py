import pdfplumber
from collections import defaultdict

def load_pdf_text(path: str):
    result = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages[4:]:
            words = page.extract_words()
            midpoint = page.width / 2

            # Dividimos en columnas
            left_col = [w for w in words if w["x0"] < midpoint]
            right_col = [w for w in words if w["x0"] >= midpoint]

            # Función auxiliar para agrupar en líneas
            def group_by_line(col):
                lines = defaultdict(list)
                for w in col:
                    # Agrupar por la coordenada Y redondeada
                    line_key = round(w["top"])
                    lines[line_key].append(w)
                # Ordenar líneas y palabras en cada línea
                sorted_lines = []
                for key in sorted(lines.keys()):
                    line_words = sorted(lines[key], key=lambda w: w["x0"])
                    sorted_lines.append(" ".join(w["text"] for w in line_words))
                return sorted_lines

            left_lines = group_by_line(left_col)
            right_lines = group_by_line(right_col)

            result.append((left_lines, right_lines))
    return result