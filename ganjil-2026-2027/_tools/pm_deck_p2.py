# -*- coding: utf-8 -*-
"""Deck Pertemuan 2 — Pembelajaran Mesin, kelas A (luring).

SUMBER (sinkron dengan Drive "pertemuan 2", 14 Sep):
  - Modul Mandiri P2 (PDF): "Missing Values, Normalization, Standardization
    (NA & Scaling Clinic)" - tujuan, narasi Titanic, grid 8 kombinasi,
    rubrik 100 poin, kuis K1-K5.
  - LKS_Pertemuan_2_NA_Scaling.ipynb: Titanic (datasciencedojo), EDA,
    split stratified, 2 imputasi x 2 skala x 2 model, scoring F1,
    confusion matrix, baseline drop-rows, exit ticket.
Slide #2 = Laporan Feedback Mingguan (ritual Senin); angka dari sweep
eBelajar Senin 14 Sep 2026.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deckkit import *

OUT = r"D:\documents\ebelajar\ganjil-2026-2027\pembelajaran-mesin"
B = "https://ebelajar.stiki.ac.id"

# ── cmid PM A (sumber: teaching/ganjil-2026-2027.md) ──
COURSE  = 7218
MATERI2 = 491679   # page materi P2 (Normalization vs Standardization)
TUGAS1  = 491680   # assign Tugas 1 (due Minggu 27 Sep 2026 23.55)
MODUL1  = 495555   # Modul Mandiri P1 (panduan + rubrik)
BAHAN1  = 496339   # url "Bahan Pertemuan 1 di Google Drive"
UMUM    = 491670   # forum Diskusi Umum
FORUM_P2 = 501183  # forum exit-ticket P2 (rating: average, 0-100)

# ── Drive "pertemuan 2" ──
FOLDER_P2 = "https://drive.google.com/drive/folders/1_XPX1i9Lp64tCGiizt98fskWFF4foTkW"
DRIVE_P1  = "https://drive.google.com/drive/folders/1Id_syspr70fBMvVLOOALkXHrbDkkH_kb"
MODUL_P2  = "https://drive.google.com/file/d/1Ph98jxlYfg3OLTYr7EUtZG0MTeWOFP5S/view"
LKS_P2    = "https://drive.google.com/file/d/1BHIlEGqa3pumI04R7-fycKByUzG-QTmJ/view"
VIDEO_1   = "https://drive.google.com/file/d/1GL3ga15p5mxsPInn8aNwCEClG9mAeOvW/view"
VIDEO_2   = "https://drive.google.com/file/d/1qcQVU1mT2bJTqPr-wc3AaVT_Jm61wdE1/view"

# ── Statistik feedback Minggu 1 (sweep eBelajar Senin 14 Sep 2026) ──
STATS = {
    "forum_dijawab": "9 dari 9 posting dibalas dan dinilai hari ini (skala 0-100, masuk gradebook)",
    "perkenalan":    "1 dari 22 - Faiz sudah mengisi; sudah dibalas",
    "tugas1":        "0 dari 22 - baru dibuka, tenggat Minggu 27 Sep 23.55",
    "respons":       "< 24 jam pada hari kerja",
}


def build():
    prs = new_deck()

    title_slide(prs, "PERTEMUAN 2 · PEMBELAJARAN MESIN",
                "NA & Scaling Clinic",
                "Missing Values, Normalization, Standardization - studi kasus dataset Titanic",
                "Mukhlis Amien, M.Kom.  ·  IF24KB53  ·  Kelas A (Reguler) · Senin 13.00-15.30 · A.2.1")

    # ══ FEEDBACK MINGGUAN ══
    table_slide(prs, "Laporan feedback - Minggu 1 (7-13 Sep)",
                ["Yang saya lakukan minggu ini", "Hasil"],
                [["*Posting forum P1", "*"+STATS["forum_dijawab"]],
                 ["*Perkenalan mahasiswa", "*"+STATS["perkenalan"]],
                 ["*Tugas 1 (tenggat 27 Sep)", "*"+STATS["tugas1"]],
                 ["*Waktu respons", "*"+STATS["respons"]]],
                col_w=[5, 7], fs=18,
                sub="Setiap Senin, deck dibuka dengan slide ini: koreksi dan feedback minggu lalu - tercatat, bukan klaim.",
                note="Ritual pembuka. Posting forum P1 hari ini dinilai 80-90 (rubrik ringan: "
                     "ketepatan konsep + contoh). Sebut satu-dua nama: Dico (90 - satu-satunya "
                     "yang menyebut umpan balik/koreksi sebagai bagian pembelajaran), Adinda (87 - "
                     "satu-satunya yang memberi contoh penerapan).")

    content_slide(prs, "Alur 150 menit hari ini",
                  ["**Hook** - kasus Titanic: siapa yang selamat? · 10'",
                   "**Mini-lecture** - imputasi: drop, SimpleImputer, KNNImputer · 30'",
                   "**Mini-lecture** - Standardization vs Normalization · 20'",
                   "**Demo** - Pipeline + ColumnTransformer, grid 8 kombinasi metrik F1 · 15'",
                   "**Studio** - LKS Titanic di Colab (bawa laptop) · 60'",
                   "**Debrief** + exit-ticket · 15'"],
                  sub="Angka = menit. Semua mengikuti Modul Mandiri P2 & LKS di Google Drive - bahan yang sama yang Anda kerjakan mandiri.")

    # ══ HOOK ══
    section_slide(prs, "HOOK", "Kasus Titanic:\nsiapa yang selamat?",
                  "Narasi pemantik dari modul - dan dataset resmi LKS hari ini")

    statement_slide(prs, "Anda diminta membuat model prediksi\nkeselamatan penumpang Titanic.",
                    "Masalah bawaan datanya: kolom Age banyak yang kosong; Fare sangat bervariasi; Sex dan Embarked kategorikal. "
                    "Pertanyaan modul: strategi NA dan skala mana yang paling menaikkan F1? Buktikan dengan eksperimen.",
                    note="Minta mahasiswa menebak dulu: kolom apa yang paling bermasalah? Sebagian "
                         "sudah tahu Titanic. Poinnya: ini dataset LKS hari ini - semua akan menghitung, bukan mendengar saja.")

    content_slide(prs, "Capaian pertemuan ini (Sub-CPMK0821)",
                  ["Mendiagnosis dan menangani **missing values**: drop, mean/median/most_frequent, **KNNImputer**",
                   "Menerapkan **Standardization vs Normalization** dan menjelaskan kapan masing-masing dipakai",
                   "Menyusun **Pipeline + ColumnTransformer** yang bebas leakage dan reproducible",
                   "Mengevaluasi dampak NA & skala pada **Logistic Regression dan KNN** - accuracy, precision, recall, F1, confusion matrix",
                   "Menulis ringkasan temuan **berbasis bukti eksperimen**"],
                  sub="Lima kemampuan inilah yang dinilai di LKS dan rubrik modul - semuanya menumpuk di Tugas 1.")

    # ══ BAGIAN 1 - IMPUTASI ══
    section_slide(prs, "BAGIAN 1", "Missing values,\nlebih dalam",
                  "Drop vs SimpleImputer vs KNNImputer - dan risikonya")

    table_slide(prs, "Lima strategi, lima konsekuensi",
                ["Strategi", "Cocok untuk", "Catatan kritis"],
                [["*Drop rows", "Missing acak, proporsi kecil", "Buang baris = buang informasi; kalau tidak acak, muncul bias"],
                 ["*Mean", "Numerik, distribusi simetris", "Sensitif outlier - satu nilai ekstrem menggesernya"],
                 ["*Median", "Numerik, ada outlier", "Pilihan paling aman; default yang layak"],
                 ["*Most frequent", "Kategorikal", "Isi dengan kategori terbanyak; lalu one-hot encoding"],
                 ["*KNNImputer (k=5)", "Numerik, pola antar-kolom kuat", "Kontekstual - tapi berbasis jarak, jadi butuh scaling & peka outlier"]],
                col_w=[3, 3, 6], fs=16,
                sub="Keputusan imputasi = keputusan tentang sifat kolomnya, bukan selera.")

    content_slide(prs, "Diagnosis dulu, baru memilih",
                  ["Titanic 891 baris: **Age** ~20% kosong, **Cabin** ~77% kosong, **Embarked** hanya 2 baris",
                   "Embarked: 2 baris - **drop saja**, dampaknya nol",
                   "Age: 20% - drop = buang 1 dari 5 penumpang; data yang hilang mungkin **tidak acak** (anak-anak tercatat lebih lengkap?)",
                   "Cabin: 77% - terlalu banyak; nanti jadi bahan **feature thinking** (Pertemuan 3)"],
                  sub="Aturan praktis modul: isi dulu; drop hanya kalau proporsinya kecil dan hilangnya memang acak.")

    content_slide(prs, "KNNImputer - imputasi yang 'pintar'",
                  ["Isi nilai kosong dengan **rata-rata dari k tetangga terdekat** yang lengkap",
                   "Kontekstual: penumpang dengan kelas & tarif serupa saling mengisi - **bukan satu angka untuk semua baris**",
                   "Tapi hati-hati: berbasis **jarak** - jadi **peka terhadap skala** dan outlier",
                   "Konsekuensi: **scaling dulu, baru imputasi** (atau imputasi di dalam Pipeline yang terskala)"],
                  note="Kunci K3 modul: KNNImputer unggul saat ada struktur antar-kolom; gagal saat data kecil "
                       "atau belum diskalakan. Minta mahasiswa tebak: apa yang terjadi kalau Fare (0-512) "
                       "dan SibSp (0-8) dipakai bersama tanpa scaling? Fare mendominasi jarak.")

    content_slide(prs, "Uji cepat 1",
                  ["Kolom *Age*: **20%** kosong. Kolom *Fare*: punya outlier ekstrem",
                   (1, "Imputasi apa yang Anda pilih untuk masing-masing, dan mengapa?"),
                   (1, "Boleh langsung KNNImputer **sebelum** scaling? Apa risikonya?"),
                   (1, "Diskusikan 2 menit - jawab di chat sebelum demo")],
                  note="Jawaban yang diharapkan: Age pakai median (atau KNNImputer SETELAH scaling); "
                       "Fare median dulu karena outlier. KNNImputer sebelum scaling = jarak didominasi "
                       "kolom berskala besar.")

    # ══ BAGIAN 2 - SKALA ══
    section_slide(prs, "BAGIAN 2", "Normalization\nvs Standardization",
                  "Dua teknik penskalaan, dua konsekuensi berbeda")

    content_slide(prs, "Normalization - Min-Max Scaling",
                  ["Mengubah skala ke rentang tetap, biasanya **[0, 1]**",
                   "Rumus:  **x' = (x - min) / (max - min)**",
                   "**Menjaga bentuk distribusi** asli - hanya digeser dan dipampatkan",
                   "**Sensitif pencilan** - satu Fare ekstrem memampatkan semua nilai lain ke rentang sempit"],
                  note="Ilustrasi dengan Titanic: Fare mayoritas 0-100, satu penumpang 512. "
                       "Tanpa outlier proporsional; dengan outlier hampir semua data terjepit di bawah 0,2.")

    content_slide(prs, "Standardization - Z-score",
                  ["Mengubah data agar punya **rata-rata 0** dan **simpangan baku 1**",
                   "Rumus:  **z = (x - mu) / sigma**",
                   "Tidak terikat rentang tertentu, relatif tahan outlier",
                   "**Cocok untuk** model berbasis jarak & gradien: **KNN, Logistic Regression, SVM**"],
                  sub="Di LKS hari ini: StandardScaler vs MinMaxScaler - pengaruhnya diukur, bukan diasumsikan.")

    table_slide(prs, "Min-Max vs Z-score - ringkasan",
                ["", "Min-Max", "Z-score"],
                [["Rentang hasil", "[0, 1] tetap", "Tanpa batas tetap"],
                 ["Outlier", "Sangat terpengaruh", "Relatif tahan"],
                 ["Bentuk distribusi", "Terjaga", "Terstandarisasi"],
                 ["Umum dipakai di", "Neural networks, citra", "KNN, LogReg, SVM, PCA"]],
                col_w=[3, 4, 5], fs=17,
                sub="Tidak ada yang menang mutlak - yang ada kecocokan dengan algoritma dan sifat datanya.")

    statement_slide(prs, "Model berbasis pohon praktis\ntidak membutuhkan penskalaan.",
                    "Decision Tree & Random Forest memutuskan lewat ambang per fitur, bukan jarak - menskalakan tidak merugikan, tapi juga tidak menolong. "
                    "Di rubrik modul, membandingkan dengan model pohon = poin bonus.",
                    color=RED,
                    note="Kunci bonus rubrik (maks 5 poin). Juga pertanyaan klasik Tugas 1. Minta mahasiswa catat kalimat ini.")

    content_slide(prs, "Uji cepat 2",
                  ["Model Anda **Random Forest**, tapi Anda tetap men-standardisasi datanya",
                   (1, "Apa yang terjadi pada hasilnya?"),
                   (1, "Jawabannya harus bisa Anda jelaskan - bukan cuma 'gapapa sih'")],
                  note="Jawaban: praktis tidak ada perubahan berarti - pohon tak peduli skala. "
                       "Kerugiannya cuma waktu & kompleksitas pipeline.")

    # ══ BAGIAN 3 - PIPELINE & EKSPERIMEN ══
    section_slide(prs, "BAGIAN 3", "Pipeline & eksperimen\nyang jujur",
                  "ColumnTransformer, grid 8 kombinasi, metrik F1")

    code_slide(prs, "Kerangka: dua jalur dalam satu ColumnTransformer",
               ["cat_prep = Pipeline([",
                "    ('imputer', SimpleImputer(strategy='most_frequent')),",
                "    ('ohe',     OneHotEncoder(handle_unknown='ignore'))])",
                "",
                "num_block = Pipeline([",
                "    ('imputer', SimpleImputer(strategy='median')),   # atau KNNImputer(5)",
                "    ('scaler',  StandardScaler())])                  # atau MinMaxScaler()",
                "",
                "prep = ColumnTransformer([",
                "    ('num', num_block, num_cols),",
                "    ('cat', cat_prep,  cat_cols)])",
                "pipe = Pipeline([('prep', prep), ('model', model)])"],
               caption="Numerik dan kategorikal jalan di jalur masing-masing; satu fit() untuk semuanya.",
               note="Ini kerangka persis di LKS. Tekankan dua jalur: kategorikal selalu "
                    "most_frequent + one-hot; numerik yang diganti-ganti (median vs KNNImputer, std vs minmax).")

    content_slide(prs, "Kenapa fit-nya di data latih saja?",
                  ["Min/max, mu/sigma, kategori one-hot = **statistik yang dipelajari** - sama statusnya dengan bobot model",
                   "Kalau dihitung dari seluruh data: informasi data uji **bocor** ke pelatihan (kunci K4 modul)",
                   "Akurasi naik tipu-panjang di eksperimen, **runtuh** di data baru",
                   "Di Pipeline + ColumnTransformer, urutan & pemisahan ini dijaga **otomatis**"],
                  sub="Cek notebook Anda: berapa yang masih menghitung scaler sebelum split?")

    content_slide(prs, "Eksperimen LKS: 8 kombinasi sekaligus",
                  ["**2 imputasi** numerik: median vs **KNNImputer**(k=5)",
                   "**x 2 skala**: StandardScaler vs MinMaxScaler",
                   "**x 2 model**: LogisticRegression vs KNN(k=5) = **8 pipeline**",
                   "Validasi: **StratifiedKFold(5-fold)**, scoring = **f1**",
                   "Rangking dari tabel hasil, lalu **fit final** pada kombinasi terbaik ke test set: classification_report + **confusion matrix**"],
                  note="Jelaskan kenapa CV: satu split bisa keberuntungan. Stratified menjaga proporsi "
                       "kelas di tiap fold. Skor yang dilaporkan = rata-rata +- simpangan baku 5 fold.")

    content_slide(prs, "Kenapa F1, bukan accuracy?",
                  ["Titanic tidak seimbang: hanya **~38%** penumpang selamat",
                   "Model bodoh 'semua tidak selamat' dapat accuracy **62%** - tanpa menyelamatkan siapa pun",
                   "**F1** = harmonic mean precision & recall - menyeimbangkan dua arah kesalahan",
                   "Tahan dominasi kelas mayoritas - itulah kenapa LKS menskor dengan f1"],
                  note="Kunci K5 modul. Coba tanya: kalau RSFK yang paling jarang selamat (kelas 3, laki-laki, "
                       "dewasa) - prediksi 'selamat semua' apa akibatnya untuk recall kelas 1?")

    # ══ STUDIO ══
    section_slide(prs, "STUDIO · 60 MENIT", "LKS Titanic\ndi Google Colab",
                  "LKS_Pertemuan_2_NA_Scaling.ipynb - di Drive, siap jalan")

    content_slide(prs, "Langkah kerja studio",
                  ["Buka LKS dari Drive **pertemuan 2** - jalan di Colab, dataset Titanic ter-unduh otomatis",
                   "EDA: proporsi missing per kolom, urutkan tertinggi; histogram fitur numerik",
                   "Split **train/test 80/20, stratify, random_state=42** - cek num_cols vs cat_cols",
                   "Jalankan grid 8 kombinasi - baca tabel F1 yang diurutkan",
                   "Fit final kombinasi terbaik: classification_report + confusion matrix",
                   "Baseline **drop-rows**: berapa F1 yang hilang karena baris dibuang?",
                   (1, "Kerjakan berpasangan · exit-ticket di akhir notebook, kirim ke forum sebelum keluar")],
                  note="Berkeliling; dua jebakan paling sering: (1) lupa stratify, (2) mencocokkan "
                       "num_cols/cat_cols dari X bukan X_train. Arahkan ke pertanyaan, bukan jawaban.")

    content_slide(prs, "Deliverables LKS - cara dinilai",
                  ["Notebook rapi: Pendahuluan, EDA, Strategi NA & Skala, Eksperimen, Evaluasi, Insight",
                   "Tabel komparatif **minimal 8 kombinasi** + **3 visualisasi** (histogram, confusion matrix, bar chart F1)",
                   "Ringkasan **150-250 kata**: strategi paling berpengaruh + alasan + risiko",
                   "Penamaan: **NIM_Nama_P2_NA_Scaling.ipynb** + folder outputs/",
                   "Rubrik: EDA 15 · Pipeline & reproduksibilitas 25 · Eksperimen & evaluasi 30 · Analisis & insight 20 · Kerapian 10 · **Bonus 5**"],
                  note="Rubrik sama dengan Modul Mandiri P2. Ingatkan: feedback & nilai LKS "
                       "tercatat di eBelajar - kaitkan dengan slide laporan di awal.")

    # ══ PENUTUP ══
    content_slide(prs, "Poin kunci",
                  ["Missing dibiarkan = **distorsi** estimasi + baris yang hilang saat training/inferensi",
                   "**StandardScaler** untuk model jarak/gradien & data mendekati Gaussian; **MinMax** menjaga bentuk distribusi tapi peka pencilan",
                   "**KNNImputer** kontekstual tapi peka skala & outlier - scaling adalah prasyaratnya",
                   "fit() scaler & encoder **hanya pada data latih**, di dalam Pipeline - selalu",
                   "Kelas tidak seimbang → laporkan **F1**, bukan hanya accuracy"])

    content_slide(prs, "Uji pemahaman mandiri (kuis modul)",
                  ["Apa **dua risiko utama** jika missing values dibiarkan?",
                   "Kapan StandardScaler lebih tepat daripada MinMaxScaler?",
                   "Kapan **KNNImputer** unggul, kapan justru tidak cocok?",
                   "Beri contoh **data leakage** pada skenario scaling - dan cara mencegahnya",
                   "Mengapa **F1** sering lebih informatif daripada accuracy?"],
                  sub="Lima pertanyaan ini persis dari modul; kunci jawaban singkat ada di halaman materi P2 di eBelajar.")

    content_slide(prs, "Tugas 1 - tenggat Minggu 27 Sep, 23.55",
                  ["Materi P1 + P2 = **bahan langsungnya** - tidak ada materi baru yang diperlukan",
                   "Panduan langkah & rubrik 100 poin: **Modul Mandiri Pertemuan 1**",
                   "Syarat wajib: **reproducible** · bebas **leakage** · **disclosure AI** jujur",
                   "Yang sudah mengumpulkan lebih awal: feedback tercatat di eBelajar - cek komentar di submission Anda"],
                  note="Sambungkan ke slide laporan feedback: tugas yang dikumpulkan dinilai minggu yang sama. "
                       "Teknik hari ini (imputasi + scaling + pipeline) = inti Tugas 1.")

    content_slide(prs, "Exit-ticket - sebelum keluar ruangan",
                  ["Buka **forum Pertemuan 2** di eBelajar, posting jawaban Anda:",
                   (1, "Kombinasi NA & skala **terbaik** Anda, dan **mengapa**"),
                   (1, "Satu hal yang masih **mengganjal**"),
                   (1, "Rencana eksperimen susulan minggu depan"),
                   "Posting dinilai & dijawab minggu ini - lihat slide laporan di atas",
                   "**Pertemuan 3: encoding & feature thinking** - bawa pertanyaan Cabin Anda"],
                  note="Tiga pertanyaan exit ticket = bawaan LKS. Kalau waktu sempit, cukup poin 1 dan 2.")

    rows = [
        ("Kursus Pembelajaran Mesin A", f"{B}/course/view.php?id={COURSE}"),
        ("Materi P2 - Normalization vs Standardization", f"{B}/mod/page/view.php?id={MATERI2}"),
        ("Forum Pertemuan 2 (exit-ticket)", f"{B}/mod/forum/view.php?id={FORUM_P2}"),
        ("Tugas 1 - Praktek Preprocessing Data", f"{B}/mod/assign/view.php?id={TUGAS1}"),
        ("Modul Mandiri P1 (panduan + rubrik Tugas 1)", f"{B}/mod/page/view.php?id={MODUL1}"),
        ("Folder Drive Pertemuan 2 (modul, LKS, slide, video)", FOLDER_P2),
        ("Modul Mandiri P2 (PDF)", MODUL_P2),
        ("LKS Titanic - NA & Scaling (Colab)", LKS_P2),
        ("Video: Rahasia Data Berantakan", VIDEO_1),
        ("Video: Dokter Data - Imputasi & Scaling", VIDEO_2),
        ("Bahan Pertemuan 1 di Google Drive", f"{B}/mod/url/view.php?id={BAHAN1}" if BAHAN1 else DRIVE_P1),
        ("Forum Diskusi Umum", f"{B}/mod/url/view.php?id={UMUM}"),
    ]
    links_slide(prs, "Tautan cepat - klik langsung dari slide ini", rows,
                sub="Salindia ini tersimpan di Google Drive; semua tautan aktif saat dibuka di PowerPoint atau Google Slides.")

    out = os.path.join(OUT, "PM_A_Pertemuan2_Ganjil2026.pptx")
    prs.save(out)
    return out


if __name__ == "__main__":
    path = build()
    from pptx import Presentation
    print("OK", path, "slides:%d" % len(Presentation(path).slides._sldIdLst))
