# -*- coding: utf-8 -*-
"""Isi ulang page materi Pertemuan 1 & 2 (PM/NLP/AP1, kelas A & P) — 11 Sep 2026.

Permintaan user: perbaiki modul P1 & P2 satu per satu (fondasi buku ajar ber-ISBN).
Sumber konten: deck P1 (yang diajarkan di kelas) → file modul_p1.html / modul_p2.html
per folder matkul. Kelas A & P isi sama kecuali tautan aktivitas (cmid beda).

Cara aman (pelajaran 7 Sep): baca SELURUH form modedit, timpa field isi saja,
kirim ulang utuh + submitbutton2. Verifikasi: view.php harus memuat frasa khas baru.

PELAJARAN 11 Sep: pada mod_page, editor konten halaman = page[text] — BUKAN introeditor[text].
introeditor adalah deskripsi singkat modul (tampil di halaman kursus kalau showdescription on).
POST pertama 11 Sep menimpa deskripsi 491676 dengan badan modul utuh — diperbaiki lewat
INTRO[*] di bawah (deskripsi ditulis ulang jadi ringkasan singkat).
"""
import os, re, sys
import moodle
from ap1_sync import repost

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EB = "https://ebelajar.stiki.ac.id"
DRIVE = lambda fid: "https://drive.google.com/drive/folders/" + fid
VIEW = lambda cmid: "%s/mod/page/view.php?id=%d" % (EB, cmid)

KELAS_A = ("Pada kelas A, kelompok proyek dibentuk saat pertemuan luring &mdash; pastikan data kelompok "
           "Anda terdaftar lewat Tugas 1b.")
KELAS_P = ("Kelas P dikerjakan <strong>perorangan</strong> &mdash; sebagai ganti kelompok, tunjuk satu "
           "<strong>mitra uji</strong> (teman, keluarga, atau rekan kerja mana pun) untuk menguji wireframe Anda.")

# Deskripsi singkat per modul (field introeditor — bukan isi halaman).
INTRO = {
    "PM P1": "Konsep dasar pembelajaran mesin: tiga paradigma, alur proyek, tiga masalah data, "
             "dan jebakan kebocoran data yang merusak evaluasi.",
    "PM P2": "Menyiapkan data sebelum modelling: imputasi nilai hilang dan normalisasi "
             "(MinMax vs Z-score) &mdash; termasuk kapan model berbasis pohon tak butuh scaling.",
    "NLP P1": "Pengantar NLP: kenapa bahasa manusia sulit bagi komputer, empat gelombang sejarah NLP, "
              "dan rantai kerja NLP yang menjadi peta 16 pertemuan kita.",
    "NLP P2": "Dua teknik preprocessing paling dasar &mdash; tokenisasi dan penghapusan stopwords "
              "&mdash; beserta jebakannya di bahasa Indonesia.",
    "AP1 P1": "UI vs UX, tiga prinsip desain antarmuka (hierarki visual, konsistensi, keterbacaan), "
              "dan wireframe sebagai alat kerja pertama proyek Anda.",
    "AP1 P2": "Ergonomi (Fitts's Law, target sentuh, zona ibu jari) dan aksesibilitas (WCAG), "
              "lalu merumuskan ide proyek dari masalah nyata.",
}

# 17 Sep 2026: Tugas 2 AP1 A dimajukan ke P2 (keputusan user). Kelas P tetap kalimat lama.
# {EXIT} diisi cmid forum exit-ticket P2 oleh ap1_p2_setup.py.
TUGAS2_A = ('<li><strong><a href="%s/mod/assign/view.php?id=491632">TUGAS 2: Audit Ergonomi &amp; Ide Proyek '
            '(Brainstorming)</a></strong> &mdash; tenggat <strong>Minggu, 27 September 2026 pukul 23.55</strong>.</li>'
            '<li><a href="%s/mod/forum/view.php?id={EXIT}">Exit-ticket Pertemuan 2</a> &mdash; tiga pertanyaan '
            'refleksi, dijawab di akhir kelas.</li>'
            '<li><a href="https://drive.google.com/drive/folders/1yvgECF7RK8l6Hr4TG0oIG-RFdIkocAou">Bahan Pertemuan 2 '
            'di Google Drive</a> &mdash; Modul Pertemuan 2 (PDF), slide, dan dua video.</li>' % (EB, EB))
