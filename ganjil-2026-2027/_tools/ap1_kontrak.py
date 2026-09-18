# -*- coding: utf-8 -*-
"""Kontrak Kuliah Application Project I (IF24KB33) — kelas A (luring) & P (daring).

Isi A dan P sengaja dibuat SAMA persis kecuali blok yang memang tidak bisa sama
(jadwal, kehadiran vs penyelesaian aktivitas, tenggat, kerja kelompok).
Sumber fakta: RPS resmi (Drive 1YfhxTu_p3GTGI6QUbsLeLsmyRr6UP9p0) + halaman
"RPS dan Capaian Pembelajaran" di eBelajar + SAKTI (jadwal).
"""
import io, os

TBL = 'border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;width:100%;"'
HDR = 'style="background:#f0f3f7;"'
OUT = r"D:\documents\ebelajar\ganjil-2026-2027\application-project-1"

# ── fakta bersama ────────────────────────────────────────────────────────────
PETA = [
    ("1",  "Prinsip-prinsip desain antarmuka pengguna (UI)", "0921", "Tugas 1 &mdash; Wireframe halaman utama", "3%"),
    ("2",  "Ergonomi dalam desain UI", "0922", "&mdash;", "&mdash;"),
    ("3",  "Estetika dalam desain UI", "0922", "Tugas 2 &mdash; Brainstorming proyek", "6%"),
    ("4",  "Teknologi front-end terkini (1): React/Vue/Angular", "0923", "&mdash;", "&mdash;"),
    ("5",  "Teknologi front-end terkini (2): SPA &amp; PWA", "0923", "Tugas 3", "6%"),
    ("6",  "Iterasi desain &amp; umpan balik pengguna (1)", "0924", "&mdash;", "&mdash;"),
    ("7",  "Iterasi desain &amp; umpan balik pengguna (2): A/B &amp; usability testing", "0924", "Tugas 4 &mdash; Siklus iterasi desain", "5%"),
    ("8",  "<strong>Ujian Tengah Semester (UTS)</strong>", "&mdash;", "UTS", "15%"),
    ("9",  "Minimum Viable Product (MVP)", "0925", "Tugas 5 &mdash; Prototipe fungsional MVP", "8%"),
    ("10", "Perencanaan &amp; manajemen proyek (1): Eisenhower, Agile", "1211", "&mdash;", "&mdash;"),
    ("11", "Perencanaan &amp; manajemen proyek (2): Trello/Asana/Jira", "1211", "Tugas 6 &mdash; Simulasi pengelolaan proyek", "9%"),
    ("12", "Identifikasi masalah dalam proyek", "1212", "&mdash;", "&mdash;"),
    ("13", "Pengambilan keputusan dalam proyek", "1212", "Tugas 7 &mdash; Studi kasus pengambilan keputusan", "2%"),
    ("14", "Evaluasi mandiri hasil kerja (1)", "1213", "Tugas 8 &mdash; Laporan evaluasi mandiri", "9%"),
    ("15", "Evaluasi mandiri hasil kerja (2)", "1213", "<strong>Progress Project</strong>", "12%"),
    ("16", "<strong>Ujian Akhir Semester (UAS)</strong>", "&mdash;", "Pengumpulan Proyek Akhir", "15%"),
]
SUBCPMK = [
    ("Sub-CPMK0921", "Merancang dan mengimplementasikan desain antarmuka pengguna (UI) yang efektif dan sesuai kebutuhan pengguna."),
    ("Sub-CPMK0922", "Mengintegrasikan prinsip ergonomi dan estetika dalam pengembangan UI."),
    ("Sub-CPMK0923", "Memanfaatkan teknologi front-end terkini dalam pembuatan aplikasi interaktif berbasis web."),
    ("Sub-CPMK0924", "Melakukan iterasi desain berbasis umpan balik pengguna untuk meningkatkan fungsionalitas dan UX."),
    ("Sub-CPMK0925", "Menghasilkan prototipe fungsional produk digital berbasis web sebagai bagian dari MVP."),
    ("Sub-CPMK1211", "Merencanakan dan mengatur tahapan kerja secara mandiri untuk menyelesaikan tugas dan proyek."),
    ("Sub-CPMK1212", "Mengidentifikasi masalah dan mengambil keputusan yang tepat selama pengembangan proyek."),
    ("Sub-CPMK1213", "Melakukan evaluasi mandiri terhadap hasil kerja untuk meningkatkan kualitas dan efektivitas solusi."),
]

