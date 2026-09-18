# -*- coding: utf-8 -*-
"""Deck Pertemuan 3 - Pembelajaran Mesin, kelas A (luring).

SUMBER (folder Drive "pertemuan 3" PM, id 1h8QxqSRIxa9xzKc6Xn0qquVJtCtDNF2o):
  - Modul Mandiri P3 (PDF): "Encoding & Feature Thinking (Feature Engineering
    Dasar)" - 5 tujuan, peta belajar A-F, rare categories, OHE vs Ordinal,
    target encoding & leakage, FeatureMaker custom transformer, ColumnTransformer
    + Pipeline, ablation study, deliverables, kuis K1-K5 + kunci,
    rubrik 25/25/25/15/10 + bonus 5, exit ticket.
  - LKS Colab: LKS_P3_Encoding_Feature_Thinking.ipynb
  - Video "Menyelami Encoding & Rekayasa Fitur: Kunci Pipeline Anti-Leakage"
  - Video "Bahasa Rahasia Data"

Slide #2 = Laporan feedback mingguan (ritual Senin). Angka diambil dari
eBelajar 18 Sep 2026: 22 peserta; Tugas 1 terkumpul 2/22 (tenggat 27 Sep);
exit-ticket P2 NOL posting mahasiswa; Perkenalan 1 dari 22.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deckkit import *

OUT = r"D:\documents\ebelajar\ganjil-2026-2027\pembelajaran-mesin"
B = "https://ebelajar.stiki.ac.id"

# -- cmid PM A (course 7218; sweep 18 Sep 2026) --
COURSE   = 7218
MATERI2  = 491679
TUGAS1   = 491680
FORUM_P2 = 501183
BAHAN2   = 501184
UMUM     = 491670

# -- Drive "pertemuan 3" PM --
FOLDER_P3 = "https://drive.google.com/drive/folders/1h8QxqSRIxa9xzKc6Xn0qquVJtCtDNF2o"
MODUL_P3  = "https://drive.google.com/file/d/1zW1Fb1fArK6eX3a6co9wIS1Fg-0pj_YC/view"
LKS_P3    = "https://colab.research.google.com/drive/1tCPukd9SPQF_mnh0kOKs5xEI_t6GGIcO"
VIDEO_1   = "https://drive.google.com/file/d/1KWxNCCKsQHeBM9Juo9b8FTji-b1sCS03/view"
VIDEO_2   = "https://drive.google.com/file/d/1exDRQYBU6AUtX1do1FPRqg-gp84Y2auE/view"


def build():
    prs = new_deck()

    title_slide(prs, "PERTEMUAN 3 - PEMBELAJARAN MESIN",
                "Encoding & Feature Thinking",
                "Dari kategori jadi angka - dan dari kolom mentah jadi fitur yang benar-benar berbicara",
                "Mukhlis Amien, M.Kom.  ·  IF24KB53  ·  Kelas A (Reguler) · Senin 13.00-15.30 · A.2.1")

    # ============ RITUAL: FEEDBACK MINGGUAN ============
    table_slide(prs, "Laporan feedback - Minggu 2 (14-20 Sep)",
                ["Yang saya periksa", "Hasil per 18 September"],
                [["*Forum P1", "*9 dari 9 posting sudah dibalas dan dinilai 80-90 - nilainya sudah ada di gradebook"],
                 ["*Exit-ticket P2", "*0 posting dari 22. Forum masih terbuka dan masih dinilai"],
                 ["*Tugas 1", "*Terkumpul 2 dari 22. Tenggat Minggu 27 Sep 23.55 - sisa 9 hari"],
                 ["*Perkenalan", "*1 dari 22 (Faiz). Sudah dibalas"],
                 ["*Blokir kumpul", "*Sudah dibuka 15 Sep (setelan warisan 2025). Kalau masih gagal, lapor hari ini"]],
                col_w=[3.6, 8.4], fs=16,
                sub="Angka ini dibaca langsung dari eBelajar pagi ini, bukan perkiraan.",
                note="Dua angka yang perlu disebut lisan dengan tegas: exit-ticket P2 NOL "
                     "posting, dan Tugas 1 baru 2 dari 22 padahal tinggal 9 hari. Jangan "
                     "menyalahkan - sampaikan sebagai fakta plus tawaran bantuan. Forum P1 "
                     "menunjukkan mereka MAU posting kalau tahu dinilai; ulangi info itu.")

    statement_slide(prs, "Tugas 1: 2 dari 22.\nSembilan hari lagi.",
                    "Tugas 1 adalah praktek preprocessing - materi P1 dan P2 yang sudah kita kerjakan bersama. "
                    "Kalau macet di satu langkah, tulis di forum Diskusi Umum hari ini juga; jangan menunggu tanggal 26.",
                    color=RED,
                    note="Satu slide khusus supaya tidak lewat begitu saja. Tawarkan: 10 menit "
                         "di akhir kelas untuk yang mau tanya Tugas 1 langsung.")

    content_slide(prs, "Alur 150 menit hari ini",
                  ["**Hook** - satu kolom kategori, tiga cara menyandikan, tiga hasil berbeda · 10'",
                   "**Mini-lecture** - One-Hot vs Ordinal, kategori langka, dan bahaya target encoding · 30'",
                   "**Praktikum 1** - encoding di dalam Pipeline/ColumnTransformer (anti-leakage) · 35'",
                   "**Praktikum 2** - Feature Thinking: bikin fitur turunan lewat custom transformer · 40'",
                   "**Ablation** - tanpa fitur baru vs dengan fitur baru, baca tabelnya · 25'",
                   "**Rangkuman** + penugasan + exit-ticket · 10'"],
                  sub="Angka = menit. Modul mandiri versinya 3-4 jam; hari ini kita kerjakan inti yang paling mudah salah kalau dikerjakan sendirian.")

    # ============ HOOK ============
    section_slide(prs, "HOOK", "Bahasa rahasia\ndata",
                  "Judul video pembuka di Drive - dan pertanyaan yang belum terjawab sejak Pertemuan 2")

    statement_slide(prs, "Model tidak bisa membaca\n\"male\", \"female\", \"Cherbourg\".",
                    "Di Pertemuan 2 kita sudah rapikan nilai hilang dan skala. Tapi seluruh kolom kategori "
                    "masih kita hindari. Hari ini kita hadapi - dan kita akan lihat bahwa CARA menyandikannya "
                    "mengubah performa model, kadang lebih besar daripada mengganti modelnya.",
                    note="Sambungkan langsung ke LKS P2 Titanic yang sudah mereka kerjakan. "
                         "Tanya: di notebook P2 kemarin, kolom Sex dan Embarked Anda apakan? "
                         "Sebagian pasti membuangnya. Itulah yang kita perbaiki hari ini.")

    content_slide(prs, "Capaian pertemuan ini (5 tujuan modul mandiri P3)",
                  ["Menjelaskan tujuan dan perbedaan **One-Hot vs Ordinal Encoding**, serta risiko **target encoding**",
                   "Melakukan encoding kategorikal **di dalam Pipeline/ColumnTransformer** untuk mencegah data leakage",
                   "Merancang **>=2 fitur turunan** (FamilySize, FarePerPerson, AgeBin, IsAlone, interaksi) dan menjelaskan rasionalnya",
                   "Mengevaluasi dampak encoding dan fitur turunan pada **model linear (LogReg) vs tree-based (DT/RF)**",
                   "Menyusun **ablation study** dan mini-report 1 halaman: *\"Tiga Fitur Baru Terbaik\"*"],
                  sub="Kelimanya dinilai di rubrik 100 poin: encoding 25 · feature engineering 25 · evaluasi & ablation 25 · analisis 15 · reproducibility 10.",
                  body_size=20)

    content_slide(prs, "Bahan belajar mandiri di Drive - pertemuan 3",
                  ["**Modul Mandiri P3 (PDF)** - *Encoding & Feature Thinking*, estimasi 3-4 jam",
                   "**LKS Colab** - `LKS_P3_Encoding_Feature_Thinking.ipynb`",
                   "Video **Menyelami Encoding & Rekayasa Fitur: Kunci Pipeline Anti-Leakage**",
                   "Video **Bahasa Rahasia Data**",
                   "__",
                   "Dataset tetap **Titanic** - sengaja sama sejak P2 supaya perbandingan antar pertemuan adil. "
                   "Alternatif kalau ingin kategori berkardinalitas tinggi: UCI Adult."],
                  sub="Tautan lengkap ada di slide terakhir. eBelajar hanya menautkan - satu salinan tunggal di Drive.",
                  note="Ingatkan: buka LKS di Colab lalu File > Save a copy in Drive dulu. "
                       "Kalau langsung diedit, pekerjaannya tidak tersimpan.")

    # ============ BAGIAN 1 - ENCODING ============
    section_slide(prs, "BAGIAN 1", "Menyandikan kategori",
                  "One-Hot, Ordinal, dan satu jebakan bernama target encoding")

    table_slide(prs, "Dua skema utama - dan kapan memakainya",
                ["", "One-Hot Encoding (OHE)", "Ordinal Encoding"],
                [["Menghasilkan", "Satu kolom biner per kategori", "Satu kolom, kategori jadi 0,1,2,3..."],
                 ["Aman untuk", "Kategori NOMINAL (tanpa urutan)", "Kategori ORDINAL (ada urutan alami)"],
                 ["Bahayanya", "Kolom meledak kalau kardinalitas tinggi", "Menyiratkan urutan yang tidak ada"],
                 ["Cocok model", "Linear (LogReg) - butuh representasi tersebar", "Tree-based - tahan terhadap penyandian sederhana"],
                 ["Setelan wajib", "handle_unknown='ignore', drop='if_binary'", "handle_unknown='use_encoded_value'"]],
                col_w=[2.8, 5.2, 5.0], fs=15,
                sub="Contoh ordinal yang sah: tingkat pendidikan SD < SMP < SMA < S1. Contoh yang TIDAK sah: kota keberangkatan.",
                note="Jawaban kuis K1 modul ada di sini: OrdinalEncoder lebih tepat kalau ada "
                     "urutan alamiah. Tekankan drop='if_binary' - tanpa itu kolom Sex jadi dua "
                     "kolom yang saling melengkapi sempurna (redundan).")

    content_slide(prs, "Kategori langka - masalah yang tidak terlihat sampai model overfit",
                  ["Kategori dengan proporsi **< 1-3%** sering hanya muncul beberapa baris",
                   "Akibatnya: kolom OHE yang hampir seluruhnya nol -> model menghafal, bukan belajar",
                   "Penanganan standar: **gabungkan jadi satu kategori `'Other'`**",
                   "__",
                   "**Syarat mutlak:** ambang dan daftar kategori langka ditentukan dari **data latih saja**.",
                   (1, "Kalau dihitung dari seluruh data (train+test), informasi test bocor ke model"),
                   (1, "Karena itu langkah ini harus hidup di dalam **transformer**, bukan di sel notebook terpisah")],
                  sub="Modul memakai ambang 2%. Angka itu bukan hukum - laporkan ambang yang Anda pakai dan alasannya.",
                  note="Ini pintu masuk ke konsep leakage. Banyak mahasiswa membersihkan data "
                       "di awal notebook sebelum split - dan itu sudah salah sejak awal.")

    statement_slide(prs, "Target encoding itu kuat.\nDan paling mudah bikin Anda tertipu.",
                    "Menyandikan kategori ke rata-rata target: sangat efektif untuk kardinalitas tinggi. "
                    "Tapi Anda sedang memasukkan JAWABAN ke dalam fitur. Tanpa out-of-fold encoding di dalam CV, "
                    "skor validasi Anda akan indah - dan bohong.",
                    color=RED,
                    note="Jawaban kuis K3: target encoding 'mengintip' target; mitigasinya "
                         "out-of-fold/cross-fitting atau smoothing. Di modul ini statusnya "
                         "OPSIONAL - katakan: kalau belum nyaman, lewati saja, jangan dipaksakan.")

    content_slide(prs, "Uji cepat 1 - dua menit, tebak dulu",
                  ["Pada dataset Titanic, kolom `Embarked` punya 3 nilai (S, C, Q):",
                   (1, "Kalau disandikan **Ordinal** jadi 0/1/2, apa yang secara tidak sengaja diklaim ke model?"),
                   (1, "Kalau disandikan **One-Hot**, berapa kolom baru yang muncul?"),
                   (1, "Kolom `Sex` hanya punya 2 nilai. Berapa kolom yang SEHARUSNYA dihasilkan OHE - dan kenapa?"),
                   "__",
                   "Diskusikan dengan sebelah. Jawaban ketiga adalah alasan `drop='if_binary'` ada."],
                  note="Jawaban: (1) mengklaim S < C < Q, urutan yang tidak bermakna - dan "
                       "model linear akan memperlakukan jarak Q-S dua kali jarak C-S. "
                       "(2) tiga kolom. (3) satu kolom sudah cukup; dua kolom saling redundan "
                       "sempurna (multikolinearitas), karena itu drop='if_binary'.")

    # ============ BAGIAN 2 - PIPELINE ============
    section_slide(prs, "BAGIAN 2 - PRAKTIKUM 1", "Encoding di dalam Pipeline",
                  "Modul bagian 5.5 - satu-satunya cara yang aman dari leakage")

    code_slide(prs, "ColumnTransformer: numerik dan kategorikal, jalur terpisah",
               ["from sklearn.compose import ColumnTransformer, make_column_selector as selector",
                "from sklearn.pipeline import Pipeline",
                "from sklearn.impute import SimpleImputer",
                "from sklearn.preprocessing import OneHotEncoder, StandardScaler",
                "",
                "num_sel = selector(dtype_include=['int64', 'float64'])",
                "cat_sel = selector(dtype_include=['object', 'category', 'bool'])",
                "",
                "prep_ohe = ColumnTransformer([",
                "    ('num', Pipeline([('imputer', SimpleImputer(strategy='median')),",
                "                      ('scaler',  StandardScaler())]), num_sel),",
                "    ('cat', Pipeline([('imputer', SimpleImputer(strategy='most_frequent')),",
                "                      ('ohe', OneHotEncoder(handle_unknown='ignore',",
                "                                           drop='if_binary'))]), cat_sel),",
                "])"],
               caption="make_column_selector memilih kolom berdasarkan TIPE - jadi kolom baru hasil feature engineering otomatis ikut terpilih.",
               note="Tekankan selector: kalau kolomnya ditulis manual, fitur turunan yang "
                    "dibuat nanti tidak akan ikut diproses dan mereka akan bingung kenapa "
                    "tidak ada efeknya.")

    statement_slide(prs, "Split dulu. Fit belakangan.\nSelalu.",
                    "Semua impute, scale, dan encode dilakukan SETELAH train_test_split, dan hanya di-fit pada data latih. "
                    "Jangan pernah fit apa pun pada gabungan train+test. Ini satu kalimat yang memisahkan eksperimen jujur dari angka fiktif.",
                    note="Ulangi persis kalimat modul. Ini akan jadi soal exit-ticket dan "
                         "juga bagian dari rubrik reproducibility 10 poin.")

    # ============ BAGIAN 3 - FEATURE THINKING ============
    section_slide(prs, "BAGIAN 3 - PRAKTIKUM 2", "Feature Thinking",
                  "Modul bagian 5.4 - bagian yang paling menentukan hasil, dan paling sedikit diajarkan")

    table_slide(prs, "Empat fitur turunan Titanic - dan alasan domainnya",
                ["Fitur", "Rumus", "Kenapa masuk akal"],
                [["*FamilySize", "SibSp + Parch + 1", "Ukuran rombongan menentukan perilaku evakuasi"],
                 ["*IsAlone", "FamilySize == 1", "Penumpang sendirian bergerak beda dari yang menjaga keluarga"],
                 ["*FarePerPerson", "Fare / FamilySize", "Fare adalah harga tiket ROMBONGAN - per orang lebih jujur soal kelas ekonomi"],
                 ["*AgeBin", "kuantil q1-q4 dari Age", "Hubungan usia-keselamatan tidak linear (anak & lansia beda)"]],
                col_w=[2.6, 3.2, 6.2], fs=15,
                sub="Jawaban kuis K4. Perhatikan FarePerPerson - itu contoh fitur yang MEMPERBAIKI kolom yang menyesatkan, bukan sekadar menambah kolom.",
                note="Bahas FarePerPerson agak lama. Ini contoh terbaik 'feature thinking': "
                     "Fare mentah membuat keluarga besar tampak kaya. Setelah dibagi jumlah "
                     "orang, sinyal kelas ekonominya baru benar. Itulah berpikir tentang fitur, "
                     "bukan sekadar membuat fitur.")

    code_slide(prs, "FeatureMaker - fitur turunan yang tidak bocor",
               ["class FeatureMaker(BaseEstimator, TransformerMixin):",
                "    def fit(self, X, y=None):",
                "        # ambang kategori langka & batas AgeBin ditentukan DI SINI",
                "        # -> artinya dari data LATIH saja",
                "        q = np.quantile(X['Age'].dropna(), [0, .25, .5, .75, 1.0])",
                "        self._age_bins = np.unique(q)",
                "        return self",
                "",
                "    def transform(self, X):",
                "        X = X.copy()",
                "        X['FamilySize']    = X['SibSp'] + X['Parch'] + 1",
                "        X['IsAlone']       = (X['FamilySize'] == 1).astype(int)",
                "        X['FarePerPerson'] = X['Fare'] / X['FamilySize'].clip(lower=1)",
                "        X['AgeBin'] = pd.cut(X['Age'], bins=self._age_bins,",
                "                             include_lowest=True).astype(str)",
                "        return X"],
               caption="Kunci desainnya: apa pun yang DIPELAJARI dari data masuk fit(); yang sekadar dihitung ulang masuk transform().",
               note="Tanya kelas: kenapa AgeBin harus dihitung di fit, tapi FamilySize boleh "
                    "di transform? Jawaban: AgeBin butuh kuantil (statistik dari data); "
                    "FamilySize cuma penjumlahan baris itu sendiri. Itu pembeda leakage.")

    code_slide(prs, "Merangkai semuanya jadi satu pipeline",
               ["pipe = Pipeline([",
                "    ('feat',  FeatureMaker()),      # fitur turunan",
                "    ('prep',  prep_ohe),            # impute + scale + encode",
                "    ('model', LogisticRegression(max_iter=1000)),",
                "])",
                "",
                "cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)",
                "scores = cross_validate(pipe, Xtr, ytr, cv=cv,",
                "        scoring=['accuracy', 'precision', 'recall', 'f1'])"],
               caption="Satu objek, tiga tahap. Seluruhnya di-fit ulang di setiap fold CV - itulah yang membuat skornya jujur.",
               note="Tunjukkan: kalau FeatureMaker dijalankan manual di luar pipeline, "
                    "cross_validate akan memberi skor optimistis karena AgeBin sudah "
                    "'melihat' seluruh data. Ini jebakan paling halus di modul ini.")

    # ============ BAGIAN 4 - ABLATION ============
    section_slide(prs, "BAGIAN 4", "Ablation study",
                  "Modul bagian 5.6 - membuktikan fitur Anda berguna, bukan mengklaimnya")

    table_slide(prs, "Tabel ablation - minimal 4 baris (2 encoding x 2 model)",
                ["Setting", "Encoding", "Model", "Acc", "F1", "Catatan"],
                [["Baseline", "OHE", "LR", "0.xxx", "0.xxx", "-"],
                 ["+Fitur", "OHE", "LR", "0.xxx", "0.xxx", "+FamilySize, +FarePerPerson"],
                 ["Baseline", "ORD", "RF", "0.xxx", "0.xxx", "-"],
                 ["+Fitur", "ORD", "RF", "0.xxx", "0.xxx", "+AgeBin, +IsAlone"]],
                col_w=[2.0, 1.8, 1.4, 1.4, 1.4, 4.0], fs=15,
                sub="Cara membuat baseline: cukup hapus step ('feat', FeatureMaker()) dari pipeline. Sisanya identik - itu syarat perbandingan yang adil.",
                note="Tekankan 'sisanya identik'. Kalau baseline pakai seed lain atau split "
                     "lain, selisihnya tidak berarti apa-apa. Ini latihan pertama mereka soal "
                     "kontrol eksperimen - yang akan dipakai terus sampai proyek akhir.")

    content_slide(prs, "Membaca hasilnya dengan jujur",
                  ["Kalau **+Fitur** menang tipis (misal 0.812 vs 0.808): itu **belum tentu** perbaikan nyata",
                   (1, "lihat simpangan baku antar-fold; kalau +/- 0.03, selisih 0.004 tenggelam di dalam derau"),
                   (1, "laporkan rata-rata **dan** simpangannya - modul sudah menyediakan formatnya"),
                   "Kalau **+Fitur** kalah: itu **hasil yang sah**, bukan kegagalan tugas",
                   (1, "tulis kenapa menurut Anda fitur itu tidak menolong - analisis inilah yang dinilai 15 poin"),
                   "Efek encoding **berbeda** antara LR dan RF - dan itu memang yang diharapkan (kuis K5)"],
                  sub="Rubrik menghargai argumen yang benar, bukan angka yang tinggi. Melaporkan fitur yang gagal dengan penjelasan yang baik nilainya penuh.",
                  note="Pesan sikap ilmiah. Banyak mahasiswa memoles angka supaya 'berhasil'. "
                       "Katakan terang-terangan: saya lebih menghargai ablation yang jujur "
                       "daripada angka yang bagus tanpa kontrol.")

    # ============ PENUGASAN ============
    section_slide(prs, "PENUGASAN", "Empat deliverable",
                  "Sesuai bagian 6 modul mandiri P3")

    table_slide(prs, "Yang dikumpulkan",
                ["#", "Deliverable", "Catatan"],
                [["*1", "Notebook rapi", "Pendahuluan - diagnostik kategori - encoding - feature engineering - model & evaluasi - ablation - insight"],
                 ["*2", "Tabel ablation >=4 baris", "Minimal 2 encoding x 2 model"],
                 ["*3", "Tiga visualisasi", "(a) confusion matrix terbaik (b) feature importance RF atau koefisien LR (c) perbandingan skor sebelum/sesudah"],
                 ["*4", "Mini-report 1 halaman", "*\"Tiga Fitur Baru Terbaik\"* - deskripsi, alasan domain, bukti metrik"]],
                col_w=[0.8, 3.2, 8.0], fs=15,
                sub="Penamaan berkas: NIM_Nama_P3_EncodingFeature.ipynb + folder outputs/ berisi gambar + P3_TigaFiturTerbaik.pdf (atau .md)",
                note="Sebutkan bonus maksimal 5 poin: out-of-fold target encoding, ATAU "
                     "perbandingan waktu latih & ukuran fitur OHE vs ORD. Bonus untuk yang "
                     "sudah selesai, bukan pengganti bagian wajib.")

    table_slide(prs, "Rubrik 100 poin - tahu persis di mana nilainya",
                ["Komponen", "Poin", "Yang dicari"],
                [["*Eksperimen encoding", "*25", "OHE vs ORD + catatan trade-off; handle_unknown disetel benar"],
                 ["*Feature engineering", "*25", ">=2 fitur baru relevan + terintegrasi dalam Pipeline (transformer kustom)"],
                 ["*Evaluasi & ablation", "*25", "Tabel jelas; Accuracy/Precision/Recall/F1; confusion matrix model terbaik"],
                 ["*Analisis & insight", "*15", "Argumen rasional pemilihan fitur/encoding; interpretasi hasil"],
                 ["*Reproducibility", "*10", "Seed disetel; split benar; notebook Run-All tanpa error"]],
                col_w=[3.0, 1.0, 8.0], fs=15,
                sub="Bonus maks 5: out-of-fold target encoding, atau perbandingan waktu latih & ukuran fitur OHE vs ORD.")

    # ============ PENUTUP ============
    content_slide(prs, "Exit-ticket Pertemuan 3 - isi sebelum keluar ruangan",
                  ["**1.** Satu contoh **leakage** yang berhasil Anda hindari hari ini - sebutkan langkah apa "
                   "yang tadinya akan Anda lakukan di luar pipeline",
                   "**2.** Fitur baru **terbaik** Anda: nama fitur, alasan domainnya, dan bukti metrik "
                   "(angka sebelum vs sesudah)",
                   "**3.** Satu rencana eksperimen lanjutan untuk **Pertemuan 4** (evaluasi & metrik)"],
                  sub="Forum exit-ticket P3 di eBelajar - dinilai skala 0-100 dan langsung masuk gradebook, sama seperti forum P1 yang sudah Anda lihat nilainya.",
                  note="Sebut eksplisit: minggu lalu exit-ticket P2 nol posting. Ingatkan bahwa "
                       "ini dinilai dan masuk gradebook, persis seperti forum P1 yang 9 orang "
                       "sudah dapat 80-90. Beri waktu 5 menit di kelas untuk mengisi.")

    content_slide(prs, "Pratinjau Pertemuan 4 - Evaluasi & Metrik yang Benar",
                  ["Hari ini Anda sudah membandingkan beberapa setting. Pertanyaan berikutnya: "
                   "**bagaimana tahu perbandingan itu adil?**",
                   (1, "split, cross-validation, dan kenapa satu angka akurasi hampir selalu menipu"),
                   (1, "metrik untuk kelas tidak seimbang - dan Titanic memang tidak seimbang"),
                   (1, "data snooping: cara paling umum menipu diri sendiri tanpa sadar"),
                   "__",
                   "Bawa tabel ablation Anda minggu depan. Kita akan bongkar mana selisih yang nyata "
                   "dan mana yang cuma derau."],
                  sub="Tabel ablation yang Anda buat hari ini menjadi bahan mentah Pertemuan 4 - jangan dibuang.")

    links_slide(prs, "Tautan cepat",
                [["Folder Drive Pertemuan 3 (modul, LKS, video)", FOLDER_P3],
                 ["Modul Mandiri P3 - Encoding & Feature Thinking", MODUL_P3],
                 ["LKS Colab - LKS_P3_Encoding_Feature_Thinking.ipynb", LKS_P3],
                 ["Video - Menyelami Encoding & Rekayasa Fitur (anti-leakage)", VIDEO_1],
                 ["Tugas 1 - tenggat Minggu 27 Sep 23.55", "%s/mod/assign/view.php?id=%d" % (B, TUGAS1)],
                 ["Forum Diskusi Umum - tempat bertanya kalau macet", "%s/mod/forum/view.php?id=%d" % (B, UMUM)]],
                sub="eBelajar menautkan, Drive menyimpan. Kalau ada tautan yang mati, lapor di forum Diskusi Umum.")

    return prs


if __name__ == "__main__":
    prs = build()
    path = os.path.join(OUT, "PM_A_Pertemuan3_Ganjil2026.pptx")
    prs.save(path)
    n = len(prs.slides._sldIdLst)
    print("OK", path, n, "slide")
