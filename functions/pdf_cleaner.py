def clean_pdf_text(pdf_pages: list) -> list:
	cleaned_pages = []
	for page in pdf_pages:
		cleaned = [line.strip().replace("  ", " ") for line in page if line.strip()]
		cleaned_pages.append(cleaned)
	return cleaned_pages