PENILAIAN = [
    ("Partisipatif", "Keaktifan forum tiap pertemuan + exit-ticket", "10%"),
    ("Observasi", "Kerja studio: Tugas 1&ndash;4", "20%"),
    ("Unjuk Kerja", "Presentasi &amp; proyek: Tugas 5 + Progress Project", "20%"),
    ("Tugas individu", "Tugas 6&ndash;8", "20%"),
    ("UTS", "Ujian Tengah Semester", "15%"),
    ("UAS", "Proyek Akhir: prototipe + laporan", "15%"),
]

# bobot per aktivitas — jumlahnya PERSIS 100, proporsi antar-tugas mengikuti RPS
BOBOT = [
    ("&mdash;", "Partisipasi: forum tiap pertemuan (+ exit-ticket kelas A)", "10%", "Partisipatif"),
    ("Tugas 1", "Wireframe halaman utama", "3%", "Observasi"),
    ("Tugas 2", "Brainstorming proyek", "6%", "Observasi"),
    ("Tugas 3", "Proposal / implementasi komponen antarmuka", "6%", "Observasi"),
    ("Tugas 4", "Siklus iterasi desain berbasis umpan balik", "5%", "Observasi"),
    ("Tugas 5", "Prototipe fungsional MVP", "8%", "Unjuk Kerja"),
    ("Tugas 6", "Simulasi pengelolaan proyek digital", "9%", "Tugas individu"),
    ("Tugas 7", "Studi kasus pengambilan keputusan", "2%", "Tugas individu"),
    ("Tugas 8", "Laporan evaluasi mandiri", "9%", "Tugas individu"),
    ("Progress Project", "Laporan &amp; presentasi kemajuan proyek", "12%", "Unjuk Kerja"),
    ("UTS", "Ujian Tengah Semester", "15%", "UTS"),
    ("UAS", "Proyek Akhir: prototipe + laporan", "15%", "UAS"),
]

PUSTAKA_UTAMA = [
    "Ries, E. (2011). <em>The Lean Startup: How Today&rsquo;s Entrepreneurs Use Continuous Innovation to Create Radically Successful Businesses.</em>",
    "Olsen, D. (2015). <em>The Lean Product Playbook: How to Innovate with Minimum Viable Products and Rapid Customer Feedback.</em> &mdash; <strong>rujukan Tugas 1</strong>",
    "Knapp, J., Zeratsky, J., dkk. (2016). <em>Sprint: How to Solve Big Problems and Test New Ideas in Just Five Days.</em>",
    "Grossman, S. (2017). <em>Minimum Viable Product: Master Early Learning and Develop an MVP with Scrum.</em>",
]
PUSTAKA_PENDUKUNG = [
    "Maurya, A. (2012). <em>Running Lean: Iterate from Plan A to a Plan That Works.</em>",
    "Cagan, M. (2018). <em>Inspired: How to Create Products Customers Love.</em>",
    "Eyal, N. (2014). <em>Hooked: How to Build Habit-Forming Products.</em>",
]

