

# 1. Temel imaj olarak hafif bir Python sürümü kullan
FROM python:3.11-slim

# 2. Çalışma dizinini ayarla
WORKDIR /code

# 3. Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Tüm proje dosyalarını kopyala
COPY . .

# 5. Portu dış dünyaya aç (FastAPI varsayılan 8000)
EXPOSE 8000

# 6. Uygulamayı başlat
# Not: Docker içinde '0.0.0.0' kullanmak zorunludur, aksi takdirde dışarıdan erişilemez.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]