# 🚀 Kurum Arıza Takip Sistemi

Bu proje, kurumsal sistemlerde meydana gelen **arıza bildirimlerinin** hızlı, güvenli ve sınıflandırılmış şekilde yönetilmesini sağlayan bir **web uygulamasıdır**.  
Sistem sayesinde arızalar etkin şekilde takip edilir ve yönetim süreçleri optimize edilir.

## 🎯 Proje Amacı

Bu sistem, kurum içindeki teknik arıza süreçlerini daha **hızlı**, **şeffaf** ve **veriye dayalı** şekilde yönetebilmek amacıyla geliştirilmiştir.  
Kullanıcı, teknisyen ve yönetici rollerine göre özelleştirilmiş paneller sunarak **farklı kullanıcı deneyimleri** sağlamaktadır.

## 🛠️ Kullanılan Teknolojiler

- **Django** (Python Web Framework)
- **Django REST Framework**
- **React.js** (Frontend framework)
- **TailwindCSS v3.3.0** (Modern CSS framework)
- **PostgreSQL** (İlişkisel veritabanı yönetim sistemi)
- **JWT** (JSON Web Token - Kimlik doğrulama)
- **NLP** (Doğal Dil İşleme) destekli otomatik sınıflandırma
- **Rol bazlı yetkilendirme sistemi**
- **MQTT** (Mesajlaşma protokolü - IoT entegrasyonu) *(Kullanıldıysa, istersen çıkarabiliriz)*

## ⚙️ Özellikler

- Hızlı ve güvenli arıza bildirim takibi
- NLP destekli otomatik kategori ve öncelik belirleme
- Kullanıcı, teknisyen ve yönetici için özelleştirilmiş arayüzler
- JWT tabanlı kimlik doğrulama ve yetkilendirme
- RESTful API mimarisi ile geliştirilen backend
- Gerçek zamanlı veri iletimi (MQTT entegrasyonu ile)
- Modern ve kullanıcı dostu frontend

## 🚀 Kurulum ve Kullanım

### Backend (Django)
```bash
git clone https://github.com/ayse-erdogan/KurumArizaTakip.git
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
