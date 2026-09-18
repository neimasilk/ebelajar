# -*- coding: utf-8 -*-
"""Buat modul baru di eBelajar untuk AP1: halaman Kontrak Kuliah + url folder Drive.

Resep handoff #9: GET form kosong modedit?add=<type> untuk ambil sesskey/module/itemid,
lalu POST balik dengan field wajib.
"""
import io, re, sys
import moodle

BASE = moodle.BASE
DRIVE_P1 = "https://drive.google.com/drive/folders/1qGzyIrZGWRyMK7rDRTFvLUXtTkhoDqPI"
OUT = r"D:\documents\ebelajar\ganjil-2026-2027\application-project-1"


def blank_form(course, section, modtype):
    s = moodle.sess()
    url = ("%s/course/modedit.php?add=%s&type=&course=%d&section=%d&return=0&sr=0"
           % (BASE, modtype, course, section))
    t = s.get(url, timeout=90).text
    d = {}

    def grab(field):
        # urutan atribut input di Moodle ini tidak tetap -> cari di dalam satu tag <input>
        for m in re.finditer(r'<input[^>]*>', t):
            tag = m.group(0)
            if re.search(r'name="%s"' % re.escape(field), tag):
                v = re.search(r'value="([^"]*)"', tag)
                if v:
                    return v.group(1)
        return None

    for key in ("sesskey", "module", "course"):
        d[key] = grab(key)
        if d[key] is None:
            raise SystemExit("field %s tidak ketemu di form %s" % (key, modtype))
    for fld in ("introeditor[itemid]", "page[itemid]", "content[itemid]"):
        v = grab(fld)
        if v is not None:
            d[fld] = v
    return d, t


def add_page(course, section, name, html):
    d, _ = blank_form(course, section, "page")
    data = [
        ("course", d["course"]), ("coursemodule", ""), ("section", str(section)),
        ("module", d["module"]), ("modulename", "page"), ("instance", ""),
        ("add", "page"), ("update", "0"), ("return", "0"), ("sr", "0"),
        ("sesskey", d["sesskey"]),
        ("_qf__mod_page_mod_form", "1"),
        ("name", name),
        ("introeditor[text]", ""), ("introeditor[format]", "1"),
        ("introeditor[itemid]", d.get("introeditor[itemid]", "")),
        ("page[text]", html), ("page[format]", "1"),
        ("page[itemid]", d.get("page[itemid]", "")),
        ("display", "5"), ("printheading", "1"), ("printlastmodified", "1"),
        ("visible", "1"), ("availabilityconditionsjson", ""),
        ("completion", "0"),
        ("tags", "_qf__force_multiselect_submission"),
        ("competencies", "_qf__force_multiselect_submission"),
        ("competency_rule", "0"),
        ("submitbutton2", "Save and return to course"),
    ]
    r = moodle.sess().post(BASE + "/course/modedit.php", data=data, timeout=180)
    return r


def add_url(course, section, name, target, intro):
    d, _ = blank_form(course, section, "url")
    data = [
        ("course", d["course"]), ("coursemodule", ""), ("section", str(section)),
        ("module", d["module"]), ("modulename", "url"), ("instance", ""),
        ("add", "url"), ("update", "0"), ("return", "0"), ("sr", "0"),
        ("sesskey", d["sesskey"]),
        ("_qf__mod_url_mod_form", "1"),
        ("name", name), ("externalurl", target),
        ("introeditor[text]", intro), ("introeditor[format]", "1"),
        ("introeditor[itemid]", d.get("introeditor[itemid]", "")),
        ("display", "0"), ("popupwidth", "620"), ("popupheight", "450"),
        ("printintro", "1"),
        ("visible", "1"), ("availabilityconditionsjson", ""),
        ("completion", "0"),
        ("tags", "_qf__force_multiselect_submission"),
        ("competencies", "_qf__force_multiselect_submission"),
        ("competency_rule", "0"),
        ("submitbutton2", "Save and return to course"),
    ]
    r = moodle.sess().post(BASE + "/course/modedit.php", data=data, timeout=180)
    return r


def cmids(course, want):
    """Cari cmid modul berdasarkan nama persis."""
    t = moodle.get("/course/view.php?id=%d" % course).text
    out = {}
    for nm in want:
        m = re.search(r'/mod/(?:page|url)/view\.php\?id=(\d+)"[^>]*>(?:<[^>]+>)*?\s*<span class="instancename">%s'
                      % re.escape(nm), t)
        out[nm] = int(m.group(1)) if m else None
    return out


if __name__ == "__main__":
    KONTRAK = "Kontrak Kuliah"
    BAHAN = "Bahan Pertemuan 1 di Google Drive (slide & pendukung)"
    INTRO = ("Semua bahan Pertemuan 1 &mdash; <strong>slide</strong>, modul, video, dan berkas pendukung &mdash; "
             "ada di satu folder Google Drive. eBelajar hanya menautkan supaya salinannya cuma satu dan selalu terbaru.")
    for course, mode in ((7278, "A"), (7426, "P")):
        html = io.open("%s\\kontrak_kuliah_AP1_%s_2026.html" % (OUT, mode), encoding="utf-8").read()
        r1 = add_page(course, 0, KONTRAK, html)
        r2 = add_url(course, 1, BAHAN, DRIVE_P1, INTRO)
        print(course, mode, "page http", r1.status_code, "| url http", r2.status_code)
        print("   ", cmids(course, [KONTRAK, BAHAN]))
