import re

class ExactSearchEngine:
    def __init__(self, index):
        self.documents = index.documents

    def parse_query(self, query):
        query = query.strip().lower()

        # Découpe sur OR
        or_parts = [part.strip() for part in query.split(" or ")]
        parsed = []

        for part in or_parts:
            if " and " in part:
                and_terms = [term.strip() for term in part.split(" and ")]
                parsed.append({"operator": "AND", "terms": and_terms})
            else:
                parsed.append({"operator": "PHRASE", "terms": [part]})

        # OR global si nécessaire
        if len(parsed) == 1:
            return parsed[0]
        else:
            return {"operator": "OR", "subqueries": parsed}

    def term_to_regex(self, term):
        if term.endswith("*"):
            return rf"\b{re.escape(term[:-1])}\w*\b"
        else:
            return rf"\b{re.escape(term)}\b"


    def search(self, query, selected_sections=None):
        parsed = self.parse_query(query)
        results = []

        for doc in self.documents:
            content = doc.page_content.lower()
            section = doc.metadata.get("section_name", "").lower()

            if selected_sections and section not in [s.lower() for s in selected_sections]:
                continue

            match, score = self.evaluate(parsed, content)
            if match:
                results.append({
                    "study_id": doc.metadata.get("study_id", "ID inconnu"),
                    "section_name": doc.metadata.get("section_name", "UNKNOWN"),
                    "score": score,
                    "document": doc
                })

        return sorted(results, key=lambda x: x["score"], reverse=True)

    def evaluate(self, parsed, content):
        operator = parsed["operator"]

        if operator == "PHRASE":
            term = parsed["terms"][0]
            pattern = re.compile(self.term_to_regex(term))
            matches = pattern.findall(content)
            return (len(matches) > 0, len(matches))

        elif operator == "AND":
            terms = parsed["terms"]
            all_match = True
            total_matches = 0
            for term in terms:
                pattern = re.compile(self.term_to_regex(term))
                matches = pattern.findall(content)
                if not matches:
                    all_match = False
                    break
                total_matches += len(matches)
            return (all_match, total_matches if all_match else 0)

        elif operator == "OR":
            total_score = 0
            any_match = False
            for subquery in parsed["subqueries"]:
                match, score = self.evaluate(subquery, content)
                if match:
                    any_match = True
                    total_score += score
            return (any_match, total_score)

        return (False, 0)

