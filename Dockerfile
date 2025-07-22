FROM python:3.12.3

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && poetry install --no-root

RUN python -m nltk.downloader -d /usr/share/nltk_data punkt wordnet stopwords averaged_perceptron_tagger omw-1.4
ENV NLTK_DATA=/usr/share/nltk_data

COPY TFIDF_SearchEngine_V4_Clean/ ./TFIDF_SearchEngine_V4_Clean/ 
COPY assets/ ./assets/
COPY site/ ./site/
COPY docs/ ./docs/

# Lancer l'app Streamlit
CMD ["streamlit", "run", "TFIDF_SearchEngine_V4_Clean/src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
