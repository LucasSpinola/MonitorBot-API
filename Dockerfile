#It instructs Docker Engine to use official python:3.10 as the base image
FROM python:3.10

#It creates a working directory(app) for the Docker image and container
WORKDIR /app

#It copies the framework and the dependencies for the FastAPI application into the working directory
COPY requirements.txt .

# It will install setuptools
RUN pip install --upgrade pip setuptools

#It will install the framework and the dependencies in the `requirements.txt` file.
RUN pip install -r requirements.txt

RUN python -m spacy download pt_core_news_md

#It will copy the remaining files and the source code from the host `fast-api` folder to the `app` container working directory
COPY . .

#It will expose the FastAPI application on port `8000` inside the container
EXPOSE 8000

#It is the command that will start and run the FastAPI application container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]