from datetime import datetime
import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Al-Sat Kâr Hesaplayıcı", page_icon="📱", layout="centered")

# --- KULLANICI GİRİŞ SİSTEMİ ---
if "giris_yapildi" not in st.session_state:
    st.session_state["giris_yapildi"] = False

# Belirlediğimiz izinli kullanıcılar ve şifreleri (Kullanıcı Adı : Şifre)
ICERDEKILER = {
    "enes": "1453",
    "usta": "3434",
    "servis": "2026",
    "admin": "admin"
}

# Eğer giriş yapılmadıysa sadece bu giriş ekranını göster
if not st.session_state["giris_yapildi"]:
    st.title("🔒 Yetkili Giriş Paneli")
    st.write("Bu uygulamayı kullanmak için lütfen giriş yapın.")

    with st.form("giris_formu"):
        k_adi = st.text_input("Kullanıcı Adı").strip().lower()
        sifre = st.text_input("Parola", type="password")
        buton = st.form_submit_button("Giriş Yap")

        if buton:
            if k_adi in ICERDEKILER and ICERDEKILER[k_adi] == sifre:
                st.session_state["giris_yapildi"] = True
                st.success("Giriş başarılı! Yönlendiriliyorsunuz...")
                st.rerun()
            else:
                st.error("❌ Hatalı kullanıcı adı veya parola!")

    # Giriş yapılmadıysa kodun devamını çalıştırma
    st.stop()

# --- GİRİŞ YAPILDIKTAN SONRAKİ ASIL UYGULAMA ---

# Kenar çubuğuna çıkış butonu ekleyelim
if st.sidebar.button("🚪 Çıkış Yap"):
    st.session_state["giris_yapildi"] = False
    st.rerun()

st.title("📱 Al-Sat & Tamir Kâr Hesaplayıcı")
st.write("Şirket içi mobil takip ve kâr analiz paneli.")

menu = st.sidebar.selectbox("Menü", ["Yeni Cihaz Hesapla", "Geçmiş Kayıtlar & Özet", "Kayıtları Temizle"])

if menu == "Yeni Cihaz Hesapla":
    st.subheader("💡 Yeni Cihaz Bilgileri")

    cihaz_modeli = st.text_input("Cihaz Modeli", "iPhone 15 Pro")

    col1, col2 = st.columns(2)
    with col1:
        alis_fiyati = st.number_input("Alış Fiyatı (TL)", min_value=0.0, value=50000.0, step=1000.0)
        ekran_maliyeti = st.number_input("Ekran Maliyeti (TL)", min_value=0.0, value=0.0, step=500.0)
    with col2:
        batarya_maliyeti = st.number_input("Batarya/Diğer Maliyet (TL)", min_value=0.0, value=0.0, step=500.0)
        satis_fiyati = st.number_input("Hedeflenen Satış Fiyatı (TL)", min_value=0.0, value=60000.0, step=1000.0)

    if st.button("Kârı Hesapla ve Kaydet"):
        toplam_maliyet = alis_fiyati + ekran_maliyeti + batarya_maliyeti
        net_kar = satis_fiyati - toplam_maliyet
        kar_orani = (net_kar / toplam_maliyet) * 100 if toplam_maliyet > 0 else 0

        st.markdown("---")
        st.subheader("📊 Analiz Sonucu")
...
m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric("Toplam Maliyet", f"{toplam_maliyet:,.0f} TL")
m_col2.metric("Hedef Satış", f"{satis_fiyati:,.0f} TL")
m_col3.metric("Net Kâr", f"{net_kar:,.0f} TL", delta=f"%{kar_orani:.1f}")

if net_kar <= 0:
    st.error("⚠️ DİKKAT: Bu işlemden zarar ediyorsun veya kârın yok!")
elif kar_orani < 15:
    st.warning(f"💡 BİLGİ: Kâr marjı biraz düşük (%{kar_orani:.1f}). Emeğine değmeyebilir.")
else:
    st.success("✅ HARİKA: Çok güzel ticaret, bu cihaz alınıp toplanır!")

simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
with open("ticaret_kayitlari.txt", "a", encoding="utf-8") as dosya:
    dosya.write(
        f"[{simdi}] Cihaz: {cihaz_modeli.upper()} | Maliyet: {toplam_maliyet:.0f} TL | Satış: {satis_fiyati:.0f} TL | Net Kâr: {net_kar:.0f} TL (%{kar_orani:.1f})\n")

st.toast("Başarıyla 'ticaret_kayitlari.txt' dosyasına kaydedildi!", icon="📁")

elif menu == "Geçmiş Kayıtlar & Özet":
st.subheader("📜 Geçmiş Ticaret Kayıtları")

try:
    with open("ticaret_kayitlari.txt", "r", encoding="utf-8") as dosya:
        satirlar = dosya.readlines()

    if len(satirlar) == 0:
        st.info("Henüz hiç kayıt bulunmuyor.")
    else:
        toplam_genel_kar = 0
        for satir in satirlar:
            st.text(satir.strip())
            if "Net Kâr: " in satir:
                kar_kismi = satir.split("Net Kâr: ")[1].split(" TL")[0]
                toplam_genel_kar += float(kar_kismi)

        st.markdown("---")
        col_a, col_b = st.columns(2)
        col_a.metric("Toplam Cihaz", f"{len(satirlar)} Adet")
        col_b.metric("Toplam Net Kâr", f"{toplam_genel_kar:,.0f} TL")

except FileNotFoundError:
    st.warning("Henüz kayıt dosyası oluşturulmamış. 'Yeni Cihaz Hesapla' sekmesinden kayıt ekleyebilirsin.")

elif menu == "Kayıtları Temizle":
st.subheader("🗑️ Kayıt Yönetimi")
if st.button("Tüm Geçmiş Kayıtları Sil"):
    with open("ticaret_kayitlari.txt", "w", encoding="utf-8") as dosya:
        pass
    st.success("Tüm geçmiş kayıtlar temizlendi!")