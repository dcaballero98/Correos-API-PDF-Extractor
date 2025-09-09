import re
from functions.peso_extractor import extract_peso

def parse_tarifas(line: str) -> dict:
	clean_numbers = []
	pattern = re.compile(r"(.+?)\s+(\d+[,.]\d+)\s+(\d+[,.]\d+)\s+(\d+[,.]\d+)")

	
	matches =  pattern.findall(line)
	if matches:
		for match in matches:
			clean_numbers = [(m.replace(",", ".")) for m in match]
	if clean_numbers:
		peso_min, peso_max = extract_peso(clean_numbers[0])
		result = {"descripción": clean_numbers[0], "tarifa": float(clean_numbers[1]), "iva": float(clean_numbers[2]), "pvp": float(clean_numbers[3])}
		if peso_min is not None and peso_max is not None:
			result["peso mínimo"] = peso_min
			result["peso máximo"] = peso_max
		return result
	else:
		return {}