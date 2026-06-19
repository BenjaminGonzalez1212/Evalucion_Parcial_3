FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r docker/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "dashboards/ejecutivo.py", "--server.address=0.0.0.0"]