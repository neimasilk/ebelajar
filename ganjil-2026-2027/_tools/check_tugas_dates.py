# -*- coding: utf-8 -*-
"""Cek setelan tanggal semua assign di 6 kursus Ganjil 2026/2027.

Laporan user 15 Sep: mahasiswa NLP A tidak bisa mengumpulkan Tugas 1.
Dugaan: allowsubmissionsfromdate masih warisan 2025 (25 Sep) -> submit tertutup.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# muat .env SEBELUM import moodle (moodle.py baca env saat import)
env = {}
with open(r"D:\knowledge-base\.env", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
os.environ.setdefault("EBELAJAR_USER", env.get("user_ebelajar", ""))
os.environ.setdefault("EBELAJAR_PASS", env.get("pass_ebelajar", ""))

import moodle, formpost, sweep_pma

COURSES = [
    (7218, "PM A"), (7226, "NLP A"), (7278, "AP1 A"),
    (7365, "PM P"), (7427, "NLP P"), (7426, "AP1 P"),
]
DATE_KEYS = ["allowsubmissionsfromdate", "duedate", "cutoffdate"]


def fmt(fields, prefix):
    d = dict(fields)
    en = d.get(prefix + "_enabled", "1")
    if en in ("0", ""):
        return None
    try:
        return "%s-%s-%s %s:%s" % (d[prefix + "[year]"], d[prefix + "[month]"],
                                   d[prefix + "[day]"], d[prefix + "[hour]"],
                                   d[prefix + "[minute]"])
    except KeyError:
        return "?"


def main():
    sweep_pma.ensure_login()
    only_visible = "--all" not in sys.argv
    for cid, label in COURSES:
        print("=" * 70)
        print("KURSUS %s (%d)" % (label, cid))
        dump = moodle.course_dump(cid)
        for num, name, hidden, mods in dump:
            if num == 0:
                continue
            for cmid, typ, nm in mods:
                if typ != "assign":
                    continue
                if only_visible and hidden:
                    print("  [section %d HIDDEN] %d %s  (dilewati)" % (num, cmid, nm))
                    continue
                f = formpost.parse_form(moodle.formfields(cmid))
                dates = []
                for k in DATE_KEYS:
                    v = fmt(f, k)
                    dates.append("%s=%s" % (k, v if v else "OFF"))
                # info submission jenis file/online text
                d = dict(f)
                st = []
                if d.get("assignsubmission_file_enabled") == "1":
                    st.append("file(max %s)" % d.get("assignsubmission_file_maxfiles", "?"))
                if d.get("assignsubmission_onlinetext_enabled") == "1":
                    st.append("onlinetext")
                print("  S%-2d cmid=%d %-45s %s | subm: %s" % (num, cmid, nm[:45], " ".join(dates), ",".join(st) or "?"))


if __name__ == "__main__":
    main()
