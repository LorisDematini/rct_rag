"""
processed_dense.py

Ce module fournit la classe `TextPreprocessor` pour normaliser et nettoyer les textes utilisés dans
le moteur de recherche dense et éventuellement dans d'autres composants du système.

Fonctionnalités :
- Remplacement d'acronymes selon un dictionnaire JSON (chargé depuis `ACRONYMS_FILE`).
- Standardisation de termes temporels (ex. : "D10" → "Day 10", "W2" → "Week 2").
- Nettoyage des caractères spéciaux (retours à la ligne, tabulations, espaces multiples).

Classe :
- TextPreprocessor :
    - replace_acronyms(text) : remplace les acronymes par leurs définitions.
    - replace_special_terms(text) : reformule les expressions temporelles + nettoyage.
    - preprocess(text) : applique tous les traitements sur un texte brut.

"""


import json
import re
from typing import Dict, List, Union
# from config.paths import ACRONYMS_FILE
ACRONYMS_FILE = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/POC/Clean/Search_engine/data/final_acronyms.json"

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