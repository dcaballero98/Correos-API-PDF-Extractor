import re 

def parse_extra_data(line: str):
	result = {}
	if "lanoicanretni" in line.lower():
		result = {"tipo": "Internacional"}
	elif "lanoican" in line.lower():
		result = {"tipo": "Nacional"}
	elif "Tarifas Correos 2025. Península y Baleares.".lower() in line.lower():
		result = {}
	elif "Índice".lower() in line.lower():
		result = {}
	else:
		result = {"info": line}
	return result