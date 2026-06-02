import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"

# ─────────────────────────────────────────────
#  Konfigurasi halaman
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Prediksi Risiko Diabetes",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS kustom
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Font & warna dasar */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Header utama */
    .main-header {
        background: linear-gradient(135deg, #185FA5 0%, #378ADD 100%);
        padding: 1.8rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 { color: white; margin: 0; font-size: 1.8rem; }
    .main-header p  { color: rgba(255,255,255,0.85); margin: 0.4rem 0 0; font-size: 0.95rem; }

    /* Kartu metrik hasil prediksi */
    .result-positive {
        background: #fff1f0;
        border: 1.5px solid #E24B4A;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    .result-negative {
        background: #f0faf4;
        border: 1.5px solid #1D9E75;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    .result-title { font-size: 1.4rem; font-weight: 700; margin-bottom: 0.3rem; }
    .result-prob  { font-size: 2.5rem; font-weight: 800; }
    .result-sub   { font-size: 0.85rem; color: #666; margin-top: 0.3rem; }

    /* Kartu info model */
    .model-card {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
    }
    .model-label { color: #666; font-size: 0.75rem; text-transform: uppercase;
                   letter-spacing: 0.05em; margin-bottom: 2px; }
    .model-value { font-weight: 600; font-size: 1rem; color: #185FA5; }

    /* Skor bar */
    .gauge-container { margin: 0.8rem 0; }
    .gauge-bar { height: 10px; border-radius: 5px; background: #e9ecef; overflow: hidden; }
    .gauge-fill { height: 100%; border-radius: 5px; transition: width 0.5s; }

    /* Disclaimer */
    .disclaimer {
        background: #fff8e1;
        border-left: 4px solid #EF9F27;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1rem;
        font-size: 0.82rem;
        color: #555;
        margin-top: 1rem;
    }

    /* Nomor input rapi */
    .stNumberInput > div > div > input { text-align: center; }

    /* Sidebar */
    .sidebar-section {
        background: #f0f4f8;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 1rem;
        font-size: 0.82rem;
    }
    .sidebar-section h4 { font-size: 0.85rem; margin: 0 0 0.4rem; color: #185FA5; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Load model & metadata
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    model  = joblib.load(MODEL_DIR / 'model.pkl')
    scaler = joblib.load(MODEL_DIR / 'scaler.pkl')
    return model, scaler

@st.cache_data
def load_metadata():
    try:
        with open(MODEL_DIR / 'metadata.json') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'model_name': 'Random Forest',
            'accuracy': 0.79, 'f1_score': 0.72, 'roc_auc': 0.84,
            'optimal_threshold': 0.45,
            'train_size': 614, 'test_size': 154,
            'features': ['Pregnancies','Glucose','BloodPressure','SkinThickness',
                         'Insulin','BMI','DiabetesPedigreeFunction','Age']
        }

try:
    model, scaler = load_model()
except ModuleNotFoundError as exc:
    st.error(
        "Model gagal dimuat karena dependency Python yang dibutuhkan tidak tersedia. "
        "Pastikan Streamlit Cloud memakai `runtime.txt` dan install ulang dependency dari `requirements.txt`."
    )
    st.exception(exc)
    st.stop()
except Exception as exc:
    st.error("Model gagal dimuat. Periksa file `model/model.pkl`, `model/scaler.pkl`, dan dependency aplikasi.")
    st.exception(exc)
    st.stop()
meta = load_metadata()
THRESHOLD = meta.get('optimal_threshold', 0.5)
FEATURES  = meta.get('features', [])


# ─────────────────────────────────────────────
#  Sidebar — info model & panduan
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🩺 Diabetes Predictor")
    st.markdown("---")

    st.markdown("### 📊 Info Model")
    cols = st.columns(2)
    cols[0].metric("Accuracy",  f"{meta['accuracy']:.1%}")
    cols[1].metric("ROC-AUC",   f"{meta['roc_auc']:.3f}")
    cols[0].metric("F1-Score",  f"{meta['f1_score']:.3f}")
    cols[1].metric("Threshold", f"{THRESHOLD:.2f}")
    st.caption(f"Model: **{meta['model_name']}**  |  Train: {meta['train_size']} | Test: {meta['test_size']}")

    st.markdown("---")
    st.markdown("### 📖 Panduan Pengisian")
    st.markdown("""
<div class="sidebar-section">
<h4>Glucose</h4>
Kadar gula darah plasma 2 jam setelah uji toleransi glukosa oral. Normal: 70–140 mg/dL.
</div>
<div class="sidebar-section">
<h4>BMI</h4>
Body Mass Index = berat (kg) / tinggi² (m²). Normal: 18.5–24.9.
</div>
<div class="sidebar-section">
<h4>Blood Pressure</h4>
Tekanan darah diastolik (mm Hg). Normal: 60–80.
</div>
<div class="sidebar-section">
<h4>DiabetesPedigreeFunction</h4>
Skor riwayat diabetes dalam keluarga (0.0–2.5). Semakin tinggi = lebih banyak kerabat penderita diabetes.
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔬 Tentang Dataset")
    st.caption("Data: Pima Indians Diabetes Database (Kaggle). 768 pasien wanita berusia ≥ 21 tahun keturunan Pima Indian.")


# ─────────────────────────────────────────────
#  Header utama
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🩺 Prediksi Risiko Diabetes</h1>
  <p>Masukkan data kesehatan pasien untuk mendapatkan prediksi risiko diabetes berbasis Machine Learning.</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Form input
# ─────────────────────────────────────────────
st.subheader("📋 Data Kesehatan Pasien")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🔢 Data Umum**")
    pregnancies = st.number_input(
        "Jumlah Kehamilan", min_value=0, max_value=20, value=1, step=1,
        help="Total jumlah kehamilan yang pernah dialami"
    )
    age = st.number_input(
        "Usia (tahun)", min_value=21, max_value=100, value=30, step=1,
        help="Usia pasien dalam tahun (minimal 21)"
    )
    dpf = st.number_input(
        "Diabetes Pedigree Function", min_value=0.0, max_value=3.0,
        value=0.47, step=0.01, format="%.3f",
        help="Skor riwayat diabetes keluarga (0.0 – 2.5)"
    )

with col2:
    st.markdown("**💉 Data Gula & Tekanan**")
    glucose = st.number_input(
        "Kadar Glukosa (mg/dL)", min_value=0, max_value=300, value=120, step=1,
        help="Kadar glukosa plasma saat tes toleransi"
    )
    blood_pressure = st.number_input(
        "Tekanan Darah Diastolik (mm Hg)", min_value=0, max_value=150,
        value=72, step=1, help="Tekanan darah diastolik"
    )
    insulin = st.number_input(
        "Insulin (μU/mL)", min_value=0, max_value=900, value=85, step=1,
        help="Kadar insulin serum 2 jam (0 = tidak diukur)"
    )

with col3:
    st.markdown("**📏 Data Fisik**")
    bmi = st.number_input(
        "BMI (kg/m²)", min_value=0.0, max_value=80.0, value=25.0,
        step=0.1, format="%.1f", help="Body Mass Index"
    )
    skin_thickness = st.number_input(
        "Skin Thickness (mm)", min_value=0, max_value=100, value=23, step=1,
        help="Ketebalan lipatan kulit trisep (mm)"
    )

    # ── Kalkulator BMI mini ──
    st.markdown("---")
    st.markdown("**🔧 Kalkulator BMI**")
    bb = st.number_input("Berat (kg)", 30.0, 200.0, 60.0, 0.5, key="bb")
    tb = st.number_input("Tinggi (cm)", 100.0, 250.0, 160.0, 0.5, key="tb")
    if tb > 0:
        bmi_calc = bb / ((tb / 100) ** 2)
        st.info(f"BMI kamu: **{bmi_calc:.1f}** — gunakan nilai ini di kolom BMI atas.")


# ─────────────────────────────────────────────
#  Tombol prediksi
# ─────────────────────────────────────────────
st.markdown("---")
predict_col, _, _ = st.columns([1, 2, 1])
with predict_col:
    predict_btn = st.button("🔍 Prediksi Sekarang", use_container_width=True, type="primary")


# ─────────────────────────────────────────────
#  Hasil prediksi
# ─────────────────────────────────────────────
if predict_btn:
    input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness,
                             insulin, bmi, dpf, age]])
    input_scaled = scaler.transform(input_data)

    proba      = model.predict_proba(input_scaled)[0][1]
    prediction = 1 if proba >= THRESHOLD else 0

    st.markdown("---")
    st.subheader("📊 Hasil Prediksi")

    # ── Kartu hasil utama ──
    r1, r2, r3 = st.columns([1.2, 1, 1])

    with r1:
        if prediction == 1:
            st.markdown(f"""
            <div class="result-positive">
              <div class="result-title" style="color:#E24B4A">⚠️ Berisiko Diabetes</div>
              <div class="result-prob" style="color:#E24B4A">{proba:.1%}</div>
              <div class="result-sub">Probabilitas positif diabetes</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-negative">
              <div class="result-title" style="color:#1D9E75">✅ Tidak Berisiko</div>
              <div class="result-prob" style="color:#1D9E75">{proba:.1%}</div>
              <div class="result-sub">Probabilitas positif diabetes</div>
            </div>""", unsafe_allow_html=True)

    with r2:
        st.markdown("**Probabilitas**")
        fig_prob, ax_prob = plt.subplots(figsize=(3.5, 3.5))
        wedge_colors = ['#1D9E75', '#E24B4A'] if prediction == 1 else ['#E24B4A', '#1D9E75']
        sizes = [1 - proba, proba]
        labels_pie = ['Tidak Diabetes', 'Diabetes']
        wedges, texts, autotexts = ax_prob.pie(
            sizes, labels=labels_pie, autopct='%1.1f%%',
            colors=['#c8f0e0', '#ffd6d5'],
            startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        autotexts[1].set_color('#E24B4A')
        autotexts[1].set_fontsize(12)
        autotexts[1].set_fontweight('bold')
        autotexts[0].set_color('#1D9E75')
        ax_prob.set_facecolor('white')
        fig_prob.patch.set_facecolor('white')
        st.pyplot(fig_prob, use_container_width=True)
        plt.close(fig_prob)

    with r3:
        st.markdown("**Level Risiko**")
        risk_pct = proba * 100
        if risk_pct < 30:
            risk_label, risk_color = "Rendah", "#1D9E75"
        elif risk_pct < 55:
            risk_label, risk_color = "Sedang", "#EF9F27"
        elif risk_pct < 75:
            risk_label, risk_color = "Tinggi", "#E24B4A"
        else:
            risk_label, risk_color = "Sangat Tinggi", "#A32D2D"

        st.markdown(f"""
        <div style="text-align:center; padding:1rem">
          <div style="font-size:3rem">{
            '🟢' if risk_pct < 30 else ('🟡' if risk_pct < 55 else ('🔴' if risk_pct < 75 else '🚨'))
          }</div>
          <div style="font-size:1.3rem; font-weight:700; color:{risk_color}">{risk_label}</div>
          <div class="gauge-container">
            <div class="gauge-bar">
              <div class="gauge-fill" style="width:{risk_pct:.0f}%; background:{risk_color}"></div>
            </div>
          </div>
          <small style="color:#666">Threshold prediksi: {THRESHOLD:.2f}</small>
        </div>
        """, unsafe_allow_html=True)

    # ── Interpretasi per fitur ──
    st.markdown("---")
    st.subheader("🔍 Analisis Faktor Risiko Pasien")

    # Referensi nilai normal
    NORMAL_RANGES = {
        'Pregnancies':              (0, 5,    "kali"),
        'Glucose':                  (70, 140,  "mg/dL"),
        'BloodPressure':            (60, 80,   "mm Hg"),
        'SkinThickness':            (10, 30,   "mm"),
        'Insulin':                  (16, 166,  "μU/mL"),
        'BMI':                      (18.5, 24.9, "kg/m²"),
        'DiabetesPedigreeFunction': (0.0, 0.6, "skor"),
        'Age':                      (21, 45,   "tahun"),
    }
    input_values = {
        'Pregnancies': pregnancies, 'Glucose': glucose,
        'BloodPressure': blood_pressure, 'SkinThickness': skin_thickness,
        'Insulin': insulin, 'BMI': bmi,
        'DiabetesPedigreeFunction': dpf, 'Age': age,
    }
    LABELS_ID = {
        'Pregnancies': 'Kehamilan', 'Glucose': 'Glukosa',
        'BloodPressure': 'Tekanan Darah', 'SkinThickness': 'Skin Thickness',
        'Insulin': 'Insulin', 'BMI': 'BMI',
        'DiabetesPedigreeFunction': 'Pedigree Diabetes', 'Age': 'Usia',
    }

    rows = []
    for feat in FEATURES:
        val = input_values[feat]
        lo, hi, unit = NORMAL_RANGES[feat]
        if val < lo:
            status = "⬇️ Di bawah normal"
        elif val > hi:
            status = "⬆️ Di atas normal"
        else:
            status = "✅ Normal"
        rows.append({'Fitur': LABELS_ID[feat], 'Nilai Pasien': f"{val} {unit}",
                     'Rentang Normal': f"{lo}–{hi} {unit}", 'Status': status})

    df_display = pd.DataFrame(rows)

    def style_status(val):
        if "atas" in val:   return "color:#E24B4A; font-weight:600"
        if "bawah" in val:  return "color:#EF9F27; font-weight:600"
        return "color:#1D9E75; font-weight:600"

    styled_display = df_display.style
    if hasattr(styled_display, "map"):
        styled_display = styled_display.map(style_status, subset=['Status'])
    else:
        styled_display = styled_display.applymap(style_status, subset=['Status'])

    st.dataframe(
        styled_display,
        use_container_width=True, hide_index=True
    )

    # ── Feature importance radar ──
    if hasattr(model, 'feature_importances_'):
        st.markdown("---")
        st.subheader("📈 Kontribusi Fitur (Feature Importance)")

        fi = model.feature_importances_
        fi_df = pd.DataFrame({'Feature': [LABELS_ID[f] for f in FEATURES], 'Importance': fi})
        fi_df = fi_df.sort_values('Importance', ascending=True)

        fig_fi, ax_fi = plt.subplots(figsize=(9, 4))
        bar_colors = ['#B5D4F4' if v < fi_df['Importance'].median() else '#185FA5'
                      for v in fi_df['Importance']]
        bars = ax_fi.barh(fi_df['Feature'], fi_df['Importance'],
                          color=bar_colors, edgecolor='white', linewidth=0.5)
        for bar, val in zip(bars, fi_df['Importance']):
            ax_fi.text(val + 0.002, bar.get_y() + bar.get_height() / 2,
                       f'{val:.3f}', va='center', fontsize=9)
        ax_fi.set_xlabel('Importance Score')
        ax_fi.set_title(f'Feature Importance — {meta["model_name"]}', fontweight='bold')
        ax_fi.set_facecolor('#f8f9fa')
        ax_fi.set_xlim(0, fi_df['Importance'].max() * 1.18)
        fig_fi.patch.set_facecolor('white')
        plt.tight_layout()
        st.pyplot(fig_fi, use_container_width=True)
        plt.close(fig_fi)

    # ── Saran ──
    st.markdown("---")
    st.subheader("💡 Saran Tindak Lanjut")

    if prediction == 1:
        st.error("⚠️ **Pasien ini diprediksi berisiko diabetes.** Disarankan:")
        saran_positif = [
            "Segera konsultasikan ke dokter untuk pemeriksaan HbA1c dan tes toleransi glukosa lebih lanjut.",
            f"Kadar glukosa {glucose} mg/dL" + (" — perlu perhatian khusus." if glucose > 140 else " — dalam batas aman."),
            f"BMI {bmi:.1f}" + (" — pertimbangkan program penurunan berat badan." if bmi > 25 else " — pertahankan berat badan ideal."),
            "Tingkatkan aktivitas fisik minimal 150 menit/minggu.",
            "Kurangi konsumsi makanan tinggi gula dan karbohidrat sederhana.",
            "Monitor gula darah secara rutin.",
        ]
        for s in saran_positif:
            st.markdown(f"- {s}")
    else:
        st.success("✅ **Pasien ini diprediksi tidak berisiko diabetes saat ini.** Tetap jaga kesehatan:")
        saran_negatif = [
            "Lanjutkan pola makan sehat dengan banyak serat, sayur, dan buah.",
            "Pertahankan BMI dalam rentang normal (18.5 – 24.9).",
            "Olahraga rutin minimal 3–4 kali seminggu.",
            "Lakukan pemeriksaan gula darah tahunan sebagai pencegahan.",
            "Hindari stres berlebihan dan jaga kualitas tidur.",
        ]
        for s in saran_negatif:
            st.markdown(f"- {s}")

    # ── Disclaimer ──
    st.markdown("""
    <div class="disclaimer">
      ⚠️ <strong>Disclaimer:</strong> Hasil prediksi ini hanya bersifat indikatif dan
      <strong>bukan diagnosis medis</strong>. Model ini dilatih pada dataset terbatas
      (Pima Indians Diabetes Database) dan mungkin tidak akurat untuk semua populasi.
      Selalu konsultasikan kondisi kesehatan dengan tenaga medis profesional.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.caption("🩺 Diabetes Predictor • Dibangun dengan Python & Streamlit • Dataset: Pima Indians Diabetes (Kaggle)")
