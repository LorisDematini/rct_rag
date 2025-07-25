"""
exact_builder.py

Module de construction du moteur, on extrait ici les sections disponibles dans les documents.

Fonction :
- get_available_sections(documents) :
    Parcourt les documents et retourne la liste triée des noms de sections uniques trouvées.
"""

#Récupération des sections disponible pour la création du moteur
def get_available_sections(documents):
    sections = set()
    for doc in documents:
        section = doc.metadata.get("section_name", "").strip()
        if section:
            sections.add(section)
    return sorted(sections)
