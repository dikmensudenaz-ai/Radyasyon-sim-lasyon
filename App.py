import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Gelişmiş mikroorganizma sınıfı
class BiyoFilmMikroorganizma:
    def __init__(self, dsup=False, melanin=False, biofilm_density=1.2, gel_thickness=1.0, regrowth_delay=3):
        self.dsup = dsup
        self.melanin = melanin
        self.biofilm_density = biofilm_density
        self.gel_thickness = gel_thickness
        self.regrowth_delay = regrowth_delay
        self.survival_rate = 100
        self.dna_damage = 0
        self.regrowth_timer = 0
        self.repair_efficiency = 0.25 if dsup else 0.15 if melanin else 0.05

    def radiation_exposure(self, radiation_level):
        resistance = 1
        damage_factor = 1
        if self.dsup:
            resistance *= 2.5
            damage_factor *= 0.4
        if self.melanin:
            resistance *= 1.8
            damage_factor *= 0.6
        protection_efficiency = 1 - (self.gel_thickness * self.biofilm_density * 0.1)
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

def run_simulation(dsup, melanin, biofilm_density, gel_thickness, cycles, radiation_level, cell_count):
    cells = [BiyoFilmMikroorganizma(dsup, melanin, biofilm_density, gel_thickness) for _ in range(cell_count)]
    return [np.mean([cell.radiation_exposure(radiation_level) or cell.survival_rate for cell in cells]) for _ in range(cycles)]

# 🌱 Bitki modeli
class Bitki:
    def __init__(self, jel_var=True, biofilm_density=1.2, gel_thickness=1.0):
        self.jel_var = jel_var
        self.biofilm_density = biofilm_density
        self.gel_thickness = gel_thickness
        self.hayatta_kalma = 100.0

    def radyasyon_maruz_kalma(self, radyasyon):
        koruma_faktoru = 1 - (self.biofilm_density * self.gel_thickness * 0.08) if self.jel_var else 1.0
        koruma_faktoru = max(0.2, koruma_faktoru)
        etkili_radyasyon = radyasyon * koruma_faktoru
        self.hayatta_kalma -= etkili_radyasyon * 0.3
        self.hayatta_kalma = max(self.hayatta_kalma, 0)

# 🔧 Arayüz Başlat
st.title("🧪 BiyoFilm Jel & Genetik Koruma Tabanlı Mikroorganizma Simülasyonu")

st.sidebar.header("🔬 Simülasyon Parametreleri")
dsup_gene = st.sidebar.checkbox("🧬 Dsup Geni")
melanin_gene = st.sidebar.checkbox("🎨 Melanin Geni")
radiation_level = st.sidebar.slider("☢️ Radyasyon Şiddeti", 10, 200, 50)
cell_count = st.sidebar.number_input("🧫 Hücre Sayısı", 50, 1000, 200)
cycles = st.sidebar.slider("🔄 Maruziyet Döngüsü", 5, 20, 10)
biofilm_density = st.sidebar.slider("🧫 Biofilm Yoğunluğu", 0.5, 2.0, 1.2)
gel_thickness = st.sidebar.slider("🧊 Jel Kalınlığı", 0.1, 2.0, 1.0)
regrowth_delay = st.sidebar.slider("🕒 Yenilenme Döngüsü", 1, 10, 3)

if st.sidebar.button("🚀 Simülasyonu Başlat"):
    # Simülasyonlar
    deney = run_simulation(dsup_gene, melanin_gene, biofilm_density, gel_thickness, cycles, radiation_level, cell_count)
    kontrol = run_simulation(False, False, 0.0, 0.0, cycles, radiation_level, cell_count)
    dsup_only = run_simulation(True, False, 0.0, 0.0, cycles, radiation_level, cell_count)
    melanin_only = run_simulation(False, True, 0.0, 0.0, cycles, radiation_level, cell_count)
    dsup_melanin = run_simulation(True, True, 0.0, 0.0, cycles, radiation_level, cell_count)
    jelsiz_mikroorganizma = run_simulation(True, True, 0.0, 0.0, cycles, radiation_level, cell_count)
    jelli_mikroorganizma = run_simulation(True, True, biofilm_density, gel_thickness, cycles, radiation_level, cell_count)

    # Grafikler
    fig, ax = plt.subplots()
    ax.plot(deney, label="Deney", color='blue')
    ax.plot(kontrol, label="Kontrol", linestyle='--', color='red')
    ax.set_title("📊 Deney vs Kontrol")
    ax.set_ylabel("Hayatta Kalma (%)")
    ax.set_xlabel("Döngü")
    ax.legend()
    st.pyplot(fig)

    fig2, ax2 = plt.subplots()
    ax2.plot(dsup_only, label="Dsup")
    ax2.plot(melanin_only, label="Melanin")
    ax2.plot(dsup_melanin, label="Dsup + Melanin")
    ax2.set_title("🧬 Genetik Koruma Etkisi")
    ax2.legend()
    st.pyplot(fig2)

    fig3, ax3 = plt.subplots()
    ax3.plot(jelsiz_mikroorganizma, label="Jelsiz Formda Mikroorganizma", linestyle='--')
    ax3.plot(jelli_mikroorganizma, label="Jel Formunda Mikroorganizma", color='green')
    ax3.set_title("🧊 Mikroorganizmların Jelli ve Jelsiz Formunun Radyasyon Direncine Etkisi")
    ax3.legend()
    st.pyplot(fig3)

    # Bitki Simülasyonu
    bitki_jelli = Bitki(True, biofilm_density, gel_thickness)
    bitki_jelsiz = Bitki(False)

    for _ in range(cycles):
        bitki_jelli.radyasyon_maruz_kalma(radiation_level)
        bitki_jelsiz.radyasyon_maruz_kalma(radiation_level)

    st.markdown("### 🌿 Bitki Kökü Simülasyonu")
    df = pd.DataFrame({
        'Kök Durumu': ['Jelsiz Kök', 'Jelli Kök (Biofilm)'],
        'Hayatta Kalma (%)': [bitki_jelsiz.hayatta_kalma, bitki_jelli.hayatta_kalma]
    })
    st.bar_chart(df.set_index('Kök Durumu'))

    # Final Tablo
    st.markdown("### 📌 Mikroorganizma Hayatta Kalma Tablosu")
    st.table({
        'Grup': ["Kontrol Grubu", "Deney Grubu", "Sadece Dsup'a Sahip", "Sadece Melanin'e Sahip", "Dsup+Melanin'e Sahip", "Jelsiz Formda Mikroorganizma", "Jel Formunda Mikroorganizma"],
        'Hayatta Kalma (%)': [
            f"{kontrol[-1]:.2f}%", f"{deney[-1]:.2f}%", f"{dsup_only[-1]:.2f}%",
            f"{melanin_only[-1]:.2f}%", f"{dsup_melanin[-1]:.2f}%",
            f"{jelsiz_mikroorganizma[-1]:.2f}%", f"{jelli_mikroorganizma[-1]:.2f}%"
        ]
    })
