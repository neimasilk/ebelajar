# -*- coding: utf-8 -*-
"""Sinkronkan Tugas 1 AP1 (A & P) dengan kontrak + deck, lalu sembunyikan duplikatnya.

Cara aman: baca SELURUH form modedit, timpa beberapa field saja, kirim ulang utuh
(pelajaran 7 Sep: menyusun POST dari nol merusak availability/completion/tanggal).
"""
import re, sys
from html.parser import HTMLParser
import moodle

BASE = moodle.BASE


class FormReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.fields = []
        self._select = None
        self._ta = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "input":
            name = a.get("name")
            if not name:
                return
            typ = (a.get("type") or "text").lower()
            if typ in ("submit", "button", "image", "reset"):
                return
            if typ in ("checkbox", "radio"):
                if "checked" in a:
                    self.fields.append((name, a.get("value", "1")))
                return
            self.fields.append((name, a.get("value", "")))
        elif tag == "select":
            self._select = [a.get("name"), [], False]
        elif tag == "option" and self._select is not None:
            if "selected" in a:
                self._select[1].append(a.get("value", ""))
                self._select[2] = True
        elif tag == "textarea":
            self._ta = [a.get("name"), []]

    def handle_endtag(self, tag):
        if tag == "select" and self._select is not None:
            name, sel, had = self._select
            if name and had:
                for v in sel:
                    self.fields.append((name, v))
            self._select = None
        elif tag == "textarea" and self._ta is not None:
            name, buf = self._ta
            if name:
                self.fields.append((name, "".join(buf)))
            self._ta = None

    def handle_data(self, data):
        if self._ta is not None:
            self._ta[1].append(data)


def read_form(cmid):
    t = moodle.get("/course/modedit.php?update=%d" % cmid).text
    m = re.search(r'<form[^>]*action="[^"]*modedit\.php[^"]*"[^>]*>.*?</form>', t, re.S)
    frag = m.group(0) if m else t
    fr = FormReader()
    fr.feed(frag)
    return fr.fields


def repost(cmid, overrides):
    fields = read_form(cmid)
    data, seen = [], set()
    for name, value in fields:
        if name in overrides:
            if name in seen:
                continue
            seen.add(name)
            data.append((name, overrides[name]))
        else:
            data.append((name, value))
    for name, value in overrides.items():
        if name not in seen:
            data.append((name, value))
            seen.add(name)
    data.append(("submitbutton2", "Save and return to course"))
    r = moodle.sess().post(BASE + "/course/modedit.php", data=data, timeout=180)
    return r


def set_visible(cmid, visible):
    sk = moodle.sesskey()
    act = "show" if visible else "hide"
    r = moodle.get("/course/mod.php?sesskey=%s&%s=%d" % (sk, act, cmid))
    return r.status_code


TUGAS1_A = """<p><strong>Tugas 1 &mdash; Wireframe Halaman Utama</strong> &nbsp;|&nbsp; Bobot <strong>5%</strong> (sesuai RPS)</p>

<p>Rancang <strong>wireframe halaman utama</strong> dari produk web yang akan dikerjakan kelompok Anda semester ini.
Wireframe = kerangka: kotak, garis, label. <strong>Tanpa warna, tanpa gaya, tanpa gambar asli</strong> &mdash;
yang diuji adalah struktur dan prioritas, bukan keindahan. Boleh di kertas (difoto) maupun di Figma.</p>

<p><strong>Yang dikumpulkan:</strong></p>
<ol>
<li><strong>1 berkas wireframe</strong> halaman utama, format <strong>PDF atau PNG</strong>, diberi
<strong>anotasi</strong> (panah + satu kalimat: kenapa elemen ini diletakkan di sini).</li>
<li><strong>1 paragraf</strong> yang menjelaskan penerapan <strong>hierarki visual</strong>,
<strong>konsistensi</strong>, dan <strong>keterbacaan</strong> pada rancangan Anda.
Bukan mendeskripsikan gambarnya &mdash; melainkan <strong>alasan</strong> di balik tiap keputusan.</li>
</ol>

<p><strong>Tugas 1b &mdash; Data Kelompok</strong> (satu berkas per kelompok): nama kelompok, ketua (NIM &amp; nama),
anggota (NIM &amp; nama), kanal komunikasi, dan komitmen jadwal pertemuan mingguan.</p>

<p><strong>Nama berkas:</strong> <code>AP1_P1_NIM_Nama_Wireframe.pdf</code> &mdash;
data kelompok: <code>AP1_P1_KelompokX_Data.txt</code></p>

<p><strong>Yang diperiksa saat menilai:</strong> apakah aksi utama benar-benar paling menonjol &middot;
apakah elemen sejenis diperlakukan sama &middot; apakah teks nyaman dibaca di layar kecil &middot;
apakah ada alasan di balik keputusan &middot; apakah keadaan kosong/error ikut dipikirkan.</p>

<p><em>Rujukan: Dan Olsen (2015), The Lean Product Playbook. Uraian lengkap ada di slide Pertemuan 1
dan di Kontrak Kuliah.</em></p>"""

TUGAS1_P = TUGAS1_A.replace(
    """<p><strong>Tugas 1b &mdash; Data Kelompok</strong> (satu berkas per kelompok): nama kelompok, ketua (NIM &amp; nama),
anggota (NIM &amp; nama), kanal komunikasi, dan komitmen jadwal pertemuan mingguan.</p>""",
    """<p><strong>Khusus kelas P: dikerjakan perorangan.</strong> Sebagai ganti kerja kelompok, tunjuk satu
<strong>mitra uji</strong> &mdash; teman, keluarga, atau rekan kerja mana pun. Minta ia menebak apa aksi utama
halaman Anda <em>tanpa Anda jelaskan lebih dulu</em>, lalu <strong>sebutkan di paragraf Anda siapa mitra uji itu
dan apa yang ia salah tebak.</strong> Kalau ia salah menebak, itu temuan &mdash; bukan kegagalan.</p>""",
).replace(
    """ &mdash;
data kelompok: <code>AP1_P1_KelompokX_Data.txt</code>""", "")

# tanggal: kelas A -> Minggu 20 Sep 2026 23.55 (aturan kontrak: Minggu 23.55 minggu berikutnya)
DUE_A = {"duedate[enabled]": "1", "duedate[day]": "20", "duedate[month]": "9", "duedate[year]": "2026",
         "duedate[hour]": "23", "duedate[minute]": "55"}

if __name__ == "__main__":
    print("== TUGAS 1 kelas A (491624) ==")
    ov = {"introeditor[text]": TUGAS1_A}
    ov.update(DUE_A)
    r = repost(491624, ov)
    print("   http", r.status_code)

    print("== TUGAS 1 kelas P (491572) ==")
    r = repost(491572, {"introeditor[text]": TUGAS1_P})
    print("   http", r.status_code)

    print("== sembunyikan duplikat ==")
    for cmid in (491626, 491574):
        print("   hide", cmid, "->", set_visible(cmid, False))
