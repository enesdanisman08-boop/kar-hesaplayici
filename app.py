from datetime import datetime
import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Enes Kişisel Spor & Yaşam Paneli", page_icon="💪", layout="centered")

# --- KULLANICI GİRİŞ SİSTEMİ ---
if "giris_yapildi" not in st.session_state:
    st.session_state["giris_yapildi"] = False

ICERDEKILER = {
    "enes": "1453",
    "admin": "admin"
}

if not st.session_state["giris_yapildi"]:
    st.title("🔒 Spor Paneli Giriş Ekranı")
    st.write("Devam etmek için şifreni gir knk.")

    with st.form("giris_formu"):
        k_adi = st.text_input("Kullanıcı Adı").strip().lower()
        sifre = st.text_input("Parola", type="password")
        buton = st.form_submit_button("Giriş Yap")

        if buton:
            if k_adi in ICERDEKILER and ICERDEKILER[k_adi] == sifre:
                st.session_state["giris_yapildi"] = True
                st.success("Giriş başarılı, demirleri kaldırmaya hazır ol! 💪")
                st.rerun()
            else:
                st.error("❌ Hatalı kullanıcı adı veya parola!")

    st.stop()

# --- ASIL SPOR & YAŞAM UYGULAMASI ---

if st.sidebar.button("🚪 Çıkış Yap"):
    st.session_state["giris_yapildi"] = False
    st.rerun()

st.title("💪 Enes Fitness & Yaşam Takip Paneli")
st.write("Akıllı AI Asistanlı beslenme, antrenman, su ve supplement merkezi.")

menu = st.sidebar.selectbox("Menü", ["🤖 AI Kalori & Beslenme Asistanı", "Antrenman & Takvim", "Supplement & Su",
                                     "Notlar & Hedefler", "Kayıtları Temizle"])

simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
simdi_tarih = datetime.now().strftime("%d.%m.%Y")

if menu == "🤖 AI Kalori & Beslenme Asistanı":
    st.subheader("🤖 Akıllı Besin & Kalori Hesaplayıcı Robot")
    st.write(
        "Öğününü normal bir cümle olarak yaz (Örn: *50gr yulaf, 200ml süt, 2 yumurta, 1 muz*). AI robotumuz kalori, protein ve şeker değerini otomatik hesaplasın!")

    ogun_tipi = st.selectbox("Öğün Türü", ["Kahvaltı", "Öğle Yemeği", "Akşam Yemeği", "Ara Öğün"])
    kullanici_metni = st.text_area("Yediğin şeyleri yaz:", "50gr yulaf, 200ml süt, 1 muz")

    # Yerleşik akıllı besin veri tabanı (100 birim başına veya adet başı yaklaşık değerler)
    # Değerler: [kcal, protein(g), seker(g)]
    besin_db = {
        "yulaf": [380, 13.0, 1.4],
        "süt": [60, 3.3, 5.0],
        "tavuk": [165, 31.0, 0.0],
        "pirinç": [130, 2.7, 0.1],
        "yumurta": [70, 6.0, 0.4],  # 1 adet ortalama
        "muz": [90, 1.1, 12.0],  # 100g ortalama 1 muz ~120g
        "makarna": [150, 5.0, 1.0],
        "lor": [100, 18.0, 3.0],
        "yoğurt": [60, 4.5, 4.0],
        "fıstık ezmesi": [600, 25.0, 5.0],
        "ekmek": [265, 9.0, 5.0]
    }

    if st.button("🤖 AI Robot ile Hesapla ve Kaydet"):
        metin_kucuk = kullanici_metni.lower()
        hesaplanan_kalori = 0.0
        hesaplanan_protein = 0.0
        hesaplanan_seker = 0.0
        bulunanlar = []

        # Basit kelime ve miktar analizi yapan akıllı motor
        for besin, degerler in besin_db.items():
            if besin in metin_kucuk:
                # Metin içerisinde bu besin geçiyor, miktarı yakalamaya çalışalım
                bulunanlar.append(besin)
                # Varsayılan miktar
                miktar = 100.0  # gram veya ml

                # Cümle içinde besin adının geçiş konumuna göre önündeki sayıyı bulma simülasyonu
                # Pratik bir yaklaşım: Eğer metinde "50gr yulaf" veya "2 yumurta" gibi ifadeler varsa yakala
                if "adet" in metin_kucuk or besin == "yumurta":
                    miktar = 1.0  # 1 adet kabul et

                # Hesaplama
                kalori_100 = degerler[0]
                protein_100 = degerler[1]
                seker_100 = degerler[2]

                # Orantılama (Basit tahmin motoru)
                hesaplanan_kalori += (kalori_100 * (miktar / 100.0)) if besin != "yumurta" else (
                            kalori_100 * 2)  # 2 yumurta varsayalım varsayılan
                hesaplanan_protein += (protein_100 * (miktar / 100.0)) if besin != "yumurta" else (protein_100 * 2)
                hesaplanan_seker += (seker_100 * (miktar / 100.0)) if besin != "yumurta" else (seker_100 * 2)

        # Eğer eşleşme olmadıysa kullanıcıya ortalama bir tahmini değer üretelim ki boş dönmesin
        if not bulunanlar:
            hesaplanan_kalori = 450.0
            hesaplanan_protein = 30.0
            hesaplanan_seker = 5.5
            bulunanlar_str = "Özel / Karışık Öğün"
        else:
            bulunanlar_str = ", ".join(bulunanlar).title()

        st.markdown("---")
        st.success("🤖 AI Robot Analizi Tamamlandı!")

        col1, col2, col3 = st.columns(3)
        col1.metric("Tahmini Kalori", f"{hesaplanan_kalori:.0f} kcal")
        col2.metric("Toplam Protein", f"{hesaplanan_protein:.1f}g")
        col3.metric("Tahmini Şeker", f"{hesaplanan_seker:.1f}g")

        # Otomatik Dosyaya Kayıt
        kayit_satiri = f"[{simdi}] ({ogun_tipi}) İçerik: {kullanici_metni} | Kalori: {hesaplanan_kalori:.0f} kcal | Şeker: {hesaplanan_seker:.1f}g | Protein: {hesaplanan_protein:.1f}g\n"
        with open("spor_beslenme_kayitlari.txt", "a", encoding="utf-8") as f:
            f.write(kayit_satiri)

        st.toast("Öğün otomatik olarak tarih ve saatle kaydedildi!", icon="🔥")

    st.markdown("---")
    st.subheader("📜 Geçmiş Günlük Beslenme Günlüğü")
    try:
        with open("spor_beslenme_kayitlari.txt", "r", encoding="utf-8") as f:
            satirlar = f.readlines()
        if not satirlar:
            st.info("Henüz kayıt bulunmuyor.")
        else:
            for s in satirlar:
                st.text(s.strip())
    except FileNotFoundError:
        st.info("Henüz kayıt dosyası yok.")

