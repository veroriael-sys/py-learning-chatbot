import streamlit as st
from FSM import PythonTutorFSM, State

# =============================================
# KONFIGURASI HALAMAN
# =============================================
st.set_page_config(
    page_title="PyTutor — Belajar Python",
    page_icon="🐍",
    layout="wide"
)

# =============================================
# CSS KUSTOM
# =============================================
st.markdown("""
<style>
/* Warna dasar */
:root {
    --biru-tua: #1a1f36;
    --biru-muda: #3b82f6;
    --hijau: #22c55e;
    --kuning: #facc15;
    --merah: #ef4444;
    --abu: #f1f5f9;
}

/* Kartu info samping */
.stMetric {
    background-color: #f8fafc;
    padding: 14px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

/* Badge state */
.badge-state {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* Chat bubble */
.stChatMessage {
    padding: 8px 0;
}
</style>
""", unsafe_allow_html=True)

# =============================================
# INISIALISASI SESSION STATE
# =============================================
if 'bot' not in st.session_state:
    st.session_state.bot = PythonTutorFSM()
    st.session_state.bot.step("")          # Trigger state IDLE → MENU
    st.session_state.history = [
        {
            "role": "assistant",
            "content": st.session_state.bot.get_response()
        }
    ]

# Shorthand
bot = st.session_state.bot

# =============================================
# HEADER UTAMA
# =============================================
st.title("🐍 PyTutor — Belajar Python Itu Seru!")
st.markdown("_Asisten belajar Python interaktif untuk siswa SD, SMP, dan SMA._")
st.markdown("---")

# =============================================
# LAYOUT UTAMA: TABS
# =============================================
tab1, tab2 = st.tabs(["💬 Chat Belajar", "📖 Daftar Materi"])

# =============================================
# TAB 1: CHAT
# =============================================
with tab1:

    col_chat, col_info = st.columns([2, 1])

    # ── KOLOM KANAN: INFO & PROGRESS ──────────
    with col_info:

        st.subheader("📊 Progres Belajar")

        # Tampilkan status state FSM
        state_labels = {
            State.IDLE:         ("⚪", "Belum mulai"),
            State.MENU:         ("🔵", "Memilih topik"),
            State.LEARNING:     ("📘", "Membaca materi"),
            State.QUIZ:         ("📝", "Mengerjakan kuis"),
            State.RESULT:       ("🏆", "Melihat hasil"),
        }
        ikon, label = state_labels.get(bot.state, ("❓", "Unknown"))
        st.caption(f"Status: {ikon} **{label}**")
        st.markdown("")

        # Progress topik yang sudah dipelajari
        semua_topik = bot.nlp.get_semua_topik()
        sudah = len(bot.materi_selesai)
        total = len(semua_topik)

        st.metric(label="Materi Dibaca", value=f"{sudah} / {total} Topik")
        st.progress(sudah / total if total > 0 else 0)

        st.markdown("")

        # Checklist per topik
        st.markdown("**Topik:**")
        for topik in semua_topik:
            data = bot.nlp.get_materi(topik)
            cek = "✅" if topik in bot.materi_selesai else "⬜"
            st.markdown(f"{cek} {data['emoji']} {topik.capitalize()}")

        st.markdown("---")

        # Riwayat kuis
        if bot.riwayat_kuis:
            st.markdown("**Riwayat Kuis:**")
            for r in bot.riwayat_kuis:
                persen = round((r['skor'] / r['total']) * 100)
                data_m = bot.nlp.get_materi(r['topik'])
                warna = "🟢" if persen >= 67 else "🔴"
                st.caption(f"{warna} {data_m['emoji']} {r['topik'].capitalize()}: {r['skor']}/{r['total']} ({persen}%)")
        else:
            st.caption("Belum ada riwayat kuis.")

        st.markdown("---")

        # Tombol reset
        if st.button("🔄 Reset Sistem", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # ── KOLOM KIRI: CHAT ──────────────────────
    with col_chat:

        # Container chat dengan scroll
        chat_container = st.container(height=520)

        with chat_container:
            for msg in st.session_state.history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        # Placeholder input sesuai state
        placeholder_map = {
            State.IDLE:         "Ketik apa saja untuk mulai...",
            State.MENU:         "Contoh: belajar variabel  |  kuis loop",
            State.LEARNING:     "Ketik 'ya' untuk kuis, 'menu' untuk kembali",
            State.QUIZ:         "Jawab dengan: A / B / C / D",
            State.RESULT:       "Ketik 'ulang', 'menu', atau topik berikutnya",
        }
        placeholder = placeholder_map.get(bot.state, "Ketik pesan...")

        # Input user
        if prompt := st.chat_input(placeholder):

            # 1. Simpan & tampilkan pesan user
            st.session_state.history.append({
                "role": "user",
                "content": prompt
            })

            # 2. Proses melalui FSM
            bot.step(prompt)
            bot_reply = bot.get_response()

            # 3. Simpan respons bot
            st.session_state.history.append({
                "role": "assistant",
                "content": bot_reply
            })

            # 4. Rerun untuk update UI
            st.rerun()

# =============================================
# TAB 2: DAFTAR MATERI (REFERENSI)
# =============================================
with tab2:

    st.header("📖 Daftar Materi Python")
    st.markdown("Klik nama topik di chat untuk belajar. Berikut ringkasan semua materi yang tersedia.")
    st.markdown("")

    # Grid 2 kolom untuk kartu materi
    cols = st.columns(2)

    for idx, topik in enumerate(bot.nlp.get_semua_topik()):
        data = bot.nlp.get_materi(topik)
        sudah = topik in bot.materi_selesai

        with cols[idx % 2]:

            jumlah_soal = bot.nlp.get_jumlah_soal(topik)

            # Badge sudah/belum
            badge = "✅ Sudah dibaca" if sudah else "🔵 Belum dibaca"

            st.markdown(f"### {data['emoji']} {data['judul']}")
            st.caption(badge)
            st.markdown(data['isi'])
            st.caption(f"📝 {jumlah_soal} soal kuis tersedia")
            st.markdown("---")

# =============================================
# FOOTER
# =============================================
st.markdown("")
st.markdown(
    "<div style='text-align:center; color:#94a3b8; font-size:13px;'>"
    "🐍 PyTutor · Kelompok Pendidikan · Teori Bahasa dan Otomata"
    "</div>",
    unsafe_allow_html=True
)
