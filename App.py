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
