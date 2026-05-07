import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Prediksi Risiko Diabetes",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>

/* ===== GLOBAL ===== */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #F4F7FB;
}

/* ===== HEADER ===== */
.main-header {
    background: linear-gradient(135deg, #0F172A 0%, #185FA5 60%, #3B82F6 100%);
    padding: 2.5rem;
    border-radius: 24px;
    margin-bottom: 2rem;
    color: white;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}

.main-header h1 {
    color: white;
    margin: 0;
    font-size: 2.4rem;
    font-weight: 800;
}

.main-header p {
    color: rgba(255,255,255,0.92);
    margin-top: 0.7rem;
    font-size: 1rem;
    line-height: 1.7;
}

.author-badge {
    display: inline-block;
    margin-top: 1rem;
    background: rgba(255,255,255,0.15);
    padding: 0.5rem 1rem;
    border-radius: 999px;
    font-size: 0.9rem;
    backdrop-filter: blur(10px);
}

/* ===== RESULT CARD ===== */
.result-positive {
    background: linear-gradient(135deg, #DC2626, #EF4444);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    color: white;
    box-shadow: 0 10px 25px rgba(220,38,38,0.25);
}

.result-negative {
    background: linear-gradient(135deg, #059669, #10B981);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    color: white;
    box-shadow: 0 10px 25px rgba(16,185,129,0.25);
}

.result-title {
    font-size: 1.5rem;
    font-weight: 700;
}

.result-prob {
    font-size: 3rem;
    font-weight: 800;
    margin: 0.5rem 0;
}

.result-sub {
    font-size: 0.95rem;
    opacity: 0.9;
}

/* ===== MODEL CARD ===== */
.model-card {
    background: rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 0.7rem;
}

/* ===== BUTTON ===== */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #185FA5, #3B82F6);
    color: white;
    border: none;
    padding: 0.9rem;
    border-radius: 14px;
    font-size: 1rem;
    font-weight: 700;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 18px rgba(24,95,165,0.35);
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #111827 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* ===== SIDEBAR SECTION ===== */
.sidebar-section {
    background: rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 1rem;
    font-size: 0.85rem;
    line-height: 1.6;
}

/* ===== METRIC ===== */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1rem;
}

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
}

/* ===== FOOTER ===== */
.footer {
    margin-top: 3rem;
    text-align: center;
    padding: 1.5rem;
    color: #64748B;
    font-size: 0.9rem;
}

.footer strong {
    color: #185FA5;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    model = joblib.load('model/model.pkl')
    scaler = joblib.load('model/scaler.pkl')
    return model, scaler

@st.cache_data
def load_metadata():
    try:
        with open('model/metadata.json') as f:
            return json.load(f)
    except:
        return {
            'model_name': 'Random Forest',
            'accuracy': 0.79,
            'roc_auc': 0.84,
            'f1_score': 0.72,
            'optimal_threshold': 0.45,
            'train_size': 614,
            'test_size': 154
        }

model, scaler = load_model()
meta = load_metadata()

THRESHOLD = meta.get('optimal_threshold', 0.5)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:

    st.markdown("## 🩺 Diabetes Predictor")
    st.markdown("---")

    st.markdown("### 📊 Info Model")

    c1, c2 = st.columns(2)

    c1.metric("Accuracy", f"{meta['accuracy']:.1%}")
    c2.metric("ROC-AUC", f"{meta['roc_auc']:.2f}")

    c1.metric("F1 Score", f"{meta['f1_score']:.2f}")
    c2.metric("Threshold", f"{THRESHOLD:.2f}")

    st.caption(
        f"Model: {meta['model_name']} | "
        f"Train: {meta['train_size']} | "
        f"Test: {meta['test_size']}"
    )

    st.markdown("---")

    st.markdown("### 📖 Panduan Pengisian")

    st.markdown("""
<div class="sidebar-section">
<h4>Glucose</h4>
Kadar gula darah plasma 2 jam setelah tes toleransi glukosa oral.
Normal: 70–140 mg/dL.
</div>

<div class="sidebar-section">
<h4>BMI</h4>
Body Mass Index = berat (kg) / tinggi² (m²).
Normal: 18.5–24.9.
</div>

<div class="sidebar-section">
<h4>Blood Pressure</h4>
Tekanan darah diastolik.
Normal: 60–80 mm Hg.
</div>

<div class="sidebar-section">
<h4>Diabetes Pedigree Function</h4>
Skor riwayat diabetes keluarga.
Semakin tinggi semakin berisiko.
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🔬 Tentang Dataset")

    st.caption("""
Dataset menggunakan Pima Indians Diabetes Database
(Kaggle) dengan 768 data pasien wanita usia ≥ 21 tahun.
""")

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">

<h1>🩺 Prediksi Risiko Diabetes</h1>

<p>
Sistem prediksi risiko diabetes berbasis Machine Learning
untuk membantu analisis kesehatan pasien secara cepat,
modern, dan interaktif.
</p>

<div class="author-badge">
👨‍💻 Developed by <strong>Taufik Qurohman</strong>
</div>

</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INPUT FORM
# ─────────────────────────────────────────────
st.subheader("📋 Data Kesehatan Pasien")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("### 🔢 Data Umum")

    pregnancies = st.number_input(
        "Jumlah Kehamilan",
        min_value=0,
        max_value=20,
        value=1
    )

    age = st.number_input(
        "Usia",
        min_value=21,
        max_value=100,
        value=30
    )

    dpf = st.number_input(
        "Diabetes Pedigree Function",
        min_value=0.0,
        max_value=3.0,
        value=0.47,
        step=0.01
    )

with col2:

    st.markdown("### 💉 Gula & Tekanan")

    glucose = st.number_input(
        "Glucose",
        min_value=0,
        max_value=300,
        value=120
    )

    blood_pressure = st.number_input(
        "Blood Pressure",
        min_value=0,
        max_value=150,
        value=72
    )

    insulin = st.number_input(
        "Insulin",
        min_value=0,
        max_value=900,
        value=80
    )

with col3:

    st.markdown("### 📏 Data Fisik")

    bmi = st.number_input(
        "BMI",
        min_value=0.0,
        max_value=80.0,
        value=25.0,
        step=0.1
    )

    skin_thickness = st.number_input(
        "Skin Thickness",
        min_value=0,
        max_value=100,
        value=23
    )

    st.markdown("---")

    st.markdown("### 🔧 Kalkulator BMI")

    bb = st.number_input("Berat (kg)", 30.0, 200.0, 60.0)
    tb = st.number_input("Tinggi (cm)", 100.0, 250.0, 160.0)

    bmi_calc = bb / ((tb / 100) ** 2)

    st.info(f"BMI Kamu: {bmi_calc:.1f}")

# ─────────────────────────────────────────────
#  Tombol prediksi
# ─────────────────────────────────────────────
st.markdown("---")

predict_col, _, _ = st.columns([1, 2, 1])

with predict_col:
    predict_btn = st.button(
        "🔍 Prediksi Sekarang",
        use_container_width=True,
        type="primary"
    )


# ─────────────────────────────────────────────
#  Hasil prediksi
# ─────────────────────────────────────────────
if predict_btn:

    input_data = np.array([[
        pregnancies,
        glucose,
        blood_pressure,
        skin_thickness,
        insulin,
        bmi,
        dpf,
        age
    ]])

    input_scaled = scaler.transform(input_data)

    proba = model.predict_proba(input_scaled)[0][1]
    prediction = 1 if proba >= THRESHOLD else 0

    st.markdown("---")
    st.subheader("📊 Hasil Prediksi")

    # ─────────────────────────────────────────
    #  Tema warna baru
    # ─────────────────────────────────────────
    PRIMARY_BLUE = "#2563EB"
    LIGHT_BLUE = "#DBEAFE"

    SUCCESS = "#0F766E"
    SUCCESS_LIGHT = "#CCFBF1"

    WARNING = "#F59E0B"
    DANGER = "#DC2626"
    DANGER_LIGHT = "#FEE2E2"

    # ─────────────────────────────────────────
    #  Kartu hasil utama
    # ─────────────────────────────────────────
    r1, r2, r3 = st.columns([1.2, 1, 1])

    with r1:

        if prediction == 1:

            st.markdown(f"""
            <div class="result-positive"
                 style="
                 background:{DANGER_LIGHT};
                 border:2px solid {DANGER};
                 border-radius:18px;
                 padding:1.7rem;
                 box-shadow:0 4px 14px rgba(0,0,0,0.08);
                 ">

              <div class="result-title"
                   style="
                   color:{DANGER};
                   font-size:1.4rem;
                   font-weight:700;
                   ">
                   ⚠️ Berisiko Diabetes
              </div>

              <div class="result-prob"
                   style="
                   color:{DANGER};
                   font-size:3rem;
                   font-weight:800;
                   margin-top:8px;
                   ">
                   {proba:.1%}
              </div>

              <div class="result-sub"
                   style="
                   color:#555;
                   margin-top:6px;
                   ">
                   Probabilitas positif diabetes
              </div>

            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown(f"""
            <div class="result-negative"
                 style="
                 background:{SUCCESS_LIGHT};
                 border:2px solid {SUCCESS};
                 border-radius:18px;
                 padding:1.7rem;
                 box-shadow:0 4px 14px rgba(0,0,0,0.08);
                 ">

              <div class="result-title"
                   style="
                   color:{SUCCESS};
                   font-size:1.4rem;
                   font-weight:700;
                   ">
                   ✅ Tidak Berisiko
              </div>

              <div class="result-prob"
                   style="
                   color:{SUCCESS};
                   font-size:3rem;
                   font-weight:800;
                   margin-top:8px;
                   ">
                   {proba:.1%}
              </div>

              <div class="result-sub"
                   style="
                   color:#555;
                   margin-top:6px;
                   ">
                   Probabilitas positif diabetes
              </div>

            </div>
            """, unsafe_allow_html=True)

    # ─────────────────────────────────────────
    #  Pie Chart Probabilitas
    # ─────────────────────────────────────────
    with r2:

        st.markdown("### 📈 Probabilitas")

        fig_prob, ax_prob = plt.subplots(figsize=(3.8, 3.8))

        sizes = [1 - proba, proba]

        labels_pie = [
            'Tidak Diabetes',
            'Diabetes'
        ]

        colors = [
            SUCCESS_LIGHT,
            DANGER_LIGHT
        ]

        wedges, texts, autotexts = ax_prob.pie(
            sizes,
            labels=labels_pie,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            wedgeprops={
                'edgecolor': 'white',
                'linewidth': 2
            }
        )

        autotexts[0].set_color(SUCCESS)
        autotexts[1].set_color(DANGER)

        for auto in autotexts:
            auto.set_fontsize(11)
            auto.set_fontweight('bold')

        ax_prob.set_facecolor("white")
        fig_prob.patch.set_facecolor("white")

        st.pyplot(fig_prob, use_container_width=True)

        plt.close(fig_prob)

    # ─────────────────────────────────────────
    #  Risk Level
    # ─────────────────────────────────────────
    with r3:

        st.markdown("### 🎯 Level Risiko")

        risk_pct = proba * 100

        if risk_pct < 30:
            risk_label = "Rendah"
            risk_color = SUCCESS
            risk_icon = "🟢"

        elif risk_pct < 55:
            risk_label = "Sedang"
            risk_color = WARNING
            risk_icon = "🟡"

        elif risk_pct < 75:
            risk_label = "Tinggi"
            risk_color = DANGER
            risk_icon = "🔴"

        else:
            risk_label = "Sangat Tinggi"
            risk_color = "#7F1D1D"
            risk_icon = "🚨"

        st.markdown(f"""
        <div style="
            text-align:center;
            padding:1.2rem;
            border-radius:18px;
            background:#F8FAFC;
            border:1px solid #E2E8F0;
            box-shadow:0 4px 14px rgba(0,0,0,0.05);
        ">

          <div style="font-size:3rem">
            {risk_icon}
          </div>

          <div style="
              font-size:1.4rem;
              font-weight:700;
              color:{risk_color};
              margin-top:8px;
          ">
            {risk_label}
          </div>

          <div style="
              width:100%;
              height:14px;
              background:#E5E7EB;
              border-radius:999px;
              overflow:hidden;
              margin-top:18px;
          ">

            <div style="
                width:{risk_pct:.0f}%;
                height:100%;
                background:{risk_color};
                border-radius:999px;
            ">
            </div>

          </div>

          <div style="
              margin-top:10px;
              color:#666;
              font-size:0.9rem;
          ">
            Threshold prediksi: {THRESHOLD:.2f}
          </div>

        </div>
        """, unsafe_allow_html=True)

    # ─────────────────────────────────────────
    #  Analisis Faktor Risiko
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader("🔍 Analisis Faktor Risiko Pasien")

    NORMAL_RANGES = {
        'Pregnancies': (0, 5, "kali"),
        'Glucose': (70, 140, "mg/dL"),
        'BloodPressure': (60, 80, "mm Hg"),
        'SkinThickness': (10, 30, "mm"),
        'Insulin': (16, 166, "μU/mL"),
        'BMI': (18.5, 24.9, "kg/m²"),
        'DiabetesPedigreeFunction': (0.0, 0.6, "skor"),
        'Age': (21, 45, "tahun"),
    }

    input_values = {
        'Pregnancies': pregnancies,
        'Glucose': glucose,
        'BloodPressure': blood_pressure,
        'SkinThickness': skin_thickness,
        'Insulin': insulin,
        'BMI': bmi,
        'DiabetesPedigreeFunction': dpf,
        'Age': age,
    }

    LABELS_ID = {
        'Pregnancies': 'Kehamilan',
        'Glucose': 'Glukosa',
        'BloodPressure': 'Tekanan Darah',
        'SkinThickness': 'Skin Thickness',
        'Insulin': 'Insulin',
        'BMI': 'BMI',
        'DiabetesPedigreeFunction': 'Pedigree Diabetes',
        'Age': 'Usia',
    }

    rows = []

    for feat in input_values.keys():

        val = input_values[feat]

        lo, hi, unit = NORMAL_RANGES[feat]

        if val < lo:
            status = "⬇️ Di bawah normal"

        elif val > hi:
            status = "⬆️ Di atas normal"

        else:
            status = "✅ Normal"

        rows.append({
            'Fitur': LABELS_ID[feat],
            'Nilai Pasien': f"{val} {unit}",
            'Rentang Normal': f"{lo}–{hi} {unit}",
            'Status': status
        })

    df_display = pd.DataFrame(rows)

    def style_status(val):

        if "atas" in val:
            return f"color:{DANGER}; font-weight:700"

        if "bawah" in val:
            return f"color:{WARNING}; font-weight:700"

        return f"color:{SUCCESS}; font-weight:700"

    st.dataframe(
        df_display.style.applymap(
            style_status,
            subset=['Status']
        ),
        use_container_width=True,
        hide_index=True
    )

    # ─────────────────────────────────────────
    #  Feature Importance
    # ─────────────────────────────────────────
    if hasattr(model, 'feature_importances_'):

        st.markdown("---")
        st.subheader("📈 Kontribusi Fitur (Feature Importance)")

        fi = model.feature_importances_

        fi_df = pd.DataFrame({
            'Feature': [LABELS_ID[f] for f in input_values.keys()],
            'Importance': fi
        })

        fi_df = fi_df.sort_values(
            'Importance',
            ascending=True
        )

        fig_fi, ax_fi = plt.subplots(figsize=(9, 4.5))

        bar_colors = [
            LIGHT_BLUE if v < fi_df['Importance'].median()
            else PRIMARY_BLUE
            for v in fi_df['Importance']
        ]

        bars = ax_fi.barh(
            fi_df['Feature'],
            fi_df['Importance'],
            color=bar_colors,
            edgecolor='white',
            linewidth=1
        )

        for bar, val in zip(bars, fi_df['Importance']):

            ax_fi.text(
                val + 0.002,
                bar.get_y() + bar.get_height() / 2,
                f'{val:.3f}',
                va='center',
                fontsize=9,
                fontweight='bold',
                color="#111827"
            )

        ax_fi.set_xlabel('Importance Score')

        ax_fi.set_title(
            f'Feature Importance — {meta["model_name"]}',
            fontweight='bold',
            color=PRIMARY_BLUE
        )

        ax_fi.set_facecolor('#F8FAFC')

        fig_fi.patch.set_facecolor('white')

        ax_fi.grid(
            axis='x',
            linestyle='--',
            alpha=0.3
        )

        st.pyplot(fig_fi, use_container_width=True)

        plt.close(fig_fi)

    # ─────────────────────────────────────────
    #  Saran
    # ─────────────────────────────────────────
    st.markdown("---")
    st.subheader("💡 Saran Tindak Lanjut")

    if prediction == 1:

        st.error(
            "⚠️ **Pasien ini diprediksi berisiko diabetes.** Disarankan:"
        )

        saran_positif = [
            "Segera konsultasikan ke dokter untuk pemeriksaan HbA1c dan tes toleransi glukosa lebih lanjut.",
            f"Kadar glukosa {glucose} mg/dL" + (
                " — perlu perhatian khusus."
                if glucose > 140
                else " — dalam batas aman."
            ),
            f"BMI {bmi:.1f}" + (
                " — pertimbangkan program penurunan berat badan."
                if bmi > 25
                else " — pertahankan berat badan ideal."
            ),
            "Tingkatkan aktivitas fisik minimal 150 menit/minggu.",
            "Kurangi konsumsi makanan tinggi gula dan karbohidrat sederhana.",
            "Monitor gula darah secara rutin.",
        ]

        for s in saran_positif:
            st.markdown(f"- {s}")

    else:

        st.success(
            "✅ **Pasien ini diprediksi tidak berisiko diabetes saat ini.** Tetap jaga kesehatan:"
        )

        saran_negatif = [
            "Lanjutkan pola makan sehat dengan banyak serat, sayur, dan buah.",
            "Pertahankan BMI dalam rentang normal (18.5 – 24.9).",
            "Olahraga rutin minimal 3–4 kali seminggu.",
            "Lakukan pemeriksaan gula darah tahunan sebagai pencegahan.",
            "Hindari stres berlebihan dan jaga kualitas tidur.",
        ]

        for s in saran_negatif:
            st.markdown(f"- {s}")

    # ─────────────────────────────────────────
    #  Disclaimer
    # ─────────────────────────────────────────
    st.markdown(f"""
    <div style="
        background:#FEF3C7;
        border-left:6px solid {WARNING};
        padding:1rem 1.2rem;
        border-radius:12px;
        margin-top:1rem;
        color:#444;
    ">

      ⚠️ <strong>Disclaimer:</strong>
      Hasil prediksi ini hanya bersifat indikatif dan
      <strong>bukan diagnosis medis</strong>.
      Selalu konsultasikan kondisi kesehatan
      dengan tenaga medis profesional.

    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">

🩺 Diabetes Predictor System <br>
Built with Python, Streamlit & Machine Learning <br><br>

<strong>Author:</strong> Taufik Qurohman

</div>
""", unsafe_allow_html=True)