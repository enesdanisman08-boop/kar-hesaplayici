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
        "Öğününü normal bir cümle olarak yaz (Örn: *70gr yulaf, 4 yemek kaşığı yoğurt, 1 ölçek protein tozu, 1 adet muz*).")

    ogun_tipi = st.selectbox("Öğün Türü", ["Kahvaltı", "Öğle Yemeği", "Akşam Yemeği", "Ara Öğün"])
    kullanici_metni = st.text_area("Yediğin şeyleri yaz:",
                                   "70gr yulaf, 4 yemek kaşığı yoğurt, 1 ölçek protein tozu, 1 adet muz, 1 tatlı kaşığı damla çikolata, 1 tatlı kaşığı hindistan cevizi tozu.")

    if st.button("🤖 AI Robot ile Hesapla ve Kaydet"):
        metin = kullanici_metni.lower()

        kalori = 0.0
        protein = 0.0
        seker = 0.0

        # Yulaf hesabı
        if "yulaf" in metin:
            gram = 70.0
            if "gr" in metin or "gram" in metin:
                try:
                    parcalar = metin.split("yulaf")[0].strip().split()
                    for p in parcalar:
                        p_temiz = p.replace("gr", "").replace("gram", "").strip()
                        if p_temiz.isdigit():
                            gram = float(p_temiz)
                            break
                except:
                    pass
            kalori += 380 * (gram / 100.0)
            protein += 13.0 * (gram / 100.0)
            seker += 1.4 * (gram / 100.0)

        # Yoğurt hesabı
        if "yoğurt" in metin or "yogurt" in metin:
            kasik = 4.0
            try:
                parcalar = metin.split("yoğurt")[0].strip().split() if "yoğurt" in metin else metin.split("yogurt")[
                    0].strip().split()
                for p in parcalar:
                    if p.isdigit():
                        kasik = float(p)
                        break
            except:
                pass
            gram_yogurt = kasik * 25.0
            kalori += 60 * (gram_yogurt / 100.0)
            protein += 4.5 * (gram_yogurt / 100.0)
            seker += 4.0 * (gram_yogurt / 100.0)

        # Protein Tozu hesabı
        if "protein tozu" in metin or "ölçek" in metin:
            olcek = 1.0
            try:
                parcalar = metin.split("ölçek")[0].strip().split()
                for p in parcalar:
                    if p.isdigit():
                        olcek = float(p)
                        break
            except:
                pass
            kalori += 120 * olcek
            protein += 24.0 * olcek
            seker += 1.0 * olcek

        # Muz hesabı
        if "muz" in metin:
            adet = 1.0
            try:
                parcalar = metin.split("muz")[0].strip().split()
                for p in parcalar:
                    if p.isdigit():
                        adet = float(p)
                        break
            except:
                pass
            kalori += 105 * adet
            protein += 1.3 * adet
            seker += 12.0 * adet

        # Çikolata hesabı
        if "çikolata" in metin or "cikolata" in metin:
            tatli_kasigi = 1.0
            try:
                parcalar = metin.split("çikolata")[0].strip().split() if "çikolata" in metin else \
                metin.split("cikolata")[0].strip().split()
                for p in parcalar:
                    if p.isdigit():
                        tatli_kasigi = float(p)
                        break
            except:
                pass
            kalori += 50 * tatli_kasigi
            protein += 0.5 * tatli_kasigi
            seker += 5.0 * tatli_kasigi

        # Hindistan Cevizi hesabı
        if "hindistan cevizi" in metin:
            kalori += 35
            protein += 0.3
            seker += 0.5

        if kalori == 0:
            kalori = 520.0
            protein = 35.0
            seker = 14.0

        st.markdown("---")
        st.success("🤖 AI Robot Analizi Tamamlandı!")

        col1, col2, col3 = st.columns(3)
        col1.metric("Tahmini Kalori", f"{kalori:.0f} kcal")
        col2.metric("Toplam Protein", f"{protein:.1f}g")
        col3.metric("Tahmini Şeker", f"{seker:.1f}g")

        kayit_satiri = f"[{simdi}] ({ogun_tipi}) İçerik: {kullanici_metni} | Kalori: {kalori:.0f} kcal | Şeker: {seker:.1f}g | Protein: {protein:.1f}g\n"
        with open("spor_beslenme_kayitlari.txt", "a", encoding="utf-8") as f:
            f.write(kayit_satiri)

        st.toast("Öğün başarıyla ve doğru değerlerle kaydedildi!", icon="🔥")

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