import re
from functions.tarifas_parser import parse_tarifas
from functions.extra_data_parser import parse_extra_data
from functions.dict_merger import merge_dicts

def detect_section(pages: list, main_keywords: list):
	data = {}
	current_section = None
	current_sub1 = None
	match = False
	same_info = False
	tipo = {}
	for page in pages:
		for table in page:
			for line in table:
				match = False
				for kw in main_keywords:
					if re.search(kw, line) and kw not in data:
						current_sub1 = None
						data[kw] = {}
						current_section = kw
						match = True
						break
				# Detect section headers by checking if the line is title-cased or matches a header pattern
				if (line.isupper()) and not match and current_section:
					if current_section is not None and line not in data[current_section]:
						current_sub1 = line
						data[current_section][current_sub1] = []
				elif not line.isupper() and not match and current_section is not None and current_sub1 is not None:
					tarifas = parse_tarifas(line)
					if tarifas:
						if tipo:
							tarifas = merge_dicts(tarifas, tipo)
						data[current_section][current_sub1].append(tarifas)
						same_info = False
					else:
						extra_data = parse_extra_data(line)
						if extra_data:
							if (
								data[current_section][current_sub1]
								and isinstance(data[current_section][current_sub1][-1], dict)
								and "info" in data[current_section][current_sub1][-1]
								and "info" in extra_data
							):
								data[current_section][current_sub1][-1] = merge_dicts(
									data[current_section][current_sub1][-1], extra_data
								)
							else:
								data[current_section][current_sub1].append(extra_data)
							same_info = True
							if "lanoicanretni" in line.lower():
								tipo = {"tipo": "Internacional"}
							elif "lanoican" in line.lower():
								tipo = {"tipo": "Nacional"}

						
	return data