TUGAS2_P = ('<li>Tugas 2 &mdash; Brainstorming akan dibuka setelah jadwal pertemuan ini terkonfirmasi kalender '
            'akademik; ikuti pengumuman.</li>')

# (label, path_html, {kelas: (cmid, overrides-placeholder)})
TARGETS = [
    ("PM P1",
     "pembelajaran-mesin/modul_p1.html",
     {"A": (491676, {"FORUM": VIEW(491677), "MODUL": VIEW(495555), "DRIVE": DRIVE("1Id_syspr70fBMvVLOOALkXHrbDkkH_kb")}),
      "P": (491728, {"FORUM": VIEW(491729), "MODUL": VIEW(496338), "DRIVE": DRIVE("1Id_syspr70fBMvVLOOALkXHrbDkkH_kb")})},
     "split dulu, baru fit"),
    ("PM P2",
     "pembelajaran-mesin/modul_p2.html",
     {"A": (491679, {"TUGAS": "%s/mod/assign/view.php?id=491680" % EB}),
      "P": (491731, {"TUGAS": "%s/mod/assign/view.php?id=491732" % EB})},
     "Model berbasis pohon"),
    ("NLP P1",
     "nlp/modul_p1.html",
     {"A": (491782, {"FORUM": VIEW(491783), "DRIVE": DRIVE("1mRF6mGDE49BDGIhaVI_PHanLjAy4Yowh")}),
      "P": (491834, {"FORUM": VIEW(491835), "DRIVE": DRIVE("1mRF6mGDE49BDGIhaVI_PHanLjAy4Yowh")})},
     "empat gelombang sejarah NLP"),
    ("NLP P2",
     "nlp/modul_p2.html",
     {"A": (491785, {"TUGAS": "%s/mod/assign/view.php?id=491786" % EB}),
      "P": (491837, {"TUGAS": "%s/mod/assign/view.php?id=491838" % EB})},
     "Negasi adalah informasi"),
    ("AP1 P1",
     "application-project-1/modul_p1.html",
     {"A": (491622, {"FORUM": VIEW(491623), "TUGAS": "%s/mod/assign/view.php?id=491624" % EB,
                     "DRIVE": DRIVE("1qGzyIrZGWRyMK7rDRTFvLUXtTkhoDqPI"), "KELAS": KELAS_A}),
      "P": (491570, {"FORUM": VIEW(491571), "TUGAS": "%s/mod/assign/view.php?id=491572" % EB,
                     "DRIVE": DRIVE("1qGzyIrZGWRyMK7rDRTFvLUXtTkhoDqPI"), "KELAS": KELAS_P})},
     "wireframe dikerjakan tanpa warna"),
    ("AP1 P2",
     "application-project-1/modul_p2.html",
     {"A": (491628, {"DISKUSI": "%s/mod/forum/view.php?id=491616" % EB, "TUGAS2": TUGAS2_A}),
      "P": (491576, {"DISKUSI": "%s/mod/forum/view.php?id=491564" % EB, "TUGAS2": TUGAS2_P})},
     "Fitts"),
]


def load(html_path, ph):
    t = open(html_path, encoding="utf-8").read()
    # buang komentar header (arsip)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    for k, v in ph.items():
        t = t.replace("{%s}" % k, v)
    leftover = re.findall(r"\{[A-Z_]+\}", t)
    assert not leftover, "placeholder sisa: %s (%s)" % (leftover, html_path)
    return t.strip()


def verify(cmid, needle):
    t = moodle.get("/mod/page/view.php?id=%d" % cmid).text
    return needle in t


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    moodle.sess()
    for label, rel, per_class, needle in TARGETS:
        html_path = os.path.join(BASE_DIR, rel)
        print("=" * 66)
        print("%s  (%s)" % (label, rel))
        for kls, (cmid, ph) in sorted(per_class.items()):
            body = load(html_path, ph)
            if not apply:
                print("   DRY %s cmid=%d  %d chars  -> skip" % (kls, cmid, len(body)))
                continue
            r = repost(cmid, {"page[text]": body, "introeditor[text]": INTRO[label]})
            ok = r.status_code == 200 and verify(cmid, needle)
            print("   %s cmid=%d  http%d  verifikasi %s (%d chars)"
                  % (kls, cmid, r.status_code, "OK" if ok else "GAGAL", len(body)))
            if not ok:
                sys.exit("STOP: %s %s gagal verifikasi" % (label, kls))
