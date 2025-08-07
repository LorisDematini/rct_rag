import re

def parse_query(query):
    """
    Parses a raw query string into a structured logical representation.

    Supports:
    - Single terms or phrases
    - Boolean operators: "AND", "OR"
    - Wildcards with "*"
    
    Args:
        query (str): The user input query.

    Returns:
        dict: Parsed query structure.
    """
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


def term_to_regex(term):
    """
    Converts a search term into a regex pattern.
    Supports wildcard '*' at the end of a word (e.g., "therap*").

    Args:
        term (str): The raw search term.

    Returns:
        str: Regex pattern to match the term.
    """
    return rf"\b{re.escape(term[:-1])}\w*\b" if term.endswith("*") else rf"\b{re.escape(term)}\b"


def evaluate(parsed, content):
    """
    Evaluates a parsed query against a text content.

    Args:
        parsed (dict): Parsed query structure.
        content (str): The text to search within (lowercase).

    Returns:
        tuple:
            - match (bool): True if the content satisfies the query.
            - score (int): Number of term matches (used for ranking).
    """
    operator = parsed["operator"]

    if operator == "PHRASE":
        term = parsed["terms"][0]
        pattern = re.compile(term_to_regex(term))
        matches = pattern.findall(content)
        return (len(matches) > 0, len(matches))

    elif operator == "AND":
        total_matches = 0
        for term in parsed["terms"]:
            pattern = re.compile(term_to_regex(term))
            matches = pattern.findall(content)
            if not matches:
                return (False, 0)
            total_matches += len(matches)
        return (True, total_matches)

    elif operator == "OR":
        total_score = 0
        any_match = False
        for subquery in parsed["subqueries"]:
            match, score = evaluate(subquery, content)
            if match:
                any_match = True
                total_score += score
        return (any_match, total_score)

    return (False, 0)  # Fallback in case of unknown operator


def search_ex(documents, query, selected_sections=None):
    """
    Performs an exact keyword search on a list of documents.

    Args:
        documents (list): List of LangChain Document objects to search through.
        query (str): User input query string.
        selected_sections (list, optional): List of section names to restrict search to.
                                            If None, all sections are searched.

    Returns:
        list: Search results as a list of dictionaries, sorted by match score (descending).
              Each result includes:
                - study_id
                - section_name
                - score
                - document (LangChain Document)
    """
    parsed = parse_query(query)
    results = []

    for doc in documents:
        content = doc.page_content.lower()
        section = doc.metadata.get("section_name", "").lower()

        # Skip if section filtering is enabled and current section is not selected
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

    # Sort results by descending score
    return sorted(results, key=lambda x: x["score"], reverse=True)
