import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Hücre modeli detaylandırılmış
class Mikroorganizma:
    def __init__(self, dsup=False, melanin=False):
        self.dsup = dsup
        self.melanin = melanin
        self.survival_rate = 100
        self.dna_damage = 0

    def radiation_exposure(self, radiation_level):
        resistance = 1
        damage_factor = 1

        if self.dsup:
            resistance *= 2.5  # Dsup geni DNA koruması sağlar
            damage_factor *= 0.4  # DNA hasarını azaltır

        if self.melanin:
            resistance *= 1.8  # Melanin radyasyonu emer
            damage_factor *= 0.6  # DNA hasarını azaltır

        damage = radiation_level / resistance
        dna_damage_increment = (radiation_level * damage_factor) / resistance

        self.dna_damage += dna_damage_increment
        self.survival_rate -= damage

        # Hücre ölümü simülasyonu
        if self.dna_damage >= 100:
            self.survival_rate = 0

        self.survival_rate = max(self.survival_rate, 0)

# Streamlit Arayüzü
st.title("🧬 Detaylı Gen Aktarım ve Radyasyon Direnci Simülasyonu")

# Kullanıcı girdileri
st.sidebar.header("Simülasyon Parametreleri")
dsup_gene = st.sidebar.checkbox("🧫 Dsup Geni")
melanin_gene = st.sidebar.checkbox("🖤 Melanin Geni")
radiation_level = st.sidebar.slider("☢️ Radyasyon Şiddeti", min_value=10, max_value=200, value=50)
cell_count = st.sidebar.number_input("🦠 Hücre Sayısı", min_value=50, max_value=1000, value=200)
exposure_cycles = st.sidebar.slider("🔄 Maruziyet Döngüleri", min_value=5, max_value=20, value=10)

if st.sidebar.button("🚀 Detaylı Simülasyonu Başlat"):
    # Deney grubu
    test_cells = [Mikroorganizma(dsup_gene, melanin_gene) for _ in range(cell_count)]
    # Kontrol grubu
    control_cells = [Mikroorganizma(False, False) for _ in range(cell_count)]

    test_survival_rates, control_survival_rates = [], []

    for cycle in range(exposure_cycles):
        for cell in test_cells:
            cell.radiation_exposure(radiation_level)
        for cell in control_cells:
            cell.radiation_exposure(radiation_level)

        test_avg_survival = np.mean([cell.survival_rate for cell in test_cells])
        control_avg_survival = np.mean([cell.survival_rate for cell in control_cells])

        test_survival_rates.append(test_avg_survival)
        control_survival_rates.append(control_avg_survival)

    # Grafik oluşturma
    fig, ax = plt.subplots()
    ax.plot(range(1, exposure_cycles + 1), test_survival_rates, marker='o', linestyle='-', color='blue', label='Deney Grubu')
    ax.plot(range(1, exposure_cycles + 1), control_survival_rates, marker='x', linestyle='--', color='red', label='Kontrol Grubu')

    ax.set_xlabel('Radyasyon Maruziyet Döngüsü')
    ax.set_ylabel('Ortalama Hücre Hayatta Kalma (%)')
    ax.set_title('Hücrelerin Radyasyona Karşı Hayatta Kalma Oranı')
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    # Sonuçların tablolaştırılması
    st.markdown("## 📊 Ayrıntılı Analiz ve Sonuçlar")

    final_test_survival = test_survival_rates[-1]
    final_control_survival = control_survival_rates[-1]

    result_table = {
        'Grup': ['Kontrol (Gen Yok)', 'Deney (Gen Aktarımı)'],
        'Başlangıç Hücre Sayısı': [cell_count, cell_count],
        'Son Döngü Hayatta Kalma (%)': [f"{final_control_survival:.2f}%", f"{final_test_survival:.2f}%"],
        'Radyasyon Şiddeti': [radiation_level, radiation_level],
        'Dsup Geni': ['Yok', 'Var' if dsup_gene else 'Yok'],
        'Melanin Geni': ['Yok', 'Var' if melanin_gene else 'Yok']
    }

    st.table(result_table)
