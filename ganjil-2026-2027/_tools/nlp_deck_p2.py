# -*- coding: utf-8 -*-
"""Deck Pertemuan 2 - Natural Language Processing, kelas A (luring).

SUMBER (sinkron dengan Drive "pertemuan 2" NLP, 14 Sep):
  - Modul Mandiri P2 (PDF): "Tokenisasi & Stopwords" - tujuan, peta materi
    120 menit, praktikum NLTK (5.1) & spaCy (5.2-5.3), ringkasan kuantitatif
    (5.4), penugasan A/B/C, rubrik 40/40/20, refleksi 3 soal.
  - Video "Membedah Fondasi NLP: Tokenisasi, Stopwords, NLTK, dan spaCy".
  - Video "Kekacauan Menuju Kejelasan".
  Catatan: folder pertemuan 2 NLP TIDAK punya LKS (beda dari PM) - jadi
  praktikum mengikuti langkah step-by-step di modul, exit-ticket = 3 soal
  Refleksi & Diskusi modul (bagian 8).
Slide #2 = Laporan Feedback Mingguan (ritual Senin); angka dari sweep
eBelajar Senin 14 Sep 2026. Kelas kecil: 3 mahasiswa (Hafiz, Bahrum, Rudolph).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deckkit import *

OUT = r"D:\documents\ebelajar\ganjil-2026-2027\nlp"
B = "https://ebelajar.stiki.ac.id"

# -- cmid NLP A (course 7226; sumber: sweep 14 Sep) --
COURSE   = 7226
MATERI2  = 491785   # page "Materi: Tokenisasi dan Stopwords" (S2)
TUGAS1   = 491786   # assign "Tugas 1: Praktik Tokenisasi dan Stopwords Removal" (S2)
MATERI1  = 491782   # page materi P1
FORUMP1  = 491783   # forum "Diskusi: Aplikasi NLP di Sekitar Kita" (rating on)
BAHAN1   = 496341   # url "Bahan Pertemuan 1 di Google Drive"
UMUM     = 491776   # forum Diskusi Umum
PERKENALAN = 491778 # forum Perkenalan (rating on)
FORUM_P2 = 501186   # forum "Exit-ticket Pertemuan 2 (Tokenisasi & Stopwords)", seed d=10894

# -- Drive "pertemuan 2" NLP --
FOLDER_P2 = "https://drive.google.com/drive/folders/1ozSzshC8eBpPGU1R5uZx_zsVkJmj0oBS"
PARENT_NLP = "https://drive.google.com/drive/folders/1CgIfTaAXN9BdjT90AnuDo7k7xpU_Mh3p"
MODUL_P2  = "https://drive.google.com/file/d/1NFtiYEW_W3cf_hiqYZo8Eb7OBRqW0CH2/view"
VIDEO_1   = "https://drive.google.com/file/d/1fWbSEAreSxH46B1_NkSk5tBmYq-Y03CL/view"
VIDEO_2   = "https://drive.google.com/file/d/1rE-Q2DFOqbNJK9OqhRJoSEtRT1P1iRa5/view"

# -- Statistik feedback Minggu 1 (sweep eBelajar Senin 14 Sep 2026) --
STATS = {
    "forum_dijawab": "1 dari 3 posting dibalas dan dinilai hari ini (skala 0-100, masuk gradebook)",
    "perkenalan":    "0 dari 3 - belum ada yang mengisi; mohon diisi minggu ini",
    "tugas1":        "Tugas 1 sudah terpasang di eBelajar - tenggat Minggu, 27 Sep 2026, 23.55",
    "respons":       "Ritual Senin - semua posting dibalas dan dinilai tiap Senin pagi",
}


def build():
    prs = new_deck()

    title_slide(prs, "PERTEMUAN 2 · NATURAL LANGUAGE PROCESSING",
                "Tokenisasi & Stopwords",
                "Fondasi pra-proses teks: dari kalimat mentah ke data terstruktur - dengan NLTK dan spaCy",
                "Mukhlis Amien, M.Kom.  ·  IF24KK64  ·  Kelas A (Reguler) · Selasa 08.00-10.30 · A.2.1")

    # ══ FEEDBACK MINGGUAN ══
    table_slide(prs, "Laporan feedback - Minggu 1 (8-13 Sep)",
                ["Yang saya lakukan minggu ini", "Hasil"],
                [["*Posting forum P1", "*"+STATS["forum_dijawab"]],
                 ["*Perkenalan mahasiswa", "*"+STATS["perkenalan"]],
                 ["*Tugas 1", "*"+STATS["tugas1"]],
                 ["*Waktu respons", "*"+STATS["respons"]]],
                col_w=[5, 7], fs=18,
                sub="Setiap Senin, deck dibuka dengan slide ini: koreksi dan feedback minggu lalu - tercatat, bukan klaim.",
                note="Ritual pembuka. Posting satu-satunya: Bahrum (88 - contoh konkret Google "
                     "Translate plus penjelasan mengapa itu termasuk NLP). Hafiz dan Rudolph: "
                     "forum masih terbuka, posting dinilai juga. Perkenalan masih kosong semua - "
                     "ingatkan lisan. Kelas ini 3 orang, jadi setiap orang terlihat.")

    content_slide(prs, "Alur 150 menit hari ini",
                  ["**Hook** - kekacauan teks: kenapa komputer butuh tokenisasi · 10'",
                   "**Mini-lecture** - konsep: tokenisasi kalimat & kata, stopwords, isu bahasa Indonesia · 30'",
                   "**Praktikum 1** - NLTK: sent_tokenize, word_tokenize, stopwords · 35'",
                   "**Praktikum 2** - spaCy: pipeline, is_stop, stopwords kustom · 35'",
                   "**Analisis & diskusi** - NLTK vs spaCy, top-10 kata · 20'",
                   "**Rangkuman** + tugas + exit-ticket · 20'"],
                  sub="Angka = menit. Semua mengikuti Modul Mandiri P2 di Google Drive - bahan yang sama yang Anda kerjakan mandiri (±120 menit).")

    # ══ HOOK ══
    section_slide(prs, "HOOK", "Kekacauan\nmenuju kejelasan",
                  "Narasi video pembuka di Drive - dan pertanyaan mendasar untuk hari ini")

    statement_slide(prs, "Komputer tidak melihat kata.\nYang dilihatnya: deretan karakter.",
                    "Ingat Google Translate dari diskusi minggu lalu? Sebelum bisa menerjemahkan, sistem memecah teks menjadi unit yang bisa dihitung. "
                    "Itulah tokenisasi - langkah pertama dari semua pipeline NLP, termasuk yang akan Anda bangun.",
                    note="Sambungkan dengan satu-satunya diskusi P1 (Google Translate). Poin hook: "
                         "teks mentah = karakter tanpa struktur; tokenisasi menciptakan struktur. "
                         "Minta mahasiswa: coba sebut kalimat yang ambigu kalau dipecah salah - "
                         "'kepala daerah' vs 'kepala daerah'... atau 'bisa' (racun/able) sebagai kata serapan.")

    content_slide(prs, "Capaian pertemuan ini (Sub-CPMK082.1 - preprocessing teks)",
                  ["Menjelaskan konsep **tokenisasi** (level kalimat dan kata) serta **peran stopwords** dalam pra-proses",
                   "Mengimplementasikan tokenisasi dan penghapusan stopwords dengan **NLTK dan spaCy** (Bahasa Indonesia & Inggris)",
                   "Menyusun **stopwords kustom sesuai domain**, lalu membandingkan hasil sebelum dan sesudah penghapusan",
                   "Menganalisis pengaruh stopwords terhadap **jumlah token dan frekuensi kata**"],
                  sub="Empat kemampuan inilah yang dinilai di penugasan dan rubrik modul - dan menumpuk ke Pertemuan 3 (stemming & lemmatization).")

    content_slide(prs, "Bahan belajar mandiri di Drive - pertemuan 2",
                  ["**Modul Mandiri P2 (PDF)** - tujuan, materi inti, langkah praktikum, rubrik",
                   "Video **Membedah Fondasi NLP: Tokenisasi, Stopwords, NLTK, dan spaCy**",
                   "Video **Kekacauan Menuju Kejelasan**",
                   "Estimasi belajar mandiri: **±120 menit** - mode modul ini mandiri (tanpa pendampingan)",
                   "Tambahan hari ini: praktikum bersama + diskusi + exit-ticket"],
                  sub="Tautan lengkap ada di slide terakhir. eBelajar hanya menautkan - satu salinan di Drive.")

    # ══ BAGIAN 1 - KONSEP ══
    section_slide(prs, "BAGIAN 1", "Konsep dasar:\ntokenisasi & stopwords",
                  "Definisi, tujuan, dan keputusan yang menyertainya")

    content_slide(prs, "Tokenisasi - memecah teks menjadi unit",
                  ["Memecah teks menjadi unit lebih kecil: **kalimat** (sentence) dan **kata** (word)",
                   "Hasilnya menjadi dasar hampir semua langkah berikutnya:",
                   (1, "perhitungan **frekuensi kata**"),
                   (1, "pembentukan fitur **BoW / TF-IDF** (Pertemuan 4)"),
                   (1, "input bagi model **RNN / Transformer** (Pertemuan 10-11)"),
                   "Contoh: \"Selamat datang di kelas NLP.\" → [Selamat] [datang] [di] [kelas] [NLP] [.]"],
                  note="Tekankan: tokenizer yang berbeda menghasilkan token berbeda - dan hasil "
                       "analisis pun berbeda. Ini benang merah sampai praktikum.")

    content_slide(prs, "Stopwords - kata umum yang (sering) dibuang",
                  ["Kata umum berfrekuensi tinggi yang sering **kurang informatif**: dan, yang, di, the, is",
                   "Tujuan penghapusan: **menekan noise**, fokus ke kata pembawa makna",
                   "TAPI - tidak wajib. Untuk **analisis gaya bahasa** atau **text generation**, stopwords justru penting dipertahankan",
                   "Keputusan stopwords = **keputusan per tugas**, bukan aturan baku"],
                  note="Kunci soal refleksi #1 modul: kapan TIDAK menghapus stopwords. "
                       "Contoh jawaban: analisis gaya penulis, chatbot generatif, penilaian "
                       "sentimen yang bergantung pada negasi ('tidak bagus' - 'tidak' sering "
                       "tercantum sebagai stopword).")

    content_slide(prs, "Isu Bahasa Indonesia - jangan salin setelan Inggris",
                  ["**Morfologi & afiksasi** me-, di-, ke-, pe-, ber-, ter-: \"membaca\" vs \"baca\" - dua token berbeda atau sama?",
                   "Daftar stopwords bawaan perlu **disesuaikan domain**: e-commerce, kesehatan, finansial",
                   "Periksa **tanda baca, angka, emotikon, kata serapan** - semuanya jadi token",
                   "**Dokumentasikan** keputusan pra-proses Anda - bagian dari laporan"],
                  note="Contoh konkret domain e-commerce: 'gratis ongkir' - 'ongkir' tak ada di "
                       "kamus mana pun. Kata serapan: 'upload', 'download', 'chat'. Praktikum 2 "
                       "nanti mempraktikkan ini lewat stopwords kustom.")

    table_slide(prs, "NLTK vs spaCy - dua alat, dua filosofi",
                ["", "NLTK", "spaCy"],
                [["Gaya", "Rangkaian alat terpisah, fleksibel", "Pipeline terintegrasi, objek Doc/Token"],
                 ["Tokenisasi", "sent_tokenize(), word_tokenize()", "nlp(text) → token otomatis"],
                 ["Stopwords", "Daftar corpus: stopwords.words('indonesian')", "Atribut token: t.is_stop"],
                 ["Model bahasa", "Resource: punkt, stopwords", "id_core_news_sm, en_core_web_sm"]],
                col_w=[3, 5, 5], fs=17,
                sub="Hari ini keduanya dipakai berdampingan - hasilnya dibandingkan, bukan diasumsikan sama.")

    content_slide(prs, "Uji cepat 1",
                  ["Dua kalimat dari modul:",
                   (1, "*\"Selamat datang di kelas NLP. Hari ini kita mempelajari tokenisasi dan stopwords.\"*"),
                   (1, "*\"Welcome to the NLP class. Today we learn tokenization and stopwords.\"*"),
                   (1, "Tebak: berapa token kata masing-masing? Mana yang lebih banyak stopword-nya?"),
                   (1, "Diskusikan 2 menit - jawab sebelum praktikum")],
                  note="Kualitatif saja: kalimat EN punya lebih banyak stopwords (to, the, we, and "
                       "setara). Poinnya: daftar stopwords ID bawaan lebih pendek - bahasa Indonesia "
                       "kurang terlayani, dan itu normal untuk tool open-source.")

    # ══ BAGIAN 2 - NLTK ══
    section_slide(prs, "BAGIAN 2 · PRAKTIKUM 1", "Tokenisasi & stopwords\ndengan NLTK",
                  "Modul bagian 5.1 - jalankan sambil saya demo")

    code_slide(prs, "NLTK - setup & tokenisasi (modul 5.1)",
               ["from nltk.tokenize import sent_tokenize, word_tokenize",
                "from nltk.corpus import stopwords",
                "",
                "text_id = \"Selamat datang di kelas NLP. Hari ini kita mempelajari\"",
                "          \" tokenisasi dan stopwords.\"",
                "text_en = \"Welcome to the NLP class. Today we learn tokenization\"",
                "          \" and stopwords.\"",
                "",
                "# Tokenisasi kalimat",
                "print(\"Kalimat (ID):\", sent_tokenize(text_id))",
                "print(\"Kalimat (EN):\", sent_tokenize(text_en))",
                "",
                "# Tokenisasi kata",
                "id_tokens = word_tokenize(text_id)",
                "en_tokens = word_tokenize(text_en)"],
               caption="Satu kali saja bila belum: nltk.download('punkt') dan nltk.download('stopwords')",
               note="Jalankan live. Tunjukkan: sent_tokenize memecah di titik; word_tokenize "
                    "memisahkan tanda baca sebagai token tersendiri - 'NLP.' jadi dua token.")

    code_slide(prs, "NLTK - menghapus stopwords (modul 5.1)",
               ["# Stopwords",
                "stop_id = set(stopwords.words('indonesian'))",
                "stop_en = set(stopwords.words('english'))",
                "",
                "id_filtered = [w for w in id_tokens if w.lower() not in stop_id]",
                "en_filtered = [w for w in en_tokens if w.lower() not in stop_en]",
                "",
                "print(\"ID tanpa stopwords:\", id_filtered)",
                "print(\"EN tanpa stopwords:\", en_filtered)"],
               caption="Perhatikan w.lower(): pencocokan dilakukan pada huruf kecil.",
               note="Tanya: kenapa lower() wajib? 'Dan' dan 'dan' adalah token berbeda bagi "
                    "Python. Bandingkan panjang list sebelum/sesudah - itulah metrik yang "
                    "dilaporkan nanti.")

    content_slide(prs, "Tiga jebakan NLTK yang paling sering",
                  ["**LookupError** saat tokenisasi → jalankan nltk.download('punkt') dan nltk.download('stopwords') - sekali saja",
                   "Lupa **w.lower()** → setengah stopwords lolos karena kapitalisasi",
                   "**Tanda baca tetap token** - \"NLP\" dan \".\" adalah dua token; bersihkan dengan t.isalpha() bila perlu (lihat modul 5.4)",
                   "Hasil aneh → periksa karakter non-alfanumerik dan normalisasi huruf kecil"],
                  sub="Ini persis bagian Troubleshooting Cepat di modul - baca ulang saat praktikum mandiri.")

    # ══ BAGIAN 3 - SPACY ══
    section_slide(prs, "BAGIAN 3 · PRAKTIKUM 2", "Tokenisasi & stopwords\ndengan spaCy",
                  "Modul bagian 5.2-5.3 - pipeline dan stopwords kustom")

    code_slide(prs, "spaCy - pipeline & is_stop (modul 5.2)",
               ["import spacy",
                "nlp_id = spacy.load('id_core_news_sm')",
                "nlp_en = spacy.load('en_core_web_sm')",
                "",
                "id_doc = nlp_id(text_id)",
                "en_doc = nlp_en(text_en)",
                "",
                "id_tokens_spacy = [t.text for t in id_doc]",
                "en_tokens_spacy = [t.text for t in en_doc]",
                "",
                "id_no_stop_spacy = [t.text for t in id_doc if not t.is_stop]",
                "en_no_stop_spacy = [t.text for t in en_doc if not t.is_stop]"],
               caption="Model spaCy terpasang di terminal: python -m spacy download id_core_news_sm / en_core_web_sm",
               note="Beda paradigma: NLTK fungsi terpisah per tugas; spaCy satu nlp(text) dan semua "
                    "atribut menempel di token. is_stop ditentukan oleh model, bukan daftar manual.")

    code_slide(prs, "spaCy - stopwords kustom domain (modul 5.3)",
               ["# Contoh domain e-commerce",
                "custom_id = {\"gratis\", \"diskon\", \"promo\", \"harga\", \"barang\"}",
                "custom_en = {\"free\", \"sale\", \"promo\", \"price\", \"item\"}",
                "",
                "stop_id_ext = stop_id.union(custom_id)",
                "stop_en_ext = stop_en.union(custom_en)",
                "",
                "id_filtered_ext = [w for w in id_tokens if w.lower() not in stop_id_ext]",
                "print(\"ID tanpa stopwords (dengan kustom):\", id_filtered_ext)"],
               caption="Minimal 5 kata kustom untuk domain pilihan Anda - itu poin rubrik analisis.",
               note="Kaitkan ke isu Bahasa Indonesia di Bagian 1: daftar bawaan tidak tahu kata "
                    "domain Anda. Di penugasan, mahasiswa menyusun kustom sendiri + alasan.")

    content_slide(prs, "Hasil NLTK dan spaCy berbeda - itu bukan kesalahan",
                  ["Tokenizer berbeda → pemecahan kata/tanda baca berbeda",
                   "Daftar stopwords bawaan berbeda → jumlah token tersisa berbeda",
                   "Keduanya **temuan yang dilaporkan**, bukan bug yang disembunyikan",
                   "Di laporan: tulis **mengapa** berbeda dan mana yang lebih cocok untuk tugas Anda",
                   "Modul: \"Hasil berbeda antara NLTK dan spaCy: jelaskan di laporan sebagai bagian dari analisis\""],
                  note="Kalimat terakhir kutipan langsung dari Troubleshooting modul. Sering mahasiswa "
                       "panik hasilnya tak sama dengan teman - justru itu bahan analisis.")

    # ══ BAGIAN 4 - ANALISIS & PENUGASAN ══
    section_slide(prs, "BAGIAN 4", "Analisis &\npenugasan",
                  "Ringkasan kuantitatif, deliverables, dan rubrik")

    code_slide(prs, "Ringkasan kuantitatif - 10 kata teratas (modul 5.4)",
               ["from collections import Counter",
                "import pandas as pd",
                "",
                "def top_terms(tokens, k=10):",
                "    # menyaring token alfanumerik sederhana",
                "    toks = [t.lower() for t in tokens if t.isalpha()]",
                "    return Counter(toks).most_common(k)",
                "",
                "print(\"Top-10 ID (asli):\", top_terms(id_tokens))",
                "print(\"Top-10 ID (tanpa stopwords):\", top_terms(id_filtered))"],
               caption="Bandingkan kedua daftar: posisi kata bergeser setelah stopwords dibuang.",
               note="Demo cepat: sebelum penghapusan, top-10 didominasi kata umum; sesudahnya, "
                    "kata konten naik. Itulah 'analisis ringkas pengaruh stopwords' di tujuan #4.")

    content_slide(prs, "Metrik yang dilaporkan (indikator ketercapaian modul)",
                  ["Jumlah **kalimat** hasil sent_tokenize",
                   "Jumlah **token** sebelum vs sesudah penghapusan stopwords",
                   "**10 kata teratas** sebelum vs sesudah",
                   "Kesimpulan singkat: **NLTK vs spaCy** + efek daftar kustom",
                   "Semua masuk notebook - satu fungsi per langkah, dijalankan berurutan"],
                  sub="Ketarampilan teknis modul: notebook berisi fungsi tokenisasi, penghapusan stopwords, dan ringkasan metrik sederhana.")

    content_slide(prs, "Penugasan mandiri - tiga tugas dari modul",
                  ["**Tugas A** - Notebook 01_tokenization.ipynb: tokenisasi NLTK & spaCy (ID & EN), stopwords default + kustom (≥5 kata domain), ringkasan metrik, kesimpulan singkat",
                   "**Tugas B** - Laporan singkat PDF (1-2 halaman): latar, metode, hasil (tabel perbandingan), pembahasan, kesimpulan",
                   "**Tugas C** (opsional) - Diagram batang frekuensi sebelum vs sesudah stopwords (matplotlib)",
                   "Arsip: **NIM_Nama_P2.zip** - notebooks/, laporan_p2.pdf, data/, images/",
                   "Penamaan di LMS: **P2-NLP-NIM-Nama**"],
                  note="Dikumpulkan ke Tugas 1 di eBelajar (section 2). Tenggat: Minggu, 27 Sep "
                       "2026, 23.55 - cek halaman Tugas 1. Tugas C opsional tapi mengangkat kualitas "
                       "laporan (visual/tabel = poin rubrik B).")

    table_slide(prs, "Rubrik penilaian - total 100",
                ["Komponen", "Bobot", "Sangat baik (A)"],
                [["*Notebook tokenisasi", "*40%", "Kode lengkap, rapi, tanpa error; mencakup NLTK & spaCy (ID & EN)"],
                 ["*Analisis stopwords", "*40%", "Perbandingan jelas; alasan kata kustom kuat; ada metrik dan contoh"],
                 ["*Laporan PDF", "*20%", "Struktur baik, ringkas, visual/tabel jelas, kesimpulan tajam"]],
                col_w=[3, 2, 7], fs=17,
                sub="Kriteria lulus pertemuan: total >= 60/100 dan notebook dapat dieksekusi.",
                note="Rubrik identik dengan Modul Mandiri P2. Skala 0-100 forum exit-ticket juga "
                     "tercatat di gradebook - ingatkan kaitannya dengan slide laporan di awal.")

    content_slide(prs, "Poin kunci",
                  ["Tokenisasi = **fondasi semua langkah NLP**: frekuensi, BoW/TF-IDF, input model",
                   "Stopwords menekan noise - tapi **tidak selalu dibuang**: gaya bahasa & generation butuh mereka",
                   "Bahasa Indonesia butuh **penyesuaian domain**: afiksasi, kata serapan, stopwords kustom",
                   "NLTK dan spaCy **memang berbeda hasil** - jadikan bahan analisis, bukan kepanikan",
                   "Dokumentasikan setiap keputusan pra-proses di **laporan**"])

    content_slide(prs, "Uji pemahaman mandiri (refleksi modul)",
                  ["Kapan sebaiknya kita **tidak menghapus stopwords**? Beri contoh tugasnya",
                   "Apa **perbedaan paling terlihat** antara tokenisasi NLTK dan spaCy pada teks Anda?",
                   "Sebutkan **5 stopwords kustom** untuk domain pilihan Anda - dan alasannya",
                   "(Bonus) Mengapa w.lower() wajib sebelum pencocokan stopwords?"],
                  sub="Tiga pertanyaan pertama persis dari modul - dan menjadi exit-ticket hari ini.")

    content_slide(prs, "Exit-ticket - sebelum keluar ruangan",
                  ["Buka **forum Pertemuan 2** di eBelajar, jawab di diskusi yang disediakan:",
                   (1, "Kapan sebaiknya kita **TIDAK** menghapus stopwords? Beri satu contoh tugas NLP"),
                   (1, "Perbedaan **paling terlihat** tokenisasi NLTK vs spaCy pada teks yang Anda coba"),
                   (1, "**5 stopwords kustom** untuk domain pilihan Anda + alasan"),
                   "Posting dinilai 0-100 dan dibalas Senin depan - lihat slide laporan di atas",
                   "**Pertemuan 3: stemming & lemmatization** - bawa pertanyaan afiksasi Anda"],
                  note="Tiga soal = Refleksi & Diskusi modul (bagian 8), sama dengan isi forum "
                       "exit-ticket. Kalau waktu sempit, cukup soal 1 dan 2 di kelas, sisanya "
                       "mandiri sebelum Senin.")

    rows = [
        ("Kursus Natural Language Processing A", f"{B}/course/view.php?id={COURSE}"),
        ("Materi P2 - Tokenisasi dan Stopwords", f"{B}/mod/page/view.php?id={MATERI2}"),
        ("Forum Pertemuan 2 (exit-ticket)", f"{B}/mod/forum/view.php?id={FORUM_P2}"),
        ("Tugas 1 - Praktik Tokenisasi dan Stopwords Removal", f"{B}/mod/assign/view.php?id={TUGAS1}"),
        ("Forum Diskusi P1 - Aplikasi NLP di Sekitar Kita", f"{B}/mod/forum/view.php?id={FORUMP1}"),
        ("Forum Perkenalan", f"{B}/mod/forum/view.php?id={PERKENALAN}"),
        ("Folder Drive Pertemuan 2 (modul, video, slide)", FOLDER_P2),
        ("Modul Mandiri P2 (PDF)", MODUL_P2),
        ("Video: Membedah Fondasi NLP", VIDEO_1),
        ("Video: Kekacauan Menuju Kejelasan", VIDEO_2),
        ("Bahan Pertemuan 1 di Google Drive", f"{B}/mod/url/view.php?id={BAHAN1}"),
        ("Forum Diskusi Umum", f"{B}/mod/forum/view.php?id={UMUM}"),
    ]
    links_slide(prs, "Tautan cepat - klik langsung dari slide ini", rows,
                sub="Salindia ini tersimpan di Google Drive; semua tautan aktif saat dibuka di PowerPoint atau Google Slides.")

    out = os.path.join(OUT, "NLP_A_Pertemuan2_Ganjil2026.pptx")
    prs.save(out)
    return out


if __name__ == "__main__":
    path = build()
    from pptx import Presentation
    print("OK", path, "slides:%d" % len(Presentation(path).slides._sldIdLst))
