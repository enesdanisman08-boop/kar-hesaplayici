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
        "Öğününü normal bir cümle olarak yaz (Örn: *30gr yulaf, 4 yemek kaşığı yoğurt, 1 ölçek protein tozu, 1 adet muz*).")

    ogun_tipi = st.selectbox("Öğün Türü", ["Kahvaltı", "Öğle Yemeği", "Akşam Yemeği", "Ara Öğün"])
    kullanici_metni = st.text_area("Yediğin şeyleri yaz:",
                                   "30gr yulaf, 4 yemek kaşığı yoğurt, 1 ölçek protein tozu, 1 adet muz, 1 tatlı kaşığı damla çikolata, 1 tatlı kaşığı hindistan cevizi tozu.")

    if st.button("🤖 AI Robot ile Hesapla ve Kaydet"):
        metin = kullanici_metni.lower()

        kalori = 0.0
        protein = 0.0
        seker = 0.0

        # Metin içindeki kelimeleri ve sayıları akıllıca tarayan fonksiyon
        kelimeler = metin.split(",")

        for parca in kelimeler:
            p = parca.strip()
            # Sayıyı bulmaya çalışalım
            sayi = 1.0
            for kelime in p.split():
                temiz_kelime = kelime.replace("gr", "").replace("g", "").replace("adet", "").replace("ölçek",
                                                                                                     "").replace(
                    "kaşığı", "").replace("tatlı", "").replace("yemek", "").strip()
                try:
                    sayi = float(temiz_kelime)
                    break
                except:
                    continue

            # Besin türüne göre dinamik hesaplama
            if "yulaf" in p:
                # 100g yulaf ~ 388 kcal, 13g protein, 1.5g şeker
                gram = sayi if sayi > 5 else 70.0  # Eğer sayı bulunamadıysa varsayılan 70 al
                kalori += 388 * (gram / 100.0)
                protein += 13.0 * (gram / 100.0)
                seker += 1.5 * (gram / 100.0)

            elif "yoğurt" in p or "yogurt" in p:
                # 1 yemek kaşığı yoğurt ~ 20g (100g yoğurt ~ 60 kcal, 4.5g protein, 4g şeker)
                kasik = sayi if sayi < 20 else 4.0
                gram_yogurt = kasik * 20.0
                kalori += 60 * (gram_yogurt / 100.0)
                protein += 4.5 * (gram_yogurt / 100.0)
                seker += 4.0 * (gram_yogurt / 100.0)

            elif "protein tozu" in p or "ölçek" in p:
                olcek = sayi if sayi < 5 else 1.0
                kalori += 120.0 * olcek
                protein += 24.0 * olcek
                seker += 1.0 * olcek

            elif "muz" in p:
                adet = sayi if sayi < 5 else 1.0
                kalori += 105.0 * adet
                protein += 1.3 * adet
                seker += 12.0 * adet

            elif "çikolata" in p or "cikolata" in p:
                kasik = sayi if sayi < 10 else 1.0
                kalori += 50.0 * kasik
                protein += 0.5 * kasik
                seker += 5.0 * kasik

            elif "hindistan cevizi" in p:
                kasik = sayi if sayi < 10 else 1.0
                kalori += 35.0 * kasik
                protein += 0.3 * kasik
                seker += 0.5 * kasik

        if kalori == 0:
            kalori = 400.0
            protein = 25.0
            seker = 10.0

        st.markdown("---")
        st.success("🤖 AI Robot Analizi Tamamlandı!")

        col1, col2, col3 = st.columns(3)
        col1.metric("Tahmini Kalori", f"{kalori:.0f} kcal")
        col2.metric("Toplam Protein", f"{protein:.1f}g")
        col3.metric("Tahmini Şeker", f"{seker:.1f}g")

        kayit_satiri = f"[{simdi}] ({ogun_tipi}) İçerik: {kullanici_metni} | Kalori: {kalori:.0f} kcal | Şeker: {seker:.1f}g | Protein: {protein:.1f}g\n"
        with open("spor_beslenme_kayitlari.txt", "a", encoding="utf-8") as f:
            f.write(kayit_satiri)

        st.toast("Öğün başarıyla ve gramajına göre doğru hesaplanıp kaydedildi!", icon="🔥")

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
        w_durum = '✅' if Whey else '❌'
        c_durum = '✅' if Creatine else '❌'
        supp_metni = f"[{simdi_tarih}] Su: {su_miktari}L | Whey: {w_durum} | Kreatin: {c_durum}\n"
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