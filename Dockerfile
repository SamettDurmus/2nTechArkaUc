FROM python:3.10-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli dosyaları kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Django sunucusunu başlat
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
