import re

def index_sections(text: str, main_kw: list) -> list:
	sections = []
	for kw in main_kw:
		match = re.search(kw, text, re.IGNORECASE)
		if match:
			sections.append((match.group(), match.start()))
	sections.sort(key=lambda x: x[1])
	return sections

def get_subsection(text: str, sections: list, main_kw: str, sub_kw: str) -> list:
	try:
		start_idx = next(start for sec, start in sections if sec.lower() == main_kw.lower())
	except StopIteration:
		return ["Nada"]
	next_start = len(text)
	for sec, s in sections:
		if s > start_idx:
			next_start = s
			break
	section_text = text[start_idx:next_start]
	pattern = re.compile(rf'.*{sub_kw}.*', re.IGNORECASE)
	return pattern.findall(section_text)