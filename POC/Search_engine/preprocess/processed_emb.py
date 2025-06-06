import json
import re
from typing import Dict, List, Union
from config.paths import ACRONYMS_FILE

class TextPreprocessor:
    def __init__(self, acronym_json_path=ACRONYMS_FILE):
        with open(acronym_json_path, "r", encoding="utf-8") as f:
            self.acronyms = json.load(f)

    def replace_acronyms(self, text: str) -> str:
        for acronym, definition in self.acronyms.items():
            pattern = r'\b' + re.escape(acronym) + r'\b'
            text = re.sub(pattern, definition, text, flags=re.IGNORECASE)
        return text

    def replace_special_terms(self, text: str) -> str:
        # Remplacer les termes spéciaux comme "Day 10", "Week 2", etc.
        text = re.sub(r'\b[Dd](\d{1,2}|100)\b', r'Day \1', text)
        text = re.sub(r'\b[Ww](\d{1,2}|100)\b', r'Week \1', text)
        text = re.sub(r'\b[Mm](\d{1,2}|100)\b', r'Month \1', text)
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')  # Nettoyer les sauts de ligne
        text = re.sub(r'\s+', ' ', text).strip()  # Réduire les espaces multiples
        return text

    def preprocess(self, text: str) -> str:
        # Appliquer le remplacement des acronymes et des termes spéciaux
        text = self.replace_acronyms(text)
        text = self.replace_special_terms(text)
        return text

    def preprocess_json_data(self, data: Dict[str, List[Union[List[str], str]]]) -> Dict[str, List]:
        processed_data = {}
        for study_name, content_list in data.items():
            new_content = []
            for entry in content_list:
                if isinstance(entry, list) and len(entry) == 2 and isinstance(entry[1], str):
                    new_content.append([entry[0], self.preprocess(entry[1])])
                else:
                    new_content.append(entry)
            processed_data[study_name] = new_content
        return processed_data

    def preprocess_json_file(self, input_path: str, output_path: str):
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        processed_data = self.preprocess_json_data(data)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)
        print(f"Prétraitement terminé. Résultat sauvegardé dans : {output_path}")
