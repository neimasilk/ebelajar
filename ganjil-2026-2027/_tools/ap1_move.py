# -*- coding: utf-8 -*-
"""Pindah modul antar-section lewat jalur non-JS Moodle 3.3 (mod.php?copy -> movetosection).
Uji 17 Sep 2026 (catatan 14 Sep: rest.php no-op; UI drag berhasil). Read-back wajib.

python ap1_move.py <cmid> <section_num>
python ap1_move.py dup <cmid>        -> modduplicate, cetak cmid baru
python ap1_move.py type <cmid>       -> tampilkan type/assessed forum
"""
import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, formpost, sweep_pma
from ap1_p2_setup import section_mods, C


def section_dbid(t, num):
    # editsection.php?id=<dbid>&sr ... dalam blok section-<num>
    body = t.split('id="section-%d"' % num, 1)[-1]
    m = re.search(r'editsection\.php\?id=(\d+)', body)
    return int(m.group(1)) if m else None


def move(cmid, num):
    sk = moodle.sesskey()
    moodle.get("/course/view.php?id=%d&sesskey=%s&edit=on" % (C, sk))
    t = moodle.get("/course/view.php?id=%d" % C).text
    sid = section_dbid(t, num)
    print("section %d dbid=%s" % (num, sid))
    r1 = moodle.get("/course/mod.php?copy=%d&sesskey=%s&sr=0" % (cmid, sk))
    print("copy http", r1.status_code, r1.url[-80:])
    t = r1.text
    links = re.findall(r'mod\.php\?[^"\']*moveto[^"\']*', t)
    print("move links:", len(links), [html.unescape(x) for x in links[:4]])
    r2 = moodle.get("/course/mod.php?movetosection=%d&sesskey=%s&sr=0" % (sid, sk))
    print("movetosection http", r2.status_code, r2.url[-80:])
    moodle.get("/course/view.php?id=%d&sesskey=%s&edit=off" % (C, sk))


def dup(cmid):
    sk = moodle.sesskey()
    before = {c for s in range(0, 3) for (_, c, _) in section_mods(s)}
    r = moodle.get("/course/mod.php?sr=0&sesskey=%s&duplicate=%d" % (sk, cmid))
    print("dup http", r.status_code)
    for s in range(0, 3):
        for typ, c, nm in section_mods(s):
            if c not in before:
                print("BARU S%d %s %d %s" % (s, typ, c, nm))


if __name__ == "__main__":
    sweep_pma.ensure_login()
    if sys.argv[1] == "dup":
        dup(int(sys.argv[2]))
    elif sys.argv[1] == "type":
        d = dict(formpost.parse_form(moodle.formfields(int(sys.argv[2]))))
        print(d.get("name"), d.get("type"), d.get("assessed"), d.get("section"))
    else:
        move(int(sys.argv[1]), int(sys.argv[2]))
        for s in (2, 3):
            print("S%d:" % s, section_mods(s))
