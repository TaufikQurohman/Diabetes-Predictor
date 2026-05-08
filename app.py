import streamlit as st
import joblib
import json
import re
from datetime import datetime

# ─────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="TokoBot · FAQ Assistant",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,600;0,9..144,700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
  --cream:      #f4faf6;
  --parchment:  #e7f3ea;
  --warm-100:   #d1e6d8;
  --warm-200:   #b2d1bc;
  --amber:      #4f9d69;
  --amber-deep: #35784c;
  --amber-glow: #74c48f;
  --ink:        #1f3327;
  --ink-muted:  #5b6f62;
  --ink-light:  #8aa091;
  --teal:       #2d9c8f;
  --teal-light: #4cc9b0;
  --rose:       #c96d6d;
  --surface:    #ffffff;
  --border:     #d7e8dc;
  --shadow:     rgba(31, 51, 39, 0.08);
}

html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
  background: var(--cream) !important;
  color: var(--ink) !important;
}

/* ── Sembunyikan elemen Streamlit bawaan yang tidak perlu ──
   PENTING: JANGAN sentuh stSidebar, collapsedControl, stSidebarNav toggle */
#MainMenu { visibility: hidden !important; }
footer    { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }

/* Kurangi padding atas */
.block-container {
  padding-top: 1rem !important;
  padding-left: 1.5rem !important;
  padding-right: 1.5rem !important;
  max-width: 100% !important;
}

