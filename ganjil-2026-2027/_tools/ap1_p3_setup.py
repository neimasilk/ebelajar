# -*- coding: utf-8 -*-
"""Setup section 3 AP1 A (course 7278) untuk Pertemuan 3, Kamis 24 Sep 2026.

Section 3 & 4 kosong (tanpa warisan 2025). Langkah:
1. Duplikat URL P2 (502322) -> Bahan Pertemuan 3 di Google Drive -> S3
2. Duplikat forum Exit P2 (502324) -> Exit-ticket P3 + seed 3 refleksi -> S3
3. Duplikat TUGAS 2 (491632) -> TUGAS 3 (due Minggu 4 Okt 23.55) -> S3
4. Duplikat page materi P2 (491628) -> isi modul_p3.html -> S3
5. Rename + buka section 3 (editsection dbid 137025), unhide semua modul baru
6. Verifikasi course_dump + read-back

Semua konten ASCII (pelajaran 14 Sep: em-dash korup jadi U+FFFD).
"""
import os, re, sys, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, sweep_pma, formpost
from ap1_sync import repost, set_visible

EB = "https://ebelajar.stiki.ac.id"
CID = 7278
S3_DBID = 137025
URL_P2 = 502322
FORUM_EXIT2 = 502324
TUGAS2 = 491632
PAGE_P2 = 491628
DRIVE_P3 = "https://drive.google.com/drive/folders/1QScoRtDclfPY3hes3UMmJv3rcj6IrhV3"

SEC3_NAME = "Pertemuan 3 - Estetika dalam Desain UI & Penyusunan Proposal Proyek"

TUGAS3_INTRO = """<p><strong>Tugas 3 - Dari wireframe ke mockup + draft proposal</strong> | Bobot sesuai RPS</p>
<p>Tiga deliverable mengikuti Modul Pertemuan 3:</p>
<ol>
<li><strong>Tugas 3a - Style Guide</strong> (individu atau kelompok kecil): satu halaman berisi
palet warna 5 peran + skala abu-abu, type scale (H1-H6, Body, Caption) + contoh ukuran/line-height,
komponen inti dengan variasi state, aturan spacing 8-point. Berkas: <code>StyleGuide_P3.pdf</code>
(tambahkan NIM_Nama untuk individu).</li>
<li><strong>Tugas 3b - Mockup Dua Layar</strong> (individu): Beranda dan Layar Fitur Inti, fidelity
menengah, konsisten dengan style guide. Berkas: <code>Mockup_P3_Home.pdf</code> +
<code>Mockup_P3_FiturInti.pdf</code> (file sumber opsional).</li>
<li><strong>Tugas 3c - Draft Proposal</strong> (kelompok): 1-2 halaman berisi 7 komponen
(Judul &amp; Ringkasan; Masalah &amp; Target Pengguna; Hipotesis Nilai; Fitur Inti MVP +
Out-of-Scope; Risiko &amp; Asumsi Kritis; Metrik Keberhasilan Awal; Rencana Validasi).
Berkas: <code>AP1_P3_KelompokX_Proposal.pdf</code>.</li>
</ol>
<p><strong>Rubrik (100 poin):</strong> Kualitas Style Guide 25; Estetika &amp; Konsistensi Mockup 30;
Aksesibilitas &amp; Keterbacaan 20; Kecocokan dengan Tujuan Pengguna 15; Kerapian &amp; Kepatuhan
Format 10. <strong>Lulus tugas: minimal 70.</strong></p>
<p><em>Pelajaran dari Tugas 1: ini sebagian tugas individu - setiap orang mengumpulkan berkas
sendiri untuk 3a/3b; foto/berkas bersama tanpa kontribusi individu dinilai rendah.</em></p>"""

EXIT3_SEED = """<p>Balas diskusi ini dengan jawaban singkat (2-3 kalimat per nomor):</p>
<ol>
<li>Keputusan estetika apa yang paling meningkatkan kejelasan tujuan pengguna?</li>
<li>Bagian mana dari style guide yang paling membantu menjaga konsistensi saat membuat mockup?</li>
<li>Risiko/asumsi apa di proposal yang perlu divalidasi paling awal, dan bagaimana caranya?</li>
</ol>
<p>Jawab setelah praktik di kelas, sebelum meninggalkan ruangan. Ini bagian dari kehadiran
berkualitas: jawaban yang mengacu ke rancangan Anda sendiri, bukan definisi umum.</p>"""


