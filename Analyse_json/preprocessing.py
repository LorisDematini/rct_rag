import json
import re
import unicodedata
from nltk.corpus import stopwords
import nltk

# Télécharger les stopwords
nltk.download('stopwords')

class TextPreprocessor:
    def __init__(self, acronyms_file):
        self.stop_words = set(stopwords.words('english')).union({
            'patient', 'patients', 'study', 'studies', 'treatment', 'trial', 'clinical'  # Termes trop fréquents à enlever
        })
        
        # Charger les acronymes à partir du fichier
        with open(acronyms_file, 'r', encoding='utf-8') as f:
            self.acronyms = json.load(f)
        
    def normalize_text(self, text):
        if not isinstance(text, str):
            return ""
        
        # Convertit en minuscules
        text = text.lower()
        # Normalisation Unicode
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        # Suppression de la ponctuation
        text = re.sub(r'[^\w\s]', ' ', text)
        # Nettoyage des espaces
        text = re.sub(r'\s+', ' ', text).strip()

        # Filtrage des stopwords
        words = text.split()
        filtered_words = [word for word in words if word not in self.stop_words]
        return ' '.join(filtered_words)
    
    def replace_acronyms(self, text):
        """
        Remplace les acronymes trouvés dans le texte par leur définition.
        """
        for acronym, definition in self.acronyms.items():
            # Remplace tous les acronymes par leur définition, en ignorant la casse
            pattern = r'\b' + re.escape(acronym.lower()) + r'\b'
            text = re.sub(pattern, definition.lower(), text)
        return text

    def replace_special_terms(self, text):
        """
        Remplace les termes comme d0, d7, m12, w1 par leur version complète (jusqu'à 100).
        """
        text = re.sub(r'\bd(\d{1,2}|100)\b', r'day \1', text)  # d0, d7, ..., d100 -> day 0, day 7, ..., day 100
        text = re.sub(r'\bm(\d{1,2}|100)\b', r'month \1', text)  # m12, m50, ..., m100 -> month 12, month 50, ..., month 100
        text = re.sub(r'\bw(\d{1,2}|100)\b', r'week \1', text)   # w1, w20, ..., w100 -> week 1, week 20, ..., week 100
        return text


def process_and_merge_json(input_path, output_path, acronyms_file):
    preprocessor = TextPreprocessor(acronyms_file)
    
    # Charger le fichier JSON d'origine
    with open(input_path, 'r', encoding='utf-8') as f:
        original_data = json.load(f)
    
    # Créer la nouvelle structure avec texte fusionné
    merged_data = {}
    
    for study_id, sections in original_data.items():
        merged_study = {}
        
        for section_name, paragraphs in sections.items():
            # Fusionner les paragraphes et appliquer le prétraitement
            merged_text = "".join(paragraphs)
            processed_text = preprocessor.normalize_text(merged_text)
            
            # Remplacer les acronymes dans le texte
            processed_text_with_acronyms = preprocessor.replace_acronyms(processed_text)
            
            # Appliquer les remplacements des termes spéciaux (d0, m12, etc.)
            processed_text_with_special_terms = preprocessor.replace_special_terms(processed_text_with_acronyms)
            
            # Ne garder que les sections non vides
            if processed_text_with_special_terms:  # Ceci élimine les chaînes vides ""
                merged_study[section_name] = processed_text_with_special_terms
        
        # Ne garder que les études qui ont au moins une section non vide
        if merged_study:
            merged_data[study_id] = merged_study
    
    # Sauvegarder le nouveau JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)
    
    print(f"Traitement terminé. Fichier sauvegardé sous : {output_path}")


# Exemple d'utilisation
input_json = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/grouped_titles2.json"
output_json = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/grouped_titles_preprocessed.json"
acronyms_file = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/analysis/Acronyme/final_acronyms.json"

process_and_merge_json(input_json, output_json, acronyms_file)
