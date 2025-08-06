import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Mikroorganizma sınıfı
class BiyoFilmMikroorganizma:
    def __init__(self, dsup=False, melanin=False, biofilm_density=1.2, gel_thickness=1.0,
                 regrowth_delay=3, dsup_effect=2.5, melanin_effect=1.8, biofilm_shield=0.1):
        self.dsup = dsup
        self.melanin = melanin
        self.biofilm_density = biofilm_density
        self.gel_thickness = gel_thickness
        self.regrowth_delay = regrowth_delay
        self.dsup_effect = dsup_effect
        self.melanin_effect = melanin_effect
        self.biofilm_shield = biofilm_shield
        self.survival_rate = 100
        self.dna_damage = 0
        self.regrowth_timer = 0
        self.repair_efficiency = 0.25 if dsup else 0.15 if melanin else 0.05

    def radiation_exposure(self, radiation_level):
        resistance = 1
        damage_factor = 1
        if self.dsup:
            resistance *= self.dsup_effect
            damage_factor *= 0.4
        if self.melanin:
            resistance *= self.melanin_effect
            damage_factor *= 0.6
        protection_efficiency = 1 - (self.gel_thickness * self.biofilm_density * self.biofilm_shield)
        protection_efficiency = max(0.1, protection_efficiency)
        effective_radiation = radiation_level * protection_efficiency
        damage = effective_radiation / resistance
        dna_damage_increment = (effective_radiation * damage_factor) / resistance
        self.dna_damage += dna_damage_increment
        self.survival_rate -= damage
        self.dna_damage -= self.dna_damage * self.repair_efficiency
        self.dna_damage = max(self.dna_damage, 0)
        if self.dna_damage < 70:
            self.regrowth_timer += 1
        else:
            self.regrowth_timer = 0
        if self.regrowth_timer >= self.regrowth_delay:
            self.survival_rate = min(self.survival_rate + 5, 100)
            self.regrowth_timer = 0
        if self.dna_damage >= 100:
            self.survival_rate = 0
        self.survival_rate = max(self.survival_rate, 0)

# Bitki sınıfı
class Bitki:
    def __init__(self, jel_var=True, biofilm_density=1.2, gel_thickness=1.0):
        self.jel_var = jel_var
        self.biofilm_density = biofilm_density
        self.gel_thickness = gel_thickness
        self.hayatta_kalma = 100.0

    def radyasyon_maruz_kalma(self, radyasyon, döngü=1):
        koruma_faktoru = 1 - (self.biofilm_density * self.gel_thickness * 0.08) if self.jel_var else 1.0
        koruma_faktoru = max(0.2, koruma_faktoru)
        etkili_radyasyon = radyasyon * koruma_faktoru
        self.hayatta_kalma -= etkili_radyasyon * 0.3 * döngü
        self.hayatta_kalma = max(self.hayatta_kalma, 0)

# Parametre paneli
st.title("🌿 Jel + Genetik Kalkan Simülasyonu (Bitki ve Mikroorganizma)")
st.sidebar.header("🔬 Parametreler")

params = {
    'dsup_effect': st.sidebar.slider("🧬 Dsup Etkisi", 1.0, 5.0, 2.5),
    'melanin_effect': st.sidebar.slider("🎨 Melanin Etkisi", 1.0, 3.0, 1.8),
    'biofilm_shield': st.sidebar.slider("🧫 Jel Koruma Katsayısı", 0.05, 0.5, 0.1),
    'biofilm_density': st.sidebar.slider("🧫 Biofilm Yoğunluğu", 0.5, 2.0, 1.2),
    'gel_thickness': st.sidebar.slider("🧊 Jel Kalınlığı", 0.1, 2.0, 1.0),
    'regrowth_delay': st.sidebar.slider("🔁 Yenilenme Döngüsü", 1, 10, 3),
    'radiation_level': st.sidebar.slider("☢️ Radyasyon Seviyesi", 10, 200, 50),
    'cell_count': st.sidebar.slider("🧫 Hücre Sayısı", 100, 1000, 200),
    'cycles': st.sidebar.slider("🔄 Maruziyet Döngüsü", 5, 20, 10)
}

