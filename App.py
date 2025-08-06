import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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

# Simülasyon fonksiyonu
def run_simulation(dsup, melanin, biofilm_density, gel_thickness, cycles, radiation_level, cell_count):
    cells = [BiyoFilmMikroorganizma(dsup, melanin, biofilm_density, gel_thickness) for _ in range(cell_count)]
    survival_rates = []

    for _ in range(cycles):
        for cell in cells:
            cell.radiation_exposure(radiation_level)
        avg_survival = np.mean([cell.survival_rate for cell in cells])
        survival_rates.append(avg_survival)

    return survival_rates

# Uygulama Başlığı
st.title("🧪 BiyoFilm Jel & Genetik Koruma Tabanlı Mikroorganizma Simülasyonu")

# Kullanıcı Girdileri
st.sidebar.header("🔬 Simülasyon Parametreleri")
dsup_gene = st.sidebar.checkbox("🧬 Dsup Geni")
melanin_gene = st.sidebar.checkbox("🎨 Melanin Geni")
radiation_level = st.sidebar.slider("☢️ Radyasyon Şiddeti", 10, 200, 50)
cell_count = st.sidebar.number_input("🧫 Hücre Sayısı", 50, 1000, 200)
cycles = st.sidebar.slider("🔄 Maruziyet Döngüsü", 5, 20, 10)
biofilm_density = st.sidebar.slider("🧫 Biofilm Yoğunluğu", 0.5, 2.0, 1.2)
gel_thickness = st.sidebar.slider("🧊 Jel Kalınlığı", 0.1, 2.0, 1.0)
regrowth_delay = st.sidebar.slider("🕒 Yenilenme Döngüsü", 1, 10, 3)

# Ana Simülasyon
if st.sidebar.button("🚀 Simülasyonu Başlat"):
    test_cells = [BiyoFilmMikroorganizma(dsup_gene, melanin_gene, biofilm_density, gel_thickness, regrowth_delay)
                  for _ in range(cell_count)]
    control_cells = [BiyoFilmMikroorganizma(False, False, 0.0, 0.0, regrowth_delay) for _ in range(cell_count)]

    test_survivals, control_survivals = [], []

    for cycle in range(cycles):
        for cell in test_cells:
            cell.radiation_exposure(radiation_level)
        for cell in control_cells:
            cell.radiation_exposure(radiation_level)

        test_avg = np.mean([cell.survival_rate for cell in test_cells])
        control_avg = np.mean([cell.survival_rate for cell in control_cells])

        test_survivals.append(test_avg)
        control_survivals.append(control_avg)

    # Grafik 1: Deney vs Kontrol
    st.subheader("📈 Deney ve Kontrol Grubu Karşılaştırması")
    fig, ax = plt.subplots()
    ax.plot(range(1, cycles + 1), test_survivals, label="Deney Grubu", color="blue", marker='o')
    ax.plot(range(1, cycles + 1), control_survivals, label="Kontrol Grubu", color="red", linestyle='--', marker='x')
    ax.set_xlabel("Döngü")
    ax.set_ylabel("Hayatta Kalma (%)")
    ax.set_title("Genetik + Jel Koruma Etkisi")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Grafik 2: Genetik Etki
    st.subheader("🧬 Genetik Korumanın Etkisi")
    plain = run_simulation(False, False, 0.0, 0.0, cycles, radiation_level, cell_count)
    dsup_only = run_simulation(True, False, 0.0, 0.0, cycles, radiation_level, cell_count)
    melanin_only = run_simulation(False, True, 0.0, 0.0, cycles, radiation_level, cell_count)
    dsup_melanin = run_simulation(True, True, 0.0, 0.0, cycles, radiation_level, cell_count)

    fig2, ax2 = plt.subplots()
    ax2.plot(plain, label="Gen Yok", linestyle='--')
    ax2.plot(dsup_only, label="Dsup Geni")
    ax2.plot(melanin_only, label="Melanin Geni")
    ax2.plot(dsup_melanin, label="Dsup + Melanin", linewidth=2)
    ax2.set_xlabel("Döngü")
    ax2.set_ylabel("Hayatta Kalma (%)")
    ax2.set_title("Genetik Koruma Karşılaştırması")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)

    # Grafik 3: Jel Etkisi
    st.subheader("🧊 Jel Uygulamasının Etkisi")
    no_jel = run_simulation(True, True, 0.0, 0.0, cycles, radiation_level, cell_count)
    jel_korumali = run_simulation(True, True, biofilm_density, gel_thickness, cycles, radiation_level, cell_count)

    fig3, ax3 = plt.subplots()
    ax3.plot(no_jel, label="Dsup+Melanin (Jel Yok)", linestyle='--', color='orange')
    ax3.plot(jel_korumali, label="Dsup+Melanin (Jel Var)", color='green')
    ax3.set_xlabel("Döngü")
    ax3.set_ylabel("Hayatta Kalma (%)")
    ax3.set_title("Jel Uygulamasının Etkisi")
    ax3.legend()
    ax3.grid(True)
    st.pyplot(fig3)

    # Sonuç Tablosu
    st.markdown("## 📊 Final Sonuç Tablosu")
    st.table({
        'Grup': ['Kontrol', 'Deney', 'Dsup', 'Melanin', 'Dsup+Melanin', 'Dsup+Melanin (Jelsiz)', 'Dsup+Melanin (Jelli)'],
        'Hayatta Kalma (%)': [
            f"{control_survivals[-1]:.2f}%", f"{test_survivals[-1]:.2f}%",
            f"{dsup_only[-1]:.2f}%", f"{melanin_only[-1]:.2f}%", f"{dsup_melanin[-1]:.2f}%",
            f"{no_jel[-1]:.2f}%", f"{jel_korumali[-1]:.2f}%"
        ]
    })