/* ══════════════════════════════════════
   SIDEBAR
══════════════════════════════════════ */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #1a2e22 0%, #152619 55%, #0f1d12 100%) !important;
  border-right: 1px solid rgba(116,196,143,0.15) !important;
}
[data-testid="stSidebar"] > div:first-child {
  padding-top: 0 !important;
}
[data-testid="stSidebar"] * {
  color: #c2d9c9 !important;
  font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] h3 {
  color: #74c48f !important;
  font-family: 'Fraunces', serif !important;
  font-size: 0.72rem !important; font-weight: 400 !important;
  letter-spacing: 0.14em !important; text-transform: uppercase !important;
}
[data-testid="stSidebar"] strong { color: #e8f5ed !important; }
[data-testid="stSidebar"] [data-testid="stMetricValue"] {
  color: #74c48f !important; font-family: 'DM Mono', monospace !important; font-size: 1.1rem !important;
}
[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
  color: #7a9e84 !important; font-size: 0.65rem !important;
  text-transform: uppercase; letter-spacing: 0.08em;
}
[data-testid="stSidebar"] [data-testid="stMetric"] {
  background: rgba(116,196,143,0.07) !important;
  border: 1px solid rgba(116,196,143,0.12) !important;
  border-radius: 10px !important; padding: 0.65rem 0.85rem !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(116,196,143,0.12) !important; }
[data-testid="stSidebar"] [data-testid="stButton"] > button {
  background: rgba(116,196,143,0.1) !important; color: #74c48f !important;
  border: 1px solid rgba(116,196,143,0.2) !important;
  border-radius: 8px !important; font-size: 0.78rem !important;
  font-weight: 500 !important; transition: all 0.18s !important; box-shadow: none !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
  background: #4f9d69 !important; color: #fff !important; border-color: #4f9d69 !important;
}

/* ══════════════════════════════════════
   HEADER (flow normal, bukan fixed)
══════════════════════════════════════ */
.chat-header {
  background: var(--surface); border: 1.5px solid var(--border);
  border-radius: 14px; padding: 12px 18px;
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 1rem; box-shadow: 0 2px 12px var(--shadow);
}
.bot-avatar-header {
  width: 38px; height: 38px; border-radius: 10px;
  background: linear-gradient(135deg, #4f9d69 0%, #2f5f3f 100%);
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; flex-shrink: 0;
  box-shadow: 0 3px 10px rgba(79,157,105,0.3);
}
.bot-name {
  font-family: 'Fraunces', serif; font-size: 1rem; font-weight: 600;
  color: var(--ink); margin: 0; letter-spacing: -0.01em;
}
.bot-status {
  font-size: 0.68rem; color: var(--teal); margin: 0;
  display: flex; align-items: center; gap: 5px; font-weight: 500;
}
.status-dot {
  display: inline-block; width: 6px; height: 6px;
  border-radius: 50%; background: var(--teal-light);
  animation: pulse 2.5s ease-in-out infinite;
}
@keyframes pulse {
  0%,100% { opacity:1; box-shadow:0 0 0 0 rgba(76,201,176,0.5); }
  50%      { opacity:0.7; box-shadow:0 0 0 5px rgba(76,201,176,0); }
}
.header-badge {
  margin-left: auto; font-family: 'DM Mono', monospace; font-size: 0.6rem;
  background: var(--parchment); border: 1px solid var(--warm-100);
  color: var(--ink-muted); padding: 4px 11px; border-radius: 20px; letter-spacing: 0.04em;
}

/* ══════════════════════════════════════
   CHAT MESSAGES
══════════════════════════════════════ */
.msg-bot {
  display: flex; gap: 12px; align-items: flex-start;
  max-width: 80%; margin-bottom: 1rem;
  animation: slideUp 0.25s cubic-bezier(0.34,1.56,0.64,1);
}
.bot-avatar {
  width: 34px; height: 34px; border-radius: 10px;
  background: linear-gradient(135deg, #4f9d69 0%, #2f5f3f 100%);
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; flex-shrink: 0; margin-top: 2px;
  box-shadow: 0 3px 10px rgba(79,157,105,0.3);
}
.msg-bubble-bot {
  background: var(--surface); border: 1.5px solid var(--border);
  border-radius: 2px 16px 16px 16px;
  padding: 1rem 1.2rem; font-size: 0.875rem; line-height: 1.7;
  color: var(--ink); box-shadow: 0 2px 12px var(--shadow);
}
.msg-bubble-bot strong { color: var(--amber-deep); font-weight: 600; }
.msg-time { font-size: 0.6rem; color: var(--ink-light); margin-top: 5px; padding-left: 46px; font-family: 'DM Mono', monospace; }
.msg-user { display: flex; justify-content: flex-end; margin-bottom: 1rem; animation: slideUp 0.25s cubic-bezier(0.34,1.56,0.64,1); }
.msg-bubble-user {
  background: linear-gradient(135deg, #4f9d69 0%, #35784c 100%);
  border-radius: 16px 2px 16px 16px;
  padding: 0.9rem 1.2rem; font-size: 0.875rem; line-height: 1.7;
  color: #fff; max-width: 75%; box-shadow: 0 4px 16px rgba(79,157,105,0.35);
  font-weight: 500; word-break: break-word;
}
.msg-time-user { font-size: 0.6rem; color: var(--ink-light); margin-top: 5px; text-align: right; font-family: 'DM Mono', monospace; }
@keyframes slideUp {
  from { opacity:0; transform:translateY(10px) scale(0.98); }
  to   { opacity:1; transform:translateY(0) scale(1); }
}

/* ── Kategori badge ── */
.kategori-badge {
  display: inline-block; font-family: 'DM Mono', monospace;
  font-size: 0.58rem; font-weight: 500; padding: 3px 9px;
  border-radius: 4px; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;
}
.k-pengiriman   { background:#e8f5e9; color:#2d6a4f; border:1px solid #a8d5b5; }
.k-pembayaran   { background:#fff8e6; color:#8b6914; border:1px solid #f0d080; }
.k-pengembalian { background:#fdecea; color:#8b2a24; border:1px solid #e8a09b; }
.k-akun         { background:#e8f0fe; color:#1a4a8a; border:1px solid #9ab4e8; }
.k-produk       { background:#f3e8ff; color:#5a2d8a; border:1px solid #c4a0e8; }
.k-promo        { background:#f0faf3; color:#35784c; border:1px solid #a8d5b5; }
.k-komplain     { background:#fdecea; color:#8b2a24; border:1px solid #e8a09b; }
.k-default      { background:var(--parchment); color:var(--ink-muted); border:1px solid var(--warm-100); }

/* ── Score bar ── */
.score-bar {
  margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--warm-100);
  display: flex; align-items: center; gap: 10px;
  font-size: 0.63rem; color: var(--ink-light); font-family: 'DM Mono', monospace;
}
.score-track { flex:1; height:3px; background:var(--warm-100); border-radius:2px; overflow:hidden; }
.score-fill  { height:100%; border-radius:2px; }

/* ── Related questions ── */
.related-wrap { margin-top:10px; padding-top:10px; border-top:1px solid var(--warm-100); }
.related-label { font-size:0.6rem; color:var(--ink-light); text-transform:uppercase; letter-spacing:0.1em; margin-bottom:6px; font-family:'DM Mono',monospace; }

/* ── Input area ── */
.input-wrapper { border-top: 1.5px solid var(--border); background: var(--surface); padding: 0.9rem 0; margin-top: 0.5rem; }
[data-testid="stTextInput"] input {
  background: var(--parchment) !important; border: 1.5px solid var(--warm-100) !important;
  border-radius: 12px !important; color: var(--ink) !important;
  font-family: 'DM Sans', sans-serif !important; font-size: 0.9rem !important;
  padding: 0.8rem 1.1rem !important; transition: all 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
  border-color: var(--amber) !important;
  box-shadow: 0 0 0 3px rgba(79,157,105,0.15) !important;
  background: var(--surface) !important;
}
[data-testid="stTextInput"] input::placeholder { color: var(--ink-light) !important; font-style: italic; }

/* ── Buttons main ── */
[data-testid="stButton"] > button {
  background: var(--parchment) !important; color: var(--amber-deep) !important;
  border: 1.5px solid var(--warm-100) !important; border-radius: 8px !important;
  font-size: 0.78rem !important; padding: 6px 14px !important;
  font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important;
  transition: all 0.18s ease !important; box-shadow: 0 1px 4px var(--shadow) !important;
}
[data-testid="stButton"] > button:hover {
  background: var(--amber) !important; color: #fff !important;
  border-color: var(--amber) !important; box-shadow: 0 4px 12px rgba(79,157,105,0.25) !important;
}

/* ── Empty state ── */
.empty-state { text-align:center; padding:3rem 2rem 2rem; color:var(--ink-muted); }
.empty-hero {
  width:80px; height:80px; border-radius:24px;
  background:linear-gradient(135deg,#4f9d69 0%,#2f5f3f 100%);
  display:flex; align-items:center; justify-content:center;
  font-size:38px; margin:0 auto 1.5rem;
  box-shadow:0 12px 32px rgba(79,157,105,0.3);
}
.empty-title { font-family:'Fraunces',serif; font-size:1.5rem; font-weight:600; color:var(--ink); margin-bottom:0.5rem; letter-spacing:-0.02em; }
.empty-sub { font-size:0.875rem; line-height:1.7; color:var(--ink-muted); max-width:360px; margin:0 auto 2rem; }
.quick-label { font-family:'DM Mono',monospace; font-size:0.63rem; text-transform:uppercase; letter-spacing:0.12em; color:var(--ink-light); margin-bottom:0.8rem; }
.msg-bubble-fallback { border-left:3px solid var(--rose) !important; background:#fff9f9 !important; }

::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:var(--warm-200); border-radius:4px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Load model
# ─────────────────────────────────────────────
@st.cache_resource
def load_chatbot_model():
    try:
        bundle = joblib.load('model/chatbot_model.pkl')
        required_keys = ['vectorizer', 'tfidf_matrix', 'corpus_idx', 'faqs', 'stopwords', 'sinonim', 'threshold']
        missing = [k for k in required_keys if k not in bundle]
        if missing:
            st.error(f"Model tidak lengkap. Key hilang: {missing}")
            st.stop()
        return bundle
    except FileNotFoundError:
        st.error("File model tidak ditemukan: model/chatbot_model.pkl")
        st.stop()
    except Exception as e:
        st.error(f"Gagal memuat model: {e}")
        st.stop()

@st.cache_data
def load_metadata():
    try:
        with open('model/metadata.json', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {
            'total_faq': 15, 'threshold': 0.15, 'f1_score': 0.88,
            'kategori': ['Pengiriman','Pembayaran','Pengembalian','Akun','Produk','Promo','Komplain']
        }

bundle       = load_chatbot_model()
meta         = load_metadata()
vectorizer   = bundle['vectorizer']
tfidf_matrix = bundle['tfidf_matrix']
corpus_idx   = bundle['corpus_idx']
faqs         = bundle['faqs']
STOPWORDS    = bundle['stopwords']
SINONIM      = bundle['sinonim']
THRESHOLD    = bundle['threshold']


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def preprocess(text: str) -> str:
    text  = text.lower().strip()
    words = [SINONIM.get(w, w) for w in text.split()]
    text  = ' '.join(words)
    text  = re.sub(r'[^a-z0-9\s]', ' ', text)
    text  = re.sub(r'\s+', ' ', text).strip()
    return ' '.join(w for w in text.split() if w not in STOPWORDS and len(w) > 1)

from sklearn.metrics.pairwise import cosine_similarity as cos_sim

def get_answer(query: str, top_k: int = 3) -> dict:
    q_vec = vectorizer.transform([preprocess(query)])
    if q_vec.shape[1] != tfidf_matrix.shape[1]:
        return {'found': False, 'score': 0.0, 'candidates': []}
    sims    = cos_sim(q_vec, tfidf_matrix).flatten()
    top_ids = sims.argsort()[::-1][:top_k * 3]
    best    = top_ids[0]
    score   = float(sims[best])
    if score < THRESHOLD:
        return {'found': False, 'score': score, 'candidates': []}
    best_faq = faqs[corpus_idx[best]]
    seen     = {corpus_idx[best]}
    candidates = []
    for idx in top_ids[1:]:
        fi = corpus_idx[idx]
        if fi not in seen and sims[idx] > THRESHOLD * 0.4:
            candidates.append({'question': faqs[fi]['pertanyaan'],
                                'kategori': faqs[fi]['kategori'],
                                'score'   : float(sims[idx])})
            seen.add(fi)
        if len(candidates) >= 2:
            break
    return {'found': True, 'score': score, 'answer': best_faq['jawaban'],
            'question': best_faq['pertanyaan'], 'kategori': best_faq['kategori'],
            'candidates': candidates}

def kategori_class(kat: str) -> str:
    return f"k-{kat.lower().replace(' ', '-').replace('/', '-')}"

def format_answer(text: str) -> str:
    lines = text.split('\n')
    html  = []
    for line in lines:
        line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        if line.startswith('- ') or line.startswith('✅') or line.startswith('❌'):
            html.append(f'<div style="padding:2px 0 2px 4px">{line}</div>')
        elif line.strip() == '':
            html.append('<div style="height:6px"></div>')
        else:
            html.append(f'<div>{line}</div>')
    return ''.join(html)

def now_str() -> str:
    return datetime.now().strftime('%H:%M')


# ─────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'pending_query' not in st.session_state:
    st.session_state.pending_query = None


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.3rem 1.1rem 1rem;border-bottom:1px solid rgba(116,196,143,0.12);
                margin-bottom:0.5rem;position:relative;">
      <div style="position:absolute;bottom:0;left:1.1rem;right:1.1rem;height:1px;
                  background:linear-gradient(90deg,transparent,#74c48f,transparent);opacity:0.35"></div>
      <div style="display:flex;align-items:center;gap:12px">
        <div style="width:42px;height:42px;border-radius:12px;
                    background:linear-gradient(135deg,#4f9d69,#2f5f3f);
                    display:flex;align-items:center;justify-content:center;
                    font-size:22px;box-shadow:0 4px 16px rgba(79,157,105,0.4);">🛍️</div>
        <div>
          <div style="font-family:'Fraunces',serif;font-size:1.05rem;font-weight:600;color:#e8f5ed;">
            TokoBot</div>
          <div style="font-size:0.67rem;color:#4cc9b0;font-weight:500;
                      display:flex;align-items:center;gap:4px;margin-top:2px;">
            <span style="width:5px;height:5px;background:#4cc9b0;border-radius:50%;display:inline-block;"></span>
            Online · Siap membantu
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 Info Model")
    c1, c2 = st.columns(2)
    c1.metric("Total FAQ", meta.get('total_faq', 15))
    c2.metric("F1-Score",  f"{meta.get('f1_score', 0.88):.2f}")
    c1.metric("Threshold", f"{meta.get('threshold', 0.15):.2f}")
    c2.metric("Fitur",     meta.get('total_features', '—'))

    st.markdown("---")
    st.markdown("### 🏷️ Kategori FAQ")
    cat_meta = {
        'Pengiriman':   ('#3da48e', '📦'),
        'Pembayaran':   ('#d29922', '💳'),
        'Pengembalian': ('#e05c52', '🔄'),
        'Akun':         ('#5b9cf6', '👤'),
        'Produk':       ('#b07ef8', '🏷️'),
        'Promo':        ('#74c48f', '🎁'),
        'Komplain':     ('#f07070', '📢'),
    }
    for kat in meta.get('kategori', []):
        color, icon = cat_meta.get(kat, ('#8aa091', '•'))
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:6px 0;
                    border-bottom:1px solid rgba(116,196,143,0.1);font-size:0.79rem;">
          <span>{icon}</span>
          <span style="color:#c2d9c9;flex:1;">{kat}</span>
          <div style="width:6px;height:6px;border-radius:50%;background:{color};"></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑 Hapus Riwayat Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="padding:0.2rem 0 1rem;font-size:0.75rem;line-height:1.9;">
      <div style="color:#7a9e84;font-weight:600;margin-bottom:4px;
                  font-family:'DM Mono',monospace;font-size:0.62rem;
                  text-transform:uppercase;letter-spacing:0.12em;">Author</div>
      <div style="color:#e8f5ed;font-family:'Fraunces',serif;font-size:0.95rem;font-weight:600;">
        Taufik Qurohman</div>
      <div style="color:#7a9e84;">Data Science · NLP</div>
      <div style="margin-top:10px;display:flex;gap:6px;">
        <a href="https://github.com/taufikqurohman" target="_blank"
           style="color:#e8f5ed;text-decoration:none;background:rgba(116,196,143,0.1);
                  border:1px solid rgba(116,196,143,0.2);padding:3px 10px;border-radius:6px;
                  font-family:'DM Mono',monospace;font-size:0.62rem;">GitHub</a>
        <a href="https://linkedin.com/in/taufikqurohman" target="_blank"
           style="color:#e8f5ed;text-decoration:none;background:rgba(116,196,143,0.1);
                  border:1px solid rgba(116,196,143,0.2);padding:3px 10px;border-radius:6px;
                  font-family:'DM Mono',monospace;font-size:0.62rem;">LinkedIn</a>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN AREA
# ─────────────────────────────────────────────

# ── Header ──
st.markdown("""
<div class="chat-header">
  <div class="bot-avatar-header">🛍️</div>
  <div>
    <p class="bot-name">TokoBot — FAQ Assistant</p>
    <p class="bot-status">
      <span class="status-dot"></span>
      Online · Siap membantu
    </p>
  </div>
  <span class="header-badge">TF-IDF · Cosine Sim</span>
</div>
""", unsafe_allow_html=True)

# ── Chat messages ──
with st.container():
    if not st.session_state.messages:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-hero">🛍️</div>
          <div class="empty-title">Selamat datang!</div>
          <div class="empty-sub">
            Saya TokoBot, siap menjawab pertanyaan seputar belanja online Anda —
            dari pengiriman, pembayaran, hingga pengembalian barang.
          </div>
          <div class="quick-label">Coba tanyakan</div>
        </div>
        """, unsafe_allow_html=True)

        quick_qs = [
            "⏱ Berapa lama pengiriman?",
            "💳 Cara bayar pakai GoPay?",
            "🔄 Mau kembalikan barang",
            "🔑 Lupa password akun",
            "🎁 Ada promo voucher?",
            "📞 Hubungi customer service",
        ]
        cols = st.columns(3)
        for i, q in enumerate(quick_qs):
            with cols[i % 3]:
                if st.button(q, key=f"quick_{i}", use_container_width=True):
                    txt = q.split(' ', 1)[1] if ' ' in q else q
                    st.session_state.pending_query = txt
                    st.rerun()
    else:
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                st.markdown(f"""
                <div class="msg-user">
                  <div>
                    <div class="msg-bubble-user">{msg['content']}</div>
                    <div class="msg-time-user">{msg['time']}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                kat       = msg.get('kategori', '')
                kat_cls   = kategori_class(kat)
                score     = msg.get('score', 0)
                score_pct = min(int(score / 0.8 * 100), 100)
                score_col = '#2d9c8f' if score > 0.4 else ('#c8832a' if score > 0.2 else '#c0524a')
                is_found  = msg.get('found', False)
                extra_cls = '' if is_found else ' msg-bubble-fallback'
                badge_html  = f'<span class="kategori-badge {kat_cls}">{kat}</span><br>' if kat else ''
                answer_html = format_answer(msg['content'])

                score_bar = ''
                if is_found:
                    score_bar = f"""
                    <div class="score-bar">
                      <span>Confidence</span>
                      <div class="score-track">
                        <div class="score-fill" style="width:{score_pct}%;background:{score_col}"></div>
                      </div>
                      <span style="color:{score_col}">{score:.2f}</span>
                    </div>"""

                cand_html = ''
                if msg.get('candidates'):
                    items = ''.join([
                        f'<div style="font-size:0.77rem;color:#5b6f62;padding:4px 0;'
                        f'border-bottom:1px solid #d7e8dc;display:flex;align-items:center;gap:8px;">'
                        f'<span style="font-family:DM Mono,monospace;font-size:0.58rem;'
                        f'color:#8aa091;text-transform:uppercase;">{c["kategori"]}</span>'
                        f'<span style="color:#1f3327;">{c["question"]}</span></div>'
                        for c in msg['candidates']
                    ])
                    cand_html = f"""
                    <div class="related-wrap">
                      <div class="related-label">Mungkin juga ditanyakan</div>
                      {items}
                    </div>"""

                st.markdown(f"""
                <div class="msg-bot">
                  <div class="bot-avatar">🛍️</div>
                  <div>
                    <div class="msg-bubble-bot{extra_cls}">
                      {badge_html}{answer_html}{score_bar}{cand_html}
                    </div>
                    <div class="msg-time">{msg['time']}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                if msg.get('candidates') and msg == st.session_state.messages[-1]:
                    st.markdown(
                        "<div style='padding-left:46px;margin-top:6px;display:flex;flex-wrap:wrap;gap:6px;'>",
                        unsafe_allow_html=True
                    )
                    for ci, cand in enumerate(msg['candidates']):
                        if st.button(f"❓ {cand['question']}",
                                     key=f"cand_{ci}_{len(st.session_state.messages)}"):
                            st.session_state.pending_query = cand['question']
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

# ── Input area ──
st.markdown("<div class='input-wrapper'>", unsafe_allow_html=True)
input_col, btn_col = st.columns([10, 1])
with input_col:
    user_input = st.text_input(
        label="Chat Input",
        placeholder="Ketik pertanyaan Anda di sini...",
        key="chat_input",
        label_visibility="collapsed",
    )
with btn_col:
    send_btn = st.button("Kirim ↗", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PROCESS QUERY
# ─────────────────────────────────────────────
query = st.session_state.pending_query or (
    user_input.strip() if send_btn and user_input.strip() else None
)

last_user_msg = next(
    (m['content'] for m in reversed(st.session_state.messages) if m['role'] == 'user'), None
)

if query and query != last_user_msg:
    st.session_state.pending_query = None
    st.session_state.messages.append({'role': 'user', 'content': query, 'time': now_str()})

    result = get_answer(query)
    if result['found']:
        st.session_state.messages.append({
            'role': 'bot', 'content': result['answer'],
            'kategori': result['kategori'], 'score': result['score'],
            'found': True, 'candidates': result['candidates'], 'time': now_str(),
        })
    else:
        fallback = (
            "Maaf, saya tidak menemukan jawaban yang sesuai. 😔\n\n"
            "Coba:\n- Gunakan kata kunci yang lebih spesifik\n"
            "- Tanyakan dalam bahasa yang lebih sederhana\n\n"
            "Atau hubungi CS kami langsung:\n"
            "- 📱 **WhatsApp**: 0812-3456-7890 (08.00–21.00 WIB)\n"
            "- 📧 **Email**: support@tokoku.com"
        )
        st.session_state.messages.append({
            'role': 'bot', 'content': fallback,
            'kategori': '', 'score': result['score'],
            'found': False, 'candidates': [], 'time': now_str()
        })

    st.rerun()