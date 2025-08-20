import json

def save_available_sections(documents, output_path):
    """
    Extracts the unique section names available in the given list of Documents,
    sorts them alphabetically, and saves the result to a JSON file.

    Args:
        documents (list): A list of LangChain Document objects with metadata containing 'section_name'.
        output_path (str): Path to the output JSON file that will store the list of section names.
    """
    sections = set()

    # Collect all unique section names from document metadata
    for doc in documents:
        section = doc.metadata.get("section_name", "").strip()
        if section:
            sections.add(section)

    # Sort the section names alphabetically
    sorted_sections = sorted(sections)

    # Save the list of section names to a JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_sections, f, ensure_ascii=False, indent=2)

    print(f"[INFO] Available sections saved to: {output_path}")
