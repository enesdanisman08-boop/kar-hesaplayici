from datetime import datetime
import os
import time
import streamlit as st

# Sayfa Ayarları ve Mobil PWA Entegrasyonu
st.set_page_config(page_title="GYM HUB | Enes Spor Paneli", page_icon="⚡", layout="wide")

# --- OTURUM VE SAYFA HAFIZASI (SESSION STATE) ---
if "giris_yapildi" not in st.session_state:
    st.session_state["giris_yapildi"] = False

if "secilen_tema" not in st.session_state:
    st.session_state["secilen_tema"] = "Koyu"

if "aktif_sayfa" not in st.session_state:
    st.session_state["aktif_sayfa"] = "🏠 Ana Menü (Komuta Merkezi)"

SAYFA_LISTESI = [
    "🏠 Ana Menü (Komuta Merkezi)",
    "📅 30 Günlük Diyet & Takvim",
    "🍳 Sporcu Tarif & Mutfak Defteri",
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


def sayfa_degistir(hedef_sayfa):
    st.session_state["aktif_sayfa"] = hedef_sayfa


def tema_degistir():
    if st.session_state["secilen_tema"] == "Koyu":
        st.session_state["secilen_tema"] = "Acik"
    else:
        st.session_state["secilen_tema"] = "Koyu"


ICERDEKILER = {
    "enes": "1453",
    "admin": "admin"
}

# Üstteki GitHub, Share, Yıldız ve Sağ Alttaki Manage App butonlarını gizleyen genel CSS
gizleme_css = """
[data-testid="stToolbarActions"],
[data-testid="stAppDeployButton"],
#MainMenu,
footer {
    display: none !important;
    visibility: hidden !important;
}
header[data-testid="stHeader"] {
    background: transparent !important;
}
"""

# --- MİNİMALİST GYM HUB GİRİŞ EKRANI ---
if not st.session_state["giris_yapildi"]:
    st.markdown(f"""
<style>
{gizleme_css}
.stApp {{
    background: radial-gradient(circle at top, #181c24 0%, #0b0e14 100%);
    color: #f8fafc;
}}
div[data-testid="stForm"] {{
    background-color: #12161f !important;
    border: 1px solid #262c3a !important;
    border-radius: 18px !important;
    padding: 35px 30px !important;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6) !important;
    margin-top: 60px !important;
}}
.gymhub-logo {{
    font-size: 32px;
    font-weight: 800;
    text-align: center;
    letter-spacing: 2px;
    color: #ffffff;
    margin-bottom: 4px;
}}
.gymhub-logo span {{
    color: #6366f1;
}}
.gymhub-welcome {{
    text-align: center;
    color: #94a3b8;
    font-size: 14px;
    margin-bottom: 25px;
    font-weight: 500;
}}
.stButton>button {{
    background: linear-gradient(90deg, #4f46e5 0%, #6366f1 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    height: 44px !important;
    border: none !important;
    margin-top: 10px !important;
}}
.stButton>button:hover {{
    opacity: 0.92 !important;
}}
</style>
""", unsafe_allow_html=True)

    # Dar ve minimal bir orta kolon
    col1, col2, col3 = st.columns([1.3, 1.4, 1.3])
    with col2:
        with st.form("giris_formu"):
            st.markdown('<div class="gymhub-logo">⚡ GYM<span>HUB</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="gymhub-welcome">Hoş Geldiniz • Sporcu Komuta Merkezi</div>',
                        unsafe_allow_html=True)

            k_adi = st.text_input("Sporcu Kimliği", placeholder="Sporcu Adı )",
                                  label_visibility="collapsed").strip().lower()
            sifre = st.text_input("Erişim Şifresi", type="password", placeholder="Erişim Parolası",
                                  label_visibility="collapsed")
            buton = st.form_submit_button("Giriş Yap →", use_container_width=True)

            if buton:
                if k_adi in ICERDEKILER and ICERDEKILER[k_adi] == sifre:
                    st.session_state["giris_yapildi"] = True
                    st.rerun()
                else:
                    st.error("❌ Kimlik veya parola hatalı!")

    st.stop()

# --- SOL MENÜ (SIDEBAR) ---
with st.sidebar:
    st.markdown("## 🧭 Navigasyon")
    secilen_menu = st.selectbox(
        "Gitmek İstediğin Bölüm:",
        SAYFA_LISTESI,
        index=SAYFA_LISTESI.index(st.session_state["aktif_sayfa"])
    )

    if secilen_menu != st.session_state["aktif_sayfa"]:
        st.session_state["aktif_sayfa"] = secilen_menu
        st.rerun()

    menu = st.session_state["aktif_sayfa"]

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

# --- SAĞ ÜST KÖŞE YUVARLAK İKONLU TEMA BUTONU & ANA MENÜYE DÖNÜŞ ---
top_col1, top_col2 = st.columns([10, 2])
with top_col1:
    if menu != "🏠 Ana Menü (Komuta Merkezi)":
        st.button("⬅️ Ana Menüye Dön", on_click=sayfa_degistir, args=("🏠 Ana Menü (Komuta Merkezi)",))
with top_col2:
    tema_ikonu = "☀️" if st.session_state["secilen_tema"] == "Koyu" else "🌙"
    st.button(tema_ikonu, key="tema_btn", on_click=tema_degistir)

secilen_tema = st.session_state["secilen_tema"]

# --- DİNAMİK TEMA VE YUVARLAK BUTON STİLLERİ ---

ortak_css = f"""
{gizleme_css}
.block-container {{
    padding-top: 3.5rem !important;
}}
div.st-key-tema_btn {{
    display: flex;
    justify-content: flex-end;
    margin-top: 10px !important;
    margin-right: 15px !important;
}}
div.st-key-tema_btn button {{
    border-radius: 50% !important;
    width: 50px !important;
    height: 50px !important;
    min-height: 50px !important;
    padding: 0 !important;
    font-size: 24px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.35) !important;
    transition: transform 0.2s ease !important;
}}
div.st-key-tema_btn button:hover {{
    transform: scale(1.1) !important;
}}
"""

if secilen_tema == "Koyu":
    st.markdown(f"""
<style>
{ortak_css}
.stApp {{ background-color: #0e1117; color: #fafafa; }}
div[data-testid="stMetric"] {{ background-color: #262730; border: 1px solid #4f46e5; padding: 12px; border-radius: 10px; }}
.stButton>button {{ background-color: #4f46e5 !important; color: #ffffff !important; font-weight: bold !important; border-radius: 8px !important; border: none !important; }}
div.st-key-tema_btn button {{
    background-color: #1e293b !important;
    border: 2px solid #4f46e5 !important;
}}
.custom-card {{
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
    color: #fafafa !important;
}}
.custom-card h3 {{ color: #ffffff !important; margin-top: 0 !important; }}
.custom-card p {{ color: #cbd5e1 !important; margin-bottom: 0 !important; }}
</style>
""", unsafe_allow_html=True)

else:  # Açık Mod
    st.markdown(f"""
<style>
{ortak_css}
.stApp {{ background-color: #f8fafc; color: #0f172a; }}
.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp span, .stApp label {{ color: #0f172a !important; }}
div[data-testid="stSidebar"] {{ background-color: #f1f5f9 !important; }}
div[data-testid="stMetric"] {{ background-color: #ffffff; border: 1px solid #cbd5e1; padding: 12px; border-radius: 10px; color: #0f172a !important; }}
.stButton>button {{ background-color: #0284c7 !important; color: #ffffff !important; font-weight: bold !important; border-radius: 8px !important; border: none !important; }}
.stButton>button p {{ color: #ffffff !important; }}
div.st-key-tema_btn button {{
    background-color: #ffffff !important;
    border: 2px solid #0284c7 !important;
}}
.custom-card {{
    background-color: #ffffff !important;
    border: 2px solid #cbd5e1 !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
    color: #0f172a !important;
}}
.custom-card h3 {{ color: #0f172a !important; margin-top: 0 !important; }}
.custom-card p {{ color: #334155 !important; margin-bottom: 0 !important; }}
</style>
""", unsafe_allow_html=True)

simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
simdi_tarih = datetime.now().strftime("%d.%m.%Y")

# --- ANA MENÜ (KOMUTA MERKEZİ) ---
if menu == "🏠 Ana Menü (Komuta Merkezi)":
    st.title("💪 Enes Fitness & Yaşam Komuta Merkezi")
    st.write("84 kg (%16 Yağ) ➡️ 80.5 kg (%11 Yağ) Kas Korumalı Definasyon Kampına Hoş Geldin!")

    st.markdown("---")
    st.subheader("🚀 Hızlı Erişim & Ana Menü")
    st.caption("Aşağıdaki kutuların altındaki butonlara tıkladığın an doğrudan o bölüme ışınlanırsın:")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            '<div class="custom-card"><h3>📅 30 Günlük Kamp</h3><p>Günlük rotasyon menüleri, kalori takibi ve akşam check-in sistemi.</p></div>',
            unsafe_allow_html=True)
        st.button("Kamp Paneline Git ➡️", use_container_width=True, key="btn_kamp", on_click=sayfa_degistir,
                  args=("📅 30 Günlük Diyet & Takvim",))

        st.write("")
        st.markdown(
            '<div class="custom-card"><h3>🍳 Tarif & Mutfak</h3><p>Profesyonel sporcu tarifleri ve kendi defterine not ettiklerin.</p></div>',
            unsafe_allow_html=True)
        st.button("Tariflere Git ➡️", use_container_width=True, key="btn_tarif", on_click=sayfa_degistir,
                  args=("🍳 Sporcu Tarif & Mutfak Defteri",))

        st.write("")
        st.markdown(
            '<div class="custom-card"><h3>💤 Uyku & Recovery</h3><p>Uyku kaliteni ve kas ağrılarını gir, günlük antrenman temposunu öğren.</p></div>',
            unsafe_allow_html=True)
        st.button("Recovery Analizine Git ➡️", use_container_width=True, key="btn_rec", on_click=sayfa_degistir,
                  args=("💤 Uyku & Toparlanma (Recovery)",))

    with c2:
        st.markdown(
            '<div class="custom-card"><h3>📸 Form Arşivi</h3><p>Haftalık form fotoğraflarını yükle, kilo ve yağ değişimini incele.</p></div>',
            unsafe_allow_html=True)
        st.button("Arşive Git ➡️", use_container_width=True, key="btn_arsiv", on_click=sayfa_degistir,
                  args=("📸 Vücut Dönüşüm & Form Arşivi",))

        st.write("")
        st.markdown(
            '<div class="custom-card"><h3>🤖 AI Kalori Asistanı</h3><p>Yediğin öğünleri yaz, kalori ve protein değerini anında hesaplasın.</p></div>',
            unsafe_allow_html=True)
        st.button("AI Asistana Git ➡️", use_container_width=True, key="btn_ai", on_click=sayfa_degistir,
                  args=("🤖 AI Kalori & Beslenme",))

        st.write("")
        st.markdown(
            '<div class="custom-card"><h3>🗓️ PPL Antrenman Takvimi</h3><p>Haftalık Push-Pull-Legs günlerini ve antrenman notlarını kaydet.</p></div>',
            unsafe_allow_html=True)
        st.button("PPL Takvimine Git ➡️", use_container_width=True, key="btn_ppl", on_click=sayfa_degistir,
                  args=("🗓️ Antrenman & PPL Takvimi",))

    with c3:
        st.markdown(
            '<div class="custom-card"><h3>🔥 Kardiyo & Yağ Yakım</h3><p>Eğimli yürüyüşte (Incline Treadmill) yaktığın saf yağı hesapla.</p></div>',
            unsafe_allow_html=True)
        st.button("Kardiyoya Git ➡️", use_container_width=True, key="btn_kardiyo", on_click=sayfa_degistir,
                  args=("🔥 Kardiyo & Yağ Yakım Hesaplayıcı",))

        st.write("")
        st.markdown(
            '<div class="custom-card"><h3>🏋️‍♂️ Ağırlık & PR Takibi</h3><p>Salonda bastığın ağırlıkları, ön/arka kol rekorlarını kaydet.</p></div>',
            unsafe_allow_html=True)
        st.button("PR Takibine Git ➡️", use_container_width=True, key="btn_pr", on_click=sayfa_degistir,
                  args=("🏋️‍♂️ Ağırlık & PR Takibi",))

        st.write("")
        st.markdown(
            '<div class="custom-card"><h3>💧 Supplement & Su</h3><p>Günlük 4 litre su hedefini ve Whey, Kreatin, Omega-3 kullanımını işaretle.</p></div>',
            unsafe_allow_html=True)
        st.button("Supplement Takibine Git ➡️", use_container_width=True, key="btn_supp", on_click=sayfa_degistir,
                  args=("💧 Supplement & Su",))

    st.markdown("---")
    st.info(
        "💡 **Günün Motivasyon İpucu:** *“Ağrıyı hissedemeyenler asla kazanamaz. 80.5 kiloya ve %11 yağ oranına ulaşana kadar durmak yok!”* 🔥")

