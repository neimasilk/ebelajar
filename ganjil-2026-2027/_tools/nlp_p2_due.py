# -*- coding: utf-8 -*-
"""Tugas 1 NLP A (491786): samakan tenggat dengan pola PM A -> 27 Sep 2026 23:55.

Repost form modedit (parser formpost, urutan atribut aman) + override duedate.
Read-back WAJIB setelah repost (modedit sering 404 tapi tersimpan).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sweep_pma, moodle, formpost

CMID = 491786
DUE = {"duedate[day]": "27", "duedate[month]": "9", "duedate[year]": "2026",
       "duedate[hour]": "23", "duedate[minute]": "55"}


def repost(cmid, ov):
    t = moodle.formfields(cmid)
    fields = formpost.parse_form(t)
    assert fields, "form kosong - login gagal?"
    data = formpost.apply(fields, ov)
    data.append(("submitbutton2", "Save and return to course"))
    r = moodle.sess().post(moodle.BASE + "/course/modedit.php", data=data, timeout=180)
    return r


def readback(cmid):
    d = dict(formpost.parse_form(moodle.formfields(cmid)))
    return {k: d[k] for k in sorted(d) if k.startswith("duedate[") or k.startswith("cutoffdate[") or k.startswith("allowsubmissionsfromdate[")}


if __name__ == "__main__":
    sweep_pma.ensure_login()
    print("sebelum:", readback(CMID))
    r = repost(CMID, DUE)
    print("POST http", r.status_code)
    after = readback(CMID)
    print("sesudah:", after)
    ok = (after.get("duedate[day]"), after.get("duedate[month]"), after.get("duedate[year]"),
          after.get("duedate[hour]"), after.get("duedate[minute]")) == ("27", "9", "2026", "23", "55")
    print("VERIFIKASI:", "OK" if ok else "GAGAL")
