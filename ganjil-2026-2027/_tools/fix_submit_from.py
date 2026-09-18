# -*- coding: utf-8 -*-
"""Fix allowsubmissionsfromdate Tugas 1 NLP A (491786) + PM A (491680).

Laporan user 15 Sep: mahasiswa tidak bisa mengumpulkan. Sebab: submit-from
masih warisan 2025 = 25 Sep 2026 00:00 (setelah tenggat barunya 27 Sep).
Digeser ke 14 Sep 2026 00:00 (pola AP1 A). Read-back WAJIB.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sweep_pma, moodle, formpost, nlp_p2_due

TARGETS = [(491786, "NLP A Tugas 1"), (491680, "PM A Tugas 1")]
OV = {"allowsubmissionsfromdate[day]": "14", "allowsubmissionsfromdate[month]": "9",
      "allowsubmissionsfromdate[year]": "2026", "allowsubmissionsfromdate[hour]": "0",
      "allowsubmissionsfromdate[minute]": "0"}


def enabled_flags(cmid):
    d = dict(formpost.parse_form(moodle.formfields(cmid)))
    out = {}
    for k in ("allowsubmissionsfromdate", "duedate", "cutoffdate"):
        out[k] = d.get(k + "_enabled", "(tidak ada di form)")
    return out


if __name__ == "__main__":
    sweep_pma.ensure_login()
    for cmid, label in TARGETS:
        print("== %s (cmid %d)" % (label, cmid))
        print("   flag enabled sebelum:", enabled_flags(cmid))
        print("   tanggal sebelum     :", nlp_p2_due.readback(cmid))
        r = nlp_p2_due.repost(cmid, OV)
        print("   POST http", r.status_code)
        after = nlp_p2_due.readback(cmid)
        print("   tanggal sesudah     :", after)
        ok = (after.get("allowsubmissionsfromdate[day]"), after.get("allowsubmissionsfromdate[month]"),
              after.get("allowsubmissionsfromdate[year]"), after.get("allowsubmissionsfromdate[hour]"),
              after.get("allowsubmissionsfromdate[minute]")) == ("14", "9", "2026", "0", "0")
        ok = ok and after.get("duedate[day]") == "27" and after.get("duedate[month]") == "9"
        print("   VERIFIKASI:", "OK" if ok else "GAGAL")
