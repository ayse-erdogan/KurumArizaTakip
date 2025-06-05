# Kurum Ar�za Takip Sistemi 
 
Bu proje, kurumsal sistemlerde meydana gelen ar�za bildirimlerinin h�zl�, g�venli ve s�n�fland�r�lm�� �ekilde y�netilebilmesini sa�layan bir web uygulamas�d�r. Django backend ile API altyap�s� sa�lanm��, React frontend ile kullan�c� dostu aray�z geli�tirilmi�tir. NLP destekli otomatik s�n�fland�rma ve rol bazl� yetkilendirme sistemleri entegre edilmi�tir. 
 
## ?? Kullan�lan Teknolojiler 

tailwindcss v3.3.0

Invalid command: CSS

Usage:
   tailwindcss <command> [options]

Commands:
   init [options]

Options:
   -h, --help               Display usage information

- PostgreSQL 
- JWT Authentication 
- MQTT protokol� ve sens�r entegrasyonu 
- NLP (Do�al Dil ��leme) ile otomatik �ncelik ve kategori belirleme 
 
## ?? Kurulum 
```bash 
# Backend i�in 
cd backend 
python -m venv env 
source env/Scripts/activate      # Windows i�in 
pip install -r requirements.txt 
python manage.py migrate 
python manage.py runserver 
``` 
 
```bash 
# Frontend i�in 
cd frontend 
npm install 
npm run dev 
``` 
 
 
## ??? Ekran G�r�nt�s� 
A�a��ya sistemin ekran g�r�nt�lerini ekleyebilirsiniz. 
``` 
![Aray�z](./screenshots/dashboard.png) 
``` 
 
## ?? Geli�tirici Notu 
Bu proje, 2025 y�l� bitirme projesi kapsam�nda geli�tirilmi�tir. Django ve React altyap�s� �zerinde detayl� bi�imde �al��ma f�rsat� sunmu�, do�al dil i�leme (NLP) ve JWT g�venlik sistemleriyle ileri seviye yaz�l�m teknikleri uygulanm��t�r. 
 
## ?? GitHub Sayfas� 
[Proje Linki](https://github.com/ayse-erdogan/KurumArizaTakip) 
