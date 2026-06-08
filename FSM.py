from enum import Enum, auto
from engine import NLPEngine


# =============================================
# DEFINISI STATE FSM
# =============================================
class State(Enum):
    IDLE        = auto()   # Belum mulai, menunggu input pertama
    MENU        = auto()   # Menampilkan pilihan topik
    LEARNING    = auto()   # Sedang membaca materi
    QUIZ        = auto()   # Sedang mengerjakan kuis
    RESULT      = auto()   # Menampilkan hasil kuis


class PythonTutorFSM:

    def __init__(self):

        self.state   = State.IDLE
        self.nlp     = NLPEngine()
        self.response = ""

        # ── Status Belajar ──────────────────────────
        self.topik_aktif    = None   # Topik yang sedang dipelajari/dikuis
        self.materi_selesai = set()  # Topik yang sudah dipelajari

        # ── Status Kuis ────────────────────────────
        self.soal_index   = 0        # Nomor soal saat ini (0-based)
        self.skor         = 0        # Jumlah jawaban benar
        self.riwayat_kuis = []       # Riwayat semua kuis: [{topik, skor, total}]

    # =============================================
    # HELPER
    # =============================================
    def get_response(self):
        return self.response

    def _get_menu_text(self):
        """Membuat teks menu utama"""

        topik_list = self.nlp.get_semua_topik()
        teks = "📚 **Pilih topik yang ingin kamu pelajari atau kuis-kan:**\n\n"

        for topik in topik_list:
            data   = self.nlp.get_materi(topik)
            sudah  = "✅" if topik in self.materi_selesai else "🔵"
            teks  += f"{sudah} **{topik.capitalize()}** — {data['judul']}\n"

        teks += (
            "\n💬 **Cara pakai:**\n"
            "- Ketik `belajar variabel` → lihat materi\n"
            "- Ketik `kuis kondisi` → langsung kuis\n"
            "- Ketik nama topik saja juga bisa!\n"
            "\n_Tersedia: variabel · kondisi · loop · fungsi_"
        )
        return teks

    def _mulai_kuis(self, topik):
        """Reset state kuis dan tampilkan soal pertama"""

        self.topik_aktif = topik
        self.soal_index  = 0
        self.skor        = 0
        self.state       = State.QUIZ

        soal = self.nlp.get_soal(topik, 0)
        jumlah = self.nlp.get_jumlah_soal(topik)
        data_materi = self.nlp.get_materi(topik)

        self.response = (
            f"🎯 **Kuis {data_materi['emoji']} {data_materi['judul']}**\n"
            f"_{jumlah} soal · Ketik A, B, C, atau D_\n\n"
            "---\n\n"
            + self.nlp.format_soal(soal, 1)
        )

    def _proses_jawaban(self, huruf):
        """Memproses jawaban kuis dan lanjut ke soal berikutnya"""

        topik  = self.topik_aktif
        soal   = self.nlp.get_soal(topik, self.soal_index)
        benar  = soal["jawaban"]
        jumlah = self.nlp.get_jumlah_soal(topik)

        # Tentukan benar/salah
        if huruf == benar:
            self.skor += 1
            feedback = f"✅ **Benar!** {soal['penjelasan']}"
        else:
            feedback = f"❌ **Salah.** Jawaban yang benar: **{benar}**\n💡 {soal['penjelasan']}"

        self.soal_index += 1

        # Masih ada soal berikutnya?
        if self.soal_index < jumlah:
            soal_berikut = self.nlp.get_soal(topik, self.soal_index)
            self.response = (
                feedback + "\n\n---\n\n"
                + self.nlp.format_soal(soal_berikut, self.soal_index + 1)
            )
        else:
            # Kuis selesai → ke state RESULT
            self.riwayat_kuis.append({
                "topik": topik,
                "skor": self.skor,
                "total": jumlah
            })
            self.state = State.RESULT
            self._tampilkan_hasil(feedback)

    def _tampilkan_hasil(self, feedback_terakhir=""):
        """Membuat ringkasan hasil kuis"""

        topik   = self.topik_aktif
        jumlah  = self.nlp.get_jumlah_soal(topik)
        persen  = round((self.skor / jumlah) * 100)
        data_m  = self.nlp.get_materi(topik)

        # Pesan motivasi berdasarkan skor
        if persen == 100:
            motivasi = "🏆 **Sempurna! Kamu luar biasa!**"
            bintang  = "⭐⭐⭐"
        elif persen >= 67:
            motivasi = "👍 **Bagus! Tinggal sedikit lagi menuju sempurna!**"
            bintang  = "⭐⭐"
        else:
            motivasi = "💪 **Jangan menyerah! Pelajari materinya lagi, pasti bisa!**"
            bintang  = "⭐"

        self.response = (
            (feedback_terakhir + "\n\n---\n\n" if feedback_terakhir else "")
            + f"## 🎉 Kuis Selesai!\n\n"
            + f"**Topik:** {data_m['emoji']} {data_m['judul']}\n"
            + f"**Skor:** {self.skor} / {jumlah} ({persen}%) {bintang}\n\n"
            + motivasi + "\n\n"
            + "---\n"
            + "**Mau apa selanjutnya?**\n"
            + "- Ketik `ulang` untuk kuis topik ini lagi\n"
            + "- Ketik `menu` untuk pilih topik lain\n"
            + "- Ketik `belajar " + topik + "` untuk review materi"
        )

    def get_skor_text(self):
        """Mengembalikan ringkasan semua riwayat kuis"""

        if not self.riwayat_kuis:
            return "Kamu belum mengerjakan kuis apapun. Ketik `menu` untuk memulai!"

        teks = "📊 **Riwayat Kuis Kamu:**\n\n"
        for r in self.riwayat_kuis:
            persen = round((r['skor'] / r['total']) * 100)
            data_m = self.nlp.get_materi(r['topik'])
            teks  += f"{data_m['emoji']} **{r['topik'].capitalize()}**: {r['skor']}/{r['total']} ({persen}%)\n"

        return teks

    # =============================================
    # STEP — TRANSISI UTAMA FSM
    # =============================================
    def step(self, user_input):

        user_input = user_input.strip()
        intent     = self.nlp.detect_intent(user_input)

        # ── INTENT GLOBAL (berlaku di semua state) ──
        if intent == "ULANG":
            if self.topik_aktif:
                self._mulai_kuis(self.topik_aktif)
            else:
                self.state    = State.MENU
                self.response = self._get_menu_text()
            return

        if intent == "MENU":
            self.state    = State.MENU
            self.response = self._get_menu_text()
            return

        if intent == "LIHAT_SKOR":
            self.response = self.get_skor_text()
            return

        # ── STATE: IDLE ──────────────────────────────
        if self.state == State.IDLE:

            self.state    = State.MENU
            self.response = (
                "👋 **Halo! Selamat datang di PyTutor — Belajar Python Itu Seru!**\n\n"
                "Aku adalah asisten belajar Python untuk kamu yang baru mulai. "
                "Di sini kamu bisa **membaca materi** dan **mengerjakan kuis** interaktif.\n\n"
                + self._get_menu_text()
            )

        # ── STATE: MENU ──────────────────────────────
        elif self.state == State.MENU:

            # Minta belajar topik tertentu
            if intent.startswith("BELAJAR_") or intent.startswith("TOPIK_"):
                topik = intent.split("_", 1)[1].lower()
                materi = self.nlp.get_materi(topik)

                if materi:
                    self.topik_aktif = topik
                    self.materi_selesai.add(topik)
                    self.state = State.LEARNING
                    self.response = (
                        f"## {materi['emoji']} {materi['judul']}\n\n"
                        + materi['isi']
                        + "\n\n---\n\n"
                        "✅ Materi selesai! **Mau langsung kuis?** (Ketik `ya` / `kuis` / `menu`)"
                    )
                else:
                    self.response = "Topik tidak ditemukan. " + self._get_menu_text()

            # Minta kuis topik tertentu
            elif intent.startswith("KUIS_"):
                topik = intent.split("_", 1)[1].lower()
                if self.nlp.get_soal(topik, 0):
                    self._mulai_kuis(topik)
                else:
                    self.response = "Topik kuis tidak ditemukan. " + self._get_menu_text()

            # Minta kuis tanpa topik
            elif intent == "KUIS":
                self.response = (
                    "📝 Kuis topik apa yang ingin kamu coba?\n\n"
                    "_Contoh: `kuis variabel`, `kuis loop`, `kuis kondisi`, `kuis fungsi`_"
                )

            else:
                self.response = (
                    "Hmm, aku kurang paham 🤔\n\n"
                    + self._get_menu_text()
                )

        # ── STATE: LEARNING ──────────────────────────
        elif self.state == State.LEARNING:

            if intent == "YA" or intent.startswith("KUIS"):
                topik = self.topik_aktif

                # Jika kuis dengan topik spesifik
                if intent.startswith("KUIS_"):
                    topik = intent.split("_", 1)[1].lower()

                if topik and self.nlp.get_soal(topik, 0):
                    self._mulai_kuis(topik)
                else:
                    self.response = "Topik tidak valid. " + self._get_menu_text()

            elif intent == "TIDAK":
                self.state    = State.MENU
                self.response = "Oke! " + self._get_menu_text()

            elif intent.startswith("BELAJAR_") or intent.startswith("TOPIK_"):
                # Pindah ke topik materi lain
                topik  = intent.split("_", 1)[1].lower()
                materi = self.nlp.get_materi(topik)

                if materi:
                    self.topik_aktif = topik
                    self.materi_selesai.add(topik)
                    self.response = (
                        f"## {materi['emoji']} {materi['judul']}\n\n"
                        + materi['isi']
                        + "\n\n---\n\n"
                        "✅ Materi selesai! **Mau langsung kuis?** (Ketik `ya` / `kuis` / `menu`)"
                    )
                else:
                    self.response = "Topik tidak ditemukan. " + self._get_menu_text()

            else:
                self.response = (
                    "Kamu sedang membaca materi. "
                    "Ketik **`ya`** untuk lanjut kuis, atau **`menu`** untuk kembali ke daftar topik."
                )

        # ── STATE: QUIZ ──────────────────────────────
        elif self.state == State.QUIZ:

            if intent.startswith("JAWABAN_"):
                huruf = intent.split("_")[1]
                self._proses_jawaban(huruf)

            elif intent == "TIDAK" or intent == "MENU":
                self.state    = State.MENU
                self.response = (
                    "⚠️ Kuis dibatalkan. Progres tidak disimpan.\n\n"
                    + self._get_menu_text()
                )

            else:
                self.response = "⌨️ Jawab dengan mengetik **A**, **B**, **C**, atau **D** ya!"

        # ── STATE: RESULT ─────────────────────────────
        elif self.state == State.RESULT:

            if intent == "ULANG":
                self._mulai_kuis(self.topik_aktif)

            elif intent.startswith("BELAJAR_") or intent.startswith("TOPIK_"):
                topik  = intent.split("_", 1)[1].lower()
                materi = self.nlp.get_materi(topik)

                if materi:
                    self.topik_aktif = topik
                    self.materi_selesai.add(topik)
                    self.state = State.LEARNING
                    self.response = (
                        f"## {materi['emoji']} {materi['judul']}\n\n"
                        + materi['isi']
                        + "\n\n---\n\n"
                        "✅ Materi selesai! **Mau langsung kuis?** (Ketik `ya` / `kuis` / `menu`)"
                    )
                else:
                    self.state    = State.MENU
                    self.response = self._get_menu_text()

            else:
                self.state    = State.MENU
                self.response = self._get_menu_text()
