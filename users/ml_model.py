import re
import logging
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob

nltk.download("punkt")
nltk.download("stopwords")

logging.basicConfig(level=logging.INFO)
STOPWORDS = set(stopwords.words("turkish"))

# 🔹 **Metni Temizleme**
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # Noktalama temizleme
    text = re.sub(r"\d+", "", text)  # Sayıları temizleme
    words = word_tokenize(text)
    cleaned = [word for word in words if word not in STOPWORDS]
    logging.info(f"🔍 Temizlenen Kelimeler: {cleaned}")
    return cleaned

# 🔹 **Kategori Kelimeleri ve Ağırlıkları**
SUB_CATEGORIES = {
    "Bilgisayar Donanım": {"ekran": 2, "kasa": 1, "fan": 1, "anakart": 2, "mavi ekran": 3,
                          "çökme": 2, "donuyor": 2, "görüntü gelmiyor": 3, "bilgisayar açılmıyor": 3},
    "Bilgisayar Yazılım": {"windows hata": 2, "mac çalışmıyor": 2, "driver yüklenmiyor": 2,
                            "sistem çöktü": 3, "program açılmıyor": 2},
    "Bilgisayar Ağ": {"wifi": 3, "internet": 3, "bağlantı": 2, "modem çalışmıyor": 3, "vpn açılmıyor": 2,
                       "ağ problemi": 3, "ethernet çalışmıyor": 2, "internet kopuyor": 3},
    "Telefon Donanım": {"dokunmatik çalışmıyor": 3, "ekran kırıldı": 3, "kamera açılmıyor": 3,
                          "hoparlör bozuk": 2, "şebeke çekmiyor": 2},
    "Telefon Yazılım": {"android hata": 2, "ios güncellenmiyor": 2, "uygulama açılmıyor": 3,
                          "telefon donuyor": 2},
    "Telefon Batarya": {"şarj olmuyor": 3, "batarya hızlı tükeniyor": 2, "telefonu fişe taktım ama açılmıyor": 3,
                         "şarj olurken kapanıyor": 3},
    "Telefon Bağlantı": {"wifi çalışmıyor": 2, "mobil veri yok": 2, "sim kart hata": 2, "bluetooth bağlanmıyor": 2}
}


TECHNICIANS = {
    "Bilgisayar Donanım": "bilgisayar_donanım_teknisyeni@example.com",
    "Bilgisayar Yazılım": "bilgisayar_yazılım_teknisyeni@example.com",
    "Bilgisayar Ağ": "bilgisayar_ag_teknisyeni@example.com",
    "Telefon Donanım": "telefon_donanım_teknisyeni@example.com",
    "Telefon Yazılım": "telefon_yazilim_teknisyeni@example.com",
    "Telefon Batarya": "telefon_batarya_teknisyeni@example.com",
    "Telefon Bağlantı": "telefon_baglanti_teknisyeni@example.com"
}

# 🔹 **Kategori Tahmini (Gelişmiş)**
# 🔹 **Kategori Tahmini (Gelişmiş)**
def predict_category(description):
    cleaned_words = clean_text(description)
    category_scores = {category: 0 for category in SUB_CATEGORIES}

    for category, keywords in SUB_CATEGORIES.items():
        for keyword, weight in keywords.items():
            for word in cleaned_words:
                if keyword in word:  # 🔥 Anahtar kelime kelimenin içinde geçiyorsa eşleştir
                    category_scores[category] += weight
                    logging.info(f"INFO:root:Eşleşen Kelime: '{keyword}' -> {category}")

    logging.info(f"📊 Kategori Skorları: {category_scores}")
    best_category = max(category_scores, key=category_scores.get)

    if category_scores[best_category] == 0:
        logging.info("⚠️ Kategori bulunamadı, 'Diğer' olarak atanıyor.")
        return "Diğer"

    logging.info(f"✅ Seçilen Kategori: {best_category}")
    return best_category


# 🔹 **Öncelik Belirleme (Duygu Analizi)**
def analyze_sentiment(description):
    sentiment_score = TextBlob(description).sentiment.polarity
    if sentiment_score > 0.2:
        return "low"
    elif sentiment_score < -0.2:
        return "high"
    else:
        return "medium"

# 🔹 **Teknisyen Atama**
def assign_technician(category):
    teknisyen_email = TECHNICIANS.get(category)

    if teknisyen_email:
        logging.info(f"✅ AI tarafından önerilen teknisyen: {teknisyen_email} ({category})")
        return teknisyen_email

    logging.warning(f"⚠️ '{category}' için belirlenmiş teknisyen yok, sistem en az işi olanı atayacak.")
    return None
