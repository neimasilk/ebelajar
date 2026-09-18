# -*- coding: utf-8 -*-
"""Verifikasi akhir AP1 A P2 (17 Sep 2026): isi Section 1-3, tanggal tugas, nilai forum di gradebook."""
import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, formpost, sweep_pma
import check_tugas_dates as ctd
from ap1_p2_setup import section_mods, C


def txt(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


if __name__ == "__main__":
    sweep_pma.ensure_login()
    t = moodle.get("/course/view.php?id=%d" % C).text
    for sn in (1, 2, 3):
        m = re.search(r'<li id="section-%d"[^>]*class="([^"]*)"' % sn, t)
        print("S%d class=%s" % (sn, m.group(1) if m else "?"))
        for typ, cmid, nm in section_mods(sn):
            extra = ""
            if typ == "assign":
                f = formpost.parse_form(moodle.formfields(cmid))
                d = dict(f)
                extra = " | " + " ".join("%s=%s" % (k[:10], ctd.fmt(f, k) or "OFF") for k in ctd.DATE_KEYS)
                extra += " | cutoff_en=%s visible=%s" % (d.get("cutoffdate[enabled]", "OFF"), d.get("visible"))
            print("   %-7s %d %s%s" % (typ, cmid, nm, extra))
        # batasi split: section_mods memotong mulai section-N sampai akhir halaman
    v = txt(moodle.get("/mod/assign/view.php?id=491632").text)
    i = v.find("Grading summary")
    print("T2 view:", v[i:i + 200])
    g = moodle.get("/grade/report/grader/index.php?id=%d" % C).text
    gt = txt(g)
    for nm in ("TYO", "DEVAN"):
        j = gt.find(nm)
        print("gradebook", nm, gt[j:j + 160] if j >= 0 else "tak ketemu")
    heads = re.findall(r'<a[^>]*class="gradeitemheader"[^>]*>(.*?)</a>', g, re.S)
    print("kolom gradebook:", [txt(h) for h in heads])
