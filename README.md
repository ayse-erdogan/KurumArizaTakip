# Kurum Arçza Takip Sistemi 
 
Bu proje, kurumsal sistemlerde meydana gelen arçza bildirimlerinin hçzlç, gÅvenli ve sçnçflandçrçlmçü üekilde yînetilebilmesini saßlayan bir web uygulamasçdçr. Django backend ile API altyapçsç saßlanmçü, React frontend ile kullançcç dostu arayÅz geliütirilmiütir. NLP destekli otomatik sçnçflandçrma ve rol bazlç yetkilendirme sistemleri entegre edilmiütir. 
 
## ?? Kullançlan Teknolojiler 

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
- MQTT protokolÅ ve sensîr entegrasyonu 
- NLP (Doßal Dil òüleme) ile otomatik încelik ve kategori belirleme 
 
## ?? Kurulum 
```bash 
# Backend iáin 
cd backend 
python -m venv env 
source env/Scripts/activate      # Windows iáin 
pip install -r requirements.txt 
python manage.py migrate 
python manage.py runserver 
``` 
 
```bash 
# Frontend iáin 
cd frontend 
npm install 
npm run dev 
``` 
 
 
## ??? Ekran GîrÅntÅsÅ 
Aüaßçya sistemin ekran gîrÅntÅlerini ekleyebilirsiniz. 
``` 
![ArayÅz](./screenshots/dashboard.png) 
``` 
 
## ?? Geliütirici Notu 
Bu proje, 2025 yçlç bitirme projesi kapsamçnda geliütirilmiütir. Django ve React altyapçsç Åzerinde detaylç biáimde áalçüma fçrsatç sunmuü, doßal dil iüleme (NLP) ve JWT gÅvenlik sistemleriyle ileri seviye yazçlçm teknikleri uygulanmçütçr. 
 
## ?? GitHub Sayfasç 
[Proje Linki](https://github.com/ayse-erdogan/KurumArizaTakip) 
