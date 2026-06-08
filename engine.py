import re
import random


class NLPEngine:

    def __init__(self):

        # =============================================
        # DATABASE MATERI PYTHON
        # =============================================
        self.materi_data = {

            "variabel": {
                "emoji": "📦",
                "judul": "Variabel & Tipe Data",
                "isi": (
                    "**📦 Variabel** adalah tempat menyimpan data di memori.\n\n"
                    "```python\n"
                    "nama = 'Budi'       # String (teks)\n"
                    "umur = 12           # Integer (bilangan bulat)\n"
                    "nilai = 9.5         # Float (bilangan desimal)\n"
                    "lulus = True        # Boolean (benar/salah)\n"
                    "print(nama, umur)   # Output: Budi 12\n"
                    "```\n\n"
                    "💡 **Tips:** Nama variabel tidak boleh diawali angka dan tidak boleh ada spasi!"
                )
            },

            "kondisi": {
                "emoji": "🔀",
                "judul": "Kondisi (if/elif/else)",
                "isi": (
                    "**🔀 Kondisi** digunakan untuk membuat keputusan dalam program.\n\n"
                    "```python\n"
                    "nilai = 85\n\n"
                    "if nilai >= 90:\n"
                    "    print('Grade A')\n"
                    "elif nilai >= 75:\n"
                    "    print('Grade B')   # ini yang tercetak\n"
                    "elif nilai >= 60:\n"
                    "    print('Grade C')\n"
                    "else:\n"
                    "    print('Remedi')\n"
                    "```\n\n"
                    "💡 **Tips:** Perhatikan **indentasi** (spasi 4) — Python sangat sensitif terhadap ini!"
                )
            },

            "loop": {
                "emoji": "🔁",
                "judul": "Perulangan (for & while)",
                "isi": (
                    "**🔁 Loop** digunakan untuk mengulang perintah berkali-kali.\n\n"
                    "**For Loop** — untuk jumlah iterasi yang diketahui:\n"
                    "```python\n"
                    "for i in range(1, 6):\n"
                    "    print(f'Hitungan ke-{i}')\n"
                    "# Output: Hitungan ke-1, ke-2, ..., ke-5\n"
                    "```\n\n"
                    "**While Loop** — selama kondisi benar:\n"
                    "```python\n"
                    "angka = 1\n"
                    "while angka <= 3:\n"
                    "    print(angka)\n"
                    "    angka += 1\n"
                    "# Output: 1, 2, 3\n"
                    "```\n\n"
                    "💡 **Tips:** Hati-hati *infinite loop* — pastikan kondisi while bisa berhenti!"
                )
            },

            "fungsi": {
                "emoji": "⚙️",
                "judul": "Fungsi (def)",
                "isi": (
                    "**⚙️ Fungsi** adalah blok kode yang bisa dipanggil berulang kali.\n\n"
                    "```python\n"
                    "# Mendefinisikan fungsi\n"
                    "def sapa(nama, umur):\n"
                    "    pesan = f'Halo {nama}, kamu berumur {umur} tahun!'\n"
                    "    return pesan\n\n"
                    "# Memanggil fungsi\n"
                    "hasil = sapa('Ani', 13)\n"
                    "print(hasil)\n"
                    "# Output: Halo Ani, kamu berumur 13 tahun!\n"
                    "```\n\n"
                    "💡 **Tips:** Fungsi membuat kode lebih **rapi** dan bisa dipakai ulang!"
                )
            }
        }

        # =============================================
        # DATABASE SOAL KUIS PER TOPIK
        # =============================================
        self.quiz_bank = {

            "variabel": [
                {
                    "soal": "Apa output dari kode berikut?\n```python\nx = 5\ny = 3\nprint(x + y)\n```",
                    "pilihan": {"A": "53", "B": "8", "C": "x + y", "D": "Error"},
                    "jawaban": "B",
                    "penjelasan": "x + y = 5 + 3 = **8**. Python menjumlahkan dua integer."
                },
                {
                    "soal": "Tipe data apa yang digunakan untuk menyimpan teks seperti `nama = 'Budi'`?",
                    "pilihan": {"A": "Integer", "B": "Boolean", "C": "Float", "D": "String"},
                    "jawaban": "D",
                    "penjelasan": "Teks diapit tanda kutip adalah tipe **String**."
                },
                {
                    "soal": "Manakah penamaan variabel yang **benar** di Python?",
                    "pilihan": {"A": "1nilai = 90", "B": "nilai siswa = 90", "C": "nilai_siswa = 90", "D": "nilai-siswa = 90"},
                    "jawaban": "C",
                    "penjelasan": "Variabel tidak boleh diawali angka atau mengandung spasi/tanda minus. Gunakan **underscore (_)**."
                }
            ],

            "kondisi": [
                {
                    "soal": "Apa output dari kode ini?\n```python\nnilai = 70\nif nilai >= 75:\n    print('Lulus')\nelse:\n    print('Remedi')\n```",
                    "pilihan": {"A": "Lulus", "B": "Remedi", "C": "70", "D": "Error"},
                    "jawaban": "B",
                    "penjelasan": "70 < 75, jadi kondisi `if` salah dan program masuk ke blok `else` → **Remedi**."
                },
                {
                    "soal": "Keyword apa yang dipakai untuk kondisi 'jika tidak' di Python?",
                    "pilihan": {"A": "otherwise", "B": "elif", "C": "else", "D": "if not"},
                    "jawaban": "C",
                    "penjelasan": "**else** digunakan sebagai kondisi default jika semua kondisi `if/elif` tidak terpenuhi."
                },
                {
                    "soal": "Berapa nilai minimum agar mencetak 'A'?\n```python\nif nilai >= 90:\n    print('A')\n```",
                    "pilihan": {"A": "80", "B": "85", "C": "90", "D": "95"},
                    "jawaban": "C",
                    "penjelasan": "Operator `>=` artinya **lebih dari atau sama dengan**, jadi nilai minimum adalah **90**."
                }
            ],

            "loop": [
                {
                    "soal": "Berapa kali kata 'Halo' tercetak?\n```python\nfor i in range(4):\n    print('Halo')\n```",
                    "pilihan": {"A": "3", "B": "4", "C": "5", "D": "0"},
                    "jawaban": "B",
                    "penjelasan": "`range(4)` menghasilkan 0, 1, 2, 3 → **4 kali** iterasi."
                },
                {
                    "soal": "Apa output dari kode ini?\n```python\nfor i in range(2, 6, 2):\n    print(i)\n```",
                    "pilihan": {"A": "2 4", "B": "2 4 6", "C": "2 3 4 5", "D": "1 3 5"},
                    "jawaban": "A",
                    "penjelasan": "`range(2, 6, 2)` mulai dari 2, berhenti sebelum 6, lompat 2 → **2, 4**."
                },
                {
                    "soal": "Loop mana yang sebaiknya dipakai jika kita **tidak tahu** berapa kali harus mengulang?",
                    "pilihan": {"A": "for loop", "B": "while loop", "C": "do-while loop", "D": "if loop"},
                    "jawaban": "B",
                    "penjelasan": "**while loop** dipakai saat jumlah iterasi tidak diketahui, bergantung pada kondisi."
                }
            ],

            "fungsi": [
                {
                    "soal": "Keyword apa yang digunakan untuk **mendefinisikan** fungsi di Python?",
                    "pilihan": {"A": "function", "B": "func", "C": "def", "D": "define"},
                    "jawaban": "C",
                    "penjelasan": "Di Python, fungsi didefinisikan dengan keyword **def** diikuti nama fungsi."
                },
                {
                    "soal": "Apa output dari kode ini?\n```python\ndef tambah(a, b):\n    return a + b\n\nprint(tambah(3, 7))\n```",
                    "pilihan": {"A": "37", "B": "a + b", "C": "10", "D": "Error"},
                    "jawaban": "C",
                    "penjelasan": "Fungsi `tambah(3, 7)` mengembalikan 3 + 7 = **10**."
                },
                {
                    "soal": "Keyword apa yang digunakan untuk **mengembalikan nilai** dari sebuah fungsi?",
                    "pilihan": {"A": "output", "B": "return", "C": "print", "D": "send"},
                    "jawaban": "B",
                    "penjelasan": "**return** digunakan untuk mengembalikan nilai dari fungsi ke pemanggil."
                }
            ]
        }

        # =============================================
        # REGEX PATTERNS UNTUK INTENT DETECTION
        # =============================================

        # Pattern topik materi
        self.re_variabel = r"\b(variabel|variable|tipe data|tipedata|string|integer|float|boolean)\b"
        self.re_kondisi  = r"\b(kondisi|condition|if|elif|else|percabangan|seleksi)\b"
        self.re_loop     = r"\b(loop|perulangan|for|while|iterasi|ulang)\b"
        self.re_fungsi   = r"\b(fungsi|function|def|metode|method)\b"

        # Pattern intent umum
        self.re_belajar  = r"\b(belajar|pelajari|materi|ajar|jelaskan|explain|tunjukkan|show)\b"
        self.re_kuis     = r"\b(kuis|quiz|latihan|soal|tes|test|uji|ujian|coba)\b"
        self.re_menu     = r"\b(menu|mulai|start|halo|hai|hi|hello|apa saja|pilihan|daftar)\b"
        self.re_ya       = r"^(ya|yes|oke|ok|iya|siap|lanjut|next|bisa|boleh|tentu)$"
        self.re_tidak    = r"^(tidak|enggak|ga|gak|no|batal|stop|selesai|cukup|keluar|exit)$"
        self.re_jawaban  = r"^[abcdABCD]$"
        self.re_ulang    = r"\b(ulang|ulangi|lagi|again|reset|restart)\b"
        self.re_skor     = r"\b(skor|score|nilai|hasil|point)\b"

    # =============================================
    # INTENT DETECTION
    # =============================================
    def detect_intent(self, text):

        text_lower = text.lower().strip()

        if re.search(self.re_ulang, text_lower):
            return "ULANG"

        if re.search(self.re_menu, text_lower):
            return "MENU"

        if re.search(self.re_kuis, text_lower):
            topik = self._detect_topik(text_lower)
            return f"KUIS_{topik.upper()}" if topik else "KUIS"

        if re.search(self.re_belajar, text_lower):
            topik = self._detect_topik(text_lower)
            return f"BELAJAR_{topik.upper()}" if topik else "BELAJAR"

        topik = self._detect_topik(text_lower)
        if topik:
            return f"TOPIK_{topik.upper()}"

        if re.match(self.re_ya, text_lower):
            return "YA"

        if re.match(self.re_tidak, text_lower):
            return "TIDAK"

        if re.match(self.re_jawaban, text_lower):
            return f"JAWABAN_{text_lower.upper()}"

        if re.search(self.re_skor, text_lower):
            return "LIHAT_SKOR"

        return "UNKNOWN"

    def _detect_topik(self, text):
        """Mendeteksi topik materi dari teks input"""

        if re.search(self.re_variabel, text):
            return "variabel"
        if re.search(self.re_kondisi, text):
            return "kondisi"
        if re.search(self.re_loop, text):
            return "loop"
        if re.search(self.re_fungsi, text):
            return "fungsi"
        return None

    # =============================================
    # GETTER SOAL KUIS
    # =============================================
    def get_soal(self, topik, index):
        """Mengambil soal kuis berdasarkan topik dan index"""

        if topik in self.quiz_bank and index < len(self.quiz_bank[topik]):
            return self.quiz_bank[topik][index]
        return None

    def get_jumlah_soal(self, topik):
        """Mengembalikan jumlah soal untuk topik tertentu"""

        return len(self.quiz_bank.get(topik, []))

    def format_soal(self, soal_data, nomor):
        """Memformat soal menjadi teks yang rapi untuk ditampilkan"""

        teks = f"**Soal {nomor}:**\n\n{soal_data['soal']}\n\n"
        for huruf, opsi in soal_data['pilihan'].items():
            teks += f"**{huruf}.** {opsi}\n"
        teks += "\n_Ketik A, B, C, atau D untuk menjawab._"
        return teks

    def get_materi(self, topik):
        """Mengambil teks materi untuk topik tertentu"""

        return self.materi_data.get(topik, None)

    def get_semua_topik(self):
        """Mengembalikan list semua topik yang tersedia"""

        return list(self.materi_data.keys())
