# -*- coding: utf-8 -*-
"""Login + helper HTTP untuk eBelajar (Moodle 3.3). Dipakai ulang sesi ini."""
import re, os, html, requests

BASE = "https://ebelajar.stiki.ac.id"
import os
# Kredensial TIDAK disimpan di berkas ini. Set dulu di shell:
#   export EBELAJAR_USER="amien@stiki.ac.id"   <- BUKAN "amien" (koreksi 8 Sep 2026)
#   export EBELAJAR_PASS="..."
USER = os.environ.get("EBELAJAR_USER", "amien@stiki.ac.id")
PASS = os.environ.get("EBELAJAR_PASS", "")

_s = None
_sesskey = None


def sess():
    global _s, _sesskey
    if _s is not None:
        return _s
    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0"
    # GET dulu agar cookie MoodleSession terbentuk — POST tanpa ini = login diam-diam gagal
    s.get(BASE + "/login/index.php", timeout=60)
    s.post(BASE + "/login/index.php",
           data={"username": USER, "password": PASS, "anchor": ""},
           timeout=60)
    r = s.get(BASE + "/my/", timeout=60)
    m = re.search(r'"sesskey":"([^"]+)"', r.text)
    if not m:
        raise SystemExit("LOGIN GAGAL")
    _s, _sesskey = s, m.group(1)
    return _s


def sesskey():
    sess()
    return _sesskey


def get(path, **kw):
    return sess().get(BASE + path if path.startswith("/") else path, timeout=90, **kw)


def course_dump(cid):
    """Kembalikan daftar section -> [(cmid, modtype, nama)]."""
    r = get("/course/view.php?id=%d" % cid)
    t = r.text
    out = []
    # potong per section
    parts = re.split(r'<li id="section-(\d+)"', t)
    for i in range(1, len(parts), 2):
        num = int(parts[i]); body = parts[i + 1]
        name = ""
        m = re.search(r'<h3 class="sectionname[^"]*"[^>]*>(?:<span[^>]*>)?(.*?)</', body, re.S)
        if m:
            name = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        hidden = 'class="section main clearfix hidden' in body[:200] or ' hidden' in parts[i - 1][-120:]
        mods = []
        for mm in re.finditer(
                r'/mod/([a-z]+)/view\.php\?id=(\d+)"[^>]*>(?:<[^>]+>)*?\s*<span class="instancename">(.*?)(?:<span class="accesshide|</span>)',
                body, re.S):
            typ, cmid, nm = mm.group(1), int(mm.group(2)), mm.group(3)
            nm = html.unescape(re.sub(r"<[^>]+>", "", nm)).strip()
            mods.append((cmid, typ, nm))
        out.append((num, name, hidden, mods))
    return out


def formfields(cmid):
    """Ambil seluruh field form modedit (untuk dibaca / dikirim ulang utuh)."""
    r = get("/course/modedit.php?update=%d" % cmid)
    return r.text
