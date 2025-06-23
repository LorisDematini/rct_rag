from typing import List
from langchain.schema import Document

class ExactIndex:
    def __init__(self, documents: List[Document]):
        self.documents = documents

    def get_available_sections(self) -> List[str]:
        sections = set()
        for doc in self.documents:
            section = doc.metadata.get("section_name", "").strip()
            if section:
                sections.add(section)
        return sorted(sections)
