from datetime import datetime
import os
import time
import streamlit as st

# Sayfa Ayarları ve Mobil PWA Entegrasyonu
st.set_page_config(page_title="Enes Spor & Yaşam Paneli", page_icon="💪", layout="centered")

st.markdown("""
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#0a0f0d">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
""", unsafe_allow_html=True)

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

# --- SOL MENÜ (SIDEBAR) & KOMPAKT DÜZEN ---

with st.sidebar:
    with st.expander("🎨 Tema & Renk Ayarları"):
        secilen_tema = st.selectbox(
            "Tema Seç:",
            [
                "🟢 Neon Gym (Siyah & Yeşil)",
                "🔴 Cyber Red (Agresif Kırmızı)",
                "💎 Cyberpunk Mor",
                "🔥 Sunset Turuncu",
                "⚪ Clean White (Ferah Beyaz)",
                "⚫ Standart Koyu"
            ]
        )

    st.markdown("---")
    st.markdown("## 🧭 Navigasyon")
    menu = st.selectbox(
        "Gitmek İstediğin Bölüm:",
        [
            "📅 30 Günlük Diyet & Takvim",
            "📸 Vücut Dönüşüm & Form Arşivi",
            "🤖 AI Kalori & Beslenme",
            "🔥 Kardiyo & Yağ Yakım Hesaplayıcı",
            "💤 Uyku & Toparlanma (Recovery)",
            "🗓️ Antrenman & PPL Takvimi",
            "🏋️‍♂️ Ağırlık & PR Takibi",
            "💧 Supplement & Su",
            "📝 Notlar & Hedefler",
            "🗑️ Kayıtları Temizle"
        ]
    )

    st.markdown("---")

    st.markdown("## 🏆 Sporcu Özeti")
    st.info(
        "👤 **Enes** (178 cm | 84 kg)\n\n"
        "🎯 **Hedef:** 80-81 kg (%11 Yağ)\n\n"
        "🔥 **Günlük Hedef:** 2250 kcal | 185g+ Protein"
    )

    col_s1, col_s2 = st.columns(2)
    col_s1.metric("Kilo", "84.0 kg", "Hedef: 80.5")
    col_s2.metric("Yağ", "%16.0", "Hedef: %11")

    st.markdown("---")

    with st.expander("⏱️ Set Arası Dinlenme"):
        sure = st.selectbox("Süre Seç:", [60, 90, 120, 180], format_func=lambda x: f"{x} Saniye", key="dinlenme_sure")
        if st.button("▶️ Sayacı Başlat", use_container_width=True):
            bar = st.progress(0)
            durum_yazisi = st.empty()
            for i in range(sure):
                kalan = sure - i
                durum_yazisi.markdown(f"⏳ Kalan: **{kalan} sn**")
                bar.progress((i + 1) / sure)
                time.sleep(1)
            durum_yazisi.success("🔔 Süre Bitti! Sete devam 💪")

    with st.expander("⚡ Hızlı 1RM (Max) Hesapla"):
        kilo_1rm = st.number_input("Ağırlık (kg)", min_value=1.0, value=80.0, step=2.5, key="rm_kilo")
        tekrar_1rm = st.number_input("Tekrar", min_value=1, max_value=30, value=8, step=1, key="rm_tekrar")
        max_agirlik = kilo_1rm * (1 + tekrar_1rm / 30.0)
        st.success(f"🔥 Tahmini Max: **{max_agirlik:.1f} kg**")

    st.markdown("---")
    if st.button("🚪 Çıkış Yap", use_container_width=True):
        st.session_state["giris_yapildi"] = False
        st.rerun()

    if 'secilen_tema' not in locals():
        secilen_tema = "🟢 Neon Gym (Siyah & Yeşil)"

# --- ÖZEL CSS TEMA KODLARI ---

