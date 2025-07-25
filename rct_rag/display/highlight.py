"""
highlight.py

Fonctions utilitaires pour la mise en évidence (highlight) de la requête dans la sortie, en fonction des types de recherche utilisés (sparse ou exacte).

Fonctions :
- highlight_text_sparse(text, raw_query, cleaned_query) :
    Surligne tous les mots présents dans la requête brute et nettoyée, pour la recherche TF-IDF.
- highlight_text_exact(text, query, mode="PHRASE") :
    Surligne les termes de la requête exacte, en mode PHRASE (exact ou avec wildcard '*'),
    ou en mode booléen AND/OR.

Les mots trouvés sont encadrés avec la balise HTML <mark> pour un affichage visuel dans Streamlit.
"""

import re

#On trouve tous les mot clés de la requête avant et après preprocessed pour ne pas en rater
def highlight_text_sparse(text, raw_query, cleaned_query):
    keywords = set()
    keywords.update(re.findall(r"\b\w+\b", raw_query.lower()))
    keywords.update(re.findall(r"\b\w+\b", cleaned_query.lower()))

    for word in sorted(keywords, key=len, reverse=True):
        pattern = re.compile(rf"(\b{re.escape(word)}\b)", flags=re.IGNORECASE)
        text = pattern.sub(r"<mark>\1</mark>", text)
    return text

#On surligne en fonction de la requête demandé
def highlight_text_exact(text, query, mode="PHRASE"):
    #Si normal, on vérifie la présence d'un wildcard et surligne en fonction le texte
    if mode == "PHRASE":
        if query.endswith("*"):
            prefix = re.escape(query[:-1])
            pattern = re.compile(rf"\b({prefix}\w*)\b", flags=re.IGNORECASE)
        else:
            pattern = re.compile(rf"\b({re.escape(query)})\b", flags=re.IGNORECASE)
        return pattern.sub(r"<mark>\1</mark>", text)

    #On retire les AND et OR 
    elif mode in ("AND", "OR"):
        terms = [t.strip() for t in re.split(r"\s+(and|or)\s+", query.lower()) if t.lower() not in {"and", "or"}]
        for word in sorted(terms, key=len, reverse=True):
            if word.endswith("*"):
                prefix = re.escape(word[:-1])
                pattern = re.compile(rf"\b({prefix}\w*)\b", flags=re.IGNORECASE)
            else:
                pattern = re.compile(rf"\b({re.escape(word)})\b", flags=re.IGNORECASE)
            text = pattern.sub(r"<mark>\1</mark>", text)
    return text