def module_cmid_set():
    out = set()
    for num, name, hid, mods in moodle.course_dump(CID):
        for cmid, typ, nm in mods:
            out.add(cmid)
    return out


def duplicate(cmid):
    """Duplikat modul; kembalikan cmid baru (diff cmid course_dump).
    PELAJARAN 24 Sep: Moodle ini TIDAK menambah '(copy)' - jangan cari nama copy."""
    before = module_cmid_set()
    moodle.sess().get("%s/course/mod.php?duplicate=%d&sesskey=%s"
                      % (EB, cmid, moodle.sesskey()), timeout=120)
    after = module_cmid_set()
    new = after - before
    assert len(new) == 1, "dup %d -> diff=%s" % (cmid, new)
    return new.pop()


def move_to_s3(cmid):
    sk = moodle.sesskey()
    moodle.sess().get("%s/course/mod.php?copy=%d&sesskey=%s" % (EB, cmid, sk), timeout=60)
    moodle.sess().get("%s/course/mod.php?movetosection=%d&sesskey=%s"
                      % (EB, S3_DBID, sk), timeout=60)


def forum_instance(cmid):
    t = moodle.get("/mod/forum/view.php?id=%d" % cmid).text
    m = re.search(r'/mod/forum/post\.php\?forum=(\d+)', t)
    return int(m.group(1)) if m else None


def post_discussion(instance, subject, body_html):
    r = moodle.get("/mod/forum/post.php?forum=%d" % instance)
    act_m = re.search(r'<form[^>]*id="mform[^"]*"[^>]*action="([^"]+)"', r.text)
    act = H.unescape(act_m.group(1))
    if not act.startswith("http"):
        act = EB + ("/" + act.lstrip("/"))
    fields = formpost.parse_form(r.text)
    data = formpost.apply(fields, {
        "subject": subject,
        "message[text]": body_html,
        "message[format]": "1",
    })
    data = [(k, v) for k, v in data if not k.startswith("cancel")]
    data.append(("submitbutton", "Post to forum"))
    rr = moodle.sess().post(act, data=data, timeout=120)
    return "http%d" % rr.status_code


def edit_section_name(dbid, name):
    r = moodle.get("/course/editsection.php?id=%d" % dbid)
    act_m = re.search(r'<form[^>]*action="([^"]*)"[^>]*>', r.text)
    act = H.unescape(act_m.group(1))
    if not act.startswith("http"):
        act = EB + ("/" + act.lstrip("/"))
    fields = formpost.parse_form(r.text)
    data = formpost.apply(fields, {"name": name})
    data = [(k, v) for k, v in data if not k.startswith("cancel")]
    rr = moodle.sess().post(act, data=data, timeout=120)
    return rr.status_code


def set_dates(cmid, from_d, due_d):
    """from_d/due_d = (day, month, year)."""
    ov = {}
    for key, (d, m, y) in (("allowsubmissionsfromdate", from_d), ("duedate", due_d)):
        ov["%s[enabled]" % key] = "1"
        ov["%s[day]" % key] = str(d)
        ov["%s[month]" % key] = str(m)
        ov["%s[year]" % key] = str(y)
        ov["%s[hour]" % key] = "23" if key == "duedate" else "16"
        ov["%s[minute]" % key] = "55" if key == "duedate" else "0"
    return ov


