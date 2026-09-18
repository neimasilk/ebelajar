# -*- coding: utf-8 -*-
"""Sekali jalan (17 Sep 2026): placeholder {TUGAS2} di modul_p2.html AP1 + konstanta di edit_modul.py."""
import os

BASE = r"D:\documents\ebelajar\ganjil-2026-2027"

p = os.path.join(BASE, "application-project-1", "modul_p2.html")
s = open(p, encoding="utf-8").read()
old = ('<li>Tugas 2 &mdash; Brainstorming akan dibuka setelah jadwal pertemuan ini terkonfirmasi '
       'kalender akademik; ikuti pengumuman.</li>')
if old in s:
    s = s.replace(old, "{TUGAS2}")
    s = s.replace("Placeholder: {DISKUSI} -->", "Placeholder: {DISKUSI} {TUGAS2} -->")
    open(p, "w", encoding="utf-8").write(s)
    print("modul_p2.html: placeholder dipasang")
else:
    print("modul_p2.html: kalimat lama tidak ada (sudah?)", "{TUGAS2}" in s)

p = os.path.join(BASE, "_tools", "edit_modul.py")
s = open(p, encoding="utf-8").read()
old_t = ('     {"A": (491628, {"DISKUSI": "%s/mod/forum/view.php?id=491616" % EB}),\n'
         '      "P": (491576, {"DISKUSI": "%s/mod/forum/view.php?id=491564" % EB})},')
new_t = ('     {"A": (491628, {"DISKUSI": "%s/mod/forum/view.php?id=491616" % EB, "TUGAS2": TUGAS2_A}),\n'
         '      "P": (491576, {"DISKUSI": "%s/mod/forum/view.php?id=491564" % EB, "TUGAS2": TUGAS2_P})},')
const = '''# 17 Sep 2026: Tugas 2 AP1 A dimajukan ke P2 (keputusan user). Kelas P tetap kalimat lama.
# {EXIT} diisi cmid forum exit-ticket P2 oleh ap1_p2_setup.py.
TUGAS2_A = ('<li><strong><a href="%s/mod/assign/view.php?id=491632">TUGAS 2: Audit Ergonomi &amp; Ide Proyek '
            '(Brainstorming)</a></strong> &mdash; tenggat <strong>Minggu, 27 September 2026 pukul 23.55</strong>.</li>'
            '<li><a href="%s/mod/forum/view.php?id={EXIT}">Exit-ticket Pertemuan 2</a> &mdash; tiga pertanyaan '
            'refleksi, dijawab di akhir kelas.</li>'
            '<li><a href="https://drive.google.com/drive/folders/1yvgECF7RK8l6Hr4TG0oIG-RFdIkocAou">Bahan Pertemuan 2 '
            'di Google Drive</a> &mdash; Modul Pertemuan 2 (PDF), slide, dan dua video.</li>' % (EB, EB))
TUGAS2_P = ('<li>Tugas 2 &mdash; Brainstorming akan dibuka setelah jadwal pertemuan ini terkonfirmasi kalender '
            'akademik; ikuti pengumuman.</li>')

'''
if old_t in s:
    s = s.replace(old_t, new_t)
    s = s.replace("# (label, path_html", const + "# (label, path_html", 1)
    open(p, "w", encoding="utf-8").write(s)
    print("edit_modul.py: TARGETS AP1 P2 diperbarui")
else:
    print("edit_modul.py: pola TARGETS tidak ketemu (sudah?)", "TUGAS2_A" in s)
