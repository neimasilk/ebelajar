# -*- coding: utf-8 -*-
"""Kelas P itu self-paced -> hapus SEMUA tenggat (permintaan user 8 Sep).

Yang dimatikan: duedate, cutoffdate, gradingduedate, allowsubmissionsfromdate (assign);
timeopen, timeclose (quiz). Gating/completion sengaja TIDAK disentuh — repost membaca
seluruh form lalu mengirimnya kembali utuh.
"""
import re, sys
import moodle
import ap1_sync as S

COURSES = [(7426, "AP1 P"), (7365, "PM P"), (7427, "NLP P")]

OFF_ASSIGN = {
    "duedate[enabled]": "",
    "cutoffdate[enabled]": "",
    "gradingduedate[enabled]": "",
    "allowsubmissionsfromdate[enabled]": "",
}
OFF_QUIZ = {
    "timeopen[enabled]": "",
    "timeclose[enabled]": "",
}


def targets(cid):
    out = []
    for num, name, hidden, mods in moodle.course_dump(cid):
        for cmid, typ, nm in mods:
            if typ in ("assign", "quiz"):
                out.append((cmid, typ, nm))
    return out


def dates_of(cmid, typ):
    """Baca tanggal yang masih aktif (untuk verifikasi)."""
    t = moodle.get("/course/modedit.php?update=%d" % cmid).text
    on = []
    keys = (["duedate", "cutoffdate", "gradingduedate", "allowsubmissionsfromdate"]
            if typ == "assign" else ["timeopen", "timeclose"])
    for k in keys:
        for m in re.finditer(r"<input[^>]*>", t):
            tag = m.group(0)
            if 'name="%s[enabled]"' % k in tag and "checked" in tag:
                on.append(k)
                break
    return on


if __name__ == "__main__":
    dry = "--apply" not in sys.argv
    for cid, label in COURSES:
        tg = targets(cid)
        print("=" * 60)
        print("%s (%d) — %d aktivitas bertanggal" % (label, cid, len(tg)))
        for cmid, typ, nm in tg:
            before = dates_of(cmid, typ)
            if not before:
                print("   %-7s %s  %-46s sudah bersih" % (typ, cmid, nm[:46]))
                continue
            if dry:
                print("   %-7s %s  %-46s aktif: %s" % (typ, cmid, nm[:46], ",".join(before)))
                continue
            ov = OFF_ASSIGN if typ == "assign" else OFF_QUIZ
            r = S.repost(cmid, dict(ov))
            after = dates_of(cmid, typ)
            print("   %-7s %s  %-46s %s -> %s  http%d"
                  % (typ, cmid, nm[:46], ",".join(before), ",".join(after) or "BERSIH", r.status_code))
