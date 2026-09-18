# -*- coding: utf-8 -*-
"""Ritual AP1 A (7278) jelang Pertemuan 2 (Kamis 17 Sep 2026).

1. Rating forum ON (Perkenalan 491618, Diskusi P1 491623): assessed=1 point 100.
2. Balas perkenalan Tyo (29083) & Devan (29118) + nilai 80.
Konten ASCII saja (em-dash korup di DB). Read-back wajib.
"""
import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, formpost, sweep_pma, nlp_p2_due

REPLIES = {
    29083: ("Tyo", 80,
            "<p>Terima kasih Tyo, Anda yang pertama mengisi perkenalan. Identitasnya lengkap (nama, asal, prodi, NRP).</p>"
            "<p>Untuk kelas proyek, perkenalan akan jauh lebih berguna kalau ditambah tiga hal: "
            "(1) pengalaman membuat web/aplikasi sejauh ini, (2) lebih nyaman di desain (UI) atau di kode (front-end), "
            "(3) masalah apa yang ingin Anda selesaikan lewat proyek semester ini. "
            "Informasi itu yang membantu kelompok JOSJIS membagi peran. Silakan tambahkan dengan membalas posting ini.</p>"
            "<p>Nilai: 80 - memenuhi syarat minimal perkenalan.</p>"),
    29118: ("Devan", 80,
            "<p>Terima kasih Devan, identitasnya lengkap (nama, asal, prodi, NRP).</p>"
            "<p>Satu saran untuk kelas proyek: tambahkan pengalaman Anda membuat web/aplikasi, "
            "apakah lebih nyaman di desain (UI) atau di kode (front-end), dan satu masalah nyata yang ingin Anda "
            "selesaikan semester ini. Itu bahan yang dibutuhkan kelompok RAWON untuk membagi peran dan memilih topik. "
            "Silakan tambahkan dengan membalas posting ini.</p>"
            "<p>Nilai: 80 - memenuhi syarat minimal perkenalan.</p>"),
}
DID = 10663


def rating_on(cmid):
    d = dict(formpost.parse_form(moodle.formfields(cmid)))
    if d.get("assessed") == "1" and d.get("scale[modgrade_point]") == "100":
        return "sudah ON"
    r = nlp_p2_due.repost(cmid, {"assessed": "1", "scale[modgrade_type]": "point",
                                 "scale[modgrade_point]": "100"})
    d2 = dict(formpost.parse_form(moodle.formfields(cmid)))
    ok = d2.get("assessed") == "1" and d2.get("type") == d.get("type") and d2.get("name") == d.get("name")
    return "http%d assessed=%s type=%s -> %s" % (r.status_code, d2.get("assessed"), d2.get("type"), "OK" if ok else "GAGAL")


def already_replied(t, pid, needle):
    return needle in t


def reply(pid, body):
    s = moodle.sess()
    t = moodle.get("/mod/forum/post.php?reply=%d" % pid).text
    m = re.search(r'<form[^>]*>(?:(?!</form>).)*_qf__mod_forum_post_form(?:(?!</form>).)*</form>', t, re.S)
    assert m, "form reply tidak ketemu"
    frag = m.group(0)
    act = re.search(r'action="([^"]+)"', frag).group(1)
    fields = formpost.parse_form(frag)
    ov = {"message[text]": body, "message[format]": "1"}
    data = formpost.apply(fields, ov)
    data = [(k, v) for k, v in data if k not in ("cancel",)]
    data.append(("submitbutton", "Post to forum"))
    act = html.unescape(act)
    if not act.startswith("http"):
        act = moodle.BASE + "/mod/forum/" + act
    r = s.post(act, data=data, timeout=120)
    return r.status_code


def rate(t, pid, val):
    m = re.search(r'<form[^>]*id="postrating%d"[^>]*>(.*?)</form>' % pid, t, re.S)
    if not m:
        return "form rating p%d tidak ada" % pid
    fields = dict(formpost.parse_form(m.group(1)))
    fields["rating"] = str(val)
    r = moodle.sess().post(moodle.BASE + "/rating/rate.php", data=fields, timeout=60)
    return "http%d fields=%s" % (r.status_code, sorted(fields))


if __name__ == "__main__":
    sweep_pma.ensure_login()
    pass
    t = moodle.get("/mod/forum/discuss.php?d=%d" % DID).text
    for pid, (nm, val, body) in REPLIES.items():
        needle = body[3:60]
        if html.escape(needle) in t or needle in t:
            print("balas p%d: sudah ada, lewati" % pid)
        else:
            print("balas p%d (%s): http%s" % (pid, nm, reply(pid, body)))
    t = moodle.get("/mod/forum/discuss.php?d=%d" % DID).text
    for pid, (nm, val, body) in REPLIES.items():
        print("nilai p%d (%s)=%d: %s" % (pid, nm, val, rate(t, pid, val)))
    # read-back
    t = moodle.get("/mod/forum/discuss.php?d=%d" % DID).text
    print("post ids:", re.findall(r'<a id="p(\d+)"', t))
    for pid, (nm, val, body) in REPLIES.items():
        print("balasan %s tampil:" % nm, body[3:50] in html.unescape(t))
    for m in re.finditer(r'id="postrating(\d+)".*?<select[^>]*>(.*?)</select>', t, re.S):
        sel = re.search(r'<option[^>]*selected[^>]*value="([^"]*)"|<option[^>]*value="([^"]*)"[^>]*selected', m.group(2))
        print("  rating p%s selected=%s" % (m.group(1), sel.groups() if sel else None))
    for m in re.finditer(r'Average of ratings:\s*(?:<[^>]+>\s*)*([\d.\-]+)', t):
        print("  avg", m.group(1))
