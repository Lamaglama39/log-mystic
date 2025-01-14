# app/Dockerfile

FROM python:3.9-slim

WORKDIR /src

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install streamlit woothee matplotlib pycountry user_agents requests

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "./app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
