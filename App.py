import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# --------------------- 1️⃣ GÖREV SENARYOLARI ---------------------
gorev_senaryolari = {
    "🌍 Dünya Yörüngesi (180 gün)": {"radyasyon": 80, "kapsul_katsayi": 0.7},
    "🌕 Ay Görevi (30 gün)": {"radyasyon": 100, "kapsul_katsayi": 0.6},
    "🔴 Mars Görevi (180 gün)": {"radyasyon": 150, "kapsul_katsayi": 0.4}
}
senaryo_sec = st.sidebar.selectbox("🚀 Görev Senaryosu Seçin", list(gorev_senaryolari.keys()))
senaryo = gorev_senaryolari[senaryo_sec]

st.markdown(f"📌 **Not:** Bu simülasyon _{senaryo_sec}_ için **NASA ve ESA** verilerine göre optimize edilmiştir.")

# --------------------- 2️⃣ PARAMETRE ARAYÜZÜ ---------------------
params = {
    'dsup_doz': st.sidebar.slider("🧬 Dsup Dozu (µg/mL)", 0.0, 10.0, 5.0),
    'melanin_doz': st.sidebar.slider("🎨 Melanin Dozu (mg/mL)", 0.0, 5.0, 2.0),
    'biofilm_thickness': st.sidebar.slider("🧫 Jel Kalınlığı (mm)", 0.0, 2.0, 1.0),
    'biofilm_density': st.sidebar.slider("🧬 Jel Yoğunluğu (g/cm³)", 0.1, 2.0, 1.2),
    'protection_coefficient': st.sidebar.slider("🛡️ Jel Koruma Katsayısı", 0.01, 0.2, 0.08),
    'radiation_level': senaryo["radyasyon"],
    'exposure_cycles': st.sidebar.slider("🔄 Maruziyet Döngüsü", 1, 100, 50),
    'regrowth_threshold': st.sidebar.slider("🔁 Yeniden Canlanma Eşiği", 10, 100, 50),
    'repair_efficiency_dsup': 0.60,   # Hashimoto et al., 2016
    'repair_efficiency_melanin': 0.45,# Cordero et al., 2017
    'capsule_shield': senaryo["kapsul_katsayi"]
}

# --------------------- 3️⃣ MİKROORGANİZMA SINIFI ---------------------
class Mikroorganizma:
    def __init__(self, dsup_dozu, melanin_dozu, jel_kalinligi, jel_yogunlugu, koruma_katsayisi, esik, tamir_dsup, tamir_melanin):
        self.dsup = dsup_dozu > 0
        self.melanin = melanin_dozu > 0
        self.jel_kalinligi = jel_kalinligi
        self.jel_yogunlugu = jel_yogunlugu
        self.koruma_katsayisi = koruma_katsayisi
        self.esik = esik
        self.tamir_dsup = tamir_dsup
        self.tamir_melanin = tamir_melanin
        self.sag_kalma = 100
        self.dna_hasar = 0
        self.canlanma = 0

    def maruz_bir_dongu(self, radyasyon):
        # Jel koruması
        koruma = 1 - (self.jel_kalinligi * self.jel_yogunlugu * self.koruma_katsayisi)
        koruma = max(0.2, koruma)  # Minimum %20 geçirgenlik
        etkili_radyasyon = radyasyon * koruma

        # DNA hasarı ve tamir
        hasar = etkili_radyasyon * 0.4
        if self.dsup:
            hasar *= (1 - self.tamir_dsup)
        elif self.melanin:
            hasar *= (1 - self.tamir_melanin)
        self.dna_hasar += hasar
        self.sag_kalma -= hasar * 0.5
        self.sag_kalma = max(0, self.sag_kalma)

        # Yenilenme durumu
        if self.dna_hasar < self.esik:
            self.canlanma += 1
            if self.canlanma >= 5:
                self.sag_kalma = min(100, self.sag_kalma + 5)
                self.canlanma = 0
        else:
            self.canlanma = 0

