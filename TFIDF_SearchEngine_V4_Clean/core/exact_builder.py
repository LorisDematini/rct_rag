#exact_builder.py

def get_available_sections(documents):
    sections = set()
    for doc in documents:
        section = doc.metadata.get("section_name", "").strip()
        if section:
            sections.add(section)
    return sorted(sections)
