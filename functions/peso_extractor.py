import re

def extract_peso(text: str):
	numeros = re.findall(r"(\d[\d\s\.]*\,?\d*)", text)
	numeros = [float(num.replace(".", "").replace(",", ".").replace(" ", "")) for num in numeros]

	if "hasta" in text.lower() and "más de" not in text.lower():
		# Caso "Hasta 20 g"
		return 0, numeros[0]
	elif "más de" in text.lower() and "hasta" in text.lower() and len(numeros) >= 2:
		# Caso "Más de 20 hasta 50 g"
		return numeros[0], numeros[1]
	elif "más de" in text.lower() and len(numeros) == 1:
		# Caso "Más de 1000 g"
		return numeros[0], None
	else:
		return None, None