"""
exact_search.py

Module de traitement et d'exécution des recherches exactes sur un corpus textuel.

Fonctions principales :
- parse_query(query) :
    Analyse une requête utilisateur simple supportant les opérateurs booléens AND, OR,
    et les wildcards en fin de terme.

- term_to_regex(term) :
    Convertit un terme avec ou sans joker en expression régulière adaptée.

- evaluate(parsed, content) :
    Évalue la présence des termes de la requête dans un contenu donné, selon l'opérateur,
    et renvoie un booléen de correspondance et un score basé sur le nombre d’occurrences.

- exact_search(documents, query, selected_sections=None) :
    Applique la recherche exacte sur une liste de documents, optionnellement filtrée par sections,
    retourne la liste des résultats triés par score décroissant.
"""
import re

#Vérification et Réécriture pour AND et OR
def parse_query(query):
    query = query.strip().lower()
    or_parts = [part.strip() for part in query.split(" or ")]
    parsed = []

    for part in or_parts:
        if " and " in part:
            and_terms = [term.strip() for term in part.split(" and ")]
            parsed.append({"operator": "AND", "terms": and_terms})
        else:
            parsed.append({"operator": "PHRASE", "terms": [part]})

    return parsed[0] if len(parsed) == 1 else {"operator": "OR", "subqueries": parsed}

#WildCard, on crée un regex pour trouver les complétion du mot
def term_to_regex(term):
    return rf"\b{re.escape(term[:-1])}\w*\b" if term.endswith("*") else rf"\b{re.escape(term)}\b"

#On fait par types d'opérateur et ça retourne un tuple (bool, int)
def evaluate(parsed, content):
    operator = parsed["operator"]
    #PHRASE : normal. Si c'est normal alors on cherche juste si le contenu existe et le nombre d'itérations
    if operator == "PHRASE":
        term = parsed["terms"][0]
        pattern = re.compile(term_to_regex(term))
        matches = pattern.findall(content)
        return (len(matches) > 0, len(matches))
    
    #AND : On vérifie si tous les différents termes existent et la somme 
    elif operator == "AND":
        total_matches = 0
        for term in parsed["terms"]:
            pattern = re.compile(term_to_regex(term))
            matches = pattern.findall(content)
            if not matches:
                return (False, 0)
            total_matches += len(matches)
        return (True, total_matches)

    #OR : On vérifie si au moins une des différentes parties existent et la somme 
    elif operator == "OR":
        total_score = 0
        any_match = False
        for subquery in parsed["subqueries"]:
            match, score = evaluate(subquery, content)
            if match:
                any_match = True
                total_score += score
        return (any_match, total_score)

    return (False, 0)

#Fonction principale qui appellent toutes les autres
def exact_search(documents, query, selected_sections=None):
    parsed = parse_query(query)
    results = []

    for doc in documents:
        content = doc.page_content.lower()
        section = doc.metadata.get("section_name", "").lower()

        if selected_sections and section not in [s.lower() for s in selected_sections]:
            continue

        match, score = evaluate(parsed, content)
        if match:
            results.append({
                "study_id": doc.metadata.get("study_id", "ID inconnu"),
                "section_name": doc.metadata.get("section_name", "UNKNOWN"),
                "score": score,
                "document": doc
            })

    return sorted(results, key=lambda x: x["score"], reverse=True)
