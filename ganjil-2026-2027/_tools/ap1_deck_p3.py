# -*- coding: utf-8 -*-
"""Deck Pertemuan 3 AP1 A - Estetika dalam Desain UI & Penyusunan Proposal.

Dibangun 24 Sep 2026 dari Modul Mandiri P3 + angka feedback sweep pagi ini.
Konvensi nama: AP1_A_Pertemuan3_Ganjil2026.pptx (sejajar P1/P2).
Angka feedback = konstanta di bawah, bisa dioverride via flag CLI --t2=N dll.
"""
import os, sys

from deckkit import (new_deck, title_slide, section_slide, content_slide,
                     table_slide, statement_slide, links_slide, RED)

OUT = r"D:\documents\ebelajar\ganjil-2026-2027\application-project-1"

# ============ ANGKA FEEDBACK (sweep eBelajar 24 Sep pagi) ============
T1_KUMPUL, T1_TOTAL = 6, 24          # Tugas 1 (due 20 Sep, lewat)
T2_KUMPUL, T2_TOTAL = 0, 24          # Tugas 2 (due Minggu 27 Sep 23.55)
EXIT2_POST = 0                       # Exit-ticket P2
PERKENALAN_DIBALAS = 5               # Tyo, Devan, Andrean, Jibril, Marchel
KELOMPOK_TERDAFTAR = 6
NAMA_BELUM_TERDAFTAR = "Firmanda, Yudha, Felix, Setya"

TABULASI = [
    # nama, Perkenalan, Exit P2, Tugas 1, Tugas 2
    ["Daffa M. Ramadhan", "-", "-", "*90", "-"],
    ["Bobby E. A. Kusuma", "-", "-", "*88", "-"],
    ["Kirana Y. R. Raharja", "-", "-", "*88", "-"],
    ["Tekiu Newegalen", "-", "-", "*85", "-"],
    ["Jovan N. F. Zaky", "-", "-", "*80", "-"],
    ["Andrean S. Bagaskara", "*80", "-", "*70", "-"],
    ["Devan Aldo Vobiscum", "*80", "-", "-", "-"],
    ["Mukhamad Jibril H.", "*80", "-", "-", "-"],
    ["Marchel Y. Sihombing", "*80", "-", "-", "-"],
    ["Tyo Dzaky Kamaludin", "-", "-", "-", "-"],
    ["(18 mahasiswa lain)", "-", "-", "-", "-"],
]

KELOMPOK = [
    ["*RAWON", "Andrean (ketua), Jovan, Jeremiah, Devan"],
    ["*JOSJIS", "Bobby (ketua), Tyo, Geraldy"],
    ["*Es Puter", "Rizkia (ketua), Kirana"],
    ["*QWERTY", "Daffa (ketua), Marchel, Jibril"],
    ["*KELOMPOK7", "Tekiu (ketua), Ferdi, Notopianus"],
    ["*Akatsuki", "Feyza (ketua), Shidqi"],
]

RUBRIK = [
    ["Kualitas Style Guide (lengkap, jelas, dapat diterapkan)", "*25"],
    ["Estetika & Konsistensi Mockup (warna, tipografi, grid, state)", "*30"],
    ["Aksesibilitas & Keterbacaan (kontras, hirarki informasi, densitas)", "*20"],
    ["Kecocokan dengan Tujuan Pengguna (alur dan fokus fitur inti)", "*15"],
    ["Kerapian & Kepatuhan Format (nama berkas, lengkap, tepat waktu)", "*10"],
    ["*Lulus tugas", "*minimal 70"],
]

