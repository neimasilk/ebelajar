# -*- coding: utf-8 -*-
"""Sweep eBelajar PM A (7218) — forum yang perlu dibalas + status Tugas 1.

Dipakai dengan cookie MoodleSession dari browser yang sudah login manual:
    python sweep_pma.py "<MOODLESESSION_COOKIE>"
"""
import re, sys, json, io
sys.path.insert(0, r"D:\documents\ebelajar\ganjil-2026-2027\_tools")
import requests
import moodle

# .env harus terbaca SEBELUM moodle.sess() — moodle membaca env saat import,
# jadi set moodle.USER/PASS langsung di sini.
load_env_done = False


def ensure_login():
    global load_env_done
    import os
    if not load_env_done:
        load_env()
        moodle.USER = os.environ.get("user_ebelajar", "amien@stiki.ac.id")
        moodle.PASS = os.environ.get("pass_ebelajar", "")
        load_env_done = True
    moodle.sess()
    print("LOGIN OK (sesskey %s...)" % moodle._sesskey[:6])

# injeksi session dari cookie browser (tanpa password)
def session_from_cookie(ck):
    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0"
    s.cookies.set("MoodleSession", ck, domain="ebelajar.stiki.ac.id")
    r = s.get(moodle.BASE + "/my/", timeout=60)
    m = re.search(r'"sesskey":"([^"]+)"', r.text)
    if not m:
        print("COOKIE EXPIRED / TIDAK VALID"); sys.exit(1)
    moodle._s, moodle._sesskey = s, m.group(1)
    return s


def text_of(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def forum_discussions(fmid):
    """Daftar diskusi forum: (did, judul). Catatan: URL diskusi Moodle = discuss.php, BUKAN discussion.php."""
    r = moodle.get("/mod/forum/view.php?id=%d" % fmid)
    out = []
    for m in re.finditer(r'discuss\.php\?d=(\d+)[^>]*>(.*?)</a>', r.text, re.S):
        did = int(m.group(1))
        title = text_of(m.group(2))
        if title:
            out.append((did, title))
    # dedup jaga-jaga
    seen, res = set(), []
    for did, t in out:
        if did not in seen:
            seen.add(did); res.append((did, t))
    return res


def forum_posts(fmid, did):
    """Semua post dalam satu diskusi: list of dict (tema lambda: <a id="pN"></a><div class="forumpost...">)."""
    r = moodle.get("/mod/forum/discuss.php?d=%d" % did)
    posts = []
    for m in re.finditer(
            r'<a id="p(\d+)"></a>\s*<div class="forumpost[^"]*"[^>]*>.*?'
            r'user/view\.php\?id=(\d+)[^"]*">(.*?)</a> - (.*?)</div>.*?'
            r'<div class="posting fullpost">(.*?)<div class="attachedimages">',
            r.text, re.S):
        posts.append({"pid": int(m.group(1)), "uid": int(m.group(2)),
                      "author": text_of(m.group(3)), "date": text_of(m.group(4)),
                      "body": text_of(m.group(5))[:400]})
    return posts


def load_env():
    """Baca kunci user_ebelajar/pass_ebelajar dari D:/knowledge-base/.env."""
    import os
    p = r"D:\knowledge-base\.env"
    for line in io.open(p, encoding="utf-8"):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def main():
    if len(sys.argv) > 1:
        session_from_cookie(sys.argv[1])
    else:
        ensure_login()
    print("=== course dump PM A 7218 ===")
    for num, name, hidden, mods in moodle.course_dump(7218):
        print("S%-3d %s %s" % (num, "HID" if hidden else "   ", name))
        for cmid, typ, nm in mods:
            print("      %-9s %d  %s" % (typ, cmid, nm))


if __name__ == "__main__":
    main()
