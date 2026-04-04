# Basit bir sahte veritabanı olarak görev yapan boş bir sözlük.
# Kullanıcı bilgilerini bellekte tutmak için kullanılır.
#fake_db = {}

'''
from sqlalchemy import create_dotenv_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserTable(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Tabloları oluştur
Base.metadata.create_all(bind=engine)
'''


'''
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite veritabanı dosyası adı: sql_app.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Veritabanındaki 'users' tablosu
class UserTable(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Tabloları fiziksel olarak oluşturur
Base.metadata.create_all(bind=engine)

# Veritabanı bağlantısını açıp kapatan yardımcı fonksiyon (Dependency)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


'''
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Veritabanı URL'sini .env'den al, eğer yoksa varsayılan olarak sqlite kullan
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# SQLite için özel bir ayar (check_same_thread), diğer DB'lerde sorun çıkarmaz
engine_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Veritabanındaki 'users' tablosu
class UserTable(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Tabloları fiziksel olarak oluşturur
Base.metadata.create_all(bind=engine)

# Veritabanı bağlantısını yöneten Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()