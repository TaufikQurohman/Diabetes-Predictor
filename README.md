# 🩺 Diabetes Risk Predictor

Aplikasi web Machine Learning untuk memprediksi risiko diabetes berdasarkan data kesehatan pasien menggunakan Python, scikit-learn, dan Streamlit.

---

## 🌐 Live Demo

🔗 https://diabetes-predictor-qgi3asnp7xdeht2tr7evda.streamlit.app/

---

## 🎯 Tentang Project

Project ini merupakan implementasi end-to-end Data Science & Machine Learning, mulai dari eksplorasi data hingga deployment aplikasi web interaktif.

### 📌 Cakupan Project

- ✅ Exploratory Data Analysis (EDA)
- ✅ Data Cleaning & Preprocessing
- ✅ Training dan Evaluasi Model Machine Learning
- ✅ Visualisasi Data & Feature Importance
- ✅ Web App Interaktif menggunakan Streamlit
- ✅ Deployment ke Streamlit Community Cloud

---

## 📊 Dataset

Dataset yang digunakan adalah:

**Pima Indians Diabetes Database** dari Kaggle

Dataset berisi data kesehatan 768 pasien wanita keturunan Pima Indian berusia ≥ 21 tahun.

| Fitur | Deskripsi |
|---|---|
| Pregnancies | Jumlah kehamilan |
| Glucose | Kadar glukosa plasma (mg/dL) |
| BloodPressure | Tekanan darah diastolik (mm Hg) |
| SkinThickness | Ketebalan lipatan kulit trisep (mm) |
| Insulin | Kadar insulin serum 2 jam (μU/mL) |
| BMI | Body Mass Index (kg/m²) |
| DiabetesPedigreeFunction | Riwayat diabetes keluarga |
| Age | Usia pasien |
| Outcome | 0 = Tidak Diabetes, 1 = Diabetes |

---

## 🏆 Performa Model

| Model | Accuracy | F1-Score | ROC-AUC |
|---|---|---|---|
| Logistic Regression | ~76% | ~0.68 | ~0.82 |
| Random Forest | ~79% | ~0.72 | ~0.84 |
| Gradient Boosting | ~80% | ~0.73 | ~0.85 |
| SVM | ~77% | ~0.70 | ~0.83 |

📌 Model terbaik dipilih berdasarkan skor ROC-AUC tertinggi.

---

## ✨ Fitur Aplikasi

- ✅ Form input data pasien yang interaktif
- ✅ Kalkulator BMI otomatis
- ✅ Prediksi risiko diabetes
- ✅ Visualisasi probabilitas prediksi
- ✅ Level risiko (Rendah / Sedang / Tinggi / Sangat Tinggi)
- ✅ Analisis faktor risiko pasien
- ✅ Feature importance visualization
- ✅ Saran tindak lanjut kesehatan
- ✅ Sidebar informasi model dan dataset

---

## 🗂️ Struktur Project

```plaintext
diabetes-predictor/
│
├── data/
│   └── diabetes.csv
│
├── notebook/
│   └── eda.ipynb
│
├── model/
│   ├── model.pkl
│   ├── scaler.pkl
│   └── metadata.json
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 🚀 Cara Menjalankan Secara Lokal

### 1️⃣ Clone Repository

```bash
git clone https://github.com/TaufikQurohman/Diabetes-Predictor.git
cd Diabetes-Predictor
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Jalankan Streamlit

```bash
python -m streamlit run app.py
```

Buka browser:

```plaintext
http://localhost:8501
```

---

## ☁️ Deployment

Aplikasi dideploy menggunakan:

- Streamlit Community Cloud
- GitHub Repository Integration

Setiap perubahan pada branch `main` akan otomatis memperbarui aplikasi.

---

## 🛠️ Tech Stack

| Teknologi | Fungsi |
|---|---|
| Python | Bahasa pemrograman utama |
| pandas | Manipulasi data |
| numpy | Komputasi numerik |
| scikit-learn | Machine Learning |
| matplotlib | Visualisasi data |
| Streamlit | Web application framework |
| joblib | Save & load model |
| Jupyter Notebook | Eksplorasi data |

---

## 📸 Tampilan Aplikasi

### Dashboard Utama
- Input data kesehatan pasien
- Prediksi risiko diabetes
- Visualisasi probabilitas
- Analisis faktor risiko

---

## ⚠️ Disclaimer

Aplikasi ini dibuat untuk tujuan pembelajaran Data Science dan Machine Learning.

Hasil prediksi **bukan diagnosis medis** dan tidak dapat menggantikan konsultasi dengan tenaga kesehatan profesional.

---

## 👨‍💻 Author

### Taufik Qurohman

- GitHub: https://github.com/TaufikQurohman
- LinkedIn: https://linkedin.com/in/Taufikqurohman31

---
