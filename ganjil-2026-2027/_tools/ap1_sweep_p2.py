# -*- coding: utf-8 -*-
"""Sweep AP1 A (7278) jelang Pertemuan 2 (Kamis 17 Sep 2026)."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, formpost, sweep_pma, check_tugas_dates as ctd

CID = 7278
sweep_pma.ensure_login()
dump = moodle.course_dump(CID)
for num, name, hidden, mods in dump:
    if num > 4: break
    print("S%-3d %s %s" % (num, "HID" if hidden else "   ", name))
    for cmid, typ, nm in mods:
        extra = ""
        if typ == "assign":
            f = formpost.parse_form(moodle.formfields(cmid))
            extra = " | " + " ".join("%s=%s" % (k[:12], ctd.fmt(f, k) or "OFF") for k in ctd.DATE_KEYS)
        print("      %-9s %d  %s%s" % (typ, cmid, nm, extra))
# forum posts di section 0-2
for num, name, hidden, mods in dump:
    if num > 2: break
    for cmid, typ, nm in mods:
        if typ != "forum": continue
        ds = sweep_pma.forum_discussions(cmid)
        print("\nFORUM %d %s: %d diskusi" % (cmid, nm, len(ds)))
        for did, t in ds[:15]:
            ps = sweep_pma.forum_posts(cmid, did)
            print("   d=%d %s  (%d post)" % (did, t[:60], len(ps)))
            for p in ps:
                print("      p%d %s | %s | %s" % (p["pid"], p["author"], p["date"], p["body"][:160]))
