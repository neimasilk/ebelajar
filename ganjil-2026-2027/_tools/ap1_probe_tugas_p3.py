# -*- coding: utf-8 -*-
"""Probe status submit Tugas 1 & 2 AP1 A - baca halaman grading lebih teliti."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, sweep_pma
from sweep_pma import text_of

for cmid, label in [(491624, "TUGAS 1"), (491632, "TUGAS 2")]:
    r = moodle.get("/mod/assign/view.php?id=%d&action=grading" % cmid)
    t = r.text
    print("=== %s (%d) ===" % (label, cmid))
    # cari kalimat jumlah submission di halaman grading
    for pat in [r'Submitted[^<]{0,40}?(\d+)',
                r'(\d+)\s+of\s+(\d+)\s+submitted',
                r'Users submitted[^0-9]*(\d+)']:
        for m in re.finditer(pat, text_of(t), re.I):
            print("  pat %r -> %s" % (pat, m.group(0)[:80]))
    # baris peserta
    names = re.findall(r'user/view\.php\?id=(\d+)"[^>]*>([^<]{3,40})</a>', t)
    print("  peserta di tabel: %d" % len(names))
    for uid, nm in names[:30]:
        print("    uid=%s %s" % (uid, nm.strip()[:40]))
    # status per baris
    rows = re.split(r'<tr[^>]*>', t)
    for row in rows:
        if "Submitted for grading" in row or "No submission" in row:
            nm = re.search(r'user/view\.php\?id=\d+"[^>]*>([^<]+)<', row)
            st = "SUBMIT" if "Submitted for grading" in row else "belum"
            gr = re.search(r'(\d+(?:\.\d+)?)\s*<', row)
            print("    %-4s %s" % (st, (nm.group(1).strip() if nm else "?")[:40]))
