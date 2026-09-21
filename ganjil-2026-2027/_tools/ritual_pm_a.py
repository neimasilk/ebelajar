# -*- coding: utf-8 -*-
"""Ritual Senin PM A (7218) - baca keadaan forum + Tugas 1 untuk slide laporan deck.

Pemakaian:
    python ritual_pm_a.py            # baca saja (login dari .env)
    python ritual_pm_a.py <pid>=<nilai> ...   # setelah baca: nilai posting via rating forum

Contoh nilai:
    python ritual_pm_a.py 29201=85 29202=90
"""
import re, sys, io, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import requests
import moodle
from sweep_pma import load_env, ensure_login, text_of, forum_discussions, forum_posts

FORUMS = {
    491672: "Perkenalan",
    491677: "Diskusi P1",
    501183: "Exit-ticket P2",
    491683: "Exit-ticket P3",
    491670: "Diskusi Umum",
}
TUGAS1 = 491680


def rating_form_fields(disc_html, pid):
    """Ambil field form rating postrating<pid> dari HTML halaman diskusi."""
    m = re.search(
        r'<form[^>]*>.*?name="postrating%d"[^>]*>.*?</form>' % pid, disc_html, re.S)
    if not m:
        return None
    form = m.group(0)
    fields = {}
    for tag in re.finditer(r'<input[^>]*>', form):
        t = tag.group(0)
        nm = re.search(r'name="([^"]+)"', t)
        vl = re.search(r'value="([^"]*)"', t)
        if nm:
            fields[nm.group(1)] = vl.group(1) if vl else ""
    fields["rating"] = None  # diisi pemanggil
    return fields


def already_rated(disc_html, pid):
    """Cek apakah post pid sudah punya rating (tampilan teks rating di sekitar post)."""
    seg = re.search(r'<a id="p%d"></a>(.*?)(?=<a id="p\d+"></a>|$)' % pid,
                    disc_html, re.S)
    if not seg:
        return "?"
    body = seg.group(1)
    # tampilan rating Moodle 3.3: "Rating: 85/100" atau angka di blok rating
    if re.search(r'class="rating', body) or re.search(r"Rating", body):
        mm = re.search(r'(\d+)\s*/\s*100', body)
        if mm:
            return mm.group(1)
        return "rated"
    return ""


def tugas1_status():
    r = moodle.get("/mod/assign/view.php?id=%d" % TUGAS1)
    t = r.text
    m = re.search(r'Submitted[^<]*</[^>]+>\s*<[^>]+>\s*(\d+)', t)
    # halaman assign punya "Submitted for grading: N"
    m2 = re.search(r'Submitted for grading[^0-9]*(\d+)', text_of_keep(t))
    return m2.group(1) if m2 else (m.group(1) if m else "?"), t


def text_of_keep(t):
    return re.sub(r"<[^>]+>", " ", t)


def main():
    ensure_login()

    # ---- forum ----
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
                st = already_rated(dr.text, p["pid"])
                print("    p%d | %s | %s | rating:%s | %s" % (
                    p["pid"], p["author"], p["date"], st, p["body"][:110]))

    # ---- tugas 1 ----
    cnt, html = tugas1_status()
    print("\n=== TUGAS 1 (%d) === submitted: %s" % (TUGAS1, cnt))
    # daftar nama yang mengumpulkan (dari halaman grading bila bisa dibaca)
    rg = moodle.get("/mod/assign/view.php?id=%d&action=grading" % TUGAS1)
    rows = re.findall(
        r'<td[^>]*>\s*<a[^>]*user/view\.php\?id=(\d+)[^>]*>(.*?)</a>.*?'
        r'(Submitted for grading|No submission)', rg.text, re.S)
    if rows:
        for uid, nm, st in rows:
            nm = text_of(nm)
            if st == "Submitted for grading":
                print("  SUBMITTED uid=%s %s" % (uid, nm))
    else:
        # fallback: halaman summary
        for m in re.finditer(r'Submitted for grading', text_of_keep(rg.text)):
            pass
        print("  (tabel grading tidak terbaca otomatis)")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # mode grading: setiap argumen pid=nilai, dari halaman diskusi masing2 post
        ensure_login()
        for arg in sys.argv[1:]:
            pid, val = arg.split("=")
            pid, val = int(pid), int(val)
            # cari halaman diskusi yang memuat pid
            dr = None
            for fmid, name in FORUMS.items():
                for did, _t in forum_discussions(fmid):
                    r = moodle.get("/mod/forum/discuss.php?d=%d" % did)
                    if re.search(r'<a id="p%d"></a>' % pid, r.text):
                        dr = r
                        break
                if dr:
                    break
            if dr is None:
                print("pid %d TIDAK KETEMU" % pid)
                continue
            f = rating_form_fields(dr.text, pid)
            if f is None:
                print("pid %d: form rating tidak ketemu" % pid)
                continue
            f["rating"] = str(val)
            data = {k: v for k, v in f.items() if v is not None}
            rr = moodle.sess().post(
                moodle.BASE + "/rating/rate.php", data=data, timeout=60)
            print("pid %d -> nilai %d : HTTP %s (404-tapi-tersimpan = biasa; cek read-back)"
                  % (pid, val, rr.status_code))
            # read-back
            r2 = moodle.get("/mod/forum/discuss.php?d=%s" %
                            re.search(r'discuss\.php\?d=(\d+)', dr.url).group(1))
            st = already_rated(r2.text, pid)
            print("   read-back rating: %s" % st)
    else:
        main()
