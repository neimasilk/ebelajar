# -*- coding: utf-8 -*-
"""Koreksi kebijakan 24 Sep (sebelum kelas 13.50): SEMUA tugas AP = tugas kelompok,
yang mengumpulkan sendirian juga sah (kelompok boleh terbentuk belakangan).
Alasan user: AP adalah mata kuliah proyek - semua tugas menuju proyek besar
untuk pameran di akhir semester.

Yang diubah:
1. TUGAS 2 (491632, masih terbuka due 27 Sep): sisip paragraf kebijakan +
   label 2a tidak lagi "(individu)".
2. TUGAS 3 (503174): intro ditulis ulang (hapus framing "3b wajib individu").
3. Komentar nilai TUGAS 1 (491624) untuk 5 mahasiswa yang berframing
   "tugas individu" - nilai numerik TIDAK diubah.

TUGAS 1 sudah tertutup dan intro-nya sudah berbau kelompok: tidak disentuh.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, sweep_pma
from ap1_sync import repost
from ap1_grade_t1 import find_row, grade_one, readback

TUGAS1 = 491624
TUGAS2 = 491632
TUGAS3 = 503174

POLICY_P = ("<p><strong>Kebijakan AP: semua tugas adalah tugas kelompok</strong> - seluruh "
            "tugas semester ini adalah potongan satu proyek kelompok menuju pameran proyek "
            "di akhir semester. Yang mengerjakan sendirian juga sah; kelompok boleh terbentuk "
            "belakangan. Yang penting: nama kelompok dan anggota tercantum di berkas dan di "
            "sheet kelompok.</p>")

T2_REPLACEMENTS = [
    # sisip paragraf kebijakan sebelum daftar 2a
    ("<p><strong>2a - Audit Ergonomi",
     POLICY_P + "<p><strong>2a - Audit Ergonomi"),
    # label 2a tidak lagi individu
    ("2a - Audit Ergonomi dan Revisi Wireframe (individu)",
     "2a - Audit Ergonomi dan Revisi Wireframe (kelompok; sendirian juga sah)"),
    # 2b: yang belum punya kelompok tetap boleh jalan
    ("Kelompok berisi <strong>2-4 orang</strong> dan sudah tercatat di sheet KELOMPOK AP 1",
     "Kelompok berisi <strong>2-4 orang</strong>; yang belum punya kelompok boleh mengerjakan "
     "sendirian dulu. Sheet KELOMPOK AP 1"),
]

T3_INTRO = """<p><strong>Tugas 3 - Dari wireframe ke mockup + draft proposal</strong> | Bobot sesuai RPS</p>
<p><strong>Kebijakan AP: semua tugas adalah tugas kelompok.</strong> Seluruh tugas semester ini adalah
potongan satu proyek kelompok yang berakhir di pameran proyek. Yang (masih) mengerjakan sendirian juga
sah - kelompok boleh terbentuk belakangan; cukup catat nama kelompok dan anggota di berkas.</p>
<p>Tiga deliverable mengikuti Modul Pertemuan 3:</p>
<ol>
<li><strong>Tugas 3a - Style Guide</strong> (kelompok; sendirian juga sah): satu halaman berisi
palet warna 5 peran + skala abu-abu, type scale (H1-H6, Body, Caption) + contoh ukuran/line-height,
komponen inti dengan variasi state, aturan spacing 8-point. Berkas: <code>StyleGuide_P3.pdf</code>.</li>
<li><strong>Tugas 3b - Mockup Dua Layar</strong> (kelompok; sendirian juga sah): Beranda dan Layar Fitur
Inti, fidelity menengah, konsisten dengan style guide. Berkas: <code>Mockup_P3_Home.pdf</code> +
<code>Mockup_P3_FiturInti.pdf</code> (file sumber opsional).</li>
<li><strong>Tugas 3c - Draft Proposal</strong> (kelompok): 1-2 halaman berisi 7 komponen
(Judul &amp; Ringkasan; Masalah &amp; Target Pengguna; Hipotesis Nilai; Fitur Inti MVP +
Out-of-Scope; Risiko &amp; Asumsi Kritis; Metrik Keberhasilan Awal; Rencana Validasi).
Berkas: <code>AP1_P3_KelompokX_Proposal.pdf</code>.</li>
</ol>
<p><strong>Rubrik (100 poin):</strong> Kualitas Style Guide 25; Estetika &amp; Konsistensi Mockup 30;
Aksesibilitas &amp; Keterbacaan 20; Kecocokan dengan Tujuan Pengguna 15; Kerapian &amp; Kepatuhan
Format 10. <strong>Lulus tugas: minimal 70.</strong></p>
<p><em>Yang kemarin mengumpulkan Tugas 1 secara individu tidak perlu mengulang apa pun - pekerjaan
itu tetap sah dan sudah dinilai. Untuk Tugas 3, manfaatkan kelompok: satu style guide bersama,
pembagian layar mockup, kualitas proposal lebih tajam.</em></p>"""

# (nama persis di tabel grading, nilai LAMA dipertahankan, komentar BARU)
KOMENTAR_BARU = [
    ("DAFFA MUHAMMAD RAMADHAN", 90,
     "Terlengkap dari semua submission: wireframe desktop dengan UX Note 1-8, "
     "perhatian ke state (empty/error/placeholder), hierarki CTA jelas. Catatan: "
     "(1) kalau ada bagian yang dibantu AI, wajib ditulis di disclosure seperti "
     "ketentuan kelas; (2) karena semua tugas AP adalah tugas kelompok, berkas "
     "berikutnya cukup satu per kelompok dengan nama kelompok + daftar anggota; "
     "(3) lanjut ke style guide + mockup P3 bersama QWERTY - jadikan standar "
     "kualitasmu acuan kelompok."),
    ("BOBBY EKA ANGGA KUSUMA", 88,
     "Bagus: empty state dan error state dipikirkan walau tidak diwajibkan, "
     "alasan desain per elemen jelas, disclosure penggunaan ChatGPT untuk "
     "merapikan tulisan sudah jujur dan itu benar. Catatan: karena semua tugas "
     "AP adalah tugas kelompok, berkas berikutnya cukup satu per kelompok "
     "(JOSJIS) dengan nama kelompok + daftar anggota. Lanjutkan ke mockup P3 "
     "dengan ketelitian yang sama."),
    ("TEKIU NEWEGALEN", 85,
     "Wireframe digital rapi, anotasi 7 bagian, paragraf penjelasan cukup. "
     "Berkas atas nama tiga orang sekarang resmi sah: semua tugas AP adalah "
     "tugas kelompok. Catatan untuk FERDI dan NOTOPIANUS: tetap tekan Add "
     "submission di eBelajar (boleh berkas yang sama plus catatan anggota) "
     "supaya ada rekaman untuk dinilai - tanpa rekaman itu sistem tidak bisa "
     "memberi nilai. Konfirmasi juga di kelas hari ini."),
    ("JOVAN NI'AM FAIRUZ ZAKY", 80,
     "Ada kerja individu nyata: versi beranotasi 13 elemen plus narasi alasan "
     "desain di halaman 3. Foto dasar identik dengan submission Andrean "
     "(kertas kelompok RAWON) - itu tidak masalah, semua tugas AP adalah tugas "
     "kelompok; nilai ini naik justru karena anotasi dan narasimu membuat "
     "berkasnya paling lengkap. Untuk Tugas 3: satu style guide untuk RAWON, "
     "pastikan tiap anggota ikut menekan submit."),
    ("ANDREAN SATRIA BAGASKARA", 70,
     "Yang dikumpulkan hanya foto wireframe kertas kelompok (yang sama dengan "
     "milik Jovan) tanpa anotasi dan tanpa narasi. Bekerja dari kertas "
     "kelompok itu sah - semua tugas AP adalah tugas kelompok - tapi nilai "
     "mengikuti kelengkapan berkas: anotasi dan narasi alasan desain adalah "
     "bagian yang dinilai, dan keduanya belum ada di berkas ini. Untuk Tugas "
     "3: kerjakan satu bagian yang jadi tanggung jawabmu di berkas kelompok "
     "RAWON (misal satu layar mockup), jangan hanya meneruskan berkas orang "
     "lain."),
]


def fetch_intro(cmid):
    t = moodle.get("/course/modedit.php?update=%d" % cmid).text
    m = re.search(r'name="introeditor\[text\]"[^>]*>(.*?)</textarea>', t, re.S)
    return html_unescape(m.group(1)) if m else None


def html_unescape(s):
    import html
    return html.unescape(s)


if __name__ == "__main__":
    sweep_pma.ensure_login()

    print("== 1. TUGAS 2: sisip kebijakan + buka label 2a ==")
    intro = fetch_intro(TUGAS2)
    assert intro, "intro T2 tidak terbaca"
    for old, new in T2_REPLACEMENTS:
        assert old in intro, "T2: pola tidak ketemu: %r" % old[:60]
        intro = intro.replace(old, new)
    assert "individu" not in intro.lower(), "T2 masih ada kata individu"
    r = repost(TUGAS2, {"introeditor[text]": intro})
    print("   repost http%s" % r.status_code)
    chk = fetch_intro(TUGAS2)
    assert "Kebijakan AP" in chk and "individu" not in chk.lower(), "T2 read-back gagal"
    print("   read-back OK (len=%d, kebijakan masuk)" % len(chk))

    print("== 2. TUGAS 3: intro baru ==")
    r = repost(TUGAS3, {"introeditor[text]": T3_INTRO})
    print("   repost http%s" % r.status_code)
    chk = fetch_intro(TUGAS3)
    assert "semua tugas adalah tugas kelompok" in chk.lower(), "T3 read-back gagal"
    assert "wajib individu" not in chk.lower(), "T3 masih ada framing wajib individu"
    print("   read-back OK (len=%d)" % len(chk))

    print("== 3. Komentar Tugas 1 (nilai tidak berubah) ==")
    rg = moodle.get("/mod/assign/view.php?id=%d&action=grading" % TUGAS1).text
    for name, nilai, catatan in KOMENTAR_BARU:
        uid, rownum = find_row(rg, name)
        if uid is None:
            print("   %-30s TIDAK KETEMU" % name)
            continue
        res = grade_one(TUGAS1, uid, rownum or 0, nilai, catatan)
        g, c = readback(TUGAS1, uid)
        ok = "OK" if (g in (str(nilai), "%d.00" % nilai)) else "CEK"
        print("   %-30s -> %s | grade=%s %s | %s" % (name, res, g, ok, c[:38]))

    print("== SELESAI ==")