PROPOSAL7 = [
    ["*1. Judul & Ringkasan", "2-3 kalimat: apa yang dibangun, untuk siapa"],
    ["*2. Masalah & Target Pengguna", "persona mini + konteks penggunaan"],
    ["*3. Hipotesis Nilai", "manfaat utama yang dirasakan pengguna"],
    ["*4. Fitur Inti MVP + Out-of-Scope", "3-5 fitur; yang TIDAK dibangun ikut ditulis"],
    ["*5. Risiko & Asumsi Kritis", "apa yang bisa membuat ini gagal"],
    ["*6. Metrik Keberhasilan Awal", "contoh: penyelesaian tugas, waktu interaksi"],
    ["*7. Rencana Validasi", "siapa diuji, bagaimana, kapan (minggu depan)"],
]

TUGAS3 = [
    ["*3a - Style Guide", "Individu / kelompok kecil", "StyleGuide_P3.pdf", "25"],
    ["*3b - Mockup 2 layar", "Individu", "Mockup_P3_Home.pdf + Mockup_P3_FiturInti.pdf", "30"],
    ["*3c - Draft Proposal", "Kelompok", "AP1_P3_KelompokX_Proposal.pdf (1-2 hal)", "20+15+10"],
]

DRIVE_P3 = "https://drive.google.com/drive/folders/1QScoRtDclfPY3hes3UMmJv3rcj6IrhV3"
EB = "https://ebelajar.stiki.ac.id"


