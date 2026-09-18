# -*- coding: utf-8 -*-
"""Deck Pertemuan 1 — Application Project I, kelas A (luring) & P (daring).

Isi materi SAMA persis untuk A dan P (permintaan user 8 Sep: "dibuat sama atau mirip
juga gpp"). Yang berbeda hanya: judul/jadwal, blok aturan kelas, blok kelompok vs
mandiri, dan tautan cepat (course id berbeda).
"""
import os
from deckkit import *

OUT = r"D:\documents\ebelajar\ganjil-2026-2027\application-project-1"
B = "https://ebelajar.stiki.ac.id"

CFG = {
    "A": dict(course=7278, kontrak=496744, drive=496745, materi=491622,
              forum_p1=491623, tugas1=491624, survey=491619, umum=491616,
              sub="Kelas A (Reguler) · Kamis 13.50–15.30 · Ruang A.2.1",
              tanggal="Kamis, 10 September 2026"),
    "P": dict(course=7426, kontrak=496746, drive=496747, materi=491570,
              forum_p1=491571, tugas1=491572, survey=491567, umum=491564,
              sub="Kelas P (Profesional) · daring penuh, mandiri (self-paced)",
              tanggal="Ganjil 2026/2027"),
}

PETA = [
    ["*1", "Prinsip desain UI", "Tugas 1"],
    ["2", "Ergonomi UI", "—"],
    ["3", "Estetika UI", "Tugas 2"],
    ["4", "Front-end 1: React/Vue/Angular", "—"],
    ["5", "Front-end 2: SPA & PWA", "Tugas 3"],
    ["6", "Iterasi & umpan balik 1", "—"],
    ["7", "Iterasi 2: A/B & usability", "Tugas 4"],
    ["*8", "UTS", "—"],
    ["9", "Minimum Viable Product", "Tugas 5"],
    ["10", "Manajemen proyek 1", "—"],
    ["11", "Manajemen proyek 2: Trello/Jira", "Tugas 6"],
    ["12", "Identifikasi masalah", "—"],
    ["13", "Pengambilan keputusan", "Tugas 7"],
    ["14", "Evaluasi mandiri 1", "Tugas 8"],
    ["15", "Evaluasi mandiri 2", "*Progress Project"],
    ["*16", "UAS — Proyek Akhir", "—"],
]