# --- 1. BÖLÜM: 30 GÜNLÜK DİYET & KAMP TAKVİMİ ---
elif menu == "📅 30 Günlük Diyet & Takvim":
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

# --- 2. BÖLÜM: SPORCU TARİF & MUTFAK DEFTERİ ---
elif menu == "🍳 Sporcu Tarif & Mutfak Defteri":
    st.subheader("🍳 Sporcu Mutfak Defteri & AI Tarif Kataloğu")
    st.write(
        "Burada hem profesyonel diyet tariflerini (tam ölçü ve adım adım hazırlanışlarıyla) inceleyebilir hem de kendi yaptığın özel tarifleri not edebilirsin!")

    tab1, tab2 = st.tabs(["📖 Örnek AI / Sporcu Tarif Kataloğu", "✍️ Kendi Tarifini Deftere Ekle"])

    with tab1:
        st.markdown("### 🏆 En Popüler Diyet & Fitness Tarifleri")

        secilen_katalog_tarif = st.selectbox(
            "İncelemek İstediğin Tarifi Seç:",
            [
                "🥣 Çikolatalı & Muzlu Proteinli Yulaf Kasesi",
                "🍗 Lokum Gibi Sulu Tavuk Göğsü & Baldo Pirinç Pilavı",
                "🥩 Anne Usulü Yağsız Diyet Köfte Sote",
                "🥞 Şekersiz Yulaf & Muzlu Protein Pankeki"
            ]
        )

        if "Yulaf Kasesi" in secilen_katalog_tarif:
            st.info("""
            ### 🥣 Çikolatalı & Muzlu Proteinli Yulaf Kasesi
            * **Öğün Türü:** Kahvaltı / Antrenman Öncesi
            * **Besin Değeri:** ~580 kcal | 42g Protein | 65g Karbonhidrat

            #### 🛒 Malzemeler:
            * 70g Yulaf Ezmesi
            * 1 su bardağı (200ml) Yağsız Süt veya Sıcak Su
            * 4 yemek kaşığı Süzme Yoğurt
            * 1 ölçek Çikolatalı Whey Protein Tozu
            * 1 adet Orta Boy Muz (Dilimlenmiş)
            * 1 tatlı kaşığı Damla Çikolata veya Kakao

            #### 👨‍🍳 Adım Adım Hazırlanışı:
            1. **Yulafın Pişirilmesi:** Yulafı bir kaseye alın, üzerine sıcak suyu veya sütü ekleyip 3-4 dakika yumuşayana kadar mikrodalgada veya ocakta ısıtın.
            2. **Protein Karışımı:** Yulaf biraz ılındıktan sonra içine 1 ölçek çikolatalı whey protein tozunu ve süzme yoğurdu ekleyip pürüzsüz kıvam alana kadar iyice karıştırın.
            3. **Süsleme:** Üzerine dilimlenmiş muzları dizin. 1 tatlı kaşığı damla çikolata serperek servis edin. Afiyet olsun knk!
            """)

        elif "Tavuk" in secilen_katalog_tarif:
            st.info("""
            ### 🍗 Lokum Gibi Sulu Tavuk Göğsü & Baldo Pirinç Pilavı
            * **Öğün Türü:** Öğle / Akşam Ana Öğün
            * **Besin Değeri:** ~620 kcal | 75g Protein | 70g Karbonhidrat

            #### 🛒 Malzemeler:
            * 200g Tavuk Göğsü (Kuşbaşı veya Fileto)
            * 150g Pişmiş Baldo veya Basmati Pirinç
            * 1 tatlı kaşığı Zeytinyağı veya Tereyağı
            * Baharatlar: Tuz, karabiber, kekik, toz kırmızı biber, sarımsak tozu

            #### 👨‍🍳 Adım Adım Hazırlanışı:
            1. **Pirinç Pilavı Tarifi:** 1 çay bardağı pirinci ılık suda 15 dakika bekletip nişastası akana kadar yıkayın. Tencerede 1 tatlı kaşığı zeytinyağı ile pirinçleri 2-3 dakika kavurun. Üzerine **1.5 su bardağı sıcak su** ve biraz tuz ekleyip kısık ateşte suyunu çekene kadar pişmeye bırakın. Suyunu çekince altını kapatıp 10 dk dinlendirin.
            2. **Tavuk Marine & Pişirme:** Tavuk göğsünü küp doğrayın. Zeytinyağı ve baharatlarla (kekik, kırmızı biber, sarımsak) harmanlayın. Yapışmaz teflon tavayı yüksek ateşte ısıtın (yağ eklemenize gerek yok). Tavukları tavaya atıp suyunu salıp çekene kadar yaklaşık 8-10 dakika mühürleyin.
            3. **Servis:** Yanına bol yeşillikli salata ile tabağa dizin!
            """)

        elif "Köfte" in secilen_katalog_tarif:
            st.info("""
            ### 🥩 Anne Usulü Yağsız Diyet Köfte Sote
            * **Öğün Türü:** Öğle Yemeği
            * **Besin Değeri:** ~650 kcal | 55g Protein | 60g Karbonhidrat

            #### 🛒 Malzemeler:
            * 200g Yağsız Dana Kıyma (%5 yağ oranlı)
            * 1 adet küçük boy rendelenmiş soğan ve 1 diş sarımsak
            * 2 yemek kaşığı galeta unu veya yulaf unu
            * 200g Pişmiş Pirinç Pilavı (Yanı için)

            #### 👨‍🍳 Adım Adım Hazırlanışı:
            1. **Köfte Harcı:** Kıyma, rendelenmiş soğan, sarımsak, galeta unu, tuz ve karabiberi bir kapta 5 dakika yoğurun. Ceviz büyüklüğünde yuvarlaklar yapın.
            2. **Pişirme:** Izgara tavada veya fırında 200 derecede 15 dakika yağsız olarak pişirin. Pilav ile servis edin.
            """)

        elif "Pankek" in secilen_katalog_tarif:
            st.info("""
            ### 🥞 Şekersiz Yulaf & Muzlu Protein Pankeki
            * **Öğün Türü:** Kahvaltı / Tatlı Krizi Giderici
            * **Besin Değeri:** ~450 kcal | 35g Protein | 50g Karbonhidrat

            #### 🛒 Malzemeler:
            * 50g Yulaf Unu (Yulafı blenderdan geçirin)
            * 1 adet olgun muz (Çatalla ezilmiş)
            * 1 tam yumurta + 1 yumurta beyazı
            * 1 ölçek Protein Tozu (Vanilya veya Çikolata)

            #### 👨‍🍳 Adım Adım Hazırlanışı:
            1. Ezilmiş muz, yumurtalar, yulaf unu ve protein tozunu bir kapta çırpın. Boza kıvamına gelmelidir (kıvam koyu olursa çok az süt/su ekleyin).
            2. Isıtılmış yapışmaz tavaya kepçeyle dökün, göz göz olunca ters çevirip pişirin. Üzerine bal veya fıstık ezmesi gezdirerek yiyebilirsiniz!
            """)

    with tab2:
        st.markdown("### ✍️ Kendi Tarifini Deftere Kaydet")

        with st.form("kendi_tarif_formu", clear_on_submit=True):
            t_adi = st.text_input("Tarifin Adı (Örn: Enes'in Özel Tavuklu Makarnası)")
            t_tur = st.selectbox("Öğün Türü", ["Kahvaltı", "Öğle Yemeği", "Akşam Yemeği", "Ara Öğün / Tatlı"])
            t_malzeme = st.text_area("Malzemeler (Örn: 200g tavuk, 1 paket makarna vb.)")
            t_tarif = st.text_area("Hazırlanışı / Sos Tarifi (Örn: Su kaynatılır, sos için salça kavrulur...)")

            kaydet_btn = st.form_submit_button("💾 Tarifi Deftere Kaydet", use_container_width=True)

            if kaydet_btn:
                if t_adi and t_tarif:
                    tarif_satiri = f"[{simdi_tarih}] 🍳 **{t_adi}** ({t_tur})\n* **Malzemeler:** {t_malzeme}\n* **Tarif:** {t_tarif}\n---\n"
                    with open("kullanici_tarifleri.txt", "a", encoding="utf-8") as tf:
                        tf.write(tarif_satiri)
                    st.success("Tarifin başarıyla deftere kaydedildi knk! 🔥")
                else:
                    st.error("Lütfen tarif adını ve hazırlanışını boş bırakma.")

        st.markdown("---")
        st.markdown("### 📜 Senin Kaydettiğin Özel Tarifler:")
        try:
            if os.path.exists("kullanici_tarifleri.txt"):
                with open("kullanici_tarifleri.txt", "r", encoding="utf-8") as tf:
                    icerik = tf.read()
                if icerik.strip():
                    st.markdown(icerik)
                else:
                    st.info("Henüz kendi defterine kaydettiğin bir tarif yok.")
            else:
                st.info("Henüz tarif defteri dosyası oluşmadı.")
        except Exception as e:
            st.info("Kayıtlar okunurken hata oluştu.")

# --- 3. BÖLÜM: VÜCUT DÖNÜŞÜM & FORM ARŞİVİ ---
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

# --- 4. BÖLÜM: AI KALORİ & BESLENME ASİSTANI ---
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

# --- 5. BÖLÜM: KARDİYO & YAĞ YAKIM ---
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

# --- 6. BÖLÜM: UYKU & TOPARLANMA ---
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

# --- 7. BÖLÜM: ANTRENMAN & PPL TAKVİMİ ---
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

# --- 8. BÖLÜM: AĞIRLIK & PR TAKİBİ ---
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

# --- 9. BÖLÜM: SUPPLEMENT & SU ---
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

# --- 10. BÖLÜM: NOTLAR & HEDEFLER ---
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

# --- 11. BÖLÜM: KAYITLARI TEMİZLE ---
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
            "form_arsiv_meta.txt",
            "kullanici_tarifleri.txt"
        ]
        for dosya in dosyalar:
            with open(dosya, "w", encoding="utf-8") as f:
                pass
        st.success("Tüm veriler sıfırlandı!")