FROM python:3.10-slim

RUN apt-get update && apt-get install --no-install-recommends -y curl

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/Home.py", "--server.port=8501", "--server.address=0.0.0.0"]