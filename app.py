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

# --- SOL MENÜ (SIDEBAR) ZENGİNLEŞTİRME ---

with st.sidebar:
    st.markdown("## 🏆 Sporcu Profili")
    st.info("**Sporcu:** Enes\n\n**Sistem:** 5 Gün PPL + Kardiyo\n\n**Durum:** Definasyon & Kas İnşası 🔥")

    # Vücut ve Dönüşüm Özeti
    col_s1, col_s2 = st.columns(2)
    col_s1.metric("Güncel Kilo", "80.5 kg", "-54.5 kg")
    col_s2.metric("Yağ Oranı", "%14.5", "Hedef: %12")

    st.caption("🚀 Dönüşüm Hedefi İlerlemesi (%90)")
    st.progress(90)

    st.markdown("---")

    # Daha şık ve açık menü yapısı
    st.markdown("### 🧭 Navigasyon")
    menu = st.radio(
        "Bölüm Seç:",
        [
            "🤖 AI Kalori & Beslenme",
            "🗓️ Antrenman & PPL Takvimi",
            "🏋️‍♂️ Ağırlık & PR Takibi",
            "💧 Supplement & Su",
            "📝 Notlar & Hedefler",
            "🗑️ Kayıtları Temizle"
        ]
    )

    st.markdown("---")

    # Sol Menüde Hızlı 1RM (Maksimum Ağırlık) Hesaplayıcı
    with st.expander("⚡ Hızlı 1RM (Max Ağırlık) Hesapla"):
        st.caption("Kaldırdığın ağırlık ve tekrarı gir, 1 tekrarda max kaç kg basabileceğini gör.")
        kilo_1rm = st.number_input("Kaldırılan Ağırlık (kg)", min_value=1.0, value=80.0, step=2.5)
        tekrar_1rm = st.number_input("Tekrar Sayısı", min_value=1, max_value=30, value=8, step=1)
        # Epley Formülü
        max_agirlik = kilo_1rm * (1 + tekrar_1rm / 30.0)
        st.success(f"🔥 Tahmini 1RM: **{max_agirlik:.1f} kg**")

    st.markdown("---")

    # Günlük Sabit Hedef Hatırlatıcı
    with st.expander("🎯 Günlük Sabit Hedeflerim"):
        st.write("🔹 **Kalori:** ~2200 - 2400 kcal")
        st.write("🔹 **Protein:** 160g - 180g")
        st.write("🔹 **Su:** Minimum 4.0 Litre")
        st.write("🔹 **Kardiyo:** 40 dk Incline Yürüyüş")

    st.markdown("---")
    if st.button("🚪 Çıkış Yap", use_container_width=True):
        st.session_state["giris_yapildi"] = False
        st.rerun()

# --- ANA EKRAN İÇERİĞİ ---

st.title("💪 Enes Fitness & Yaşam Takip Paneli")
st.write("Akıllı AI Asistanlı beslenme, antrenman, su ve supplement merkezi.")

simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
simdi_tarih = datetime.now().strftime("%d.%m.%Y")

if menu == "🤖 AI Kalori & Beslenme":
    st.subheader("🤖 Akıllı Besin & Kalori Hesaplayıcı Robot")
    st.write(
        "Öğününü normal bir cümle olarak yaz (Örn: *30gr yulaf, 4 yemek kaşığı yoğurt, 1 ölçek protein tozu, 1 adet muz*).")

    ogun_tipi = st.selectbox("Öğün Türü",
                             ["Kahvaltı", "Öğle Yemeği", "Akşam Yemeği", "Antrenman Öncesi", "Antrenman Sonrası",
                              "Ara Öğün"])
    kullanici_metni = st.text_area("Yediğin şeyleri yaz:",
                                   "30gr yulaf, 4 yemek kaşığı yoğurt, 1 ölçek protein tozu, 1 adet muz, 1 tatlı kaşığı damla çikolata, 1 tatlı kaşığı hindistan cevizi tozu.")

    if st.button("🤖 AI Robot ile Hesapla ve Kaydet"):
        metin = kullanici_metni.lower()

        kalori = 0.0
        protein = 0.0
        seker = 0.0

        kelimeler = metin.split(",")

        for parca in kelimeler:
            p = parca.strip()
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

            if "yulaf" in p:
                gram = sayi if sayi > 5 else 70.0
                kalori += 388 * (gram / 100.0)
                protein += 13.0 * (gram / 100.0)
                seker += 1.5 * (gram / 100.0)

            elif "yoğurt" in p or "yogurt" in p:
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

            elif "tavuk" in p:
                gram = sayi if sayi > 10 else 200.0
                kalori += 165 * (gram / 100.0)
                protein += 31.0 * (gram / 100.0)

            elif "pilav" in p or "pirinç" in p:
                gram = sayi if sayi > 10 else 150.0
                kalori += 130 * (gram / 100.0)
                protein += 2.7 * (gram / 100.0)

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

        st.toast("Öğün başarıyla kaydedildi!", icon="🔥")

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

