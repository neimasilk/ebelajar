# -*- coding: utf-8 -*-
"""Deck Pertemuan 3 - Natural Language Processing, kelas A (luring).

SUMBER (folder Drive "pertemuan 3" NLP, id 14fspLWwgKmTOxrJnNs7d01-isrnW7oxY):
  - Modul Mandiri P3 (PDF) "Stemming & Lemmatization (Tanpa spaCy)" - tujuan,
    peta kegiatan 120', materi inti, langkah praktikum 1-9, penugasan A/B/C,
    rubrik 45/35/20, format & reproducibility, etika data, referensi.
  - Modul Mandiri P3 (PDF) versi awal "(stemming & Lemmatization) - NLP".
  - LKS Colab: NLP_Pertemuan_3_Stemming_Lemmatization.ipynb
  - Video "Membedah Stemming vs ..."  +  "video presentasi pertemuan 3".

Slide #2 = Laporan feedback mingguan (ritual Senin). Angka diambil dari
eBelajar 21 Sep 2026 siang (siap kelas 22 Sep): exit-ticket P2 diisi 2/3
(Bahrum 88, Rudolph 90 - Rudolph mengisi Minggu 20 Sep malam), diskusi P1
2/3 posting (keduanya 88 dan sudah dibalas), Tugas 1 terkumpul 1/3
(Bahrum, Kamis 17 Sep 00.49 - DINILAI 78 dengan catatan revisi: langkah
wajib tokenisasi KALIMAT hilang, placeholder kesimpulan belum diisi,
analisis pindah ke markdown), Perkenalan masih 0/3 (d=10667 cuma seed
dosen). Kelas Selasa 22 Sep 08.00.

Catatan penting: P2 mengajarkan spaCy, P3 justru TIDAK memakainya - modul
memilih Sastrawi (stemming BI) + NLTK WordNet (lemmatization EN) karena
lemmatizer Bahasa Indonesia yang stabil belum umum tersedia. Deck ini
menjelaskan alasan itu supaya pergantian alat tidak terasa sewenang-wenang.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deckkit import *

OUT = r"D:\documents\ebelajar\ganjil-2026-2027\nlp"
B = "https://ebelajar.stiki.ac.id"

# -- cmid NLP A (course 7226; sweep 18 Sep 2026) --
COURSE     = 7226
MATERI2    = 491785
TUGAS1     = 491786
FORUM_P2   = 501186
BAHAN2     = 501187
PERKENALAN = 491778
UMUM       = 491776

# -- Drive "pertemuan 3" NLP --
FOLDER_P3 = "https://drive.google.com/drive/folders/14fspLWwgKmTOxrJnNs7d01-isrnW7oxY"
MODUL_P3  = "https://drive.google.com/file/d/1kjHjfnYXyVu4eY7CBaEfSb-suNmqOKex/view"
MODUL_P3B = "https://drive.google.com/file/d/1LSTStAfQPramQHzzM0gWOL9cRUdEUiJV/view"
LKS_P3    = "https://colab.research.google.com/drive/1BzpZ4VtrCF6YCAEw5w2RIfbufdKKKLh3"
VIDEO_1   = "https://drive.google.com/file/d/1r02JuqTgE7yyo-J7ni7qc-55WnNr9Ist/view"
VIDEO_2   = "https://drive.google.com/file/d/1ogalNavSXje3TIPepCPjynBCRtZFrAPW/view"


def build():
    prs = new_deck()

    title_slide(prs, "PERTEMUAN 3 - NATURAL LANGUAGE PROCESSING",
                "Stemming & Lemmatization",
                "Normalisasi morfologi: memangkas bentuk permukaan tanpa ikut membuang makna",
                "Mukhlis Amien, M.Kom.  ·  IF24KK64  ·  Kelas A (Reguler) · Selasa 08.00-10.30 · A.2.1")

    # ============ RITUAL: FEEDBACK MINGGUAN ============
    table_slide(prs, "Laporan feedback - Minggu 2 (14-20 Sep)",
                ["Yang saya periksa", "Hasil per 21 September"],
                [["*Exit-ticket P2", "*2 dari 3 mengisi - Bahrum 88, Rudolph 90 (Minggu 20 Sep). Keduanya dibalas"],
                 ["*Diskusi P1", "*2 dari 3 posting - Bahrum 88, Rudolph 88. Keduanya dibalas"],
                 ["*Tugas 1", "*Terkumpul 1 dari 3 (Bahrum) - SUDAH DINILAI 78 dengan catatan revisi. Tenggat 27 Sep, sisa 6 hari"],
                 ["*Perkenalan", "*Masih 0 dari 3 - forum tetap dibuka, tetap dinilai"],
                 ["*Blokir kumpul", "*Sudah dibuka 15 Sep (setelan warisan 2025); kalau masih gagal, lapor hari ini"]],
                col_w=[4, 8], fs=17,
                sub="Kelas 3 orang: tidak ada yang tidak terlihat. Angka ini diambil langsung dari eBelajar, bukan perkiraan.",
                note="Rudolph bangkit: awalnya diam, kini mengisi exit P2 (Minggu malam, jawaban "
                     "level lanjut) dan P1 - dua-duanya dibalas dan dinilai. Hafiz belum muncul "
                     "sama sekali: nol posting, nol submission - sapa langsung hari ini. Bahrum "
                     "sudah kerja semua. Forum exit-ticket tidak punya tenggat mati; yang punya "
                     "tenggat mati: Tugas 1, 27 Sep.")

    table_slide(prs, "Tabulasi nilai s.d. pagi ini (21 Sep)",
                ["Mahasiswa", "Forum P1", "Exit P2", "Tugas 1"],
                [["Bahrum Rumbalifar", "*88", "*88", "*78"],
                 ["Rudolph Gaspersz", "*88", "*90", "-"],
                 ["Hafizh Habibulloh", "-", "-", "-"]],
                col_w=[4.6, 2.4, 2.4, 2.6], fs=16,
                sub="Sumber: rating forum + grade Tugas 1 di eBelajar, dibaca pagi ini. Perkenalan: belum ada yang mengisi. Kosong = masih bisa dikejar - Tugas 1 tenggat 27 Sep.",
                note="Tiga orang, jadi tabulasinya kecil tapi personal. Sebut dua hal: (1) Tugas 1 "
                     "Bahrum 78 punya catatan revisi konkret di kolom komentar tugas - tunjukkan "
                     "CARA melihat komentar itu di layar; (2) Rudolph dan Hafiz masih bisa "
                     "mengumpulkan sampai Minggu 27 Sep 23.55.")

    statement_slide(prs, "Tugas 1: 1 dari 3.\nEnam hari lagi.",
                    "Bahrum sudah mengumpulkan dan sudah menerima nilai plus catatan revisi. Rudolph, "
                    "Hafiz: tenggat Minggu 27 Sep 23.55 - dan langkah nomor satu (tokenisasi kalimat) "
                    "adalah langkah yang paling sering terlewat. Kalau macet, tulis di forum Diskusi "
                    "Umum hari ini; jangan menunggu tanggal 26.",
                    note="Kelas 3 orang - ini bukan peringatan massal, ini pesan personal ke dua orang "
                         "di ruangan. Ucapkan nama mereka.")

    content_slide(prs, "Jawaban exit-ticket P2 yang jadi pintu masuk hari ini",
                  ["Bahrum menjawab benar ketiganya. Dua hal darinya langsung menyambung ke materi P3:",
                   (1, "*\"Menghapus 'tidak' membalik sentimen 180 derajat\"* - benar. Membuang stopword = membuang informasi"),
                   (1, "*\"spaCy memberi lemma dan POS dalam satu langkah\"* - hampir benar, dan koreksinya penting"),
                   "__",
                   "**Koreksinya:** tokenizer spaCy juga berbasis aturan. Lemma dan POS diisi oleh komponen "
                   "**berikutnya** dalam pipeline (tagger, lemmatizer) - bukan oleh tokenisasi.",
                   "Hari ini kita bongkar komponen itu satu per satu, dan kita kerjakan **tanpa spaCy**."],
                  sub="Pola yang berulang: setiap langkah normalisasi membuang sesuatu. Pertanyaannya selalu - apa yang boleh hilang?",
                  note="Ini jembatan naratif dari P2 ke P3. Poin besarnya: di P2 kita belajar "
                       "membuang stopwords bisa merusak negasi. Di P3 kita belajar memangkas "
                       "imbuhan bisa merusak aspek/intensitas. Prinsipnya sama, korbannya beda. "
                       "Pembanding: Rudolph juga mengisi exit P2 Minggu malam dan jawaban nomor "
                       "1-nya menyentuh negasi yang tersembunyi di daftar stopwords - level lanjut.")

    content_slide(prs, "Alur 150 menit hari ini",
                  ["**Hook** - satu kata, lima bentuk: kenapa kosakata meledak · 10'",
                   "**Mini-lecture** - stemming vs lemmatization, dan kenapa BI tidak punya lemmatizer · 25'",
                   "**Praktikum 1** - Sastrawi: stemming Bahasa Indonesia · 35'",
                   "**Praktikum 2** - NLTK WordNet + POS tagger: lemmatization Inggris · 35'",
                   "**Eksperimen** - ukur ukuran kosakata sebelum vs sesudah, susun tabel komparasi · 25'",
                   "**Rangkuman** + penugasan + exit-ticket + pratinjau P4 · 20'"],
                  sub="Angka = menit. Modul mandiri versinya 120 menit; 30 menit tambahan hari ini dipakai untuk eksperimen bersama dan diskusi.")

    # ============ HOOK ============
    section_slide(prs, "HOOK", "Satu kata,\nlima bentuk",
                  "Dan mesin menghitungnya sebagai lima kata yang berbeda")

    statement_slide(prs, "membaca, dibaca, bacaan,\nmembacakan, terbaca.",
                    "Bagi manusia: satu keluarga kata. Bagi program yang baru saja Anda tulis di Pertemuan 2: "
                    "lima token berbeda, lima kolom berbeda, lima hitungan terpisah. "
                    "Kosakata membengkak, dan setiap bentuk hanya dilihat sedikit contoh.",
                    note="Tulis kelimanya di papan. Tanya: menurut Anda apakah ini masalah? "
                        "Jawabannya: tergantung tugas. Untuk klasifikasi topik - masalah "
                        "(data terpecah). Untuk analisis gaya penulisan - justru sinyal. "
                        "Jangan buru-buru bilang normalisasi selalu baik.")

    content_slide(prs, "Capaian pertemuan ini (sesuai modul mandiri P3)",
                  ["Melakukan **stemming Bahasa Indonesia** (Sastrawi) dan **lemmatization Inggris** "
                   "(NLTK WordNet) dengan pustaka open-source yang sesuai",
                   "Menganalisis **dampak normalisasi morfologi terhadap ukuran kosakata**, dan implikasinya "
                   "terhadap fitur - langsung menuju BoW/TF-IDF di Pertemuan 4",
                   "Menyusun **tabel komparasi** dan ringkasan: kapan memilih stemming, kapan lemmatization"],
                  sub="Tiga capaian ini persis yang dinilai rubrik: Notebook & Kode 45% · Tabel Komparasi 35% · Ringkasan Analisis 20%.")

    content_slide(prs, "Bahan belajar mandiri di Drive - pertemuan 3",
                  ["**Modul Mandiri P3 (PDF)** - *Stemming & Lemmatization (Tanpa spaCy)*, estimasi 120 menit",
                   "**LKS Colab** - `NLP_Pertemuan_3_Stemming_Lemmatization.ipynb`, starter notebook siap jalan",
                   "Video **Membedah Stemming vs Lemmatization**",
                   "Video **presentasi pertemuan 3**",
                   "__",
                   "Berbeda dari Pertemuan 2: folder P3 **punya LKS notebook**. Buka dari Drive, "
                   "*Save a copy in Drive* dulu sebelum mengedit."],
                  sub="Tautan lengkap ada di slide terakhir. eBelajar hanya menautkan - satu salinan tunggal di Drive.",
                  note="Ingatkan: LKS di Colab bersifat read-only kalau dibuka langsung. Harus "
                       "File > Save a copy in Drive, kalau tidak pekerjaannya hilang.")

    # ============ BAGIAN 1 - KONSEP ============
    section_slide(prs, "BAGIAN 1", "Stemming vs\nLemmatization",
                  "Dua cara mengecilkan kosakata - dan keduanya membuang sesuatu")

    table_slide(prs, "Dua pendekatan, satu tujuan",
                ["", "Stemming", "Lemmatization"],
                [["Cara kerja", "Heuristik / aturan morfologi - potong imbuhan", "Cari lemma di kamus - butuh analisis kata"],
                 ["Hasil", "Stem: belum tentu kata yang sah", "Lemma: selalu kata kamus yang sah"],
                 ["Butuh POS?", "Tidak", "Ya - hasil berubah menurut kelas kata"],
                 ["Kecepatan", "Cepat", "Lebih lambat (lookup + tagging)"],
                 ["Alat hari ini", "Sastrawi (Bahasa Indonesia)", "NLTK WordNetLemmatizer (Inggris)"]],
                col_w=[3, 5, 5], fs=16,
                sub="Perbedaan praktisnya: stemming berani salah demi cepat; lemmatization berhati-hati tapi menuntut informasi tambahan.",
                note="Contoh klasik: 'studies' -> stem 'studi' (bukan kata Inggris) tapi lemma "
                     "'study'. Sebaliknya 'better' -> stem tetap 'better', lemma (adjektiva) "
                     "'good'. Lemmatization bisa melompat ke bentuk yang sama sekali beda.")

    content_slide(prs, "Kenapa Bahasa Indonesia hanya dapat stemming?",
                  ["Modul menyatakannya terang-terangan: **lemmatization Bahasa Indonesia yang stabil belum umum tersedia**",
                   "Yang ada dan matang: **Sastrawi**, implementasi algoritma **Nazief-Adriani** - berbasis aturan imbuhan + kamus kata dasar",
                   "Akibatnya di modul ini: **BI pakai stemming, EN pakai lemmatization**",
                   "Ini bukan sekadar keterbatasan teknis - ini **fakta lapangan tentang bahasa berkekurangan sumber daya**",
                   (1, "bahasa dengan morfologi kaya + sumber daya terbatas = alat NLP-nya tertinggal"),
                   (1, "itu juga alasan hasil riset NLP Bahasa Indonesia masih terbuka lebar")],
                  sub="Kalau nanti Anda mencari topik tugas akhir: celah ini nyata, dan bisa diukur.",
                  note="Kesempatan menyisipkan motivasi riset. Sastrawi = Nazief-Adriani, "
                       "dipublikasikan 1996, masih jadi standar de facto sampai sekarang. "
                       "Itu sendiri sudah menunjukkan betapa lambatnya perkembangan alat BI.")

    content_slide(prs, "Kenapa P3 tidak memakai spaCy (padahal P2 memakainya)",
                  ["Judul modulnya eksplisit: **\"Tanpa spaCy\"** - dan itu keputusan yang disengaja",
                   "spaCy memang punya lemmatizer, tapi kualitasnya untuk Bahasa Indonesia **tidak setara** "
                   "dengan Sastrawi yang dirancang khusus untuk morfologi BI",
                   "Untuk Inggris, **NLTK WordNet** memberi kendali yang lebih eksplisit: Anda melihat "
                   "POS-nya, Anda yang memetakan - bukan tersembunyi di dalam pipeline",
                   "__",
                   "**Pelajaran alat:** pilih pustaka menurut bahasa dan menurut seberapa banyak kendali "
                   "yang Anda butuhkan - bukan menurut mana yang paling populer."],
                  note="Jawab langsung kalau ditanya 'kenapa ganti alat lagi'. Poinnya bukan "
                       "spaCy jelek; poinnya setiap alat punya cakupan bahasa yang berbeda, dan "
                       "menyerahkan semuanya ke satu pustaka adalah kebiasaan buruk.")

    content_slide(prs, "Yang hilang saat normalisasi - dan kapan itu berbahaya",
                  ["**berlari-lari -> lari**: reduplikasi hilang, padahal ia membawa makna *berulang/terus-menerus*",
                   "**membacakan -> baca**: sufiks -kan hilang, padahal ia menandai *untuk orang lain*",
                   "**terpukul -> pukul**: prefiks ter- hilang, padahal ia menandai *tidak sengaja / pasif*",
                   "__",
                   "Aturan praktis yang bisa Anda pegang:",
                   (1, "tugas soal **TOPIK** (klasifikasi, pencarian, klaster) -> normalisasi biasanya menolong"),
                   (1, "tugas soal **MAKNA HALUS atau GAYA** (sentimen bernuansa, atribusi penulis, generasi teks) -> hati-hati"),
                   (1, "kalau ragu: **ukur**, jangan tebak - bandingkan metrik dengan dan tanpa normalisasi")],
                  sub="Persis pola yang sama dengan stopwords di Pertemuan 2. Yang berubah cuma jenis informasi yang dikorbankan.",
                  note="Hubungkan eksplisit ke jawaban Bahrum tentang negasi. P2: yang hilang = "
                       "negasi. P3: yang hilang = aspek, kesengajaan, arah perbuatan. Prinsip "
                       "besarnya identik - setiap pra-proses adalah keputusan bertrade-off.")

    content_slide(prs, "Uji cepat 1 - tebak dulu, baru jalankan",
                  ["Empat kata Bahasa Indonesia:",
                   (1, "*mempermainkan · berlari-lari · keadilan · pembelajaran*"),
                   "Dua kata Inggris (dengan POS-nya):",
                   (1, "*studies* (kata kerja) · *better* (kata sifat)"),
                   "__",
                   "Tulis tebakan Anda di kertas: apa hasil stem / lemma masing-masing?",
                   "Kita jalankan sebentar lagi. Yang menarik bukan yang benar - **yang meleset**."],
                  sub="2 menit. Tebakan yang salah adalah bahan diskusi terbaik di sesi ini.",
                  note="Kunci: mempermainkan->main, berlari-lari->lari, keadilan->adil, "
                       "pembelajaran->ajar. studies(v)->study, better(a)->good. "
                       "Yang paling sering meleset: 'better'->'good' (lompatan leksikal, bukan "
                       "pemotongan) dan 'pembelajaran'->'ajar' (dua imbuhan sekaligus).")

    # ============ BAGIAN 2 - PRAKTIKUM BI ============
    section_slide(prs, "BAGIAN 2 - PRAKTIKUM 1", "Stemming Bahasa Indonesia\ndengan Sastrawi",
                  "Modul langkah 1-5 - jalankan sambil saya demo")

    code_slide(prs, "Persiapan lingkungan (modul bagian 2)",
               ["!pip install sastrawi nltk pandas matplotlib",
                "",
                "import nltk",
                "for pkg in ['punkt', 'stopwords', 'wordnet', 'omw-1.4',",
                "            'averaged_perceptron_tagger']:",
                "    nltk.download(pkg)"],
               caption="Lima resource NLTK. Lupa satu saja -> LookupError di tengah praktikum. Jalankan sel ini paling awal.",
               note="omw-1.4 = Open Multilingual WordNet, sering terlupa dan menyebabkan "
                    "error yang membingungkan saat lemmatize. averaged_perceptron_tagger "
                    "dipakai pos_tag di Praktikum 2.")

    code_slide(prs, "Sastrawi - stemming Bahasa Indonesia",
               ["from Sastrawi.Stemmer.StemmerFactory import StemmerFactory",
                "from nltk.tokenize import word_tokenize",
                "",
                "stemmer = StemmerFactory().create_stemmer()",
                "",
                "teks_id = \"Mereka mempermainkan keadilan dan berlari-lari\"",
                "          \" menghindari pembelajaran.\"",
                "",
                "tokens = [t.lower() for t in word_tokenize(teks_id) if t.isalnum()]",
                "stems  = [stemmer.stem(t) for t in tokens]",
                "",
                "for a, b in zip(tokens, stems):",
                "    print(f'{a:20s} -> {b}')"],
               caption="Normalisasi dulu (lowercase + buang token non-alfanumerik), baru stemming - urutan ini penting.",
               note="Tunjukkan hasil live dan bandingkan dengan tebakan di Uji Cepat 1. "
                    "Perhatikan: stemmer.stem() menerima STRING, bisa juga seluruh kalimat "
                    "sekaligus - tapi per-token lebih mudah dibaca untuk tabel komparasi.")

    content_slide(prs, "Tiga jebakan Sastrawi yang paling sering",
                  ["**Import-nya rewel.** Paket di pip bernama `sastrawi` (huruf kecil), tapi modulnya "
                   "`Sastrawi` (huruf besar S). Salah kapital -> ModuleNotFoundError",
                   "**Stemmer dibuat sekali, bukan tiap token.** `StemmerFactory().create_stemmer()` di dalam "
                   "loop membuat program lambat berkali-kali lipat",
                   "**Kata di luar kamus dikembalikan apa adanya.** Nama orang, istilah asing, singkatan - "
                   "tidak di-stem. Itu perilaku benar, bukan bug",
                   "__",
                   "Bonus: Sastrawi juga punya `StopWordRemoverFactory` - tapi hari ini kita fokus stemming saja."],
                  note="Jebakan kapitalisasi adalah penyebab error nomor satu di kelas "
                       "sebelumnya. Tulis di papan: pip install sastrawi / from Sastrawi...")

    # ============ BAGIAN 3 - PRAKTIKUM EN ============
    section_slide(prs, "BAGIAN 3 - PRAKTIKUM 2", "Lemmatization Inggris\ndengan NLTK WordNet",
                  "Modul langkah 6 - dan di sinilah POS menjadi wajib")

    code_slide(prs, "WordNet tanpa POS - dan kenapa hasilnya mengecewakan",
               ["from nltk.stem import WordNetLemmatizer",
                "lem = WordNetLemmatizer()",
                "",
                "print(lem.lemmatize('studies'))   # -> 'study'   (default: noun)",
                "print(lem.lemmatize('studying'))  # -> 'studying' (TIDAK berubah!)",
                "print(lem.lemmatize('better'))    # -> 'better'   (TIDAK berubah!)",
                "",
                "# dengan POS yang benar:",
                "print(lem.lemmatize('studying', pos='v'))  # -> 'study'",
                "print(lem.lemmatize('better',   pos='a'))  # -> 'good'"],
               caption="Default lemmatize() menganggap semua kata adalah KATA BENDA. Itu sumber kesalahan paling umum.",
               note="Slide terpenting di bagian ini. Tanpa POS, lemmatizer terlihat 'tidak "
                    "bekerja' padahal ia bekerja sesuai instruksi. Ini juga yang menjelaskan "
                    "koreksi untuk jawaban Bahrum: lemma bergantung pada komponen POS tagger, "
                    "bukan pada tokenisasi.")

    code_slide(prs, "pos_tag + peta Treebank -> WordNet (modul langkah 6)",
               ["from nltk import pos_tag",
                "from nltk.corpus import wordnet",
                "",
                "def to_wordnet(tag):",
                "    if tag.startswith('J'): return wordnet.ADJ",
                "    if tag.startswith('V'): return wordnet.VERB",
                "    if tag.startswith('R'): return wordnet.ADV",
                "    return wordnet.NOUN          # default",
                "",
                "teks_en = 'The students were studying better methods quietly.'",
                "tokens  = [t.lower() for t in word_tokenize(teks_en) if t.isalnum()]",
                "tagged  = pos_tag(tokens)",
                "lemmas  = [lem.lemmatize(w, to_wordnet(t)) for w, t in tagged]",
                "",
                "for (w, t), l in zip(tagged, lemmas):",
                "    print(f'{w:12s} {t:5s} -> {l}')"],
               caption="pos_tag memakai label Treebank (NN, VBG, JJR, RB). WordNet hanya mengenal 4 kelas - jadi perlu dipetakan.",
               note="Jalankan live. Tunjukkan 'studying VBG -> study' dan 'better JJR -> good'. "
                    "Kalau ada waktu: hapus fungsi to_wordnet dan tunjukkan hasilnya berubah "
                    "jadi tidak ternormalisasi - bukti bahwa POS-lah yang mengerjakan.")

    # ============ BAGIAN 4 - EVALUASI ============
    section_slide(prs, "BAGIAN 4", "Mengukur dampaknya\npada kosakata",
                  "Modul langkah 7-8 - bagian yang dinilai 35% di rubrik")

    code_slide(prs, "Hitung ukuran kosakata: sebelum vs sesudah",
               ["def vocab(xs):",
                "    return len(set(xs))",
                "",
                "print('BI  sebelum:', vocab(tokens_id), ' sesudah:', vocab(stems))",
                "print('EN  sebelum:', vocab(tokens_en), ' sesudah:', vocab(lemmas))",
                "",
                "red_id = 1 - vocab(stems)  / max(vocab(tokens_id), 1)",
                "red_en = 1 - vocab(lemmas) / max(vocab(tokens_en), 1)",
                "print(f'penyusutan BI: {red_id:.1%}   EN: {red_en:.1%}')"],
               caption="Inilah angka yang harus muncul di laporan Anda - bukan 'kosakata berkurang', tapi berkurang BERAPA PERSEN.",
               note="Tekankan: pakai teks yang cukup panjang (5-10 kalimat minimal). Pada "
                    "teks 1 kalimat penyusutannya nyaris nol dan kesimpulannya menyesatkan. "
                    "Ini juga latihan pertama membaca angka secara jujur.")

    table_slide(prs, "Tabel komparasi - format wajib (Produk B, 35%)",
                ["Language", "Original", "Tokens", "After (Stem/Lemma)"],
                [["ID", "berlari-lari", "berlari-lari", "lari"],
                 ["ID", "pembelajaran", "pembelajaran", "ajar"],
                 ["ID", "mempermainkan", "mempermainkan", "main"],
                 ["EN", "studying (VBG)", "studying", "study"],
                 ["EN", "better (JJR)", "better", "good"]],
                col_w=[2, 4, 3, 4], fs=17,
                sub="Empat kolom persis seperti di modul. Isi minimal: beberapa contoh BI dan EN yang representatif - termasuk yang hasilnya mengejutkan.",
                note="Minta mereka sengaja memasukkan 1-2 baris yang salah-normalisasi. "
                     "Rubrik menghargai 'contoh representatif', dan contoh yang gagal justru "
                     "paling informatif untuk analisis di Produk C.")

    content_slide(prs, "Yang harus ada di Ringkasan Analisis (Produk C, 20%)",
                  ["**Kapan memilih stemming**: butuh cepat, korpus besar, tugas berbasis topik, "
                   "Bahasa Indonesia (karena memang itu yang tersedia)",
                   "**Kapan memilih lemmatization**: butuh bentuk kata yang sah, analisis makna, "
                   "ada POS tagger yang andal untuk bahasa itu",
                   "**Satu contoh perubahan makna** yang Anda temukan sendiri di data Anda",
                   "**Implikasi ke fitur**: berapa persen kosakata menyusut, dan apa artinya untuk "
                   "jumlah kolom BoW/TF-IDF di Pertemuan 4",
                   "__",
                   "Satu halaman saja. Yang dinilai kedalaman argumennya, bukan panjangnya."],
                  sub="Rubrik: A (>=85) menjawab 'kapan memilih' + dampak ke fitur DENGAN contoh. Tanpa contoh, nilainya turun ke B.")

    # ============ PENUGASAN ============
    section_slide(prs, "PENUGASAN", "Tiga produk,\nsatu berkas kumpulan",
                  "Sesuai bagian 6 modul mandiri")

    table_slide(prs, "Penugasan mandiri P3 - wajib dikumpulkan",
                ["Produk", "Isi", "Bobot"],
                [["*A - Notebook (.ipynb)", "Kode lengkap BI & EN + tabel komparasi + sel markdown analisis 1-2 paragraf", "*45%"],
                 ["*B - Tabel komparasi", "Kolom: Language | Original | Tokens | After (Stem/Lemma)", "*35%"],
                 ["*C - Ringkasan 1 halaman", "PDF/DOCX: kapan stemming vs lemmatization, contoh perubahan makna, implikasi fitur", "*20%"]],
                col_w=[3.4, 7.4, 1.4], fs=16,
                sub="Penamaan berkas di eBelajar: P3-NLP-NIM-Nama",
                note="Ingatkan beda dengan Tugas 1: ini penugasan modul P3, tenggatnya akan "
                     "diumumkan di eBelajar. Tugas 1 (tokenisasi & stopwords) tenggat 27 Sep - "
                     "Bahrum sudah kumpul (dinilai 78, ada catatan revisi); Rudolph dan Hafiz "
                     "masih bisa mengumpulkan.")

    content_slide(prs, "Reproducibility & etika - dua syarat yang mudah dilupakan",
                  ["**Cantumkan versi paket** (`pip freeze` secukupnya, atau `requirements.txt`)",
                   "**Dokumentasikan keputusan pra-proses**: stopwords apa yang dipakai, normalisasi apa, tokenisasi apa",
                   "Jaga struktur folder: `data/` · `notebooks/` · `reports/`",
                   "__",
                   "**Etika data**: pakai data legal dan non-sensitif; anonimkan bila perlu; "
                   "**sertakan atribusi sumber data**",
                   "Kalau memakai AI untuk membantu: tulis di notebook bagian mana yang dibantu - "
                   "itu bukan pengurang nilai, yang mengurangi nilai adalah menyembunyikannya."],
                  note="Bagian etika sering dilewati mahasiswa. Sebut satu kalimat saja tapi "
                       "tegas: sumber data wajib dicantumkan, sama seperti sitasi.")

    # ============ PENUTUP ============
    content_slide(prs, "Exit-ticket Pertemuan 3 - isi sebelum keluar ruangan",
                  ["**1.** Satu kata Bahasa Indonesia yang hasil stemming-nya menurut Anda **merusak makna** - "
                   "tulis kata, hasil stem-nya, dan makna apa yang hilang",
                   "**2.** Kenapa `lemmatize('better')` mengembalikan `'better'`, dan apa yang harus "
                   "ditambahkan supaya menjadi `'good'`?",
                   "**3.** Berapa persen kosakata menyusut di teks percobaan Anda (BI dan EN), dan "
                   "menurut Anda apakah penyusutan itu menolong atau merugikan tugas yang Anda bayangkan?"],
                  sub="Forum exit-ticket P3 di eBelajar - dinilai skala 0-100 dan langsung masuk gradebook, seperti P2.",
                  note="Soal 1 menguji pemahaman trade-off. Soal 2 menguji hal teknis paling "
                       "sering salah. Soal 3 memaksa mereka melihat angka sendiri, bukan "
                       "menyalin kesimpulan modul.")

    content_slide(prs, "Pratinjau Pertemuan 4 - Representasi Teks",
                  ["Semua yang kita kerjakan sejak P2 bermuara ke sini: **teks jadi angka**",
                   (1, "P2 tokenisasi & stopwords -> menentukan **apa yang dihitung**"),
                   (1, "P3 stemming & lemmatization -> menentukan **berapa banyak kolom** yang muncul"),
                   (1, "P4 **BoW & TF-IDF** -> akhirnya matriks fitur yang bisa masuk model"),
                   "__",
                   "Angka penyusutan kosakata yang Anda hitung hari ini **adalah** jumlah kolom yang "
                   "Anda hemat di P4. Bawa angka itu minggu depan."],
                  sub="Catatan modul: siapkan 1-2 slide rekap hasil kelas (kasus paling menarik + jebakan umum) untuk dibahas di P4.")

    links_slide(prs, "Tautan cepat",
                [["Folder Drive Pertemuan 3 (modul, LKS, video)", FOLDER_P3],
                 ["Modul Mandiri P3 - Stemming & Lemmatization (tanpa spaCy)", MODUL_P3],
                 ["LKS Colab - NLP_Pertemuan_3_Stemming_Lemmatization.ipynb", LKS_P3],
                 ["Video - Membedah Stemming vs Lemmatization", VIDEO_1],
                 ["Forum exit-ticket P3 (eBelajar)", "%s/course/view.php?id=%d" % (B, COURSE)],
                 ["Tugas 1 - tenggat Minggu 27 Sep 23.55", "%s/mod/assign/view.php?id=%d" % (B, TUGAS1)]],
                sub="eBelajar menautkan, Drive menyimpan. Kalau ada tautan yang mati, lapor di forum Diskusi Umum.")

    return prs


if __name__ == "__main__":
    prs = build()
    path = os.path.join(OUT, "NLP_A_Pertemuan3_Ganjil2026.pptx")
    prs.save(path)
    print("OK", path, len(prs.slides.__iter__.__self__._sldIdLst), "slide")
