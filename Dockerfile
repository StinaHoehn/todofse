# Basis-Image mit Python
FROM python:3.8

# Arbeitsverzeichnis festlegen
WORKDIR /app

COPY requirements.txt ./

# Installieren der Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren des gesamten Projektverzeichnisses in den Container
COPY . .

# Port freigeben
EXPOSE 5001

CMD ["python", "app.py"]
