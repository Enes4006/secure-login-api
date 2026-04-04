import logging
import sys

# Log formatı: Zaman - Log Seviyesi - Mesaj
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# 1. Logger nesnesini oluştur
logger = logging.getLogger("my_api_logger")
logger.setLevel(logging.INFO)

# 2. Dosyaya yazma ayarı (app.log dosyasına ekleyerek gider)
file_handler = logging.FileHandler("app.log", encoding="utf-8")
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# 3. Terminale (Konsola) yazma ayarı
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# 4. Ayarları logger'a ekle
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.propagate = False # Logların FastAPI'nin kendi loglarıyla karışmasını engeller