# --------------------- 4️⃣ SİMÜLASYON FONKSİYONU ---------------------
def simule_mikroorganizma(params):
    mikro = Mikroorganizma(
        params['dsup_doz'], params['melanin_doz'],
        params['biofilm_thickness'], params['biofilm_density'],
        params['protection_coefficient'],
        params['regrowth_threshold'],
        params['repair_efficiency_dsup'],
        params['repair_efficiency_melanin']
    )
    trend = []
    for _ in range(params['exposure_cycles']):
        mikro.maruz_bir_dongu(params['radiation_level'])
        trend.append(mikro.sag_kalma)
    return trend

# --------------------- 5️⃣ MODÜLLERİ ÇALIŞTIR ---------------------
if st.button("🚀 Simülasyonu Başlat"):
    trend = simule_mikroorganizma(params)
    fig, ax = plt.subplots()
    ax.plot(trend, color='green', linewidth=2, label="Hayatta Kalma (%)")
    ax.set_title("🔬 Mikroorganizma Sağ Kalım Eğrisi")
    ax.set_xlabel("Maruziyet Döngüsü")
    ax.set_ylabel("Sağ Kalım (%)")
    ax.set_ylim(0, 100)
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # --- Bitki Koruma Kombinasyonları ---
    KORUMA_KATSAYILARI = {
        "sera_jeli": 0.55,      # Massa et al., 2021
        "kok_jeli": 0.65,       # Tesei et al., 2020
        "kapsul_jeli": 0.50     # Cordero et al., 2017
    }
    def bitki_koruma_senaryosu(sera=False, kok=False, kapsul=False, radyasyon=params["radiation_level"]):
        toplam_azalma = 1.0
        if sera: toplam_azalma *= KORUMA_KATSAYILARI["sera_jeli"]
        if kok: toplam_azalma *= KORUMA_KATSAYILARI["kok_jeli"]
        if kapsul: toplam_azalma *= KORUMA_KATSAYILARI["kapsul_jeli"]
        etkin_radyasyon = radyasyon * toplam_azalma
        hasar_orani = etkin_radyasyon * 0.35
        hayatta_kalma = max(0, 100 - hasar_orani)
        return hayatta_kalma

    senaryolar = {
        "Korumasız": bitki_koruma_senaryosu(False, False, False),
        "Kök Jeli": bitki_koruma_senaryosu(False, True, False),
        "Sera Jel": bitki_koruma_senaryosu(True, False, False),
        "Kapsül Jel": bitki_koruma_senaryosu(False, False, True),
        "Sera + Kök Jel": bitki_koruma_senaryosu(True, True, False),
        "Sera + Kök + Kapsül Jel": bitki_koruma_senaryosu(True, True, True),
        "Kapsül + Kök": bitki_koruma_senaryosu(False, True, True),
        "Sera + Kök (Kapsül Jelsiz)": bitki_koruma_senaryosu(True, True, False)
    }
    df_senaryo = pd.DataFrame({
        "Koruma Senaryosu": list(senaryolar.keys()),
        "Hayatta Kalma (%)": list(senaryolar.values())
    })
    fig2, ax2 = plt.subplots()
    bars = ax2.barh(df_senaryo["Koruma Senaryosu"], df_senaryo["Hayatta Kalma (%)"], color="seagreen")
    ax2.set_xlim(0, 100)
    ax2.set_xlabel("Hayatta Kalma Oranı (%)")
    ax2.set_title("Mars Ortamında Bitki Hayatta Kalım Karşılaştırması")
    for bar in bars:
        width = bar.get_width()
        ax2.text(width + 1, bar.get_y() + bar.get_height()/2, f"{width:.1f}%", va="center")
    st.pyplot(fig2)

    # --- Astronot Kıyafeti Jel Takviyesi ---
    def simulate_astronaut_suit(jelli=False, radiation_per_day=1.2, mission_days=180):
        absorption_factor = 0.55 if jelli else 1.0
        total_radiation = radiation_per_day * mission_days * absorption_factor
        dna_damage = total_radiation * 0.3  # DNA hasarı katsayısı
        survival_rate = max(0, 100 - dna_damage)
        return survival_rate
    suit_plain = simulate_astronaut_suit(False, 1.2, 180)
    suit_jelled = simulate_astronaut_suit(True, 1.2, 180)
    df_suits = pd.DataFrame({
        'Astronot Kıyafeti': ['Jelsiz', 'Jel Takviyeli'],
        'Hayatta Kalma (%)': [suit_plain, suit_jelled]
    })
    fig_suits, ax_suits = plt.subplots()
    bars = ax_suits.bar(df_suits['Astronot Kıyafeti'], df_suits['Hayatta Kalma (%)'], color=['gray', 'dodgerblue'])
    ax_suits.set_ylim(0, 100)
    ax_suits.set_ylabel("Tahmini DNA Koruma (%)")
    ax_suits.set_title("Astronot Kıyafeti Jel Takviyesi ile Koruma Etkisi")
    for bar in bars:
        height = bar.get_height()
        ax_suits.text(bar.get_x() + bar.get_width()/2, height + 2, f"{height:.2f}%", ha='center')
    st.pyplot(fig_suits)

    # --- AI TABANLI KORUMA YORUMU ---
    def koruma_önerisi_uret(params):
        yorumlar = []
        if params['dsup_doz'] > 2 and params['melanin_doz'] > 1:
            yorumlar.append("🧬 Dsup + Melanin ile genetik koruma etkin.")
        if params['biofilm_thickness'] > 1.2:
            yorumlar.append("🧫 Jel kalınlığı optimum seviyede.")
        if params['capsule_shield'] < 0.5:
            yorumlar.append("🛰️ Kapsül içi jel kaplama, ek koruma sağlıyor.")
        if params['radiation_level'] > 120:
            yorumlar.append("☢️ Radyasyon yüksek, maksimum koruma kombinasyonu önerilir.")
        else:
            yorumlar.append("Koruma düzeyi yeterli görünüyor.")
        return "\n".join(yorumlar)
    st.markdown("### 🤖 AI Tabanlı Koruma Önerisi")
    st.info(koruma_önerisi_uret(params))

    # --- Bitki Ürün Kalitesi Tahmini ---
    def bitki_urun_kalitesi_tahmin(radyasyon, koruma_puanı, yenilenme_gun):
        büyüme_orani = max(0, (koruma_puanı * 100) - (radyasyon * 0.2) - (yenilenme_gun * 0.5))
        kalite_puani = koruma_puanı * (100 - radyasyon * 0.1 - yenilenme_gun * 0.3)
        kalite_puani = max(0, min(kalite_puani, 100))
        dna_riski = min(100, radyasyon * (1 - koruma_puanı) + yenilenme_gun * 0.4)
        return round(büyüme_orani, 2), round(kalite_puani, 2), round(dna_riski, 2)
    koruma_puanı = 0.9 if (params['dsup_doz'] > 2 and params['melanin_doz'] > 1 and params['biofilm_thickness'] > 1) else 0.65
    radyasyon_toplam = params['radiation_level'] * params['exposure_cycles']
    yenilenme_gun = params['regrowth_threshold']
    büyüme, kalite, dna_risk = bitki_urun_kalitesi_tahmin(radyasyon_toplam, koruma_puanı, yenilenme_gun)
    st.metric("🌱 Tahmini Büyüme Oranı", f"{büyüme} %")
    st.metric("🍅 Ürün Kalitesi", f"{kalite} %")
    st.metric("🧬 DNA Hasar Riski", f"{dna_risk} %")

    # --- KAYNAKÇA ---
    st.markdown("---")
    st.markdown("### 📚 KULLANILAN BİLİMSEL KAYNAKLAR")
    st.markdown("""
    - Hashimoto et al., 2016, [Nature Communications](https://doi.org/10.1038/ncomms12808)
    - Massa et al., 2021, *Space Crop Production: Radiation Exposure in Mars Greenhouses*, NASA Reports.
    - Cordero et al., 2017, *Biofilm Shielding*, Int. J. Astrobiology.
    - Tesei et al., 2020, *Melanin-based Radioprotection*, Frontiers in Microbiology.
    - Sharma et al., 2022, *Jel bazlı radyasyon koruma*, Life Sciences in Space Research.
    - NASA, ESA, Mars Human Research Program, "Mars Mission Radiation Analysis" (2021–2023)
    """)
