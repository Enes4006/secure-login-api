'''

from fastapi import FastAPI, HTTPException, Header
from app.models import UserRegister, UserLogin
from app.auth import hash_password, verify_password, create_token, verify_token
from app.database import fake_db

# Bu modül API uç noktalarını tanımlar ve kimlik doğrulama akışını yönetir.
# Kayıt, giriş ve korumalı kaynaklara erişim için FastAPI route'ları içerir.
app = FastAPI()

# Ana sayfa endpoint'i. API'nin çalıştığını kontrol etmek için kullanılır.
@app.get("/")
def home():
    return {"message": "Secure API çalışıyor 🚀"}


# Kullanıcı kayıt endpoint'i.
# Gelen verileri UserRegister modeli ile doğrular ve şifreyi saklar.
@app.post("/register")
def register(user: UserRegister):
    if user.username in fake_db:
        raise HTTPException(status_code=400, detail="User already exists")

    # Parola hashlenir ve kullanıcı adı ile birlikte kayıt edilir.
    hashed = hash_password(user.password)
    fake_db[user.username] = hashed

    return {"message": "User created"}


# Kullanıcı giriş endpoint'i.
# Şifre kontrolü yapılır ve geçerliyse JWT döner.
@app.post("/login")
def login(user: UserLogin):
    if user.username not in fake_db:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(user.password, fake_db[user.username]):
        raise HTTPException(status_code=400, detail="Wrong password")

    # Giriş başarılıysa kullanıcı için JWT oluşturulur.
    token = create_token(user.username)
    return {"access_token": token}


# Korumalı endpoint. Authorization header içindeki Bearer token doğrulanır.
@app.get("/protected")
def protected(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    user = verify_token(token)

    return {"message": f"Hello {user}"}

'''

'''
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
#from models import UserRegister, UserLogin
#from auth import hash_password, verify_password, create_token, verify_token
#from database import fake_db

from .models import UserRegister, UserLogin
from .auth import hash_password, verify_password, create_token, verify_token
from .database import fake_db

app = FastAPI()
# Güvenlik şemasını tanımlıyoruz
security = HTTPBearer()

@app.get("/")
def home():
    return {"message": "Secure API çalışıyor 🚀"}

@app.post("/register")
def register(user: UserRegister):
    if user.username in fake_db:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = hash_password(user.password)
    fake_db[user.username] = hashed
    return {"message": "User created"}

@app.post("/login")
def login(user: UserLogin):
    if user.username not in fake_db:
        raise HTTPException(status_code=400, detail="User not found")
    if not verify_password(user.password, fake_db[user.username]):
        raise HTTPException(status_code=400, detail="Wrong password")
    
    token = create_token(user.username)
    return {"access_token": token, "token_type": "bearer"}

# KORUMALI ENDPOINT - YENİ YÖNTEM
@app.get("/protected")
def protected(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Artık manuel split işlemine gerek yok. 
    FastAPI 'Bearer' kelimesini kendisi ayıklar.
    """
    token = credentials.credentials # Sadece saf token'ı verir
    user = verify_token(token)
    return {"message": f"Hello {user}", "status": "authorized"}

'''
from fastapi import FastAPI, HTTPException, Depends,Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# Kendi dosyalarımızdan importlar
from .models import UserRegister, UserLogin
from .auth import hash_password, verify_password, create_token, verify_token
from .database import get_db, UserTable



app = FastAPI()
security = HTTPBearer()

# frontend ile iletişim için CORS middleware ekleyelim
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Geliştirme aşamasında her şeye izin verebiliriz
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    # Kullanıcı var mı kontrol et (Veritabanı sorgusu)
    db_user = db.query(UserTable).filter(UserTable.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten alınmış.")

    # Şifreyi hashle ve kaydet
    hashed = hash_password(user.password)
    new_user = UserTable(username=user.username, hashed_password=hashed)
    
    db.add(new_user)
    db.commit() # Veritabanına işle
    db.refresh(new_user)
    
    return {"message": "Kullanıcı başarıyla oluşturuldu", "id": new_user.id}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Kullanıcıyı bul
    db_user = db.query(UserTable).filter(UserTable.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Kullanıcı bulunamadı.")

    # Şifreyi doğrula (db_user.hashed_password veritabanından gelir)
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Hatalı şifre.")

    token = create_token(user.username)
    return {"access_token": token, "token_type": "bearer"}




from .logger import logger  # Logger'ı import et

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Bilgi logu
    logger.info(f"Giriş denemesi yapıldı: {user.username}")

    db_user = db.query(UserTable).filter(UserTable.username == user.username).first()
    
    if not db_user:
        # Hata logu
        logger.warning(f"Giriş başarısız: Kullanıcı bulunamadı ({user.username})")
        raise HTTPException(status_code=400, detail="Kullanıcı bulunamadı.")

    if not verify_password(user.password, db_user.hashed_password):
        logger.warning(f"Giriş başarısız: Yanlış şifre ({user.username})")
        raise HTTPException(status_code=400, detail="Hatalı şifre.")

    token = create_token(user.username)
    logger.info(f"Giriş başarılı: {user.username} için token üretildi.")
    return {"access_token": token, "token_type": "bearer"}



@app.get("/protected")
def protected(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_name = verify_token(token)
    return {"message": f"Hoş geldin {user_name}, veritabanından doğrulandın!"}

#-------------------------
# global exception handler ekleyelim

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Beklenmedik Hata: {str(exc)} | URL: {request.url}")
    return JSONResponse(
        status_code=500,
        content={"message": "Sunucu tarafında bir hata oluştu, teknik ekip bilgilendirildi."}
    )

# main.py
from .logger import logger # Kendi oluşturduğun nesneyi almalısın

@app.get("/")
def home():
    logger.info("Ana sayfa tetiklendi!") # logging.info değil, logger.info
    return {"message": "Hello"}