def run_simulation(params, dsup, melanin):
    cells = [
        BiyoFilmMikroorganizma(
            dsup, melanin,
            params['biofilm_density'], params['gel_thickness'],
            params['regrowth_delay'], params['dsup_effect'],
            params['melanin_effect'], params['biofilm_shield']
        ) for _ in range(params['cell_count'])
    ]
    survival_rates = []
    for _ in range(params['cycles']):
        for cell in cells:
            cell.radiation_exposure(params['radiation_level'])
        avg = np.mean([cell.survival_rate for cell in cells])
        survival_rates.append(avg)
    return survival_rates

if st.sidebar.button("🚀 Simülasyonu Başlat"):
    control = run_simulation(params, False, False)
    test = run_simulation(params, True, True)

    # Bitki simülasyonu
    bitki_jelli = Bitki(True, params['biofilm_density'], params['gel_thickness'])
    bitki_jelsiz = Bitki(False)
    for _ in range(params['cycles']):
        bitki_jelli.radyasyon_maruz_kalma(params['radiation_level'])
        bitki_jelsiz.radyasyon_maruz_kalma(params['radiation_level'])

    # Grafik 1 - Mikroorganizma: Deney vs Kontrol
    st.subheader("🧬 Mikroorganizma Hayatta Kalma")
    fig1, ax1 = plt.subplots()
    ax1.plot(control, label="Kontrol", linestyle="--", color="red")
    ax1.plot(test, label="Dsup + Melanin + Jel", color="green")
    ax1.set_xlabel("Döngü")
    ax1.set_ylabel("Hayatta Kalma (%)")
    ax1.set_title("Radyasyon Altında Mikroorganizma Sağ Kalımı")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    # Grafik 2 - Bitki
    st.subheader("🌱 Bitki Kökü Jel Koruması Etkisi")
    df = pd.DataFrame({
        'Kök Durumu': ['Jelsiz Kök', 'Jelli Kök (Biofilm)'],
        'Hayatta Kalma (%)': [bitki_jelsiz.hayatta_kalma, bitki_jelli.hayatta_kalma]
    })
    fig2, ax2 = plt.subplots()
    bars = ax2.bar(df['Kök Durumu'], df['Hayatta Kalma (%)'], color=['gray', 'green'])
    for bar in bars:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval + 2, f'{yval:.2f}%', ha='center')
    ax2.set_ylim(0, 100)
    ax2.set_title("Bitki Kökü Sağ Kalımı")
    st.pyplot(fig2)

    # Literatür karşılaştırması
    st.markdown("### 📚 Akademik Karşılaştırma")
    st.markdown("- **Dsup geni:** %60–75 daha az DNA hasarı")
    st.markdown("- **Melanin:** Radyasyon soğurumu %40–60")
    st.markdown("- **Biofilm jel:** Fiziksel koruma + hücresel yenilenme avantajı")
    st.markdown(f"**Mikroorganizma Sonuçları:** {test[-1]:.2f}% hayatta kalım | Kontrol: {control[-1]:.2f}%")
    st.markdown(f"**Bitki Sonuçları:** Jel yok: {bitki_jelsiz.hayatta_kalma:.2f}% — Jel var: {bitki_jelli.hayatta_kalma:.2f}%")
        # ——————————————————————————
    # 1️⃣ Genetik + Jel Formu Karşılaştırması
    st.subheader("🧪 Genetik + Jel Formu Karşılaştırması")

    # Alt senaryolar için biofilm parametrelerini geçici ayarlıyoruz
    no_gel_params = params.copy()
    no_gel_params['biofilm_density'] = 0.0
    no_gel_params['gel_thickness']  = 0.0

    scenarios = {
        "Dsup (Jelsiz)"            : run_simulation(no_gel_params, True, False),
        "Dsup (Jelli)"             : run_simulation(params,       True, False),
        "Melanin (Jelsiz)"         : run_simulation(no_gel_params, False, True),
        "Melanin (Jelli)"          : run_simulation(params,       False, True),
        "Dsup+Melanin (Jelsiz)"    : run_simulation(no_gel_params, True, True),
        "Dsup+Melanin (Jelli)"     : run_simulation(params,       True, True),
    }

    fig4, ax4 = plt.subplots()
    for label, curve in scenarios.items():
        ax4.plot(
            range(1, params['cycles']+1),
            curve,
            marker='o' if "Jelli" in label else 'x',
            linestyle='-' if "Jelli" in label else '--',
            label=label
        )
    ax4.set_xlabel("Maruziyet Döngüsü")
    ax4.set_ylabel("Ortalama Hücre Hayatta Kalma (%)")
    ax4.set_title("Gen + Jel Formu: Hayatta Kalma Karşılaştırması")
    ax4.legend(loc="lower left", bbox_to_anchor=(1.0, 0.2))
    ax4.grid(True)
    st.pyplot(fig4)
    3️⃣ Uzay Kapsülü İç Yüzeyi Jel Uygulaması Simülasyonu
    st.subheader("🛰️ Uzay Kapsülü: Jel ile İç Yüzey Koruma Simülasyonu")

    def kapsul_simulasyon(jelli=False):
        kapsul_koruma = 0.4 if jelli else 1.0  # %60 oranında radyasyon absorbe eder
        toplam_hasar = 0
        for _ in range(params['cycles']):
            etkili_radyasyon = radiation_level * kapsul_koruma
            toplam_hasar += etkili_radyasyon * 0.4  # orta seviye hasar katsayısı
        hayatta_kalma = max(0, 100 - toplam_hasar * 0.25)
        return hayatta_kalma
        kapsul_jelli = simulate_astronaut(jelli=True, radiation_level=params["radiation_level"], cycles=params["cycles"]),
        kapsul_jelsiz = simulate_astronaut(jelli=False, radiation_level=params["radiation_level"], cycles=params["cycles"]),
    df_kapsul = pd.DataFrame({
        'Koruma Durumu': ['Jelsiz Kapsül', 'İçi Jel ile Kaplanmış Kapsül'],
        'Hayatta Kalma (%)': [kapsul_jelsiz, kapsul_jelli]
    })

    fig_kapsul, ax_kapsul = plt.subplots()
    colors = ['gray', 'green']
    bars = ax_kapsul.bar(df_kapsul['Koruma Durumu'], df_kapsul['Hayatta Kalma (%)'], color=colors)
    ax_kapsul.set_ylim(0, 100)
    ax_kapsul.set_ylabel("Hayatta Kalma Oranı (%)")
    ax_kapsul.set_title("🛰️ Uzay Kapsülünün Jel ile Korunmasının Etkisi")

    for bar in bars:
        height = bar.get_height()
        ax_kapsul.text(bar.get_x() + bar.get_width()/2, height + 2, f"{height:.2f}%", ha='center')

    st.pyplot(fig_kapsul)
    # ——————————————————————————
    # 4️⃣ Bitki Kombinasyonlu Koruma Simülasyonu
    st.subheader("🌱 Bitki Koruma Kombinasyonları Simülasyonu")

    def bitki_kombinasyon_simulasyonu(sera_jeli=False, kok_jeli=False, kapsul_jeli=False):
        total_protection = 1.0
        if sera_jeli:
            total_protection *= 0.6  # %40 azaltır
        if kok_jeli:
            total_protection *= 0.7  # %30 azaltır
        if kapsul_jeli:
            total_protection *= 0.5  # %50 azaltır
        etkili_radyasyon = radiation_level * total_protection
        hayatta_kalma = 100 - etkili_radyasyon * 0.4  # etki oranı
        return max(0, hayatta_kalma)

    scenarios = {
        "🌱 A | Hiçbir Koruma Yok"              : bitki_kombinasyon_simulasyonu(False, False, False),
        "🌱 B | Sadece Sera Jel Koruması"       : bitki_kombinasyon_simulasyonu(True, False, False),
        "🌱 C | Sera + Kök Jel Koruması"        : bitki_kombinasyon_simulasyonu(True, True, False),
        "🌱 D | Sera + Kök + Kapsül Koruması"   : bitki_kombinasyon_simulasyonu(True, True, True)
    }

    df_bitki_koruma = pd.DataFrame({
        'Koruma Senaryosu': list(scenarios.keys()),
        'Hayatta Kalma (%)': list(scenarios.values())
    })

    fig_bitki_koruma, ax = plt.subplots()
    bars = ax.barh(df_bitki_koruma['Koruma Senaryosu'], df_bitki_koruma['Hayatta Kalma (%)'], color='seagreen')
    ax.set_xlim(0, 100)
    ax.set_xlabel("Hayatta Kalma Oranı (%)")
    ax.set_title("🌿 Bitki Koruma Kombinasyonlarının Etkisi")

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.2f}%', va='center')

    st.pyplot(fig_bitki_koruma)
    # ——————————————————————————
        # ——————————————————————————
    # 4️⃣ Bitki Kombinasyonlu Koruma Simülasyonu
    st.subheader("🌱 Bitki Koruma Kombinasyonları Simülasyonu")

    def bitki_kombinasyon_simulasyonu(sera_jeli=False, kok_jeli=False, kapsul_jeli=False):
        total_protection = 1.0
        if sera_jeli:
            total_protection *= 0.6  # %40 azaltır
        if kok_jeli:
            total_protection *= 0.7  # %30 azaltır
        if kapsul_jeli:
            total_protection *= 0.5  # %50 azaltır
        etkili_radyasyon = radiation_level * total_protection
        hayatta_kalma = 100 - etkili_radyasyon * 0.4  # etki oranı
        return max(0, hayatta_kalma)

    scenarios = {
        "🌱 A | Hiçbir Koruma Yok"              : bitki_kombinasyon_simulasyonu(False, False, False),
        "🌱 B | Sadece Sera Jel Koruması"       : bitki_kombinasyon_simulasyonu(True, False, False),
        "🌱 C | Sera + Kök Jel Koruması"        : bitki_kombinasyon_simulasyonu(True, True, False),
        "🌱 D | Sera + Kök + Kapsül Koruması"   : bitki_kombinasyon_simulasyonu(True, True, True)
    }

    df_bitki_koruma = pd.DataFrame({
        'Koruma Senaryosu': list(scenarios.keys()),
        'Hayatta Kalma (%)': list(scenarios.values())
    })

    fig_bitki_koruma, ax = plt.subplots()
    bars = ax.barh(df_bitki_koruma['Koruma Senaryosu'], df_bitki_koruma['Hayatta Kalma (%)'], color='seagreen')
    ax.set_xlim(0, 100)
    ax.set_xlabel("Hayatta Kalma Oranı (%)")
    ax.set_title("🌿 Bitki Koruma Kombinasyonlarının Etkisi")

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.2f}%', va='center')

    st.pyplot(fig_bitki_koruma)
    # ——————————————————————————
  # Astronot karşılaştırması
    st.subheader("🧍 Astronot Kıyafeti: Jel ile Koruma Simülasyonu")
    astronot_jelsiz = simulate_astronaut(jelli=False, radiation_level=params["radiation_level"], cycles=params["cycles"])
    astronot_jelli = simulate_astronaut(jelli=True, radiation_level=params["radiation_level"], cycles=params["cycles"])

    df_astronaut = pd.DataFrame({
        'Astronot Kıyafeti': ['Jelsiz', 'Jelli'],
        'Hayatta Kalma (%)': [astronot_jelsiz, astronot_jelli]
    })
    fig2, ax2 = plt.subplots()
    bars = ax2.bar(df_astronaut['Astronot Kıyafeti'], df_astronaut['Hayatta Kalma (%)'], color=['gray', 'blue'])
    ax2.set_ylim(0, 100)
    for bar in bars:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval + 2, f'{yval:.2f}%', ha='center')
    ax2.set_title("Astronot Koruma Etkisi")
    st.pyplot(fig2)