AI_POLICY = u"""
<h4>Kebijakan Penggunaan AI</h4>
<p>Alat bantu AI (ChatGPT, Claude, Copilot, v0, Figma AI, dsb.) adalah bagian wajar dari pekerjaan seorang
pengembang produk digital. Kelas ini <strong>tidak melarangnya</strong>. Prinsipnya satu:
<strong>AI adalah alat untuk Anda mengerti, bukan pengganti Anda mengerti.</strong></p>

<h5>Cara memakai AI yang membuat Anda paham</h5>
<ul>
<li>Minta AI <strong>menjelaskan</strong> sampai Anda bisa mengulanginya sendiri tanpa membuka AI.</li>
<li>Minta AI <strong>menanyai balik</strong> Anda tentang rancangan UI Anda &mdash; biarkan ia mencari lubangnya.</li>
<li>Minta <strong>dua pendekatan berbeda</strong>, lalu <strong>Anda</strong> yang memutuskan mana yang dipakai dan mengapa.</li>
<li>Pakai untuk <strong>mencari bug</strong>, lalu perbaiki sendiri supaya Anda tahu letak salahnya.</li>
<li>Tutup AI-nya, lalu jelaskan ulang pekerjaan Anda dari nol. Kalau macet, berarti belum paham.</li>
</ul>

<h5>Batasnya</h5>
<table %s>
<tr><td style="background:#eef7ee;width:16%%;"><strong>BOLEH</strong></td><td>Boilerplate kode front-end, debugging pesan error,
menjelaskan konsep yang belum dipahami, merapikan bahasa laporan, membangkitkan varian ide desain untuk Anda seleksi</td></tr>
<tr><td style="background:#fdeeee;"><strong>TIDAK BOLEH</strong></td><td>Menyerahkan desain, analisis, atau kesimpulan
yang belum Anda verifikasi sendiri; menyerahkan kode yang belum pernah Anda jalankan; mengaku menguji ke pengguna
padahal umpan baliknya dikarang</td></tr>
<tr><td style="background:#fdf6e3;"><strong>WAJIB</strong></td><td><strong>Disclosure</strong> di akhir laporan/berkas:
alat apa yang dipakai, untuk bagian mana. Satu paragraf singkat sudah cukup</td></tr>
</table>

<p>Alasannya nyata. Yang paling sering rusak dari pemakaian AI tanpa verifikasi bukan kodenya &mdash; kode yang salah
akan gagal jalan dan langsung ketahuan. Yang rusak adalah <strong>kalimat yang terdengar benar padahal isinya
karangan</strong>: alasan desain yang tidak pernah diuji, umpan balik pengguna yang tidak pernah ada, rujukan yang
tidak pernah terbit. Ini terjadi di dunia nyata sampai ke tingkat jurnal internasional, dan akibatnya bukan sekadar
nilai turun melainkan reputasi.</p>

<h5>Uji mandiri</h5>
<p><strong>Kalau AI-nya dimatikan sekarang, apakah Anda masih bisa menjelaskan pekerjaan Anda?</strong>
Kalau ya, Anda memakainya dengan benar. Kalau tidak, Anda sedang menyewa pemahaman orang lain.</p>
""" % TBL

INTEGRITAS = u"""
<h4>Integritas Akademik</h4>
<ol>
<li><strong>Diskusi dianjurkan, penyalinan dilarang.</strong> Boleh berdiskusi tentang pendekatan; rancangan, kode,
dan tulisan harus Anda susun sendiri.</li>
<li>Dua berkas yang identik atau nyaris identik: <strong>keduanya dinilai 0</strong>, tanpa memeriksa siapa menyalin siapa.</li>
<li>Setiap klaim di laporan harus bisa Anda pertanggungjawabkan saat ditanya lisan.
<strong>Klaim yang tidak bisa dijelaskan pemiliknya dinilai 0</strong> &mdash; meskipun hasilnya bagus.</li>
<li>Aset pihak ketiga (ikon, template, foto, komponen UI) <strong>boleh dipakai</strong> asal lisensinya
mengizinkan dan <strong>disebutkan sumbernya</strong> di laporan.</li>
</ol>
"""


def head(judul, sub):
    return u'<h3>%s</h3>\n<p><strong>%s</strong></p>\n<hr />\n' % (judul, sub)


def tabel(rows, headers=None, width=None):
    h = u'<table %s>\n' % TBL
    if headers:
        h += u'<tr %s>%s</tr>\n' % (HDR, u''.join(u'<th>%s</th>' % c for c in headers))
    for r in rows:
        h += u'<tr>%s</tr>\n' % u''.join(u'<td>%s</td>' % c for c in r)
    return h + u'</table>\n'


