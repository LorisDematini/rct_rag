FROM python:3.12.3

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && poetry install --no-root

RUN python -m nltk.downloader -d /usr/share/nltk_data punkt wordnet stopwords averaged_perceptron_tagger omw-1.4
ENV NLTK_DATA=/usr/share/nltk_data

COPY search_engine/ ./search_engine/ 
COPY builder/ ./builder/
COPY assets/ ./assets/
COPY site/ ./site/
COPY docs/ ./docs/

# Lancer l'app Streamlit
CMD ["streamlit", "run", "search_engine/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
