import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# --- SINIF TANIMLARI ---
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

def kapsul_simulasyon(jelli, params):
    koruma = 0.4 if jelli else 1.0
    toplam_hasar = sum(params['radiation_level'] * koruma * 0.4 for _ in range(params['cycles']))
    return max(0, 100 - toplam_hasar * 0.25)

def simulate_astronaut(jelli, radiation_level, cycles):
    koruma_katsayisi = 0.4 if jelli else 1.0
    toplam_hasar = sum(radiation_level * koruma_katsayisi for _ in range(cycles))
    return max(0, 100 - toplam_hasar * 0.25)

def bitki_kombinasyon_simulasyonu(sera_jeli, kok_jeli, kapsul_jeli, radiation_level):
    koruma = 1.0
    if sera_jeli: koruma *= 0.6
    if kok_jeli: koruma *= 0.7
    if kapsul_jeli: koruma *= 0.5
    etkili_radyasyon = radiation_level * koruma
    return max(0, 100 - etkili_radyasyon * 0.4)

st.set_page_config(layout="wide")
st.title("🌌 BiyoFilm Jel + Genetik Koruma Simülasyonu")

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

if st.sidebar.button("🚀 Simülasyonu Başlat"):
    # Deney ve Kontrol
    deney = run_simulation(params, True, True)
    kontrol = run_simulation(params, False, False)

    if deney and kontrol and len(deney) == len(kontrol):
        st.subheader("🧬 Deney vs Kontrol")
        fig1, ax1 = plt.subplots()
        ax1.plot(deney, label="Dsup+Melanin+Jel", color='green')
        ax1.plot(kontrol, label="Kontrol", linestyle='--', color='red')
        ax1.set_xlabel("Döngü")
        ax1.set_ylabel("Hayatta Kalma (%)")
        ax1.legend()
        st.pyplot(fig1)

    # Genetik + Jel Karşılaştırma
    st.subheader("🧪 Genetik + Jel Formu Karşılaştırması")
    no_gel = params.copy()
    no_gel['biofilm_density'] = 0.0
    no_gel['gel_thickness'] = 0.0
    scenario_labels = [
        "Dsup (Jelsiz)", "Dsup (Jelli)", "Melanin (Jelsiz)", "Melanin (Jelli)",
        "Dsup+Melanin (Jelsiz)", "Dsup+Melanin (Jelli)"
    ]
    scenario_funcs = [
        run_simulation(no_gel, True, False),
        run_simulation(params, True, False),
        run_simulation(no_gel, False, True),
        run_simulation(params, False, True),
        run_simulation(no_gel, True, True),
        run_simulation(params, True, True)
    ]
    fig2, ax2 = plt.subplots()
    for label, curve in zip(scenario_labels, scenario_funcs):
        if curve and len(curve) == params['cycles']:
            ax2.plot(curve, label=label, linestyle='-' if "Jelli" in label else '--')
    ax2.set_title("Genetik + Jel Etkisi")
    ax2.legend()
    st.pyplot(fig2)

    # Uzay kapsülü
    kapsul_jelsiz = kapsul_simulasyon(False, params)
    kapsul_jelli = kapsul_simulasyon(True, params)
    df_kapsul = pd.DataFrame({
        'Kapsül Durumu': ['Jelsiz', 'İç Yüzey Jel'],
        'Hayatta Kalma (%)': [kapsul_jelsiz, kapsul_jelli]
    })
    if not df_kapsul.empty:
        st.bar_chart(df_kapsul.set_index('Kapsül Durumu'))

    # Bitki kombinasyonları
    st.subheader("🌱 Bitki Koruma Kombinasyonları")
    kombine_sonuclar = {
        "Korumasız": bitki_kombinasyon_simulasyonu(False, False, False, params["radiation_level"]),
        "Sera Jel": bitki_kombinasyon_simulasyonu(True, False, False, params["radiation_level"]),
        "Sera+Kök": bitki_kombinasyon_simulasyonu(True, True, False, params["radiation_level"]),
        "Full Koruma": bitki_kombinasyon_simulasyonu(True, True, True, params["radiation_level"])
    }
    df_bitki = pd.DataFrame({
        'Koruma': list(kombine_sonuclar.keys()),
        'Hayatta Kalma (%)': list(kombine_sonuclar.values())
    })
    if not df_bitki.empty:
        st.bar_chart(df_bitki.set_index("Koruma"))

    # Astronot
    st.subheader("🧍 Astronot Kıyafeti: Jel ile Koruma")
    astro_jelsiz = simulate_astronaut(False, params["radiation_level"], params["cycles"])
    astro_jelli = simulate_astronaut(True, params["radiation_level"], params["cycles"])
    df_astronaut = pd.DataFrame({
        'Astronot': ['Jelsiz Kıyafet', 'Jel Kaplamalı Kıyafet'],
        'Hayatta Kalma (%)': [astro_jelsiz, astro_jelli]
    })
    if not df_astronaut.empty:
        st.bar_chart(df_astronaut.set_index("Astronot"))

    # Literatür özeti
    st.markdown("### 📚 Akademik Bulgularla Karşılaştırma")
    st.markdown("- Dsup: %60–75 DNA koruması")
    st.markdown("- Melanin: %40–60 radyasyon soğurumu")
    st.markdown("- Biofilm Jel: Fiziksel + biyolojik koruma")