if __name__ == "__main__":
    sweep_pma.ensure_login()
    sk = moodle.sesskey()
    moodle.sess().get("%s/course/view.php?id=%d&edit=on&sesskey=%s" % (EB, CID, sk), timeout=60)

    print("== 0. bersihkan salinan yatim dari percobaan pertama ==")
    # 503170/503171 = duplikat 502322 yang terlanjur terbuat saat diff masih salah.
    for stray in (503170, 503171):
        if stray in module_cmid_set():
            # mod.php?delete = halaman konfirmasi; POST balik dengan confirm=1
            rr = moodle.sess().post("%s/course/mod.php" % EB,
                                    data={"confirm": "1", "delete": str(stray),
                                          "sesskey": sk, "sr": "", "id": str(CID)},
                                    timeout=60)
            print("   hapus %d: http%d (konfirmasi)" % (stray, rr.status_code))
    left = module_cmid_set()
    for stray in (503170, 503171):
        assert stray not in left, "stray %d masih ada" % stray

    print("== 1. duplikat URL P2 ==")
    url3 = duplicate(URL_P2)
    print("   baru cmid=%d" % url3)
    r = repost(url3, {
        "name": "Bahan Pertemuan 3 di Google Drive (modul, slide)",
        "externalurl": DRIVE_P3,
    })
    print("   edit http%d" % r.status_code)
    move_to_s3(url3)

    print("== 2. duplikat forum Exit P2 ==")
    ex3 = duplicate(FORUM_EXIT2)
    print("   baru cmid=%d" % ex3)
    r = repost(ex3, {
        "name": "Exit-ticket Pertemuan 3 (Estetika UI & Proposal)",
        "introeditor[text]": "Tiga pertanyaan refleksi Pertemuan 3. Dijawab di akhir kelas.",
    })
    print("   edit http%d" % r.status_code)
    move_to_s3(ex3)
    inst = forum_instance(ex3)
    print("   instance=%s" % inst)
    if inst:
        print("   seed:", post_discussion(
            inst,
            "Exit-ticket Pertemuan 3 - jawab tiga pertanyaan ini",
            EXIT3_SEED))

    print("== 3. duplikat TUGAS 2 -> TUGAS 3 ==")
    tg3 = duplicate(TUGAS2)
    print("   baru cmid=%d" % tg3)
    ov = {
        "name": "TUGAS 3: Style Guide, Mockup & Draft Proposal",
        "introeditor[text]": TUGAS3_INTRO,
    }
    ov.update(set_dates(tg3, (24, 9, 2026), (4, 10, 2026)))
    r = repost(tg3, ov)
    print("   edit http%d" % r.status_code)
    move_to_s3(tg3)

    print("== 4. duplikat page materi P2 -> materi P3 ==")
    pg3 = duplicate(PAGE_P2)
    print("   baru cmid=%d" % pg3)
    tpl = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "application-project-1", "modul_p3.html"), encoding="utf-8").read()
    tpl = re.sub(r"<!--.*?-->", "", tpl, flags=re.S)
    body = tpl.strip()
    ph = {
        "{DISKUSI}": "%s/mod/forum/view.php?id=491616" % EB,
        "{TUGAS3}": "%s/mod/assign/view.php?id=%d" % (EB, tg3),
        "{EXIT}": "%s/mod/forum/view.php?id=%d" % (EB, ex3),
        "{DRIVE}": DRIVE_P3,
    }
    for k, v in ph.items():
        body = body.replace(k, v)
    left = re.findall(r"\{[A-Z_]+\}", body)
    assert not left, "placeholder sisa: %s" % left
    r = repost(pg3, {
        "name": "Estetika dalam Desain UI & Penyusunan Proposal Proyek",
        "introeditor[text]": "Lima alat estetika UI (komposisi, warna, tipografi, whitespace, state), "
                             "dari wireframe ke mockup 2 layar, dan draft proposal 7 komponen.",
        "page[text]": body,
    })
    print("   edit http%d" % r.status_code)
    move_to_s3(pg3)

    print("== 5. rename + buka section 3 ==")
    print("   rename http%s" % edit_section_name(S3_DBID, SEC3_NAME))
    r = moodle.sess().get("%s/course/mod.php?show=%d&sesskey=%s" % (EB, S3_DBID, sk), timeout=60)
    print("   unhide section http%d" % r.status_code)

    print("== 6. unhide modul baru ==")
    for cmid in (url3, ex3, tg3, pg3):
        print("   show %d -> %s" % (cmid, set_visible(cmid, True)))

    print("== ringkasan cmid ==")
    print("URL3=%d EXIT3=%d TUGAS3=%d PAGE3=%d" % (url3, ex3, tg3, pg3))
