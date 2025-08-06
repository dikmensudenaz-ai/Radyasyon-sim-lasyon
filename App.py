import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Gelişmiş mikroorganizma sınıfı: genetik + biofilm + rejenerasyon
class BiyoFilmMikroorganizma:
    def __init__(self, dsup=False, melanin=False, biofilm_density=1.2, gel_thickness=1.0):
        self.dsup = dsup
        self.melanin = melanin
        self.biofilm_density = biofilm_density
        self.gel_thickness = gel_thickness
        self.survival_rate = 100
        self.dna_damage = 0
        self.regrowth_timer = 0

        # Genlere göre DNA onarım oranı
        if self.dsup:
            self.repair_efficiency = 0.25
        elif self.melanin:
            self.repair_efficiency = 0.15
        else:
            self.repair_efficiency = 0.05

    def radiation_exposure(self, radiation_level):
        resistance = 1
        damage_factor = 1

        if self.dsup:
            resistance *= 2.5
            damage_factor *= 0.4
        if self.melanin:
            resistance *= 1.8
            damage_factor *= 0.6

        # Biofilm yoğunluğu ve jel kalınlığı koruma sağlar
        protection_multiplier = 1 + (self.biofilm_density * self.gel_thickness * 0.2)
        effective_resistance = resistance * protection_multiplier

        damage = radiation_level / effective_resistance
        dna_damage_increment = (radiation_level * damage_factor) / effective_resistance

        self.dna_damage += dna_damage_increment
        self.survival_rate -= damage

        # DNA tamiri
        self.dna_damage -= self.dna_damage * self.repair_efficiency
        self.dna_damage = max(self.dna_damage, 0)

        # Yenilenme mekanizması
        if self.dna_damage < 70:
            self.regrowth_timer += 1
        else:
            self.regrowth_timer = 0

        if self.regrowth_timer >= 3:
            self.survival_rate = min(self.survival_rate + 5, 100)
            self.regrowth_timer = 0

        if self.dna_damage >= 100:
            self.survival_rate = 0

        self.survival_rate = max(self.survival_rate, 0)

# Streamlit Arayüzü
st.title("🌱 Gelişmiş BiyoFilm Mikroorganizma Simülasyonu")

st.sidebar.header("🔬 Simülasyon Parametreleri")
dsup_gene = st.sidebar.checkbox("🧬 Dsup Geni")
melanin_gene = st.sidebar.checkbox("🎨 Melanin Geni")
radiation_level = st.sidebar.slider("☢️ Radyasyon Şiddeti (Gy)", 10, 200, 50)
cell_count = st.sidebar.number_input("🦠 Hücre Sayısı", 50, 1000, 200)
exposure_cycles = st.sidebar.slider("🔁 Maruziyet Döngüsü", 5, 20, 10)
biofilm_density = st.sidebar.slider("🧫 Biofilm Yoğunluğu", 0.5, 2.0, 1.2)
gel_thickness = st.sidebar.slider("🧊 Jel Kalınlığı", 0.1, 2.0, 1.0)

if st.sidebar.button("🚀 Simülasyonu Başlat"):
    test_cells = [BiyoFilmMikroorganizma(dsup_gene, melanin_gene, biofilm_density, gel_thickness)
                  for _ in range(cell_count)]
    control_cells = [BiyoFilmMikroorganizma(False, False, 0.0, 0.0) for _ in range(cell_count)]

    test_survivals, control_survivals = [], []

    for cycle in range(exposure_cycles):
        for cell in test_cells:
            cell.radiation_exposure(radiation_level)
        for cell in control_cells:
            cell.radiation_exposure(radiation_level)

        test_avg = np.mean([cell.survival_rate for cell in test_cells])
        control_avg = np.mean([cell.survival_rate for cell in control_cells])

        test_survivals.append(test_avg)
        control_survivals.append(control_avg)

    fig, ax = plt.subplots()
    ax.plot(range(1, exposure_cycles + 1), test_survivals, marker='o', linestyle='-', color='blue', label='Deney Grubu (Biofilm)')
    ax.plot(range(1, exposure_cycles + 1), control_survivals, marker='x', linestyle='--', color='red', label='Kontrol Grubu')
    ax.set_xlabel('Radyasyon Maruziyet Döngüsü')
    ax.set_ylabel('Ortalama Hücre Hayatta Kalma (%)')
    ax.set_title('Gelişmiş Radyasyon Direnci Simülasyonu')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.markdown("## 📊 Sonuç Tablosu")
    final_test_survival = test_survivals[-1]
    final_control_survival = control_survivals[-1]

    st.table({
        'Grup': ['Kontrol (Gen Yok)', 'Deney (Gen Aktarımı + Biofilm)'],
        'Hayatta Kalma (%)': [f"{final_control_survival:.2f}%", f"{final_test_survival:.2f}%"],
        'Dsup Geni': ['Yok', 'Var' if dsup_gene else 'Yok'],
        'Melanin Geni': ['Yok', 'Var' if melanin_gene else 'Yok'],
        'Biofilm Yoğunluğu': [0.0, biofilm_density],
        'Jel Kalınlığı': [0.0, gel_thickness]
    })
