# -*- coding: utf-8 -*-
"""AP1 A: Tugas 2 dimajukan ke P2 (keputusan user 17 Sep 2026) + Tugas 1 bobot 5%->3%.
Isi Tugas 2 = Modul Pertemuan 2 di Drive (2a audit+revisi wireframe, 2b ide proyek kelompok).
Tenggat Minggu 27 Sep 2026 23:55; submit-from 17 Sep 00:00; cutoff OFF; grading reminder 4 Okt.
ASCII saja. Read-back wajib.
"""
import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, formpost, sweep_pma, nlp_p2_due

T2_NAME = "TUGAS 2: Audit Ergonomi & Ide Proyek (Brainstorming)"
T2_INTRO = """<p><strong>Tugas 2 - Audit Ergonomi &amp; Ide Proyek (Brainstorming)</strong> | Bobot 6% (komponen Observasi) | <strong>Tenggat: Minggu, 27 September 2026 pukul 23.55</strong></p>
<p>Tugas ini melanjutkan wireframe Tugas 1: Anda mengaudit rancangan sendiri dengan kacamata ergonomi dan aksesibilitas, memperbaikinya, lalu bersama kelompok merumuskan ide proyek awal. Sumber: <em>Modul Pertemuan 2</em> di folder Drive Pertemuan 2.</p>
<p><strong>2a - Audit Ergonomi dan Revisi Wireframe (individu)</strong></p>
<ul>
<li>Tabel audit wireframe Pertemuan 1, <strong>minimal 5 temuan</strong>, dengan kolom: masalah - dampak - usulan perbaikan. Daftar cek: tombol utama menonjol dan mudah dijangkau; jarak antar elemen interaktif cukup; navigasi selalu di lokasi yang sama; pesan error dan status sistem tampak serta mudah dipahami; kontras teks terhadap latar memadai; urutan tab/fokus keyboard mudah diprediksi.</li>
<li>Wireframe revisi: pilih <strong>3-5 perbaikan prioritas</strong> dari tabel audit, terapkan, lalu beri catatan pada wireframe (apa yang berubah dan alasannya).</li>
<li>Nama berkas: <code>AP1_P2_NIM_Nama_Audit.pdf</code> dan <code>AP1_P2_NIM_Nama_WireframeRevisi.pdf</code></li>
</ul>
<p><strong>2b - Ide Proyek Awal (kelompok)</strong></p>
<ul>
<li>1-2 ide proyek, maksimal 1 halaman per ide, berisi: (1) judul sementara dan deskripsi singkat; (2) pernyataan masalah: siapa penggunanya, konteksnya, kendala utamanya; (3) target pengguna: persona mini (tujuan utama, kebiasaan, perangkat utama); (4) hipotesis nilai: manfaat utama bagi pengguna; (5) 3-5 fitur inti yang langsung mengatasi masalah; (6) risiko dan asumsi kritis; (7) metrik awal keberhasilan.</li>
<li>Cantumkan daftar anggota beserta peran singkat masing-masing. Kelompok berisi <strong>2-4 orang</strong> dan sudah tercatat di sheet KELOMPOK AP 1 (tautan di forum Pengumuman).</li>
<li>Nama berkas: <code>AP1_P2_KelompokX_IdeProyek.pdf</code> (X = nama kelompok).</li>
<li><strong>Setiap anggota mengunggah berkas 2b yang sama.</strong> Aturan "berkas identik dinilai 0" tidak berlaku untuk berkas kelompok ini.</li>
</ul>
<p><strong>Cara mengumpulkan:</strong> unggah ketiga berkas di aktivitas ini (maksimal 5 berkas; PDF, PNG, atau DOCX). Kolom teks boleh diisi tautan Figma bila ada. Keterlambatan -10% per hari, maksimal 3 hari.</p>
<p><strong>Rubrik (100 poin, lulus minimal 70):</strong> kelengkapan dan ketajaman temuan audit (20) | kualitas perbaikan wireframe: penerapan prinsip ergonomi dan aksesibilitas (30) | kejelasan ide proyek: masalah, target pengguna, hipotesis nilai (25) | kelayakan dan fokus fitur inti (15) | kerapian penyajian dan kepatuhan format (10).</p>
<p>Penggunaan AI wajib diungkapkan di akhir berkas (alat apa, untuk bagian mana) - lihat Kontrak Kuliah bagian 8.</p>
<p><em>Catatan: Tugas 2 dimajukan dari Pertemuan 3 ke Pertemuan 2 mengikuti Modul Pertemuan 2; bobotnya tetap 6%.</em></p>"""


def dt(prefix, d, m, y, hh, mm):
    return {prefix + "[enabled]": "1", prefix + "[day]": str(d), prefix + "[month]": str(m),
            prefix + "[year]": str(y), prefix + "[hour]": str(hh), prefix + "[minute]": str(mm)}


def show(cmid, keys):
    f = formpost.parse_form(moodle.formfields(cmid))
    d = dict(f)
    out = {k: d.get(k) for k in keys}
    for p in ("allowsubmissionsfromdate", "duedate", "cutoffdate", "gradingduedate"):
        en = d.get(p + "[enabled]")
        out[p] = ("%s-%s-%s %s:%s" % (d.get(p + "[year]"), d.get(p + "[month]"), d.get(p + "[day]"),
                                      d.get(p + "[hour]"), d.get(p + "[minute]"))) if en == "1" else "OFF"
    return out, d


if __name__ == "__main__":
    sweep_pma.ensure_login()
    # --- Tugas 1: bobot 5% -> 3% (kontrak bagian 6)
    before, d1 = show(491624, ["name"])
    print("T1 sebelum:", before)
    intro = d1["introeditor[text]"]
    if "Bobot 5% (sesuai RPS)" in intro:
        ov = {"introeditor[text]": intro.replace("Bobot 5% (sesuai RPS)",
                                                 "Bobot 3% (komponen Observasi, lihat Kontrak Kuliah bagian 6)")}
        if d1.get("gradingduedate[enabled]") == "1" and d1.get("gradingduedate[year]") == "2025":
            ov.update(dt("gradingduedate", 27, 9, 2026, 23, 55))
        r = nlp_p2_due.repost(491624, ov)
        after, d1b = show(491624, ["name"])
        print("T1 http%d sesudah:" % r.status_code, after, "| 3% ada:", "Bobot 3%" in d1b["introeditor[text]"])
    else:
        print("T1: frasa 5% tidak ada, lewati")
    # --- Tugas 2
    before, d2 = show(491632, ["name", "visible", "assignsubmission_file_enabled", "assignsubmission_file_maxfiles", "assignsubmission_onlinetext_enabled"])
    print("T2 sebelum:", before)
    ov = {"name": T2_NAME, "introeditor[text]": T2_INTRO, "introeditor[format]": "1",
          "assignsubmission_file_enabled": "1", "assignsubmission_file_maxfiles": "5",
          "assignsubmission_onlinetext_enabled": "1", "visible": "1"}
    ov.update(dt("allowsubmissionsfromdate", 17, 9, 2026, 0, 0))
    ov.update(dt("duedate", 27, 9, 2026, 23, 55))
    ov.update(dt("gradingduedate", 4, 10, 2026, 23, 55))
    r = nlp_p2_due.repost(491632, ov)
    after, d2b = show(491632, ["name", "visible", "assignsubmission_file_enabled", "assignsubmission_file_maxfiles", "assignsubmission_onlinetext_enabled"])
    print("T2 http%d sesudah:" % r.status_code, after)
    print("T2 intro baru:", "Tenggat: Minggu, 27 September 2026" in d2b["introeditor[text]"])
