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
st.write("Günlük beslenme, antrenman, su ve supplement takip merkezi.")

menu = st.sidebar.selectbox("Menü",
                            ["Günlük Özet & Beslenme", "Antrenman & Takvim", "Supplement & Su", "Notlar & Hedefler",
                             "Kayıtları Temizle"])

simdi_tarih = datetime.now().strftime("%d.%m.%Y")

if menu == "Günlük Özet & Beslenme":
    st.subheader(f"🍽️ Günlük Beslenme Takibi ({simdi_tarih})")

    ogun_turu = st.selectbox("Öğün Seç", ["Kahvaltı / Sabah", "Öğle Yemeği", "Akşam Yemeği", "Ara Öğün / Atıştırmalık"])
    yemek_aciklama = st.text_area("Ne yedin? (Örn: 200g tavuk göğsü, 150g pilav, salata)")

    col1, col2 = st.columns(2)
    with col1:
        tahmini_kalori = st.number_input("Tahmini Kalori (kcal)", min_value=0, value=600, step=50)
    with col2:
        tahmini_protein = st.number_input("Tahmini Protein (gram)", min_value=0, value=45, step=5)

    if st.button("Öğünü Kaydet"):
        kayit_metni = f"[{simdi_tarih} - {ogun_turu}] {yemek_aciklama} | Kalori: {tahmini_kalori} kcal | Protein: {tahmini_protein}g\n"
        with open("spor_beslenme_kayitlari.txt", "a", encoding="utf-8") as f:
            f.write(kayit_metni)
        st.success("Öğün başarıyla eklendi, koç onayladı! 🔥")

    st.markdown("---")
    st.subheader("📜 Bugünün ve Geçmişin Beslenme Dökümü")
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
    st.write("Hangi gün hangi bölge çalışacağını buradan planlayabilir ve takip edebilirsin.")

    secilen_gun = st.selectbox("Gün Seç", ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"])
    bolge = st.selectbox("Antrenman Türü / Bölge",
                         ["Push (Göğüs - Omuz - Arka Kol)", "Pull (Sırt - Ön Kol)", "Legs (Bacak - Karın)",
                          "Cardio & Core", "Dinlenme (Rest Day)"])
    notlar_antrenman = st.text_input("Antrenman Notu (Örn: Göğüste ağırlık artırıldı, 40 dk incline kardiyo yapıldı)")

    if st.button("Antrenman Planını Kaydet"):
        antrenman_metni = f"[ANTRENMAN - {secilen_gun}] Bölge: {bolge} | Not: {notlar_antrenman}\n"
        with open("antrenman_programi.txt", "a", encoding="utf-8") as f:
            f.write(antrenman_metni)
        st.success(f"{secilen_gun} antrenman programı kaydedildi!")

    st.markdown("---")
    st.subheader("📋 Kayıtlı Antrenman Programın")
    try:
        with open("antrenman_programi.txt", "r", encoding="utf-8") as f:
            ant_satirlar = f.readlines()
        if not ant_satirlar:
            st.info("Henüz antrenman programı girilmemiş.")
        else:
            for sat in ant_satirlar:
                st.text(sat.strip())
    except FileNotFoundError:
        st.info("Henüz dosya oluşturulmamış.")

elif menu == "Supplement & Su":
    st.subheader("💧 Su ve Supplement Takibi")

    st.markdown("### 💧 Günlük Su Takibi")
    su_miktari = st.slider("Bugün içtiğin toplam su (Litre cinsinden)", 0.0, 6.0, 3.0, 0.5)
    st.metric("Günlük Su Hedefi Durumu", f"{su_miktari} Litre",
              delta="Hedef: 4.0 L" if su_miktari < 4 else "Hedef Tamamlandı! 🔥")

    st.markdown("---")
    st.markdown("### 💊 Günlük Supplement Rutini")

    Whey = st.checkbox("Whey Protein (Antrenman sonrası)")
    Creatine = st.checkbox("Creatine (Günlük 5g)")
    Omega3 = st.checkbox("Omega-3 / Balık Yağı")
    Multivitamin = st.checkbox("Multivitamin")

    if st.button("Supplementleri Günlük İşaretle"):
        supp_metni = f"[{simdi_tarih} Supplementler] Whey: {'✅' if Whey else '❌'} | Kreatin: {'✅' if Creatine else '❌'} | Omega3: {'✅' if Omega3 else '❌'} | Multi: {'✅' if Multivitamin else '❌'}\n"
        with open("supplement_takip.txt", "a", encoding="utf-8") as f:
            f.write(supp_metni)
        st.success("Supplement takibi kaydedildi!")

elif menu == "Notlar & Hedefler":
    st.subheader("📝 Koçluk Notları ve Hedefler")
    yeni_not = st.text_area("Aklındaki bir hedef, tarif veya notu buraya yazabilirsin:")

    if st.button("Notu Kaydet"):
        with open("spor_notlari.txt", "a", encoding="utf-8") as f:
            f.write(f"[{simdi_tarih}] {yeni_not}\n")
        st.success("Not kaydedildi.")

    try:
        with open("spor_notlari.txt", "r", encoding="utf-8") as f:
            not_satirlar = f.readlines()
        st.markdown("### Kayıtlı Notlar:")
        for n in not_satirlar:
            st.text(n.strip())
    except FileNotFoundError:
        pass

elif menu == "Kayıtları Temizle":
    st.subheader("🗑️ Veri Sıfırlama")
    if st.button("Tüm Spor ve Beslenme Geçmişini Temizle"):
        for dosya_adi in ["spor_beslenme_kayitlari.txt", "antrenman_programi.txt", "supplement_takip.txt",
                          "spor_notlari.txt"]:
            with open(dosya_adi, "w", encoding="utf-8") as f:
                pass
        st.success("Tüm veriler tertemiz sıfırlandı!")