def build(mode):
    c = CFG[mode]
    A = mode == "A"
    prs = new_deck()

    title_slide(prs, "PERTEMUAN 1 · APPLICATION PROJECT I",
                "Dari Ide ke Antarmuka\nyang Bisa Dipakai Orang",
                "Prinsip desain UI: hierarki visual, konsistensi, keterbacaan",
                "Mukhlis Amien, M.Kom.  ·  IF24KB33  ·  " + c["sub"])

    # ══ BAGIAN 1 — KONTRAK ══
    section_slide(prs, "BAGIAN 1", "Kontrak Kuliah",
                  "Aturan main disepakati di depan, bukan diperdebatkan di akhir semester")

    table_slide(prs, "Identitas mata kuliah", ["", ""],
                [["*Mata Kuliah", "Application Project I (IF24KB33) · 2 SKS · Semester 5"],
                 ["*Program Studi", "Informatika"],
                 ["*Jadwal", "Kamis 13.50–15.30, Ruang A.2.1" if A else "Daring penuh — dikerjakan mandiri, tanpa tatap muka"],
                 ["*Periode", "7 September 2026 – 28 Februari 2027"],
                 ["*Dosen", "Mukhlis Amien, M.Kom."],
                 ["*CPL", "CPL09 (UI & aplikasi interaktif) · CPL10 (kinerja mandiri)"],
                 ["*CPMK", "CPMK092 · CPMK121"]],
                col_w=[3, 9], fs=17)

    statement_slide(prs, "Yang dinilai bukan\nseberapa ramai tampilannya.",
                    "Melainkan seberapa masuk akal keputusan desain Anda — dan seberapa jujur Anda mengujinya.",
                    note="Ini kalimat kunci mata kuliah. Ulangi di akhir pertemuan.")

    table_slide(prs, "Lima fase satu semester", ["Fase", "Pertemuan", "Fokus"],
                [["*1 — Merancang", "1–3", "Prinsip UI, ergonomi, estetika, wireframe"],
                 ["*2 — Membangun", "4–5", "Front-end terkini, SPA & PWA, komponen antarmuka"],
                 ["*3 — Menguji", "6–7", "Iterasi desain, A/B testing, usability testing"],
                 ["*4 — Mengelola", "9–13", "MVP, perencanaan proyek, alat bantu, keputusan"],
                 ["*5 — Mengevaluasi", "14–16", "Evaluasi mandiri, progress project, proyek akhir"]],
                col_w=[3, 2, 7], fs=17,
                sub="Setiap fase berakhir dengan sesuatu yang bisa ditunjukkan, bukan sekadar dipahami.")

    dual_table_slide(prs, "Peta 16 pertemuan", ["#", "Topik", "Tugas"], PETA,
                     col_w=[1, 6, 3], fs=13,
                     sub="Tugas 1–8 bukan latihan terpisah — tiap tugas adalah satu potong nyata dari proyek Anda.")

    table_slide(prs, "Komponen dan bobot penilaian", ["Komponen", "Bentuk", "Bobot"],
                [["*Partisipatif", "Keaktifan forum + exit-ticket" if A else "Penyelesaian aktivitas & keaktifan forum", "10%"],
                 ["*Observasi", "Kerja studio: Tugas 1–4", "20%"],
                 ["*Unjuk Kerja", "Tugas 5 + Progress Project", "20%"],
                 ["*Tugas individu", "Tugas 6–8", "20%"],
                 ["*UTS", "Ujian Tengah Semester", "15%"],
                 ["*UAS", "Proyek Akhir: prototipe + laporan", "15%"],
                 ["*TOTAL", "", "*100%"]],
                col_w=[3, 6.5, 1.8], fs=17,
                sub="Pendekatan Outcome-Based Education (OBE), sesuai RPS mata kuliah.",
                note="Perhatikan: 70% nilai datang dari kerja sepanjang semester, hanya 30% dari UTS+UAS.")

    dual_table_slide(prs, "Bobot per aktivitas — ini yang dipakai saat menilai",
                     ["Aktivitas", "Bobot"],
                     [["Partisipasi (forum tiap pertemuan)", "10%"],
                      ["Tugas 1 — Wireframe halaman utama", "3%"],
                      ["Tugas 2 — Brainstorming proyek", "6%"],
                      ["Tugas 3 — Proposal / komponen antarmuka", "6%"],
                      ["Tugas 4 — Siklus iterasi desain", "5%"],
                      ["Tugas 5 — Prototipe fungsional MVP", "8%"],
                      ["Tugas 6 — Simulasi pengelolaan proyek", "9%"],
                      ["Tugas 7 — Studi kasus keputusan", "2%"],
                      ["Tugas 8 — Laporan evaluasi mandiri", "9%"],
                      ["*Progress Project", "*12%"],
                      ["*UTS", "*15%"],
                      ["*UAS — Proyek Akhir", "*15%"]],
                     col_w=[7, 2], fs=14,
                     sub="Jumlahnya persis 100%. Tidak ada aktivitas tanpa bobot, dan tidak ada bobot tanpa aktivitas.",
                     note="Kalau ditanya kenapa tidak ada pos Quiz: mata kuliah ini tidak punya kuis selain UTS, "
                          "jadi 10% pos Quiz di RPS dilebur ke Tugas individu. Dijelaskan di Kontrak Kuliah bagian 6.")

    if A:
        content_slide(prs, "Aturan kelas",
                      ["**Kehadiran minimal 75%** dari pertemuan terlaksana untuk berhak ikut UAS",
                       "Toleransi terlambat **15 menit**; **3× terlambat = 1× tidak hadir**",
                       "**Laptop wajib** mulai Pertemuan 2 — 55 menit tiap pertemuan dipakai bekerja",
                       "Siapkan akun **Figma** (atau Adobe XD) dan lingkungan front-end",
                       "Semua tugas lewat **eBelajar** — bukan WhatsApp, bukan email",
                       "Nama berkas: **AP1_P<pertemuan>_NIM_Nama_<Topik>**",
                       "__",
                       "**Tenggat: Minggu 23.55** pada minggu berikutnya setelah tugas diberikan",
                       "Terlambat: **−10% per hari**, maksimal 3 hari. Lewat itu dinilai 0 — **tapi tetap wajib dikumpulkan**"],
                      body_size=19)
        content_slide(prs, "Kerja kelompok",
                      ["Proyek dikerjakan **berkelompok**; kelompok dibentuk **hari ini**",
                       "Kelompok **tidak berubah** sepanjang semester, kecuali disetujui dosen",
                       "Setiap anggota wajib punya **bagian yang bisa ditunjuk**",
                       (1, "Nilai kelompok bisa diturunkan **per orang** kalau kontribusinya tidak terlihat"),
                       "__",
                       "Yang dinilai bukan siapa paling sibuk, melainkan **apakah pekerjaan Anda ada jejaknya**"],
                      body_size=20)
    else:
        content_slide(prs, "Cara kelas ini berjalan",
                      ["Tidak ada tatap muka. Tiap pertemuan berisi paket yang sama:",
                       (1, "**Baca** halaman materi — ini yang membuka pertemuan berikutnya"),
                       (1, "**Kerjakan** tugas pertemuan itu, unggah lewat eBelajar"),
                       (1, "**Diskusikan** di forum — balas minimal satu tulisan teman"),
                       "__",
                       "**Semua sudah terbuka sejak hari pertama, dan tidak ada tenggat sama sekali**",
                       "Pertemuan N+1 terbuka setelah materi pertemuan N ditandai selesai dibaca",
                       (1, "Kalau pertemuan berikutnya terkunci, hampir selalu sebabnya ini")],
                      body_size=19)
        content_slide(prs, "Kerja mandiri — dan satu peringatan",
                      ["Seluruh tugas kelas P dikerjakan **perorangan**",
                       (1, "Termasuk yang judulnya masih menyebut *kelompok* — itu warisan penamaan kelas reguler"),
                       "Proyek akhir juga perorangan; lingkupnya boleh lebih kecil, asal **utuh dari rancangan sampai prototipe jalan**",
                       "__",
                       "**Peringatan yang serius:** menumpuk 16 pertemuan di bulan terakhir adalah cara paling umum gagal di kelas ini.",
                       "Ritme yang aman: **satu pertemuan per minggu**."],
                      body_size=19)

    content_slide(prs, "Integritas akademik",
                  ["**Diskusi dianjurkan, penyalinan dilarang**",
                   "Dua berkas identik atau nyaris identik: **keduanya dinilai 0** — tanpa mencari siapa menyalin siapa",
                   "Setiap klaim di laporan harus bisa Anda pertanggungjawabkan **saat ditanya lisan**",
                   (1, "Klaim yang tidak bisa dijelaskan pemiliknya dinilai 0, meskipun hasilnya bagus"),
                   "Aset pihak ketiga (ikon, template, foto, komponen UI) **boleh dipakai** — asal lisensinya mengizinkan dan **sumbernya disebut**"],
                  body_size=19)

    section_slide(prs, "KEBIJAKAN AI", "AI adalah alat untuk Anda mengerti,\nbukan pengganti Anda mengerti")

    content_slide(prs, "Cara memakai AI yang membuat Anda paham",
                  ["Minta AI **menjelaskan** sampai Anda bisa mengulanginya **tanpa membuka AI**",
                   "Minta AI **menanyai balik** rancangan UI Anda — biarkan ia mencari lubangnya",
                   "Minta **dua pendekatan berbeda**, lalu **Anda** yang memutuskan mana dipakai dan mengapa",
                   "Pakai untuk **mencari bug**, lalu perbaiki sendiri supaya tahu letak salahnya",
                   "**Tutup AI-nya**, lalu jelaskan ulang pekerjaan Anda dari nol"],
                  sub="Kelas ini tidak melarang AI. Yang diatur cara memakainya.",
                  body_size=20)

    table_slide(prs, "Batasnya", ["", ""],
                [["*BOLEH", "Boilerplate kode front-end · debugging error · menjelaskan konsep · merapikan bahasa laporan · membangkitkan varian ide desain untuk Anda seleksi"],
                 ["*TIDAK BOLEH", "Menyerahkan desain/analisis/kesimpulan yang belum Anda verifikasi · kode yang belum pernah Anda jalankan · mengaku menguji ke pengguna padahal umpan baliknya dikarang"],
                 ["*WAJIB", "Disclosure di akhir laporan: alat apa, untuk bagian mana. Satu paragraf cukup"]],
                col_w=[2.2, 9.8], fs=15)

    statement_slide(prs, "Kalau AI-nya dimatikan sekarang,\napakah Anda masih bisa menjelaskan\npekerjaan Anda?",
                    "Kalau ya — Anda memakainya dengan benar. Kalau tidak — Anda sedang menyewa pemahaman orang lain.",
                    color=RED,
                    note="Diamkan sejenak. Ini uji mandiri yang dipakai sepanjang semester.")

    # ══ BAGIAN 2 — MATERI ══
    section_slide(prs, "BAGIAN 2", "Prinsip Desain Antarmuka",
                  "Hierarki visual · Konsistensi · Keterbacaan")

    statement_slide(prs, "Setiap kali Anda salah pencet,\nitu bukan kebodohan Anda.",
                    "Itu kegagalan desain. Dan hari ini Anda pindah posisi: dari yang salah pencet, jadi yang bertanggung jawab.",
                    note="Hook. Pancing 2–3 contoh dari mahasiswa: tombol yang salah tekan, form yang bikin frustrasi.")

    content_slide(prs, "UI dan UX — beda, dan sering tertukar",
                  ["**UI (User Interface)** — apa yang dilihat dan disentuh: tata letak, warna, tipografi, tombol",
                   "**UX (User Experience)** — apa yang **dirasakan** sepanjang memakai: cepat/lambat, yakin/bingung, selesai/menyerah",
                   "__",
                   "UI yang cantik **tidak menjamin** UX yang baik. Tapi UI yang buruk **hampir selalu** merusak UX.",
                   "__",
                   "Di mata kuliah ini Anda mengerjakan keduanya — tapi mulai dari UI, karena itu yang bisa langsung diuji ke orang."],
                  body_size=20)

    content_slide(prs, "Prinsip 1 — Hierarki visual",
                  ["Mata pengguna **tidak memindai semua** elemen. Ia mencari yang paling menonjol lebih dulu.",
                   "Alat untuk mengatur urutan itu:",
                   (1, "**Ukuran** — makin besar, makin dulu dilihat"),
                   (1, "**Kontras** — warna yang berbeda tajam menarik mata"),
                   (1, "**Posisi** — kiri-atas dibaca lebih dulu (untuk aksara Latin)"),
                   (1, "**Ruang kosong** — elemen yang diberi jarak terasa lebih penting"),
                   "__",
                   "**Uji cepatnya:** picingkan mata sampai layar buram. Yang masih terbaca = yang Anda tonjolkan.",
                   "Kalau yang tersisa bukan aksi utamanya, hierarki Anda salah."],
                  body_size=19,
                  note="Peragakan squint test langsung di layar dengan satu situs nyata.")

    content_slide(prs, "Prinsip 2 — Konsistensi",
                  ["Hal yang sama harus **terlihat sama** dan **berperilaku sama** di seluruh aplikasi",
                   (1, "Satu gaya tombol utama, bukan lima"),
                   (1, "Satu pola penamaan: *Simpan* di semua halaman, bukan *Simpan* / *Kirim* / *OK* bergantian"),
                   (1, "Satu posisi tetap untuk aksi yang sama"),
                   "__",
                   "**Kenapa penting:** konsistensi membuat pengguna bisa **menebak**. Menebak dengan benar = tidak perlu berpikir.",
                   "__",
                   "Konsistensi **eksternal** juga berlaku: ikon keranjang, tanda silang untuk tutup — jangan dilawan tanpa alasan kuat."],
                  body_size=19)

    content_slide(prs, "Prinsip 3 — Keterbacaan",
                  ["**Kontras teks** cukup terhadap latar (acuan WCAG: rasio **4.5:1** untuk teks biasa)",
                   "**Ukuran** minimal nyaman di layar kecil — jangan 11 px untuk teks isi",
                   "**Panjang baris** 45–75 karakter; terlalu lebar membuat mata kehilangan baris",
                   "**Jarak antarbaris** longgar (±1,5×) supaya paragraf tidak terlihat padat",
                   "**Hindari teks di atas foto ramai** tanpa lapisan gelap/terang",
                   "__",
                   "Uji paling murah: buka rancangan Anda **di ponsel, di bawah sinar matahari**. Kalau tak terbaca, itu jawabannya."],
                  body_size=19)

    content_slide(prs, "Bongkar satu antarmuka bersama",
                  ["Ambil satu aplikasi yang Anda pakai tiap hari",
                   "Jawab empat pertanyaan:",
                   (1, "**Apa aksi utama** di layar ini? Apakah ia yang paling menonjol?"),
                   (1, "**Berapa gaya tombol** berbeda yang Anda hitung?"),
                   (1, "**Bisakah teksnya dibaca** sambil berjalan?"),
                   (1, "**Apa yang bikin ragu** — dan apa yang membuat ragu itu muncul?"),
                   "__",
                   "Ini kerangka yang akan Anda pakai lagi di Pertemuan 6–7 saat menguji desain sendiri ke pengguna nyata."],
                  body_size=19,
                  note="Sesi diskusi 10 menit. Minta 2 kelompok melaporkan temuan.")

    content_slide(prs, "Wireframe — dan kenapa harus jelek",
                  ["**Wireframe** = kerangka halaman: kotak, garis, label. **Tanpa warna, tanpa gaya, tanpa gambar asli**",
                   "Tujuannya menguji **struktur dan prioritas** — bukan keindahan",
                   "__",
                   "**Kenapa sengaja dibuat jelek?** Karena rancangan yang sudah rapi membuat orang enggan mengkritiknya, dan Anda enggan membuangnya.",
                   "Wireframe yang jelek **murah dibuang** — dan di fase ini, dibuang itu justru kemajuan.",
                   "__",
                   "Boleh di kertas, boleh di Figma. Yang dinilai isinya, bukan alatnya."],
                  body_size=19)

    content_slide(prs, "Anatomi wireframe yang layak dinilai",
                  ["**Header** — identitas + navigasi utama",
                   "**Aksi utama** — satu, dan paling menonjol",
                   "**Konten inti** — apa yang benar-benar dicari pengguna",
                   "**Aksi sekunder** — ada, tapi tidak berebut perhatian",
                   "**Keadaan kosong / error** — sering dilupakan, padahal paling sering dilihat pengguna baru",
                   "__",
                   "Beri **anotasi**: panah + satu kalimat yang menjelaskan *kenapa* elemen ini diletakkan di sini.",
                   "Anotasi itulah yang membedakan wireframe dari coretan."],
                  body_size=19)

    content_slide(prs, "Lima kesalahan yang paling sering muncul",
                  ["Menaruh **semua** yang penting jadi menonjol — akhirnya tidak ada yang menonjol",
                   "Memakai **lorem ipsum** untuk teks yang sebenarnya menentukan tata letak",
                   "Merancang hanya keadaan **ideal** — lupa keadaan kosong, gagal, dan memuat",
                   "Menyalin tata letak aplikasi terkenal **tanpa tahu alasannya**",
                   "Merancang di layar besar saja, lalu kaget saat dibuka di ponsel",
                   "__",
                   "Kelimanya akan diperiksa saat penilaian Tugas 1."],
                  body_size=19)

    # ══ BAGIAN 3 — KERJA ══
    if A:
        section_slide(prs, "BAGIAN 3", "Studio 55 Menit",
                      "Kelompok dibentuk, wireframe pertama dimulai hari ini juga")
        content_slide(prs, "Pembentukan kelompok proyek",
                      ["Kelompok **3–4 orang**, dibentuk hari ini dan **tetap sampai akhir semester**",
                       "Sepakati di dalam kelompok:",
                       (1, "**Ketua** — bukan yang paling pintar, tapi yang paling rajin menagih"),
                       (1, "**Kanal komunikasi** dan **jadwal pertemuan mingguan**"),
                       (1, "**Ide awal produk** — boleh berubah, tapi harus ada hari ini"),
                       "__",
                       "Data kelompok diunggah sebagai **Tugas 1b** — lihat aktivitas TUGAS 1 di eBelajar."],
                      body_size=19)
        content_slide(prs, "Studio hari ini — 55 menit",
                      ["**10'** — tentukan satu masalah nyata yang ingin kelompok Anda selesaikan",
                       "**10'** — tulis **satu kalimat** siapa penggunanya dan apa yang ingin ia capai",
                       "**25'** — sketsa wireframe **halaman utama** di kertas",
                       "**10'** — tukar dengan kelompok sebelah, minta mereka menebak apa aksi utamanya",
                       "__",
                       "Kalau mereka **salah menebak**, itu temuan paling berharga hari ini — bukan kegagalan."],
                      body_size=20,
                      note="Berkeliling per kelompok. Fokus pertanyaan: siapa penggunanya, apa aksi utamanya.")
    else:
        section_slide(prs, "BAGIAN 3", "Kerja Anda Minggu Ini",
                      "Tanpa kelas, tetap ada urutan yang harus dijalani")
        content_slide(prs, "Rencana kerja mandiri Pertemuan 1",
                      ["**Baca** halaman materi Pertemuan 1 di eBelajar sampai selesai",
                       "**Tentukan** satu masalah nyata yang ingin Anda selesaikan lewat sebuah produk web",
                       "**Tulis satu kalimat**: siapa penggunanya, dan apa yang ingin ia capai",
                       "**Sketsa** wireframe halaman utama — boleh kertas difoto, boleh Figma",
                       "**Minta satu orang** menebak apa aksi utamanya, tanpa Anda jelaskan lebih dulu",
                       "__",
                       "Kalau ia **salah menebak**, catat itu — jadi bahan paragraf refleksi Tugas 1."],
                      body_size=19)
        content_slide(prs, "Ganti kelompok: mitra uji",
                      ["Kelas P tidak berkelompok. Tapi **desain tidak bisa diuji sendirian.**",
                       "Cari **satu orang mana pun** — teman, keluarga, rekan kerja — sebagai mitra uji Anda semester ini",
                       (1, "Ia tidak perlu paham desain. Justru lebih baik kalau tidak"),
                       (1, "Tugasnya cuma satu: mencoba, lalu mengatakan apa yang membingungkan"),
                       "__",
                       "Di Pertemuan 6–7 orang inilah yang jadi sumber umpan balik Anda."],
                      body_size=19)

    section_slide(prs, "BAGIAN 4", "Tugas 1", "Wireframe halaman utama")

    content_slide(prs, "Tugas 1 — apa yang dikumpulkan",
                  ["**1 berkas wireframe** halaman utama (PDF atau PNG)",
                   "**1 paragraf** yang menjelaskan penerapan **hierarki visual, konsistensi, dan keterbacaan** pada rancangan Anda",
                   (1, "Bukan mendeskripsikan gambarnya — melainkan **alasan** setiap keputusan"),
                   ] + ([(0, "**Tugas 1b — Data kelompok**: nama kelompok, ketua, anggota, kanal komunikasi, komitmen pertemuan mingguan")] if A else
                        [(0, "Sebutkan juga **siapa mitra uji** Anda dan apa yang ia salah tebak")]) +
                  ["__",
                   "Nama berkas: **AP1_P1_NIM_Nama_Wireframe.pdf**",
                   "Dikumpulkan lewat **eBelajar**, aktivitas **TUGAS 1** — bukan WhatsApp, bukan email"],
                  body_size=19)

    table_slide(prs, "Yang diperiksa saat menilai", ["Aspek", "Pertanyaan penilai"],
                [["*Hierarki visual", "Apakah aksi utama benar-benar paling menonjol?"],
                 ["*Konsistensi", "Apakah elemen sejenis diperlakukan sama?"],
                 ["*Keterbacaan", "Apakah teks nyaman dibaca di layar kecil?"],
                 ["*Anotasi", "Apakah ada alasan di balik keputusan, bukan sekadar label?"],
                 ["*Kejujuran", "Apakah keadaan kosong/error ikut dipikirkan?"]],
                col_w=[3, 9], fs=17,
                sub="Bobot Tugas 1: 5% (sesuai RPS). Kecil — tapi ini fondasi seluruh proyek Anda.")

    if A:
        content_slide(prs, "Tenggat",
                      ["**Minggu, 20 September 2026, pukul 23.55**",
                       "Terlambat: **−10% per hari**, maksimal 3 hari",
                       "Lewat 3 hari dinilai 0, **tapi tetap wajib dikumpulkan**",
                       "__",
                       "Aturan umum: tugas Pertemuan N dikumpulkan **Minggu 23.55 minggu berikutnya**"],
                      body_size=20)
    else:
        content_slide(prs, "Tenggat: tidak ada",
                      ["Kelas ini *self-paced*. **Tidak ada satu pun tanggal pengumpulan.**",
                       "Tidak ada penalti keterlambatan — karena tidak ada yang bisa disebut terlambat",
                       "Satu-satunya batas nyata: **akhir masa perkuliahan, 28 Februari 2027**, karena nilai harus masuk",
                       (1, "Itu batas administratif kampus, bukan tenggat tugas"),
                       "__",
                       "**Konsekuensinya pindah ke tangan Anda.** Tanpa tenggat, tidak ada yang mengingatkan selain diri sendiri.",
                       "Ritme aman: **satu pertemuan per minggu**. Menumpuk 16 pertemuan di akhir gagal bukan karena aturannya — tapi karena waktunya memang tidak cukup."],
                      body_size=19)

    content_slide(prs, "Exit-ticket sebelum Anda pergi" if A else "Sebelum lanjut ke Pertemuan 2",
                  ["Tulis di forum diskusi Pertemuan 1:",
                   (1, "**Satu** antarmuka yang menurut Anda buruk, dan **prinsip mana** yang dilanggarnya"),
                   (1, "**Satu** hal dari hari ini yang ingin Anda coba di proyek sendiri"),
                   "Balas **minimal satu** tulisan teman — sebutkan satu hal yang belum ia pertimbangkan",
                   "__",
                   "Isi juga **Survey Awal Mahasiswa** — supaya saya tahu titik berangkat Anda."],
                  body_size=20)

    content_slide(prs, "Siapkan sebelum Pertemuan 2",
                  ["Akun **Figma** (gratis) — dipakai mulai Pertemuan 2",
                   "Baca **Dan Olsen — The Lean Product Playbook** (rujukan utama Tugas 1)",
                   "Kendala teknis → tanyakan di **forum Diskusi Umum**, bukan japri",
                   "__",
                   "Pertemuan 2: **ergonomi dan aksesibilitas** — kenapa desain yang nyaman untuk sebagian orang bisa menutup pintu bagi yang lain."],
                  body_size=20)

    links_slide(prs, "Tautan cepat — klik langsung dari slide ini",
                [("Kursus Application Project I %s di eBelajar" % mode, "%s/course/view.php?id=%d" % (B, c["course"])),
                 ("Kontrak Kuliah (versi lengkap)", "%s/mod/page/view.php?id=%d" % (B, c["kontrak"])),
                 ("Bahan Pertemuan 1 di Google Drive (slide & pendukung)", "%s/mod/url/view.php?id=%d" % (B, c["drive"])),
                 ("Materi Pertemuan 1: Prinsip Desain UI", "%s/mod/page/view.php?id=%d" % (B, c["materi"])),
                 ("Forum Diskusi Pertemuan 1", "%s/mod/forum/view.php?id=%d" % (B, c["forum_p1"])),
                 ("TUGAS 1 — unggah di sini", "%s/mod/assign/view.php?id=%d" % (B, c["tugas1"])),
                 ("Survey Awal Mahasiswa", "%s/mod/choice/view.php?id=%d" % (B, c["survey"])),
                 ("Forum Diskusi Umum — tempat bertanya", "%s/mod/forum/view.php?id=%d" % (B, c["umum"]))],
                sub="Salindia ini tersimpan di Google Drive; semua tautan aktif saat dibuka di PowerPoint atau Google Slides.")

    statement_slide(prs, "Desain yang baik tidak terlihat.\nYang terlihat cuma: orang berhasil.",
                    "Sampai jumpa di Pertemuan 2 — %s" % ("Kamis depan" if A else "kapan pun Anda siap"))

    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "AP1_%s_Pertemuan1_Ganjil2026.pptx" % mode)
    prs.save(p)
    print("AP1 %s: %d slide -> %s" % (mode, len(prs.slides._sldIdLst), p))


if __name__ == "__main__":
    build("A")
    build("P")
