# exact_search_engine.py

import re

class ExactSearchEngine:
    def __init__(self, index):
        self.documents = index.documents

    def search(self, query, selected_sections = None):
        #Requête
        query_lower = query.lower()
        results = []

        #On récupère le contenu
        for doc in self.documents:
            content = doc.page_content.lower()
            section = doc.metadata.get("section_name", "").lower()

            #On filtre la section voulue ou l'ensemble
            if selected_sections:
                if section not in [s.lower() for s in selected_sections]:
                    continue

            #Crée la sortie avec les résultats
            if query_lower in content:
                count = len(re.findall(re.escape(query_lower), content))
                results.append({
                    "study_id": doc.metadata.get("study_id", "ID inconnu"),
                    "section_name": doc.metadata.get("section_name", "UNKNOWN"),
                    "score": count,
                    "document": doc
                })

        #Sortie en affichage en décroissant
        sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
        return sorted_results
