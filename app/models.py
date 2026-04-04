'''

from pydantic import BaseModel

# Bu dosya, API'ye gelen kullanıcı verilerini doğrulamak için kullanılan veri modellerini tanımlar.
# Pydantic BaseModel sınıfını kullanarak alan türlerini belirler ve gelen JSON verisinin
# doğru tipte olup olmadığını kontrol eder.

class UserRegister(BaseModel):
    # Kayıt sırasında gönderilen kullanıcı adı
    username: str
    # Kayıt sırasında gönderilen şifre
    password: str

class UserLogin(BaseModel):
    # Giriş sırasında gönderilen kullanıcı adı
    username: str
    # Giriş sırasında gönderilen şifre
    password: str

'''
    

from pydantic import BaseModel, Field, field_validator
import re

# Bu model, yeni bir kullanıcı kayıt olurken gönderilen verileri doğrular.
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="Kullanıcı adı 3-20 karakter olmalı")
    password: str = Field(..., min_length=8, description="Şifre en az 8 karakter olmalı")

    # Şifre karmaşıklığı için özel bir doğrulayıcı (Validator)
    @field_validator('password')
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if not re.search(r'\d', v):
            raise ValueError('Şifre en az bir rakam içermelidir.')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Şifre en az bir büyük harf içermelidir.')
        return v

# Bu model, sadece giriş yapmak isteyen kullanıcıdan alınan verileri doğrular.
# Kayıttaki kadar katı kurallara (büyük harf vb.) burada gerek yoktur, 
# çünkü zaten kayıtlı olan bir veriyi kontrol edeceğiz.
class UserLogin(BaseModel):
    username: str
    password: str