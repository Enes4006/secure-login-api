'''
import bcrypt
import jwt
import datetime
from fastapi import HTTPException

# Bu dosya kimlik doğrulama işlemlerini yönetir.
# - Parola karma üretme ve doğrulama
# - JWT oluşturma ve doğrulama
# Bu yöntemler API'de kayıt, giriş ve yetkilendirme için kullanılır.

# Uygulamanın JWT imzası için kullanılan gizli anahtar.
SECRET = "supersecretkey"

def hash_password(password: str):
    # Kullanıcının şifresini güvenli şekilde karma hale getirir.
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes):
    # Girilen şifreyi saklanan karma ile karşılaştırır.
    return bcrypt.checkpw(password.encode(), hashed)

def create_token(username: str):
    # Kullanıcı adıyla JWT oluşturur. Token 30 dakika sonra geçersiz olur.
    return jwt.encode(
        {
            "user": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        },
        SECRET,
        algorithm="HS256"
    )

def verify_token(token: str):
    # JWT'yi doğrular ve içindeki kullanıcı adını döner.
    # Geçersiz veya süresi dolmuş token durumunda 401 hatası döner.
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["user"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
'''




import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv() #.env dosyasını yükler


SECRET = os.getenv("SECRET_KEY") # .env dosyasından gizli anahtarı alır
ALGORITHM = os.getenv("ALGORITHM") # JWT imzalama algoritması

def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes):
    return bcrypt.checkpw(password.encode(), hashed)

def create_token(username: str):
    # utcnow yerine güncel kullanım
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    return jwt.encode(
        {"user": username, "exp": expire},
        SECRET,
        algorithm="HS256"
    )

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["user"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token süresi dolmuş")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Geçersiz token")