def build():
    prs = new_deck()

    title_slide(prs, "PERTEMUAN 3 - APPLICATION PROJECT I",
                "Estetika dalam Desain UI\n& Penyusunan Proposal",
                "Dari wireframe polos ke mockup yang konsisten - dan arah proyek dalam 1-2 halaman",
                "Mukhlis Amien, M.Kom.  ·  IF24KB33  ·  Kelas A  ·  Kamis 13.50-15.30  ·  A.2.1")

    # ============ RITUAL: FEEDBACK MINGGUAN ============
    table_slide(prs, "Laporan feedback - Minggu 3 (17-23 Sep)",
                ["Yang saya periksa", "Hasil per 24 September pagi"],
                [["*Tugas 1", "*6 dari 24 terkumpul - keenamnya SUDAH dinilai dengan catatan revisi di kolom komentar tugas"],
                 ["*Tugas 2", "*0 dari 24. Tenggat Minggu 27 Sep pukul 23.55 - sisa 3 hari"],
                 ["*Exit-ticket P2", "*%d posting. Forum terbuka dan tetap dinilai" % EXIT2_POST],
                 ["*Perkenalan", "*%d sudah dibalas dan dinilai 80 (Tyo, Devan, Andrean, Jibril, Marchel)" % PERKENALAN_DIBALAS],
                 ["*Kelompok", "*%d kelompok terdaftar di sheet Drive. 4 nama belum tercatat: %s" % (KELOMPOK_TERDAFTAR, NAMA_BELUM_TERDAFTAR)]],
                col_w=[3.6, 8.4], fs=16,
                sub="Angka dibaca langsung dari eBelajar pagi ini, bukan perkiraan.",
                note="Poin lisan: (1) Tugas 1 yang 6 orang itu nilai plus catatannya sudah ada - "
                     "tunjukkan di layar cara membuka kolom komentar. (2) Tugas 2 nol tapi "
                     "tenggatnya Minggu - masih sangat bisa dikejar; Tugas 2 itu audit ergonomi "
                     "wireframe masing-masing + brainstorming ide, bahan ada di modul P2. "
                     "(3) 4 nama yang belum tercatat di sheet: urus sebelum kelas berakhir.")

    statement_slide(prs, "Tugas 2: %d dari %d.\nTiga hari lagi." % (T2_KUMPUL, T2_TOTAL),
                    "Tugas 2 = audit ergonomi + aksesibilitas atas wireframe Tugas 1 Anda, plus satu halaman "
                    "brainstorming ide proyek. Semua bahan ada di modul Pertemuan 2 dan halaman materi di eBelajar. "
                    "Kalau macet, tulis di forum Diskusi Umum hari ini - jangan menunggu Minggu malam.",
                    color=RED,
                    note="Tawarkan 10 menit di akhir kelas untuk tanya Tugas 2 langsung. "
                         "Ingatkan: Tugas 2 memakai hasil Tugas 1 - yang kemarin dikumpulkan "
                         "tinggal melanjutkan.")

    table_slide(prs, "Tabulasi nilai s.d. pagi ini (24 Sep)",
                ["Mahasiswa", "Perkenalan", "Exit P2", "Tugas 1", "Tugas 2"],
                TABULASI,
                col_w=[4.4, 2.2, 1.9, 1.9, 1.9], fs=14,
                sub="Sumber: rating forum + grade tugas di eBelajar, pagi ini. Kosong = belum ada aktivitas - semuanya masih bisa dikejar sebelum tenggat.",
                note="Sebut: (1) Tugas 1 punya catatan revisi konkret per orang - buka "
                     "komentar tugas di layar, tunjukkan caranya. (2) Daffa 90 karena state "
                     "empty/error dipikirkan; Andrean 70 karena yang dikumpulkan foto kelompok "
                     "tanpa bagian individu - jangan disebut nama untuk contoh negatif tanpa "
                     "perlu, cukup katakan 'tugas individu, berkas bersama dinilai rendah'. "
                     "(3) Kolom Exit P2 kosong semua - hari ini wajib beda.")

    table_slide(prs, "Pembagian kelompok (sheet Drive, %d kelompok)" % KELOMPOK_TERDAFTAR,
                ["Kelompok", "Anggota"],
                KELOMPOK,
                col_w=[3.0, 9.0], fs=15,
                sub="Belum tercatat: %s - lengkapi sheet hari ini sebelum kelas bubar; tanpa kelompok, Tugas 3c tidak bisa dinilai." % NAMA_BELUM_TERDAFTAR,
                note="Sekali sekaligus: kelompok = unit Tugas 3c (proposal) dan proyek "
                     "semester. Yang belum masuk sheet datang ke depan setelah kelas. "
                     "Firmanda/Yudha lintas angkatan boleh gabung kelompok 2025 yang ada "
                     "atau bentuk pasangan sendiri.")

    content_slide(prs, "Alur 100 menit hari ini",
                  ["**Feedback + kunci kelompok** - tabulasi, Tugas 2, daftar hadir kelompok · 15'",
                   "**Mini-lecture** - empat alat estetika: komposisi, warna, tipografi, whitespace · 25'",
                   "**Praktik A** - style guide 1 halaman dari palet kelompok Anda · 30'",
                   "**Praktik B+C** - mulai mockup 2 layar + draft 7 komponen proposal · 25'",
                   "**Exit-ticket** - 3 pertanyaan refleksi, jawab sebelum keluar · 5'"],
                  sub="Modul mandiri versinya 120-150 menit; hari ini kita kerjakan inti yang paling butuh diskusi.",
                  note="Sisakan 5 menit terakhir untuk exit-ticket - jangan sampai terlewat "
                       "lagi seperti P2. Tulis 3 pertanyaannya di papan atau tampilkan slide "
                       "terakhir.")

    # ============ BAGIAN 1: ESTETIKA ============
    section_slide(prs, "BAGIAN 1", "Estetika = sistem,\nbukan selera",
                  "Palet 5 peran, type scale, grid 8-point - 10 layar yang terlihat seperti satu produk")

    statement_slide(prs, "Wireframe menjawab \"di mana\".\nMockup menjawab \"apakah ini bisa dipercaya\".",
                    "Pertemuan 1-2 Anda membangun struktur. Hari ini kita beri dia kulit yang konsisten: "
                    "keputusan warna, huruf, dan jarak yang bisa dipertanggungjawabkan - bukan tempelan rasa.",
                    note="Jembatan dari P1-P2 ke P3. Estetika di sini = kredibilitas produk "
                         "di mata pengguna pertama kali.")

    content_slide(prs, "Peta kerja hari ini",
                  ["**Audit visual** wireframe P2 dengan kacamata estetika - catat minimal 3 temuan",
                   "**Style guide 1 halaman** - palet, type scale, komponen + state, aturan spacing",
                   "**Mockup fidelity menengah, 2 layar** - Beranda + Layar Fitur Inti",
                   "**Draft proposal 1-2 halaman** - 7 komponen, kerja kelompok"],
                  sub="Urutannya tidak boleh dibalik: mockup tanpa style guide = setiap layar punya selera sendiri.")

    content_slide(prs, "Alat 1 - Komposisi & layout: grid 8-point",
                  ["Semua jarak adalah **kelipatan 4/8**: 4, 8, 16, 24, 32 px - tidak ada 13 px atau 21 px",
                   "**Visual grouping (proximity)** - yang berhubungan didekatkan, yang tidak dipisah",
                   "**Alignment konsisten** - tepi kiri elemen sejenis segaris; hierarki ditegaskan lewat jarak, bukan kekacauan"],
                  sub="Cek cepat wireframe Anda: tandai semua nilai gap - berapa persen yang bukan kelipatan 4/8?",
                  note="Minta 1-2 mahasiswa buka wireframe Tugas 1 mereka dan hitung gap. "
                       "Biasanya muncul 11, 15, 25 - itu temuan audit pertama.")

    table_slide(prs, "Alat 2 - Warna: palet 5 peran",
                ["Peran", "Dipakai untuk", "Contoh keputusan"],
                [["*Primary", "aksi utama (tombol daftar, CTA)", "satu warna saja - jangan dua tombol primer"],
                 ["*Secondary", "aksi pendukung", "outline / versi lebih tenang dari primary"],
                 ["*Background", "latar halaman", "netral, hampir putih"],
                 ["*Surface", "kartu, panel, navbar", "putih di atas background"],
                 ["*Accent", "sorotan jarang (badge, link aktif)", "paling janggal muncul - kalau sering muncul, bukan accent"]],
                col_w=[2.2, 4.4, 5.0], fs=15,
                sub="Tambahkan skala abu-abu Gray-50 s.d. Gray-900 untuk teks dan garis bantu. Jaga kontras teks terhadap latar.",
                note="Tegaskan: 5 peran ini yang diminta di Tugas 3a. Skala abu-abu bukan "
                     "hiasan - teks sekunder pakai Gray-600, disabled pakai Gray-400, dst.")

    content_slide(prs, "Alat 3 - Tipografi: type scale",
                  ["Tentukan **skala tetap**: H1-H6, Body, Caption - dan pegang itu",
                   "**Line-height memadai**: body sekitar 1.4-1.6; judul lebih rapat",
                   "**Maksimal 2 keluarga font** - satu sans-serif untuk UI sudah cukup untuk kelas proyek ini",
                   "Ukuran bukan selera: H1 = 32, H2 = 24, Body = 16, Caption = 12-13 adalah titik mulai yang aman"],
                  sub="Skala yang konsisten membuat halaman baru langsung terlihat 'anggota keluarga'.",
                  note="Kalau mahasiswa pakai Figma: buat text styles sekali di awal, "
                       "jangan set ukuran per teks.")

    content_slide(prs, "Alat 4 & 5 - Whitespace dan state",
                  ["**Whitespace mengarahkan perhatian** - halaman padat bukan tanda lengkap; itu tanda prioritas belum diputuskan",
                   "**Densitas informasi** diatur: satu layar satu tugas utama",
                   "**Komponen punya state**: default / hover / pressed / disabled - tentukan semuanya sejak style guide",
                   "Konsistensi bentuk: radius, border, shadow sama untuk semua kartu"],
                  sub="State adalah bagian yang paling sering hilang di pekerjaan mahasiswa - dan paling murah untuk dipikirkan duluan.",
                  note="Ingatkan Tugas 1: yang menyebut empty/error state mendapat nilai "
                       "tertinggi. Pola yang sama dinilai lagi di Tugas 3b.")

    # ============ PRAKTIK A ============
    section_slide(prs, "BAGIAN 2 - PRAKTIK A", "Style guide\n1 halaman",
                  "30-40 menit - kontrak visual kelompok Anda sebelum menyentuh mockup")

    content_slide(prs, "Isi style guide (4 blok, satu halaman)",
                  ["**Palet warna** - 5 swatch + skala abu-abu; tulis FUNGSI tiap warna, bukan hanya kotak warna",
                   "**Type scale** - H1-H6, Body, Caption + contoh ukuran dan line-height",
                   "**Komponen inti** - tombol primer/sekunder, input, kartu konten - tampilkan variasi state",
                   "**Spacing & grid** - tulis aturan 8-point dan satu contoh penerapannya di layout"],
                  sub="Output Tugas 3a: StyleGuide_P3.pdf (individu atau kelompok kecil).",
                  note="Dikerjakan sekarang 30 menit di kelas. Kelompok yang sudah punya "
                       "ide proyek langsung pakai konteks proyeknya - palet untuk aplikasi "
                       "kesehatan beda dengan palet marketplace.")

    # ============ PRAKTIK B ============
    section_slide(prs, "BAGIAN 3 - PRAKTIK B", "Mockup\n2 layar",
                  "Fidelity menengah - Beranda + Layar Fitur Inti, konsisten dengan style guide")

    content_slide(prs, "Mockup fidelity menengah - aturan main",
                  ["**Frame sesuai target**: desktop 1440 atau mobile 390 - pilih satu, jangan campur",
                   "**Auto Layout** untuk jarak antar elemen - konsisten otomatis, bukan dikejar manual",
                   "**Components & Variants** untuk tombol/kartu - satu komponen, beberapa state",
                   "**Cek kontras** teks vs latar; elemen interaktif menonjol tapi tidak berteriak"],
                  sub="Output Tugas 3b (individu): Mockup_P3_Home.pdf + Mockup_P3_FiturInti.pdf.",
                  note="Fidelity MENENGAH: warna dan tipografi nyata, tapi belum perlu foto "
                       "asli/ilustrasi penuh. Placeholder berwarna solid masih boleh.")

    # ============ PROPOSAL ============
    section_slide(prs, "BAGIAN 4", "Draft proposal\n7 komponen",
                  "Kerja kelompok - 1-2 halaman yang memaksa keputusan: apa dibangun, apa tidak, bagaimana tahu berhasil")

    table_slide(prs, "7 komponen proposal",
                ["Komponen", "Isi ringkas"],
                PROPOSAL7,
                col_w=[4.6, 7.0], fs=15,
                sub="Output Tugas 3c: AP1_P3_KelompokX_Proposal.pdf - satu berkas per kelompok.",
                note="Komponen 4 dan 5 paling menentukan nilai: Out-of-Scope membuktikan "
                     "kelompok berani memilih; risiko yang jujur lebih bernilai daripada "
                     "keyakinan kosong.")

    statement_slide(prs, "\"Kita tidak membangun X\"\nadalah kalimat paling mahal di proposal.",
                    "Out-of-Scope menjaga 5 minggu ke depan tidak bocor jadi segala-galanya. Metrik keberhasilan "
                    "membuat minggu depan ada angka untuk dibandingkan, bukan sekadar perasaan.",
                    note="Hubungkan ke Olsen P2: hipotesis nilai + uji paling murah dulu. "
                         "Proposal = kontrak mini kelompok dengan dosen.")

    table_slide(prs, "Rubrik penilaian Tugas 3 (100 poin)",
                ["Kriteria", "Poin"],
                RUBRIK,
                col_w=[9.6, 2.0], fs=15,
                sub="Kerapian & kepatuhan format termasuk NIM_Nama di berkas individu dan nama kelompok di berkas kelompok.",
                note="Rubrik ini juga rubrik AUDIT diri: sebelum submit, cek sendiri per "
                     "baris. Nilai di bawah 70 = tugas diulang per bagian yang lemah.")

    # ============ PENUTUP ============
    section_slide(prs, "PENUGASAN", "Tiga deliverable",
                  "Tenggat: Minggu, 4 Oktober 2026 pukul 23.55 - satu minggu, tiga berkas")

    table_slide(prs, "Tugas 3 - apa yang dikumpulkan",
                ["Bagian", "Siapa", "Berkas", "Poin rubrik"],
                TUGAS3,
                col_w=[2.8, 3.2, 4.4, 1.5], fs=14,
                sub="Tugas 3a boleh kelompok kecil (max 2 orang); 3b WAJIB individu; 3c satu berkas per kelompok.",
                note="Pelajaran Tugas 1 dibaca keras: sebagian tugas ini individu. Berkas "
                     "bersama atas nama 3 orang TIDAK menghitung untuk yang tidak "
                     "mengumpulkan. Ferdi dan Notopianus: berkas versi sendiri untuk Tugas 1 "
                     "masih bisa menyelamatkan nilai - batas revisi ikut tenggat.")

    content_slide(prs, "Refleksi cepat - jawab sebelum keluar",
                  ["Keputusan estetika apa yang paling meningkatkan **kejelasan tujuan pengguna**?",
                   "Bagian mana dari style guide yang paling membantu **konsistensi** saat membuat mockup?",
                   "Risiko/asumsi apa di proposal yang perlu **divalidasi paling awal** - dan bagaimana caranya?"],
                  sub="Balas di forum Exit-ticket Pertemuan 3, 2-3 kalimat per nomor - ini bagian dari kehadiran berkualitas.",
                  note="Buka forumnya di layar sekarang supaya semua tahu di mana menjawab. "
                       "Sasar minimal satu jawaban per orang hari ini - P2 nol posting.")

    links_slide(prs, "Tautan hari ini",
                [("Halaman materi Pertemuan 3 (eBelajar)", EB + "/mod/page/view.php?id=503175"),
                 ("Modul + slide Pertemuan 3 (Google Drive)", DRIVE_P3),
                 ("TUGAS 3: Style Guide, Mockup & Draft Proposal", EB + "/mod/assign/view.php?id=503174"),
                 ("Exit-ticket Pertemuan 3", EB + "/mod/forum/view.php?id=503173"),
                 ("Sheet kelompok (lengkapi bila belum tercatat)", "https://drive.google.com/open?id=12mbDubq6xxfcrlFEQir4aG4h-ICjM0g2B9EU1IuzJUU")],
                sub="Semua tautan juga ada di section Pertemuan 3 di eBelajar.")

    content_slide(prs, "Pratinjau Pertemuan 4",
                  ["**Teknologi front-end terkini (Bagian 1)** - pemilihan framework (mis. React/Vue)",
                   "**Struktur proyek awal** - dari mockup ke kerangka aplikasi",
                   "**Presentasi singkat proposal** - tiap kelompok; kelas memberi masukan",
                   "Yang belum menyelesaikan draft proposal: minggu depan sudah mempresentasikan"],
                  sub="Proposal yang dikumpulkan minggu ini langsung dipakai - bukan dokumen yang dikubur.",
                  note="Tutup dengan komitmen waktu: 25' presentasi tiap kelompok 3-4 menit "
                       "di P4. Kelompok tanpa proposal tetap presentasi dengan apa yang "
                       "ada - itu bukan hukuman, itu uji paling murah.")

    return prs


if __name__ == "__main__":
    from pptx import Presentation  # noqa: F401
    prs = build()
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "AP1_A_Pertemuan3_Ganjil2026.pptx")
    prs.save(p)
    print("OK %s (%d slides, %d KB)" % (p, len(prs.slides.__iter__.__self__._sldIdLst), os.path.getsize(p) // 1024))