elif menu == "🗓️ Antrenman & PPL Takvimi":
    st.subheader("🗓️ Haftalık Antrenman ve PPL Takvimi")
    secilen_gun = st.selectbox("Gün Seç", ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"])
    bolge = st.selectbox("Antrenman Türü / Bölge", [
        "Push (Göğüs - Omuz - Arka Kol)",
        "Pull (Sırt - Ön Kol - Arka Omuz)",
        "Legs (Bacak - Kalf - Karın)",
        "Incline Kardiyo (40 dk) & Core",
        "Dinlenme (Rest Day)"
    ])
    notlar_antrenman = st.text_input("Antrenman Notu (Örn: Pump çok iyiydi, 40 dk eğimli yürüyüş tamamlandı)")

    if st.button("Antrenman Planını Kaydet"):
        antrenman_metni = f"[{simdi_tarih} - {secilen_gun}] Bölge: {bolge} | Not: {notlar_antrenman}\n"
        with open("antrenman_programi.txt", "a", encoding="utf-8") as f:
            f.write(antrenman_metni)
        st.success(f"{secilen_gun} antrenman programı kaydedildi!")

    st.markdown("---")
    st.subheader("📋 Geçmiş Antrenman Kayıtları")
    try:
        with open("antrenman_programi.txt", "r", encoding="utf-8") as f:
            for sat in f.readlines():
                st.text(sat.strip())
    except FileNotFoundError:
        st.info("Henüz antrenman kaydı yok.")

elif menu == "🏋️‍♂️ Ağırlık & PR Takibi":
    st.subheader("🏋️‍♂️ Salonda Bastığın Ağırlıklar & PR (Kişisel Rekor) Takibi")
    st.write("Hangi harekette kaç kg ile kaç tekrar yaptığını kaydet, gelişimini takip et!")

    hareket = st.selectbox("Hareket Seç", [
        "Bench Press / Dumbbell Press",
        "Incline Dumbbell Press",
        "Lat Pulldown / Barfiks",
        "Barbell Row / Cable Row",
        "Shoulder Press",
        "Lateral Raise",
        "Squat / Leg Press",
        "Romanian Deadlift (RDL)",
        "Barbell Curl / Hammer Curl",
        "Triceps Pushdown"
    ])

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        agirlik_kg = st.number_input("Ağırlık (kg)", min_value=0.0, value=60.0, step=2.5)
    with col_p2:
        set_sayisi = st.number_input("Set Sayısı", min_value=1, value=4, step=1)
    with col_p3:
        tekrar_sayisi = st.number_input("Tekrar Sayısı", min_value=1, value=10, step=1)

    if st.button("🔥 Ağırlık Rekorunu Kaydet"):
        pr_metni = f"[{simdi_tarih}] {hareket} -> {agirlik_kg} kg ({set_sayisi} Set x {tekrar_sayisi} Tekrar)\n"
        with open("agirlik_rekorlari.txt", "a", encoding="utf-8") as f:
            f.write(pr_metni)
        st.success("Ağırlık kaydı eklendi! Güçlenmeye devam 💪")

    st.markdown("---")
    st.subheader("📈 Kayıtlı Ağırlık Geçmişin")
    try:
        with open("agirlik_rekorlari.txt", "r", encoding="utf-8") as f:
            pr_satirlar = f.readlines()
        if not pr_satirlar:
            st.info("Henüz ağırlık kaydı girilmemiş.")
        else:
            for p_satir in pr_satirlar:
                st.text(p_satir.strip())
    except FileNotFoundError:
        st.info("Henüz kayıt dosyası oluşturulmadı.")

elif menu == "💧 Supplement & Su":
    st.subheader("💧 Su ve Supplement Takibi")
    su_miktari = st.slider("Bugün içtiğin toplam su (Litre)", 0.0, 6.0, 3.5, 0.5)
    st.metric("Su Durumu", f"{su_miktari} Litre", delta="Hedef: 4.0L" if su_miktari < 4.0 else "Hedef Tamamlandı! 💧")

    st.markdown("### 💊 Günlük Supplementler")
    Whey = st.checkbox("Whey Protein")
    Creatine = st.checkbox("Creatine (5g)")
    Omega3 = st.checkbox("Omega-3")
    Multivitamin = st.checkbox("Multivitamin / ZMA")

    if st.button("Supplementleri Kaydet"):
        w_durum = '✅' if Whey else '❌'
        c_durum = '✅' if Creatine else '❌'
        o_durum = '✅' if Omega3 else '❌'
        m_durum = '✅' if Multivitamin else '❌'
        supp_metni = f"[{simdi_tarih}] Su: {su_miktari}L | Whey: {w_durum} | Kreatin: {c_durum} | Omega3: {o_durum} | Multi: {m_durum}\n"
        with open("supplement_takip.txt", "a", encoding="utf-8") as f:
            f.write(supp_metni)
        st.success("Kaydedildi!")

    st.markdown("---")
    try:
        with open("supplement_takip.txt", "r", encoding="utf-8") as f:
            for s_sat in f.readlines():
                st.text(s_sat.strip())
    except FileNotFoundError:
        pass

elif menu == "📝 Notlar & Hedefler":
    st.subheader("📝 Koçluk Notları ve Hedefler")
    yeni_not = st.text_area("Notunu veya yeni tarif fikirlerini yaz:")
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

elif menu == "🗑️ Kayıtları Temizle":
    st.subheader("🗑️ Veri Sıfırlama")
    if st.button("Tüm Geçmişi Temizle"):
        for dosya in ["spor_beslenme_kayitlari.txt", "antrenman_programi.txt", "agirlik_rekorlari.txt",
                      "supplement_takip.txt", "spor_notlari.txt"]:
            with open(dosya, "w", encoding="utf-8") as f:
                pass
        st.success("Tüm veriler sıfırlandı!")