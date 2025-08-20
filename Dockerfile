FROM python:3.12.3

#Folder in docker for the app
WORKDIR /app

#Copy in the folder the dependences
COPY pyproject.toml poetry.lock* ./

#Install poetry to install requirements
RUN pip install poetry

#Install requirements
RUN poetry config virtualenvs.create false && poetry install --no-root

#Install nltk data 
RUN python -m nltk.downloader -d /usr/share/nltk_data punkt wordnet stopwords averaged_perceptron_tagger omw-1.4
ENV NLTK_DATA=/usr/share/nltk_data

#Copy folders needed for the app
COPY search_engine/ ./search_engine/ 
COPY builder/data/ ./builder/data/

#Launch the app
CMD ["streamlit", "run", "search_engine/main.py", "--server.port=8080", "--server.address=0.0.0.0"]