if secilen_tema == "🟢 Neon Gym (Siyah & Yeşil)":
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0a0f0d 0%, #111a16 100%);
            color: #e0f2e9;
        }
        div[data-testid="stMetric"] {
            background-color: #16241d;
            border: 1px solid #00ff88;
            padding: 12px;
            border-radius: 10px;
            box-shadow: 0 0 8px rgba(0, 255, 136, 0.15);
        }
        .stButton>button {
            background-color: #00ff88 !important;
            color: #05140c !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

elif secilen_tema == "🔴 Cyber Red (Agresif Kırmızı)":
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #120606 0%, #1f0b0b 100%);
            color: #fcebeb;
        }
        div[data-testid="stMetric"] {
            background-color: #290f0f;
            border: 1px solid #ff2a2a;
            padding: 12px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(255, 42, 42, 0.2);
        }
        .stButton>button {
            background-color: #ff2a2a !important;
            color: #ffffff !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

elif secilen_tema == "💎 Cyberpunk Mor":
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0d0914 0%, #171026 100%);
            color: #f3e8ff;
        }
        div[data-testid="stMetric"] {
            background-color: #221638;
            border: 1px solid #a855f7;
            padding: 12px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(168, 85, 247, 0.25);
        }
        .stButton>button {
            background-color: #a855f7 !important;
            color: #ffffff !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

elif secilen_tema == "🔥 Sunset Turuncu":
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #140a06 0%, #26120b 100%);
            color: #ffedd5;
        }
        div[data-testid="stMetric"] {
            background-color: #36190f;
            border: 1px solid #f97316;
            padding: 12px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(249, 115, 22, 0.25);
        }
        .stButton>button {
            background-color: #f97316 !important;
            color: #ffffff !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

elif secilen_tema == "⚪ Clean White (Ferah Beyaz)":
    st.markdown("""
        <style>
        .stApp {
            background-color: #f4f7f9;
            color: #1c252c;
        }
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border: 2px solid #007bff;
            padding: 12px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        }
        .stButton>button {
            background-color: #007bff !important;
            color: #ffffff !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

# --- ANA EKRAN İÇERİĞİ ---

st.title("💪 Enes Fitness & Yaşam Takip Paneli")
st.write("84 kg (%16 Yağ) ➡️ 80.5 kg (%11 Yağ) Kas Korumalı Definasyon Merkezi.")

simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
simdi_tarih = datetime.now().strftime("%d.%m.%Y")

# --- 1. BÖLÜM: 30 GÜNLÜK DİYET & KAMP TAKVİMİ ---
if menu == "📅 30 Günlük Diyet & Takvim":
    st.subheader("📅 30 Günlük Kas Korumalı Definasyon Kampı")
    st.write(
        "Her gün aynı şeyi yemekten sıkılmaman için senin sevdiğin besinlerle hazırlanmış **3 farklı rotasyon menüsü**. Gününü seç, menünü gör ve akşam uyup uymadığını işaretle!")

    tamamlanan_gun_sayisi = 0
    basarili_gun_sayisi = 0
    kayitli_gunler = []
    try:
        with open("diyet_takvimi_kayitlari.txt", "r", encoding="utf-8") as f:
            kayitli_gunler = f.readlines()
            tamamlanan_gun_sayisi = len(kayitli_gunler)
            for kg in kayitli_gunler:
                if "✅ Tam Uydum" in kg:
                    basarili_gun_sayisi += 1
    except FileNotFoundError:
        pass

    k_col1, k_col2, k_col3 = st.columns(3)
    k_col1.metric("Tamamlanan Kamp Günü", f"{tamamlanan_gun_sayisi} / 30 Gün")
    k_col2.metric("Tam Uyulan Gün", f"{basarili_gun_sayisi} Gün", "Disiplin 🔥")
    basari_orani = int((basarili_gun_sayisi / tamamlanan_gun_sayisi) * 100) if tamamlanan_gun_sayisi > 0 else 100
    k_col3.metric("Kamp Başarı Oranı", f"%{basari_orani}")

    st.caption(f"🚀 30 Günlük Kamp İlerlemesi (%{int((tamamlanan_gun_sayisi / 30) * 100)})")
    st.progress(min(int((tamamlanan_gun_sayisi / 30.0) * 100), 100))

    st.markdown("---")

    secilen_kamp_gunu = st.selectbox(
        "📌 Planını Görmek veya İşaretlemek İstediğin Günü Seç:",
        [f"{i}. Gün" for i in range(1, 31)]
    )
    gun_no = int(secilen_kamp_gunu.split(".")[0])

    if gun_no % 3 == 1:
        menu_baslik = "🅰️ MENÜ A: Klasik Yulaf Kasesi & Çift Tavuk Günü (Yüksek Protein)"
        kahvalti = "🥣 **Kahvaltı:** 70g Yulaf + 4 YK Yoğurt + 1 Ölçek Whey Protein + 1 Muz + 1 TK Damla Çikolata & Hindistan Cevizi (~600 kcal | 45g Protein)"
        ogle = "🍗 **Öğle Yemeği:** 200g Haşlama/Izgara Tavuk Göğsü + 200g Pişmiş Basmati/Baldo Pirinç Pilavı + Bol Yeşillik (~590 kcal | 67g Protein)"
        ara_ogun = "🍏 **Antrenman Öncesi / Ara Öğün:** 10-12 Adet Çiğ Badem veya Fındık + 1 Yeşil Elma + Sade Kahve (~180 kcal | 4g Protein)"
        aksam = "🥗 **Akşam (Antrenman Sonrası):** 200g Tavuk Göğsü + 150g Pişmiş Pirinç Pilavı + Salata (1 TK Zeytinyağlı) + 1 Ölçek Whey (~640 kcal | 90g Protein)"
        toplam_ozet = "🎯 **Günlük Toplam:** ~2010 - 2150 kcal | **~206g Protein** (Sıfır Kas Kaybı!)"
    elif gun_no % 3 == 2:
        menu_baslik = "🅱️ MENÜ B: Anne Köftesi / Kıyma & Yumurta Rotasyonu"
        kahvalti = "🍳 **Kahvaltı:** 3 Tam Yumurta + 2 Yumurta Beyazı (Omlet) + 50g Yulaf (Sıcak su/süt ile) + 5-6 Zeytin + Domates/Salatalık (~520 kcal | 34g Protein)"
        ogle = "🥩 **Öğle Yemeği:** 200g Izgara Köfte veya Yağsız Dana Kıyma Sote + 200g Pişmiş Pirinç Pilavı + Mevsim Salata (~680 kcal | 52g Protein)"
        ara_ogun = "🍌 **Antrenman Öncesi / Ara Öğün:** 1 Ölçek Whey Protein + 1 Orta Boy Muz (~225 kcal | 25g Protein)"
        aksam = "🍗 **Akşam Yemeği:** 200g Tavuk Göğsü + 150g Pişmiş Pirinç Pilavı + 1 Kase Yoğurt (~620 kcal | 70g Protein)"
        toplam_ozet = "🎯 **Günlük Toplam:** ~2045 - 2150 kcal | **~181g Protein** (Demir ve Kreatin Deposu!)"
    else:
        menu_baslik = "🆎 MENÜ C: Performans & Yoğun Antrenman Günü (Bacak / Sırt Gününe İdeal)"
        kahvalti = "🥣 **Kahvaltı:** 60g Yulaf + 1 Ölçek Whey Protein + 4 YK Yoğurt + 1 Tatlı Kaşığı Fıstık Ezmesi + Tarçın (~560 kcal | 43g Protein)"
        ogle = "🍗 **Öğle Yemeği:** 250g Tavuk Göğsü + 250g Pişmiş Pirinç Pilavı + Salata (~735 kcal | 84g Protein)"
        ara_ogun = "☕ **Antrenman Öncesi:** 1 Adet Muz + 10 Çiğ Badem + Espresso/Filtre Kahve (~190 kcal | 3g Protein)"
        aksam = "🥩 **Akşam Yemeği:** 180g Köfte / Kıyma veya Tavuk + 100g Pişmiş Pirinç + Bol Yeşil Salata + 1 Kase Yoğurt (~580 kcal | 50g Protein)"
        toplam_ozet = "🎯 **Günlük Toplam:** ~2065 - 2200 kcal | **~180g Protein** (Yüksek Enerji & Pump!)"

    st.info(f"### 📋 {secilen_kamp_gunu} Beslenme Planın — {menu_baslik}\n\n"
            f"{kahvalti}\n\n"
            f"{ogle}\n\n"
            f"{ara_ogun}\n\n"
            f"{aksam}\n\n"
            f"---\n{toplam_ozet}")

    st.markdown("### ✅ Gün Sonu Kontrolü (Check-in)")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        uyum_durumu = st.radio(
            f"{secilen_kamp_gunu} Diyetine Uydun mu?",
            ["✅ Tam Uydum (Sıfır Şeker / Tam Makro)", "⚠️ Ufak Değişiklik Oldu (Kalori Tuttu)",
             "❌ Kaçamak Oldu (Cheat Meal)"]
        )
    with c_col2:
        gunluk_su_takvim = st.slider(f"{secilen_kamp_gunu} İçilen Su (Litre)", 1.0, 6.0, 4.0, 0.5)
        gunluk_not_takvim = st.text_input("Günün Notu (Örn: Pilavı annem yaptı, enerjim süperdi)")

    if st.button(f"💾 {secilen_kamp_gunu} Durumunu Takvime Kaydet", use_container_width=True):
        not_eki = f" | Not: {gunluk_not_takvim}" if gunluk_not_takvim else ""
        su_rozet = "💧 Su Hedefi Tamam" if gunluk_su_takvim >= 4.0 else "⚠️ Su Az Kaldı"
        takvim_satiri = f"[{simdi_tarih}] 📌 {secilen_kamp_gunu}: {uyum_durumu} | Su: {gunluk_su_takvim}L ({su_rozet}){not_eki}\n"

        with open("diyet_takvimi_kayitlari.txt", "a", encoding="utf-8") as f:
            f.write(takvim_satiri)
        st.success(f"{secilen_kamp_gunu} başarıyla takvime işlendi knk! Hedefe adım adım! 🔥")
        st.rerun()

    st.markdown("---")
    st.subheader("📜 30 Günlük Kamp Çizelgesi Geçmişin")
    if not kayitli_gunler:
        st.info("Henüz hiçbir günü işaretlemedin. Bugün 1. Gün ile başla!")
    else:
        for k_gun in reversed(kayitli_gunler):
            if "✅ Tam Uydum" in k_gun:
                st.success(k_gun.strip())
            elif "⚠️" in k_gun:
                st.warning(k_gun.strip())
            else:
                st.error(k_gun.strip())

# --- 2. BÖLÜM: VÜCUT DÖNÜŞÜM & FORM ARŞİVİ ---
elif menu == "📸 Vücut Dönüşüm & Form Arşivi":
    st.subheader("📸 Vücut Dönüşüm & Form Fotoğraf Arşivi")
    st.write(
        "İster bilgisayarından ister telefondan form fotoğraflarını yükle; hangi gün olduğunu ve kilosunu not et, değişimini anlık takip et!")

    UPLOAD_FOLDER = "form_fotolari"
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    with st.form("form_yukleme_formu", clear_on_submit=True):
        yuklenen_dosya = st.file_uploader("Form Fotoğrafı Seç (JPG, PNG)", type=["jpg", "jpeg", "png"])

        f_col1, f_col2 = st.columns(2)
        with f_col1:
            form_etiket = st.selectbox("Dönem / Hafta",
                                       ["1. Hafta (Başlangıç)", "10. Gün Formu", "2. Hafta Formu", "15. Gün Formu",
                                        "3. Hafta Formu", "25. Gün Formu", "30. Gün (Final Formu)", "Özel Tarih Formu"])
        with f_col2:
            form_kilo = st.text_input("O Anki Kilon & Yağ Durumu (Örn: 84.0 kg)", "84.0 kg")

        form_notu = st.text_area("Form Notu (Örn: Sabah karnı tok/aç, pump durumu vb.)")

        submit_foto = st.form_submit_button("📸 Fotoğrafı Arşive Kaydet", use_container_width=True)

        if submit_foto and yuklenen_dosya is not None:
            dosya_adi = f"{simdi_tarih.replace('.', '-')}_{yuklenen_dosya.name}"
            dosya_yolu = os.path.join(UPLOAD_FOLDER, dosya_adi)

            with open(dosya_yolu, "wb") as f:
                f.write(yuklenen_dosya.getbuffer())

            meta_satir = f"{dosya_adi}|{simdi_tarih}|{form_etiket}|{form_kilo}|{form_notu}\n"
            with open("form_arsiv_meta.txt", "a", encoding="utf-8") as meta_f:
                meta_f.write(meta_satir)

            st.success("Form fotoğrafı arşive başarıyla eklendi! 🔥")

    st.markdown("---")
    st.subheader("🏛️ Geçmiş Form Arşivin & Değişim Galerisi")

    try:
        if os.path.exists("form_arsiv_meta.txt"):
            with open("form_arsiv_meta.txt", "r", encoding="utf-8") as meta_f:
                meta_satirlar = meta_f.readlines()

            if not meta_satirlar:
                st.info("Henüz arşivde form fotoğrafı bulunmuyor.")
            else:
                for sat in reversed(meta_satirlar):
                    parcalar = sat.strip().split("|")
                    if len(parcalar) == 5:
                        d_adi, d_tarih, d_etiket, d_kilo, d_not = parcalar
                        p_yolu = os.path.join(UPLOAD_FOLDER, d_adi)

                        if os.path.exists(p_yolu):
                            with st.container():
                                st.markdown(f"### 📌 {d_etiket} — ({d_tarih})")
                                st.image(p_yolu, caption=f"Kilo: {d_kilo} | Not: {d_not}", width=350)
                                st.markdown("---")
        else:
            st.info("Henüz arşiv kaydı yok.")
    except Exception as e:
        st.warning("Arşiv yüklenirken bilgi okunamadı.")

# --- 3. BÖLÜM: AI KALORİ & BESLENME ASİSTANI ---
elif menu == "🤖 AI Kalori & Beslenme":
    st.subheader("🤖 Akıllı Besin & Kalori Hesaplayıcı Robot")

    st.caption("⚡ Hızlı Öğün Şablonları (Tıkla Otomatik Doldursun):")
    if "varsayilan_ogun" not in st.session_state:
        st.session_state[
            "varsayilan_ogun"] = "70gr yulaf, 4 yemek kaşığı yoğurt, 1 ölçek protein tozu, 1 adet muz, 1 tatlı kaşığı damla çikolata, 1 tatlı kaşığı hindistan cevizi tozu."

    s_col1, s_col2, s_col3 = st.columns(3)
    if s_col1.button("🥣 Favori Yulaf Kasem"):
        st.session_state[
            "varsayilan_ogun"] = "70gr yulaf, 4 yemek kaşığı yoğurt, 1 ölçek protein tozu, 1 adet muz, 1 tatlı kaşığı damla çikolata, 1 tatlı kaşığı hindistan cevizi tozu."
    if s_col2.button("🍗 Tavuk & Pilav"):
        st.session_state["varsayilan_ogun"] = "200gr tavuk, 150gr pilav"
    if s_col3.button("🍳 Sabah Yumurta"):
        st.session_state["varsayilan_ogun"] = "3 adet yumurta, 50gr yulaf"

    ogun_tipi = st.selectbox("Öğün Türü",
                             ["Kahvaltı", "Öğle Yemeği", "Akşam Yemeği", "Antrenman Öncesi", "Antrenman Sonrası",
                              "Ara Öğün"])
    kullanici_metni = st.text_area("Yediğin şeyleri yaz:", value=st.session_state["varsayilan_ogun"])

    if st.button("🤖 AI Robot ile Hesapla ve Kaydet", use_container_width=True):
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
                kalori += 30.0 * kasik
                protein += 0.5 * kasik
                seker += 3.0 * kasik

            elif "hindistan cevizi" in p:
                kasik = sayi if sayi < 10 else 1.0
                kalori += 25.0 * kasik
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

            elif "yumurta" in p:
                adet = sayi if sayi < 15 else 3.0
                kalori += 70.0 * adet
                protein += 6.0 * adet
                seker += 0.4 * adet

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
            bugun_kalori = 0.0
            bugun_protein = 0.0
            for s in satirlar:
                st.text(s.strip())
                if simdi_tarih in s and "Kalori: " in s:
                    try:
                        k_deger = float(s.split("Kalori: ")[1].split(" kcal")[0])
                        bugun_kalori += k_deger
                        if "Protein: " in s:
                            p_deger = float(s.split("Protein: ")[1].split("g")[0])
                            bugun_protein += p_deger
                    except:
                        pass

            st.markdown("---")
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                st.markdown(f"**🎯 Günlük Kalori:** {bugun_kalori:.0f} / 2250 kcal")
                oran_k = min(int((bugun_kalori / 2250.0) * 100), 100)
                st.progress(oran_k)
            with col_b2:
                st.markdown(f"**🥩 Günlük Protein (Kas Koruma):** {bugun_protein:.1f} / 185g")
                oran_p = min(int((bugun_protein / 185.0) * 100), 100)
                st.progress(oran_p)
    except FileNotFoundError:
        st.info("Henüz kayıt dosyası yok.")

elif menu == "🔥 Kardiyo & Yağ Yakım Hesaplayıcı":
    st.subheader("🔥 Eğimli Yürüyüş (Incline Treadmill) Kalori & Yağ Yakım Hesaplayıcı")
    st.write(
        "Kas kaybetmeden sadece yağ yakmak için en etkili silahın: **Eğimli Yürüyüş!** 84 kg ağırlığına göre bilimsel ACSM formülüyle ne kadar yaktığını hesapla.")

    c_col1, c_col2, c_col3 = st.columns(3)
    with c_col1:
        kardiyo_kilo = st.number_input("Güncel Kilon (kg)", min_value=50.0, max_value=150.0, value=84.0, step=0.5)
    with c_col2:
        hiz_kmh = st.slider("Bant Hızı (km/s)", min_value=3.0, max_value=8.0, value=5.0, step=0.2)
    with c_col3:
        egim_yuzde = st.slider("Bant Eğimi (%)", min_value=0, max_value=18, value=12, step=1)

    sure_dk = st.slider("Yürüyüş Süresi (Dakika)", min_value=10, max_value=90, value=40, step=5)

    hiz_mdk = hiz_kmh * 16.667
    egim_ondalik = egim_yuzde / 100.0
    vo2 = (0.1 * hiz_mdk) + (1.8 * hiz_mdk * egim_ondalik) + 3.5
    dk_kalori = (vo2 * kardiyo_kilo / 1000.0) * 5.0
    toplam_yakilan = dk_kalori * sure_dk
    yakilan_yag_gram = toplam_yakilan / 7.7

    st.markdown("---")
    k_m1, k_m2, k_m3 = st.columns(3)
    k_m1.metric("Yakılan Toplam Kalori", f"{toplam_yakilan:.0f} kcal", "Net Yağ Odaklı")
    k_m2.metric("Eritilen Saf Yağ", f"~{yakilan_yag_gram:.1f} gram", "Kas Kaybı Yok")
    k_m3.metric("Kardiyo Şiddeti", "Düşük-Orta Nabız", "Zone 2 (İdeal)")

    if st.button("🔥 Kardiyo Seansını Kaydet", use_container_width=True):
        kardiyo_kayit = f"[{simdi}] Incline Kardiyo: {sure_dk} dk | Hız: {hiz_kmh} km/s | Eğim: %{egim_yuzde} | Yakılan: {toplam_yakilan:.0f} kcal (~{yakilan_yag_gram:.1f}g yağ)\n"
        with open("kardiyo_kayitlari.txt", "a", encoding="utf-8") as f:
            f.write(kardiyo_kayit)
        st.success("Kardiyo seansı kaydedildi! %10-12 yağ oranına bir adım daha yaklaştın! 💪")

    st.markdown("---")
    st.subheader("📜 Geçmiş Kardiyo Seansların")
    try:
        with open("kardiyo_kayitlari.txt", "r", encoding="utf-8") as f:
            k_satirlar = f.readlines()
        if not k_satirlar:
            st.info("Henüz kardiyo kaydı girilmedi.")
        else:
            for ks in k_satirlar:
                st.text(ks.strip())
    except FileNotFoundError:
        st.info("Henüz kardiyo dosyası oluşturulmadı.")

elif menu == "💤 Uyku & Toparlanma (Recovery)":
    st.subheader("💤 Uyku & Kas Toparlanma (Recovery) Analizi")
    st.write(
        "Definasyon döneminde **kas kaybetmemenin** 1 numaralı kuralı iyi toparlanmaktır. Güncel durumunu gir, bugünkü antrenman stratejini belirleyelim!")

    u_col1, u_col2 = st.columns(2)
    with u_col1:
        uyku_saat = st.slider("Dün Gece Kaç Saat Uyudun?", 3.0, 11.0, 7.5, 0.5)
        uyku_kalite = st.selectbox("Uyku Kaliten Nasıldı?",
                                   ["Çok İyi (Deliksiz)", "Orta (1-2 kez uyandım)", "Kötü (Bölük pörçük)"])
    with u_col2:
        kas_agrisi = st.selectbox("Kas Ağrısı (DOMS) Durumu",
                                  ["Ağrı Yok / Dinç", "Hafif Tatlı Ağrı", "Çok Şiddetli Ağrı / Yorgunluk"])
        stres_enerji = st.slider("Bugünkü Enerji & Motivasyon Seviyen (1-10)", 1, 10, 8, 1)

    skor = 0
    if uyku_saat >= 7.5:
        skor += 45
    elif uyku_saat >= 6.0:
        skor += 30
    else:
        skor += 15

    if "Çok İyi" in uyku_kalite:
        skor += 20
    elif "Orta" in uyku_kalite:
        skor += 12
    else:
        skor += 5

    if "Ağrı Yok" in kas_agrisi:
        skor += 15
    elif "Hafif" in kas_agrisi:
        skor += 10
    else:
        skor += 3

    skor += (stres_enerji * 2)

    st.markdown("---")
    st.metric("⚡ Bugünkü Vücut Toparlanma (Recovery) Skorun", f"{skor} / 100")
    st.progress(min(skor, 100))

    if skor >= 80:
        st.success(
            "🚀 **MÜKEMMEL TOPARLANMA!** Kasların tamamen dinlenmiş ve glikojen depoların hazır. Bugün salonda **PR (Ağırlık Rekoru)** deneyebilir, setleri tükenişe kadar götürebilirsin!")
        tavsiye = "Tam kapasite ağır antrenman / PR Günü"
    elif skor >= 55:
        st.info(
            "👍 **ORTALAMA TOPARLANMA:** Vücudun iyi durumda ama merkezi sinir sistemini aşırı yıpratma. Bugün **mevcut ağırlıklarını koru**, forma odaklan ve 40 dk eğimli yürüyüşünü aksatma.")
        tavsiye = "Standart PPL Antrenmanı + Kardiyo"
    else:
        st.warning(
            "⚠️ **DÜŞÜK TOPARLANMA (KORTİZOL RİSKİ):** Uyku azlığı veya yorgunluk var. Definasyonda böyle günlerde çok ağır girmek **kas yıkımına veya sakatlığa** yol açabilir. Bugün ağırlıkları %10-15 düşürüp pump odaklı çalış veya aktif dinlenme yap!")
        tavsiye = "Hafif Pump Antrenmanı veya Dinlenme"

    if st.button("💤 Toparlanma Durumunu Kaydet", use_container_width=True):
        rec_kayit = f"[{simdi_tarih}] Uyku: {uyku_saat} saat ({uyku_kalite}) | Recovery Skoru: {skor}/100 | Koç Tavsiyesi: {tavsiye}\n"
        with open("recovery_kayitlari.txt", "a", encoding="utf-8") as f:
            f.write(rec_kayit)
        st.toast("Toparlanma raporu kaydedildi!", icon="💤")

    st.markdown("---")
    try:
        with open("recovery_kayitlari.txt", "r", encoding="utf-8") as f:
            for r_sat in f.readlines():
                st.text(r_sat.strip())
    except FileNotFoundError:
        pass

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
    st.subheader("🏋️‍♂️ Salonda Bastığın Ağırlıklar & PR Takibi")
    st.caption(
        "💡 İpucu: Önce çalıştığın **Kas Grubunu** seç, ardından o bölgeye ait hareketi seçip bastığın ağırlığı kaydet!")

    hareket_kutuphanesi = {
        "💪 Ön Kol (Biceps & Forearm)": [
            "Barbell Curl (Düz Bar)", "EZ-Bar Curl (Z-Bar)", "Dumbbell Alternating Curl",
            "Hammer Curl (Çekiç Tutuş)", "Incline Dumbbell Curl (Sehpada)", "Preacher Curl (Scott Sehpası / Makine)",
            "Concentration Curl", "Cable Bicep Curl (Alt Makara)", "High Cable Curl (Çift Kol Pozlama)",
            "Spider Curl", "Reverse Barbell / Cable Curl (Ön Kol & Bilek)", "Wrist Curl (Bilek Güçlendirme)",
            "➕ Listede Olmayan Özel Hareket Yaz"
        ],
        "🔱 Arka Kol (Triceps)": [
            "Triceps Rope Pushdown (Halat İtiş)", "Triceps Straight / V-Bar Pushdown (Düz/V Demir)",
            "Overhead Cable Triceps Extension (Baş Üstü Halat)", "Overhead Dumbbell Extension (Tek/Çift Dumbbell)",
            "Skullcrusher / Lying Triceps Extension (Alna Press)", "Close Grip Bench Press (Dar Tutuş Göğüs Press)",
            "Triceps Dips (Vücut Ağırlığı / Ağırlıklı)", "Bench Dips",
            "Single Arm Cable Reverse Pushdown (Tek Kol Ters Tutuş)",
            "Dumbbell Triceps Kickback", "➕ Listede Olmayan Özel Hareket Yaz"
        ],
        "🔥 Göğüs (Chest)": [
            "Barbell Bench Press", "Dumbbell Flat Bench Press", "Incline Barbell Bench Press (Üst Göğüs)",
            "Incline Dumbbell Press (Üst Göğüs)", "Chest Press Machine", "Pec Deck / Butterfly (Makine Sıkıştırma)",
            "Cable Crossover (Üst / Orta / Alt Makara)", "Dumbbell Fly / Incline Fly", "Chest Dips (Göğüs Odaklı)",
            "Push-up / Şınav", "➕ Listede Olmayan Özel Hareket Yaz"
        ],
        "🦅 Sırt (Back)": [
            "Lat Pulldown (Geniş Tutuş)", "Close Grip / V-Bar Lat Pulldown (Dar Tutuş)", "Pull-up / Barfiks",
            "Barbell Bent-Over Row", "Seated Cable Row (Oturarak Çekiş)", "One-Arm Dumbbell Row (Tek Kol Testere)",
            "T-Bar Row / Chest Supported Row", "Rope Straight-Arm Pulldown (Halatla Kanat İtiş)", "Deadlift",
            "Hyperextension (Alt Sırt / Bel)", "➕ Listede Olmayan Özel Hareket Yaz"
        ],
        "🥥 Omuz (Shoulders)": [
            "Overhead Dumbbell Shoulder Press", "Military Press / Barbell Overhead Press", "Shoulder Press Machine",
            "Smith Machine Shoulder Press", "Dumbbell Lateral Raise (Yan Omuz Açış)",
            "Cable Lateral Raise (Kabloda Yan Omuz)",
            "Face Pull (Arka Omuz & Trapez)", "Reverse Pec Deck / Rear Delt Fly (Arka Omuz Makine)",
            "Dumbbell Front Raise (Ön Omuz)",
            "Dumbbell / Barbell Shrug (Trapez)", "➕ Listede Olmayan Özel Hareket Yaz"
        ],
        "🦵 Bacak & Karın (Legs & Core)": [
            "Barbell Squat / Smith Machine Squat", "Leg Press", "Hack Squat", "Leg Extension (Ön Bacak Makine)",
            "Lying / Seated Leg Curl (Arka Bacak Makine)", "Romanian Deadlift - RDL (Arka Bacak & Kalça)",
            "Bulgarian Split Squat / Walking Lunge", "Standing / Seated Calf Raise (Kalf)",
            "Cable Crunch (Kabloda Karın)",
            "Hanging Leg Raise (Asılarak Karın)", "➕ Listede Olmayan Özel Hareket Yaz"
        ]
    }

    secilen_kas_grubu = st.selectbox("1️⃣ Kas Grubu Seç:", list(hareket_kutuphanesi.keys()))
    secilen_hareket = st.selectbox("2️⃣ Hareket Seç:", hareket_kutuphanesi[secilen_kas_grubu])

    if secilen_hareket == "➕ Listede Olmayan Özel Hareket Yaz":
        hareket = st.text_input("Hareketin Adını Yaz:", "Özel Hareket")
    else:
        hareket = secilen_hareket

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        agirlik_kg = st.number_input("Ağırlık (kg)", min_value=0.0, value=30.0, step=2.5)
    with col_p2:
        set_sayisi = st.number_input("Set Sayısı", min_value=1, value=4, step=1)
    with col_p3:
        tekrar_sayisi = st.number_input("Tekrar Sayısı", min_value=1, value=10, step=1)

    pr_notu = st.text_input("Set Notu (İsteğe bağlı - Örn: Son set drop yapıldı)")

    if st.button("🔥 Ağırlık Rekorunu Kaydet", use_container_width=True):
        not_kismi = f" | Not: {pr_notu}" if pr_notu else ""
        pr_metni = f"[{simdi_tarih}] ({secilen_kas_grubu.split()[1]}) {hareket} -> {agirlik_kg} kg ({set_sayisi} Set x {tekrar_sayisi} Tekrar){not_kismi}\n"
        with open("agirlik_rekorlari.txt", "a", encoding="utf-8") as f:
            f.write(pr_metni)
        st.success(f"{hareket} kaydı eklendi! Güçlenmeye devam 💪")

    st.markdown("---")
    st.subheader("📈 Kayıtlı Ağırlık Geçmişin")

    pr_filtre = st.text_input("🔍 Kayıtlarda Hareket veya Bölge Ara:").strip().lower()

    try:
        with open("agirlik_rekorlari.txt", "r", encoding="utf-8") as f:
            pr_satirlar = f.readlines()
        if not pr_satirlar:
            st.info("Henüz ağırlık kaydı girilmemiş.")
        else:
            for p_satir in reversed(pr_satirlar):
                if pr_filtre in p_satir.lower():
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
        dosyalar = [
            "diyet_takvimi_kayitlari.txt",
            "spor_beslenme_kayitlari.txt",
            "antrenman_programi.txt",
            "agirlik_rekorlari.txt",
            "supplement_takip.txt",
            "spor_notlari.txt",
            "kardiyo_kayitlari.txt",
            "recovery_kayitlari.txt",
            "form_arsiv_meta.txt"
        ]
        for dosya in dosyalar:
            with open(dosya, "w", encoding="utf-8") as f:
                pass
        st.success("Tüm veriler sıfırlandı!")