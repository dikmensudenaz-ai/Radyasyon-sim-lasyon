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
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 1. Mikroorganizma Modeli
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

# 2. Simülasyon Fonksiyonu
def run_simulation(dsup, melanin, biofilm_density, gel_thickness, cycles, radiation_level, cell_count):
    cells = [BiyoFilmMikroorganizma(dsup, melanin, biofilm_density, gel_thickness) for _ in range(cell_count)]
    return [np.mean([cell.radiation_exposure(radiation_level) or cell.survival_rate for cell in cells]) for _ in range(cycles)]

# 3. Bitki Modeli
class Bitki:
    def __init__(self, sera_jeli=False, kok_jeli=False, kapsul_jeli=False):
        self.hayatta_kalma = 100.0
        self.protection = 1.0
        if sera_jeli:
            self.protection *= 0.6
        if kok_jeli:
            self.protection *= 0.7
        if kapsul_jeli:
            self.protection *= 0.5

    def radyasyon_al(self, radyasyon):
        etkili_radyasyon = radyasyon * self.protection
        self.hayatta_kalma -= etkili_radyasyon * 0.4
        self.hayatta_kalma = max(0, self.hayatta_kalma)

# 4. Arayüz
st.title("🌌 Uzayda Radyasyona Karşı BiyoFilm Simülasyonu")

st.sidebar.header("🔬 Parametreler")
params = {
    "dsup": st.sidebar.checkbox("🧬 Dsup Geni"),
    "melanin": st.sidebar.checkbox("🎨 Melanin Geni"),
    "radiation_level": st.sidebar.slider("☢️ Radyasyon Şiddeti", 10, 200, 50),
    "cell_count": st.sidebar.number_input("🧫 Hücre Sayısı", 50, 1000, 200),
    "cycles": st.sidebar.slider("🔁 Maruziyet Döngüsü", 5, 20, 10),
    "biofilm_density": st.sidebar.slider("🧫 Biofilm Yoğunluğu", 0.5, 2.0, 1.2),
    "gel_thickness": st.sidebar.slider("🧊 Jel Kalınlığı", 0.1, 2.0, 1.0),
    "regrowth_delay": st.sidebar.slider("🕒 Yenilenme Döngüsü", 1, 10, 3)
}

if st.sidebar.button("🚀 Simülasyonu Başlat"):
    deney = run_simulation(params["dsup"], params["melanin"], params["biofilm_density"], params["gel_thickness"], params["cycles"], params["radiation_level"], params["cell_count"])
    kontrol = run_simulation(False, False, 0.0, 0.0, params["cycles"], params["radiation_level"], params["cell_count"])

    st.subheader("📊 Deney vs Kontrol")
    fig1, ax1 = plt.subplots()
    ax1.plot(deney, label="Deney Grubu", color='blue')
    ax1.plot(kontrol, label="Kontrol Grubu", linestyle='--', color='red')
    ax1.set_xlabel("Döngü")
    ax1.set_ylabel("Hayatta Kalma (%)")
    ax1.legend()
    st.pyplot(fig1)

    st.subheader("🧬 Genetik Farklar")
    dsup_only = run_simulation(True, False, 0.0, 0.0, params["cycles"], params["radiation_level"], params["cell_count"])
    melanin_only = run_simulation(False, True, 0.0, 0.0, params["cycles"], params["radiation_level"], params["cell_count"])
    dsup_melanin = run_simulation(True, True, 0.0, 0.0, params["cycles"], params["radiation_level"], params["cell_count"])

    fig2, ax2 = plt.subplots()
    ax2.plot(dsup_only, label="Dsup")
    ax2.plot(melanin_only, label="Melanin")
    ax2.plot(dsup_melanin, label="Dsup+Melanin", linewidth=2)
    ax2.legend()
    st.pyplot(fig2)

    st.subheader("🧊 Jel vs Jelsiz Mikroorganizma")
    jelsiz = run_simulation(True, True, 0.0, 0.0, params["cycles"], params["radiation_level"], params["cell_count"])
    jelli = run_simulation(True, True, params["biofilm_density"], params["gel_thickness"], params["cycles"], params["radiation_level"], params["cell_count"])

    fig3, ax3 = plt.subplots()
    ax3.plot(jelsiz, label="Jelsiz Form", linestyle='--', color='orange')
    ax3.plot(jelli, label="Jelli Form", color='green')
    ax3.legend()
    st.pyplot(fig3)

    st.subheader("🛰️ Uzay Kapsülü Koruması")
    kapsul_jelsiz = max(0, 100 - sum(params["radiation_level"] * 1.0 * 0.4 for _ in range(params["cycles"])) * 0.25)
    kapsul_jelli = max(0, 100 - sum(params["radiation_level"] * 0.4 * 0.4 for _ in range(params["cycles"])) * 0.25)

    df_kapsul = pd.DataFrame({
        'Kapsül Durumu': ['Jelsiz', 'Jel Kaplı'],
        'Hayatta Kalma (%)': [kapsul_jelsiz, kapsul_jelli]
    })
    st.bar_chart(df_kapsul.set_index('Kapsül Durumu'))

    st.subheader("🌱 Bitki Kombinasyonları")
    kombinasyonlar = {
        "Korumasız": Bitki(False, False, False),
        "Sera Jel": Bitki(True, False, False),
        "Sera+Kök": Bitki(True, True, False),
        "Full Koruma": Bitki(True, True, True)
    }
    for bitki in kombinasyonlar.values():
        for _ in range(params["cycles"]):
            bitki.radyasyon_al(params["radiation_level"])

    df_bitki = pd.DataFrame({
        "Koruma": list(kombinasyonlar.keys()),
        "Hayatta Kalma (%)": [bitki.hayatta_kalma for bitki in kombinasyonlar.values()]
    })
    st.bar_chart(df_bitki.set_index("Koruma"))
