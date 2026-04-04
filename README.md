🛡️ Secure FastAPI Authentication System
Bu proje, modern web standartlarına uygun, güvenliği ön plana alan bir Kullanıcı Kayıt ve Yetkilendirme (Authentication & Authorization) sistemidir. Sadece bir API olmanın ötesinde; şifreleme, kalıcı veri saklama ve kurumsal hata izleme mekanizmalarını içerir.

FastAPI kullanarak geliştirdiğim bu sistemde, güvenli bir login akışı için şifreleri Bcrypt ile hashliyorum. Kullanıcı doğrulamasının ardından JWT (JSON Web Token) üreterek "Protected" (Korumalı) endpointlerde token doğrulaması yapıyorum. Ayrıca sistem güvenliğini artırmak adına Rate Limiting ve HTTPS uyumlu yapılandırmalar kullanılmıştır.

🚀 Projenin İşlevleri
Kullanıcı Kaydı: Pydantic ile veri doğrulaması (şifre karmaşıklığı, uzunluk vb.) yapılarak yeni kullanıcı oluşturma.

Güvenli Giriş: Bcrypt ile şifrelerin hash'lenmiş (tuzlanmış) haliyle kontrol edilmesi.

JWT Yetkilendirme: Başarılı girişte 30 dakika geçerli Bearer Token üretimi.

Korumalı Rotalar: Sadece geçerli token'a sahip kullanıcıların erişebildiği özel uç noktalar.

Kalıcı Veritabanı: SQLite ve SQLAlchemy (ORM) ile verilerin dosya sisteminde güvenle saklanması.

Hata Günlüğü (Logging): Uygulama hatalarının ve önemli olayların hem konsolda hem de app.log dosyasında tarihli olarak tutulması.

Frontend Entegrasyonu: Saf JavaScript ile yazılmış, API ile tam uyumlu çalışan kullanıcı arayüzü.

CORS & Middleware: Farklı kaynaklardan gelen istekleri güvenli bir şekilde yöneten Middleware katmanı.

🛠️ Kullanılan Teknolojiler
Framework: FastAPI (Python)

Veritabanı: SQLite & SQLAlchemy (ORM)

Güvenlik: JWT (PyJWT), Bcrypt (Password Hashing)

Doğrulama: Pydantic (Data Validation)

Ortam Yönetimi: Dotenv (.env configuration)

Sunucu: Uvicorn & Docker

Lokalde Çalıştırma:
''' bash
uvicorn app.main:app --reload
'''

API Dokümantasyonu: http://127.0.0.1:8000/docs

Docker ile Çalıştırma:
''' bash
docker build -t secure-login-api .
docker run -d --name api-container -p 8000:8000 secure-login-api
'''

🧠 Bu Projede Neler Öğrendim?
Bu projeyi geliştirirken aşağıdaki kritik backend kavramlarını deneyimledim:

Güvenlik Protokolleri: Şifrelerin asla açık metin olarak saklanmaması gerektiğini ve Bcrypt ile tek yönlü hash'leme mantığını öğrendim.

Stateless Auth: JWT kullanarak, sunucuda oturum (session) tutmadan kullanıcının nasıl doğrulanacağını kavradım.

Dependency Injection: FastAPI'nin Depends yapısını kullanarak veritabanı bağlantılarını ve güvenlik şemalarını profesyonelce yönetmeyi öğrendim.

Middleware & CORS: Tarayıcı güvenliği için CORS hatalarını Middleware kullanarak nasıl çözeceğimi ve istekleri nasıl filtreleyeceğimi deneyimledim.

Clean Code & Architecture: Kodu; modeller, kimlik doğrulama, veritabanı ve logger olarak parçalara ayırmanın (Separation of Concerns) sürdürülebilirlik için önemini gördüm.

Hata İzleme: logging modülü ile "Nerede hata oluştu?" sorusuna hızlıca cevap bulabilmek için profesyonel günlük tutmayı öğrendim.

Dockerization: Bir uygulamayı tüm bağımlılıklarıyla paketleyip her ortamda aynı şekilde çalışmasını sağlamayı öğrendim.