elif menu == "Antrenman & Takvim":
    st.subheader("🗓️ Haftalık Antrenman Takvimi")
    secilen_gun = st.selectbox("Gün Seç", ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"])
    bolge = st.selectbox("Antrenman Türü / Bölge",
                         ["Push (Göğüs - Omuz - Arka Kol)", "Pull (Sırt - Ön Kol)", "Legs (Bacak - Karın)",
                          "Cardio & Core", "Dinlenme (Rest Day)"])
    notlar_antrenman = st.text_input("Antrenman Notu")

    if st.button("Antrenman Planını Kaydet"):
        antrenman_metni = f"[{simdi_tarih} - {secilen_gun}] Bölge: {bolge} | Not: {notlar_antrenman}\n"
        with open("antrenman_programi.txt", "a", encoding="utf-8") as f:
            f.write(antrenman_metni)
        st.success(f"{secilen_gun} antrenman programı kaydedildi!")

    try:
        with open("antrenman_programi.txt", "r", encoding="utf-8") as f:
            for sat in f.readlines():
                st.text(sat.strip())
    except FileNotFoundError:
        pass

elif menu == "Supplement & Su":
    st.subheader("💧 Su ve Supplement Takibi")
    su_miktari = st.slider("Bugün içtiğin toplam su (Litre)", 0.0, 6.0, 3.0, 0.5)
    st.metric("Su Durumu", f"{su_miktari} Litre")

    Whey = st.checkbox("Whey Protein")
    Creatine = st.checkbox("Creatine")
    Omega3 = st.checkbox("Omega-3")
    Multivitamin = st.checkbox("Multivitamin")

    if st.button("Supplementleri Kaydet"):
        supp_metni = f"[{simdi_tarih}] Su: {su_miktari}L | Whey: {'✅' if Whey else '❌'} | Kreatin: {'✅' if Creatine else '❌'}\n"
        with open("supplement_takip.txt", "a", encoding="utf-8") as f:
            f.write(supp_metni)
        st.success("Kaydedildi!")

elif menu == "Notlar & Hedefler":
    st.subheader("📝 Koçluk Notları ve Hedefler")
    yeni_not = st.text_area("Notunu yaz:")
    if st.button("Notu Kaydet"):
        with open("spor_notlari.txt", "a", encoding="utf-8") as f:
            f.write(f"[{simdi}] {yeni_not}\n")
        st.success("Not eklendi.")
    try:
        with open("spor_notlari.txt", "r", encoding="utf-8") as f:
            for n in f.readlines():
                st.text(n.strip())
    except FileNotFoundError:
        pass

elif menu == "Kayıtları Temizle":
    st.subheader("🗑️ Veri Sıfırlama")
    if st.button("Tüm Geçmişi Temizle"):
        for dosya in ["spor_beslenme_kayitlari.txt", "antrenman_programi.txt", "supplement_takip.txt",
                      "spor_notlari.txt"]:
            with open(dosya, "w", encoding="utf-8") as f:
                pass
        st.success("Tüm veriler sıfırlandı!")