def build(mode):
    """mode: 'A' (luring reguler) atau 'P' (daring, kelas Profesional)."""
    A = mode == "A"
    judul = u"Kontrak Kuliah &mdash; Application Project I"
    sub = (u"Semester Ganjil 2026/2027 &middot; Kelas A (Reguler) &middot; Kamis 13.50&ndash;15.30, Ruang A.2.1"
           if A else
           u"Semester Ganjil 2026/2027 &middot; Kelas P (Profesional) &middot; daring penuh, mandiri (self-paced)")
    h = head(judul, sub)

    # 1 identitas
    h += u"<h4>1. Identitas Mata Kuliah</h4>\n"
    h += tabel([
        (u"<strong>Mata Kuliah</strong>", u"Application Project I"),
        (u"<strong>Kode</strong>", u"IF24KB33"),
        (u"<strong>Bobot</strong>", u"2 SKS"),
        (u"<strong>Semester</strong>", u"5 (Lima)"),
        (u"<strong>Program Studi</strong>", u"Informatika"),
        (u"<strong>Bahan Kajian</strong>", u"BK24 &mdash; Application Project I (Data Management, HCI, SEC, SEP)"),
        (u"<strong>Prasyarat</strong>", u"&mdash;"),
        (u"<strong>Kelas / Jadwal</strong>",
         u"A &mdash; <strong>Kamis, 13.50&ndash;15.30, Ruang A.2.1</strong>" if A else
         u"P &mdash; <strong>daring penuh lewat eBelajar</strong>, dikerjakan mandiri sesuai ritme sendiri"),
        (u"<strong>Periode</strong>", u"7 September 2026 &ndash; 28 Februari 2027"),
        (u"<strong>Dosen Pengampu</strong>", u"Mukhlis Amien, M.Kom."),
        (u"<strong>Kelas daring (LMS)</strong>",
         u"ebelajar.stiki.ac.id &mdash; kursus <em>Application Project I %s 2026-Ganjil</em>" % mode),
    ])

    # 2 deskripsi
    h += u"""
<h4>2. Deskripsi Singkat</h4>
<p>Mata kuliah ini membawa Anda dari <strong>ide mentah</strong> sampai <strong>prototipe web yang benar-benar bisa
dipakai orang</strong>. Fokusnya adalah <em>Minimum Viable Product</em> (MVP): merancang antarmuka yang efektif,
membangunnya dengan teknologi front-end terkini, lalu <strong>memperbaikinya berdasarkan umpan balik pengguna
sungguhan</strong> &mdash; bukan berdasarkan selera sendiri.</p>
<p>Yang dinilai bukan seberapa ramai tampilannya, melainkan <strong>seberapa masuk akal keputusan desain Anda dan
seberapa jujur Anda mengujinya.</strong></p>
"""
    h += tabel([
        (u"<strong>1 &mdash; Merancang</strong>", u"1&ndash;3", u"Prinsip UI, ergonomi, estetika, wireframe"),
        (u"<strong>2 &mdash; Membangun</strong>", u"4&ndash;5", u"Teknologi front-end, SPA &amp; PWA, komponen antarmuka"),
        (u"<strong>3 &mdash; Menguji</strong>", u"6&ndash;7", u"Iterasi desain, A/B testing, usability testing"),
        (u"<strong>4 &mdash; Mengelola</strong>", u"9&ndash;13", u"MVP, perencanaan proyek, alat manajemen, pengambilan keputusan"),
        (u"<strong>5 &mdash; Mengevaluasi</strong>", u"14&ndash;16", u"Evaluasi mandiri, progress project, proyek akhir"),
    ], [u"Fase", u"Pertemuan", u"Fokus"])

    # 3 capaian
    h += u"""
<h4>3. Capaian Pembelajaran</h4>
<p><strong>CPL Program Studi yang dibebankan</strong></p>
<ul>
<li><strong>CPL09</strong> &mdash; Kemampuan menganalisis, merancang, membuat, dan mengevaluasi <em>user interface</em>
dan aplikasi interaktif dengan mempertimbangkan kebutuhan pengguna dan perkembangan ilmu transdisiplin.</li>
<li><strong>CPL10</strong> &mdash; Mampu menunjukkan kinerja mandiri, bermutu, dan terukur.</li>
</ul>
<p><strong>CPMK</strong></p>
<ul>
<li><strong>CPMK092</strong> &mdash; Mampu membuat <em>user interface</em> dan aplikasi interaktif.</li>
<li><strong>CPMK121</strong> &mdash; Mampu menyelesaikan tugas dan proyek secara mandiri, dengan inisiatif pribadi,
mengambil keputusan yang tepat, dan menerapkan solusi kreatif.</li>
</ul>
<p><strong>Sub-CPMK</strong></p>
"""
    h += tabel([(u"<strong>%s</strong>" % k, v) for k, v in SUBCPMK], [u"Kode", u"Kemampuan akhir"])

    # 4 peta
    h += u"<h4>4. Peta 16 Pertemuan</h4>\n"
    h += tabel([(n, t, s, tg, b) for n, t, s, tg, b in PETA],
               [u"#", u"Topik", u"Sub-CPMK", u"Penugasan", u"Bobot"])
    h += (u"<p><em>Kolom bobot di atas adalah porsi nilai akhir yang sesungguhnya. Sisa 10% adalah partisipasi, "
          u"yang tidak menempel pada satu pertemuan tertentu &mdash; rinciannya di bagian 6.</em></p>\n")
    if A:
        h += (u"<p>Tanggal setiap pertemuan, <strong>UTS</strong>, dan <strong>UAS</strong> mengikuti kalender akademik "
              u"kampus. Perubahan diumumkan lewat forum Pengumuman di eBelajar.</p>\n")
    else:
        h += (u"<p><strong>Materi terbuka bertahap.</strong> Pertemuan berikutnya terbuka setelah materi pertemuan "
              u"sebelumnya Anda baca sampai selesai. Urutannya sengaja &mdash; Pertemuan 9 tidak masuk akal sebelum "
              u"Pertemuan 5 dikerjakan.</p>\n")

    # 5 format
    if A:
        h += u"<h4>5. Format Setiap Pertemuan</h4>\n<p>Kelas ini berbentuk <strong>studio</strong>, bukan ceramah satu arah. Setiap pertemuan 100 menit:</p>\n"
        h += tabel([
            (u"5'", u"<strong>Hook</strong>", u"Satu contoh antarmuka yang gagal, atau satu angka yang mengganggu"),
            (u"25'", u"<strong>Mini-lecture</strong>", u"Konsep inti &mdash; sesingkat mungkin, secukupnya untuk mulai bekerja"),
            (u"55'", u"<strong>Studio</strong>", u"Anda mengerjakan proyek; dosen berkeliling per kelompok"),
            (u"10'", u"<strong>Debrief</strong>", u"Membandingkan hasil antar kelompok, membahas yang gagal"),
            (u"5'", u"<strong>Exit-ticket</strong>", u"Refleksi tertulis singkat &mdash; bahan penilaian partisipatif"),
        ], [u"Durasi", u"Bagian", u"Isi"])
        h += (u"<p><strong>Konsekuensinya: kelas ini tidak bisa diikuti secara pasif.</strong> "
              u"Bawa laptop mulai Pertemuan 2.</p>\n")
    else:
        h += u"<h4>5. Cara Kelas Ini Berjalan</h4>\n<p>Tidak ada tatap muka. Setiap pertemuan berisi paket yang sama:</p>\n"
        h += tabel([
            (u"<strong>1. Baca</strong>", u"Halaman materi pertemuan &mdash; ini yang membuka pertemuan berikutnya"),
            (u"<strong>2. Kerjakan</strong>", u"Tugas pada pertemuan itu, diunggah lewat eBelajar"),
            (u"<strong>3. Diskusikan</strong>", u"Forum diskusi pertemuan &mdash; balas minimal satu tulisan teman"),
        ], [u"Langkah", u"Isi"])
        h += (u"<p><strong>Semua sudah terbuka sejak hari pertama, dan tidak ada tenggat sama sekali.</strong> "
              u"Kerjakan dengan ritme Anda sendiri. Tapi ritme bukan berarti menumpuk di akhir: menyelesaikan "
              u"satu pertemuan per minggu adalah pola yang terbukti paling aman.</p>\n")

    # 6 penilaian
    h += u"<h4>6. Komponen dan Bobot Penilaian</h4>\n<p>Penilaian memakai pendekatan <strong>Outcome-Based Education (OBE)</strong>.</p>\n"
    rows = [(u"<strong>%s</strong>" % a, b, u"<strong>%s</strong>" % c) for a, b, c in PENILAIAN]
    rows.append((u"", u"<strong>Total</strong>", u"<strong>100%</strong>"))
    h += tabel(rows, [u"Komponen", u"Bentuk", u"Bobot"])
    if not A:
        h += (u"<p><em>Untuk kelas P, komponen <strong>Partisipatif</strong> dinilai dari "
              u"<strong>penyelesaian aktivitas dan keaktifan di forum</strong>, bukan dari kehadiran fisik.</em></p>\n")

    h += u"<p><strong>Bobot per aktivitas &mdash; ini yang dipakai saat menilai</strong></p>\n"
    brows = [(u"<strong>%s</strong>" % a, b, u"<strong>%s</strong>" % c, d) for a, b, c, d in BOBOT]
    brows.append((u"", u"<strong>Total</strong>", u"<strong>100%</strong>", u""))
    h += tabel(brows, [u"Aktivitas", u"Isi", u"Bobot", u"Masuk komponen"])

    h += u"""
<p><strong>Catatan penyesuaian &mdash; supaya angkanya benar-benar berjumlah 100.</strong> RPS memuat dua tabel bobot
yang tidak saling cocok, dan keduanya asli: tabel komponen OBE berjumlah 100%, sedangkan kolom bobot per blok minggu
berjumlah <strong>95%</strong> dengan minggu UTS dan UAS tidak diberi bobot sama sekali. Selain itu tabel OBE memuat
pos <strong>Quiz 10%</strong>, padahal mata kuliah ini <strong>tidak punya aktivitas kuis</strong> selain UTS &mdash;
dan UTS sudah dihitung terpisah 15%.</p>
<p>Penyesuaian yang diambil, sesedikit mungkin: <strong>pos Quiz 10% dilebur ke Tugas individu</strong>
(10% &rarr; 20%), karena di mata kuliah proyek itulah bentuk penilaian yang benar-benar ada. Lima komponen lain
<strong>tidak diubah</strong>, dan urutan besar-kecil antar-tugas tetap mengikuti proporsi RPS. Hasilnya: setiap
aktivitas punya bobot, tidak ada pos yang kosong, dan jumlahnya persis 100%.</p>
"""
    h += u"<p><strong>Alur penugasan sepanjang semester</strong></p>\n<ul>\n"
    h += u"<li><strong>Tugas 1&ndash;8</strong> &mdash; menempel pada pertemuan tertentu; tiap tugas adalah satu potong nyata dari proyek Anda, bukan latihan terpisah.</li>\n"
    h += u"<li><strong>Progress Project</strong> (Pertemuan 15) &mdash; laporan kemajuan proyek beserta evaluasi mandiri.</li>\n"
    h += u"<li><strong>Proyek Akhir (UAS)</strong> &mdash; prototipe MVP + laporan; dikumpulkan pada Pertemuan 16.</li>\n"
    h += u"</ul>\n"

    # 7 aturan
    h += u"<h4>7. Aturan Kelas</h4>\n"
    if A:
        h += u"""
<p><strong>Kehadiran</strong></p>
<ol>
<li>Kehadiran minimal <strong>75%</strong> dari pertemuan yang terlaksana untuk berhak mengikuti UAS.</li>
<li>Toleransi keterlambatan <strong>15 menit</strong>. Lewat dari itu tetap boleh masuk, tetapi dicatat terlambat.
<strong>3&times; terlambat dihitung 1&times; tidak hadir.</strong></li>
<li>Ketidakhadiran karena sakit / tugas kampus / musibah: sertakan surat keterangan, paling lambat pertemuan berikutnya.</li>
</ol>
<p><strong>Kerja kelompok</strong></p>
<ol start="4">
<li>Proyek dikerjakan <strong>berkelompok</strong>; kelompok dibentuk pada Pertemuan 1 dan <strong>tidak berubah</strong>
sepanjang semester kecuali atas persetujuan dosen.</li>
<li>Setiap anggota wajib punya <strong>bagian yang bisa ditunjuk</strong>. Nilai kelompok dapat diturunkan per orang
bila kontribusinya tidak terlihat pada riwayat kerja.</li>
</ol>
<p><strong>Perangkat</strong></p>
<ol start="6">
<li><strong>Laptop wajib dibawa mulai Pertemuan 2.</strong> 55 menit setiap pertemuan dipakai bekerja.</li>
<li>Siapkan akun <strong>Figma</strong> (atau Adobe XD) dan lingkungan front-end (Node.js + editor).</li>
</ol>
<p><strong>Tugas</strong></p>
<ol start="8">
<li>Semua tugas dikumpulkan lewat <strong>eBelajar</strong> &mdash; bukan WhatsApp, bukan email.</li>
<li>Format nama berkas: <code>AP1_P&lt;pertemuan&gt;_NIM_Nama_&lt;Topik&gt;</code> &mdash;
contoh: <code>AP1_P1_2023001_Budi_Wireframe.pdf</code>.</li>
<li><strong>Batas pengumpulan: Minggu pukul 23.55</strong> pada minggu berikutnya setelah tugas diberikan,
kecuali dinyatakan lain di aktivitasnya.</li>
<li>Keterlambatan: <strong>&minus;10% per hari</strong>, maksimal 3 hari. Lewat 3 hari dinilai 0 tetapi
<strong>tetap wajib dikumpulkan</strong> sebagai syarat kelengkapan portofolio.</li>
</ol>
"""
    else:
        h += u"""
<p><strong>Penyelesaian aktivitas</strong></p>
<ol>
<li>Tidak ada absensi. Yang menggantikannya: <strong>penyelesaian aktivitas</strong> &mdash; materi dibaca, tugas
diunggah, forum diikuti.</li>
<li>Pertemuan berikutnya <strong>terbuka otomatis</strong> setelah materi pertemuan sebelumnya ditandai selesai dibaca.
Kalau pertemuan berikutnya terkunci, hampir selalu sebabnya ini.</li>
<li>Materi UTS terbuka setelah Pertemuan 7 selesai, dan <strong>UTS harus dinilai</strong> sebelum Pertemuan 9 terbuka.</li>
</ol>
<p><strong>Kerja mandiri</strong></p>
<ol start="4">
<li>Seluruh tugas di kelas P dikerjakan <strong>perorangan</strong>, termasuk yang judulnya masih menyebut
&ldquo;kelompok&rdquo; (warisan penamaan kelas reguler). Kalau ragu, anggap individu.</li>
<li>Proyek akhir juga perorangan &mdash; lingkupnya boleh lebih kecil daripada kelas reguler, asalkan
<strong>utuh dari rancangan sampai prototipe yang jalan</strong>.</li>
</ol>
<p><strong>Tugas</strong></p>
<ol start="6">
<li>Semua tugas dikumpulkan lewat <strong>eBelajar</strong> &mdash; bukan WhatsApp, bukan email.</li>
<li>Format nama berkas: <code>AP1_P&lt;pertemuan&gt;_NIM_Nama_&lt;Topik&gt;</code> &mdash;
contoh: <code>AP1_P1_2023001_Budi_Wireframe.pdf</code>.</li>
<li><strong>Tidak ada tenggat.</strong> Kelas ini <em>self-paced</em>: seluruh aktivitas terbuka sejak hari pertama
dan <strong>tidak ada satu pun tanggal pengumpulan</strong>. Tidak ada penalti keterlambatan, karena tidak ada yang
bisa disebut terlambat.</li>
<li>Satu-satunya batas yang nyata adalah <strong>akhir masa perkuliahan semester ini (28 Februari 2027)</strong>
&mdash; nilai harus sudah masuk sebelum itu. Itu batas administratif kampus, bukan tenggat tugas.</li>
<li><strong>Konsekuensinya pindah ke tangan Anda.</strong> Tanpa tenggat, tidak ada yang mengingatkan selain diri
sendiri. Ritme yang terbukti aman: <strong>satu pertemuan per minggu</strong>. Menumpuk 16 pertemuan di
minggu-minggu terakhir adalah cara paling umum gagal di kelas ini &mdash; bukan karena aturannya, melainkan karena
waktunya benar-benar tidak cukup.</li>
</ol>
"""

    h += INTEGRITAS
    h += u"<h4>8. Kebijakan Penggunaan AI</h4>\n" + AI_POLICY.replace(u"<h4>Kebijakan Penggunaan AI</h4>", u"")

    # 9 komunikasi
    extra = (u'<tr><td><strong>Tatap muka</strong></td><td>Konsultasi proyek &mdash; setelah kelas atau dengan janji</td><td>&mdash;</td></tr>'
             if A else
             u'<tr><td><strong>Konsultasi daring</strong></td><td>Konsultasi proyek &mdash; ajukan lewat forum Diskusi Umum</td><td>&mdash;</td></tr>')
    h += u"""
<h4>9. Komunikasi</h4>
<table %s>
<tr %s><th>Saluran</th><th>Untuk apa</th><th>Waktu tanggap</th></tr>
<tr><td><strong>Forum eBelajar</strong></td><td>Pertanyaan teknis &amp; materi</td><td>Hari kerja, &le; 1&times;24 jam</td></tr>
<tr><td><strong>Grup WhatsApp kelas</strong></td><td>Pengumuman mendadak, koordinasi</td><td>&mdash;</td></tr>
<tr><td><strong>Forum Pengumuman</strong></td><td>Perubahan jadwal, informasi resmi</td><td>&mdash;</td></tr>
%s
</table>
<p>Pertanyaan teknis <strong>diarahkan ke forum</strong>, bukan japri. Satu jawaban menolong banyak orang, dan Anda
terbiasa merumuskan pertanyaan dengan jelas &mdash; keterampilan yang dinilai di dunia kerja.</p>
""" % (TBL, HDR, extra)

    # 10 pustaka
    h += u"<h4>10. Referensi</h4>\n<p><strong>Utama</strong></p>\n<ol>\n"
    h += u"".join(u"<li>%s</li>\n" % x for x in PUSTAKA_UTAMA)
    h += u"</ol>\n<p><strong>Pendukung</strong></p>\n<ol>\n"
    h += u"".join(u"<li>%s</li>\n" % x for x in PUSTAKA_PENDUKUNG)
    h += u"</ol>\n<p><em>Daftar ini diambil apa adanya dari RPS resmi mata kuliah.</em></p>\n"

    # 11 kesepakatan
    if A:
        h += u"""
<h4>11. Kesepakatan</h4>
<p>Kontrak ini dibacakan dan disepakati pada <strong>Pertemuan 1, Kamis 10 September 2026</strong>.
Perubahan atas isinya hanya lewat kesepakatan kelas dan diumumkan di forum Pengumuman.</p>
<table %s>
<tr %s><th>Dosen Pengampu</th><th>Perwakilan Kelas</th></tr>
<tr><td style="height:60px;"></td><td></td></tr>
<tr><td><strong>Mukhlis Amien, M.Kom.</strong></td><td><strong>Nama &amp; NIM:</strong></td></tr>
</table>
""" % (TBL, HDR)
    else:
        h += u"""
<h4>11. Kesepakatan</h4>
<p>Dengan mengerjakan aktivitas pertama di kelas ini, Anda dianggap <strong>telah membaca dan menyetujui</strong>
kontrak ini. Kalau ada yang ingin ditanyakan atau dinegosiasikan, tulis di
<strong>forum Diskusi Umum</strong> &mdash; jangan didiamkan.</p>
"""
    return h


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for mode in ("A", "P"):
        html = build(mode)
        p = os.path.join(OUT, "kontrak_kuliah_AP1_%s_2026.html" % mode)
        io.open(p, "w", encoding="utf-8").write(html)
        print(mode, len(html), "chars ->", p)
