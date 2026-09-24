# -*- coding: utf-8 -*-
"""Sweep AP1 A (7278) jelang Pertemuan 3 (Kamis 24 Sep 2026).

Baca: semua forum (Perkenalan, Diskusi P1, Exit P2, Diskusi Umum) + TUGAS 1 + TUGAS 2.
Tanpa perubahan apapun - baca saja.
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, sweep_pma
from sweep_pma import text_of, forum_discussions, forum_posts

CID = 7278
FORUMS = {
    491618: "Perkenalan",
    491623: "Diskusi P1",
    502324: "Exit-ticket P2",
    491616: "Diskusi Umum",
}
TUGAS1 = 491624
TUGAS2 = 491632


def rating_status(disc_html, pid):
    seg = re.search(r'<a id="p%d"></a>(.*?)(?=<a id="p\d+"></a>|$)' % pid,
                    disc_html, re.S)
    if not seg:
        return "?"
    body = seg.group(1)
    mm = re.search(r'Average of ratings:\s*(?:<[^>]+>\s*)*([\d.\-]+)', body)
    if mm:
        return "avg=" + mm.group(1)
    sel = re.search(r'id="postrating%d".*?<option[^>]*value="(\d+)"[^>]*selected' % pid, body, re.S)
    if sel:
        return "rated=" + sel.group(1)
    return "-"


def assign_detail(cmid, label):
    print("\n=== %s (%d) ===" % (label, cmid))
    r = moodle.get("/mod/assign/view.php?id=%d&action=grading" % cmid)
    t = r.text
    plain = text_of(t)
    m = re.search(r'Submitted for grading[^0-9]*(\d+)', plain)
    print("  submitted: %s" % (m.group(1) if m else "?"))
    # baris tabel grading: nama + status + grade
    rows = re.findall(
        r'user/view\.php\?id=(\d+)[^"]*">(.*?)</a>.*?'
        r'(Submitted for grading - .*?|No submission|Submitted for grading).*?'
        r'(?:Graded|gradeinfo|c\d+ grade)(.*?)</td>',
        t, re.S)
    seen = set()
    for uid, nm, st, tail in rows:
        if uid in seen:
            continue
        seen.add(uid)
        nm = text_of(nm)
        grade = ""
        gm = re.search(r'>(\d+(?:[.,]\d+)?)\s*/\s*100', text_of(tail))
        if gm:
            grade = " nilai=" + gm.group(1)
        # status submission terakhir + waktu
        stt = "submitted" if st.startswith("Submitted") else "belum"
        print("  uid=%s %-28s %s%s" % (uid, nm, stt, grade))
    if not rows:
        print("  (tabel grading tidak terbaca; cek manual)")


def main():
    sweep_pma.ensure_login()
    print("=== course dump AP1 A %d ===" % CID)
    for num, name, hidden, mods in moodle.course_dump(CID):
        if num > 4:
            break
        print("S%-3d %s %s" % (num, "HID" if hidden else "   ", name))
        for cmid, typ, nm in mods:
            print("      %-9s %d  %s" % (typ, cmid, nm))

    for fmid, name in FORUMS.items():
        r = moodle.get("/mod/forum/view.php?id=%d" % fmid)
        print("\n=== FORUM %d: %s ===" % (fmid, name))
        discs = forum_discussions(fmid)
        if not discs:
            print("  (tidak ada diskusi)")
        for did, title in discs:
            print("  diskusi d=%d: %s" % (did, title))
            dr = moodle.get("/mod/forum/discuss.php?d=%d" % did)
            for p in forum_posts(fmid, did):
                st = rating_status(dr.text, p["pid"])
                print("    p%d | %s | %s | %s | %s" % (
                    p["pid"], p["author"], p["date"], st, p["body"][:120]))

    assign_detail(TUGAS1, "TUGAS 1 (due 20 Sep)")
    assign_detail(TUGAS2, "TUGAS 2 (due 27 Sep)")


if __name__ == "__main__":
    main()
