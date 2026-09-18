# -*- coding: utf-8 -*-
"""AP1 A (7278) Pertemuan 2 - 17 Sep 2026. Idempoten sebisanya; read-back tiap langkah.

Langkah: Tugas 1 bobot 5%->3% · Kontrak (peta P2/P3, label Tugas 2, kelompok 2-4 orang) ·
tampilkan Section 2 · URL Drive P2 · forum Exit-ticket P2 (+ seed) · halaman materi P2 · label U+FFFD.
"""
import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, formpost, sweep_pma, nlp_p2_due, ap1_addmods, edit_modul
from ap1_tugas2 import dt

C = 7278
DRIVE_P2 = "https://drive.google.com/drive/folders/1yvgECF7RK8l6Hr4TG0oIG-RFdIkocAou"
EXIT_NAME = "Exit-ticket Pertemuan 2 (Ergonomi & Ide Proyek)"
URL_NAME = "Bahan Pertemuan 2 di Google Drive (modul, slide, video)"
EXIT_INTRO = "<p>Jawab di akhir kelas (5 menit), satu balasan per mahasiswa. Masuk nilai partisipatif.</p>"
SEED_SUBJ = "Exit-ticket Pertemuan 2 - jawab tiga pertanyaan ini"
SEED = ("<p>Balas diskusi ini dengan jawaban singkat (2-3 kalimat per nomor):</p><ol>"
        "<li>Perbaikan apa yang paling mengurangi beban kognitif pada wireframe Anda?</li>"
        "<li>Asumsi kritis apa dalam ide proyek kelompok Anda yang harus diverifikasi terlebih dahulu?</li>"
        "<li>Jika harus menghapus satu fitur, mana yang paling sedikit dampaknya pada nilai untuk pengguna? Mengapa?</li>"
        "</ol><p>Sebutkan nama kelompok Anda di baris pertama.</p>")


def section_mods(sn):
    t = moodle.get("/course/view.php?id=%d&section=%d" % (C, sn)).text
    body = t.split('id="section-%d"' % sn, 1)[-1]
    out = []
    for m in re.finditer(r'<li class="activity ([a-z]+)[^"]*" id="module-(\d+)">(.*?)</li>', body, re.S):
        nm = re.search(r'instancename">(.*?)<', m.group(3))
        out.append((m.group(1), int(m.group(2)), html.unescape(nm.group(1)) if nm else ""))
    return out


def step_t1():
    d = dict(formpost.parse_form(moodle.formfields(491624)))
    intro = d["introeditor[text]"]
    old = "Bobot <strong>5%</strong> (sesuai RPS)"
    if old not in intro:
        return "T1 lewati (sudah)" if "Bobot <strong>3%</strong>" in intro else "T1 frasa tak ketemu!"
    ov = {"introeditor[text]": intro.replace(
        old, "Bobot <strong>3%</strong> (komponen Observasi, lihat Kontrak Kuliah bagian 6)")}
    ov.update(dt("gradingduedate", 27, 9, 2026, 23, 55))
    r = nlp_p2_due.repost(491624, ov)
    d2 = dict(formpost.parse_form(moodle.formfields(491624)))
    ok = ("Bobot <strong>3%</strong>" in d2["introeditor[text]"] and d2.get("duedate[day]") == "20"
          and d2.get("allowsubmissionsfromdate[day]") == "14")
    return "T1 http%d -> %s | due %s-%s %s:%s | grading %s-%s-%s" % (
        r.status_code, "OK" if ok else "GAGAL",
        d2.get("duedate[day]"), d2.get("duedate[month]"), d2.get("duedate[hour]"), d2.get("duedate[minute]"),
        d2.get("gradingduedate[day]"), d2.get("gradingduedate[month]"), d2.get("gradingduedate[year]"))


KONTRAK_REPS = [
    ("<tr><td>2</td><td>Ergonomi dalam desain UI</td><td>0922</td><td>&mdash;</td><td>&mdash;</td></tr>",
     "<tr><td>2</td><td>Ergonomi dalam desain UI</td><td>0922</td>"
     "<td>Tugas 2 &mdash; Audit ergonomi &amp; ide proyek (brainstorming)</td><td>6%</td></tr>"),
    ("<tr><td>3</td><td>Estetika dalam desain UI</td><td>0922</td><td>Tugas 2 &mdash; Brainstorming proyek</td><td>6%</td></tr>",
     "<tr><td>3</td><td>Estetika dalam desain UI</td><td>0922</td><td>&mdash;</td><td>&mdash;</td></tr>"),
    ("<td><strong>Tugas 2</strong></td><td>Brainstorming proyek</td>",
     "<td><strong>Tugas 2</strong></td><td>Audit ergonomi &amp; ide proyek (brainstorming)</td>"),
    ("<li>Proyek dikerjakan <strong>berkelompok</strong>; kelompok dibentuk",
     "<li>Proyek dikerjakan <strong>berkelompok</strong>, <strong>2 sampai 4 orang</strong> per kelompok; kelompok dibentuk"),
]


def step_kontrak():
    d = dict(formpost.parse_form(moodle.formfields(496744)))
    t = d["page[text]"]
    miss = [a[:60] for a, b in KONTRAK_REPS if a not in t and b not in t]
    if miss:
        return "KONTRAK frasa tak ketemu: %s" % miss
    new = t
    for a, b in KONTRAK_REPS:
        new = new.replace(a, b)
    p = os.path.join(edit_modul.BASE_DIR, "application-project-1", "kontrak_kuliah_AP1_A_2026.html")
    loc = open(p, encoding="utf-8").read()
    for a, b in KONTRAK_REPS:
        loc = loc.replace(a, b)
    open(p, "w", encoding="utf-8").write(loc)
    if new == t:
        return "KONTRAK lewati (sudah)"
    r = nlp_p2_due.repost(496744, {"page[text]": new})
    v = html.unescape(moodle.get("/mod/page/view.php?id=496744").text)
    ok = "Audit ergonomi & ide proyek" in v and "2 sampai 4 orang" in v
    return "KONTRAK http%d -> %s" % (r.status_code, "OK" if ok else "CEK")


def step_show():
    moodle.get("/course/view.php?id=%d&show=2&sesskey=%s" % (C, moodle.sesskey()))
    t = moodle.get("/course/view.php?id=%d" % C).text
    m = re.search(r'<li id="section-2"[^>]*class="([^"]*)"', t)
    return "SECTION2 class=%s" % (m.group(1) if m else "?")


def step_url():
    for typ, cmid, nm in section_mods(2):
        if typ == "url" and nm.startswith("Bahan Pertemuan 2"):
            return cmid, "URL sudah ada"
    intro = ("Semua bahan Pertemuan 2 &mdash; <strong>Modul Pertemuan 2 (PDF)</strong>, slide, dan dua video "
             "&mdash; ada di satu folder Google Drive. eBelajar hanya menautkan supaya salinannya cuma satu "
             "dan selalu terbaru.")
    r = ap1_addmods.add_url(C, 2, URL_NAME, DRIVE_P2, intro)
    for typ, cmid, nm in section_mods(2):
        if typ == "url" and nm.startswith("Bahan Pertemuan 2"):
            return cmid, "URL dibuat http%d" % r.status_code
    return None, "URL GAGAL http%d" % r.status_code


def step_forum():
    for typ, cmid, nm in section_mods(2):
        if typ == "forum" and nm.startswith("Exit-ticket Pertemuan 2"):
            return cmid, "FORUM sudah ada"
    url = "/course/modedit.php?add=forum&type=&course=%d&section=2&return=0&sr=0" % C
    t = moodle.get(url).text
    m = re.search(r'<form[^>]*action="[^"]*modedit\.php"[^>]*>.*?</form>', t, re.S)
    fields = formpost.parse_form(m.group(0) if m else t)
    ov = {"name": EXIT_NAME, "introeditor[text]": EXIT_INTRO, "introeditor[format]": "1",
          "type": "general", "assessed": "1", "scale[modgrade_type]": "point",
          "scale[modgrade_point]": "100", "visible": "1", "section": "2"}
    data = formpost.apply(fields, ov)
    data.append(("submitbutton2", "Save and return to course"))
    r = moodle.sess().post(moodle.BASE + "/course/modedit.php", data=data, timeout=180)
    for typ, cmid, nm in section_mods(2):
        if typ == "forum" and nm.startswith("Exit-ticket Pertemuan 2"):
            return cmid, "FORUM dibuat http%d" % r.status_code
    errs = re.findall(r'class="error"[^>]*>(.*?)<', r.text)[:3]
    return None, "FORUM GAGAL http%d %s" % (r.status_code, errs)


def step_seed(fcm):
    t = moodle.get("/mod/forum/view.php?id=%d" % fcm).text
    if "Exit-ticket Pertemuan 2 - jawab" in t:
        d = re.search(r'discuss\.php\?d=(\d+)', t)
        return "SEED sudah ada d=%s" % (d.group(1) if d else "?")
    inst = re.search(r'name="forum" value="(\d+)"', t) or re.search(r'post\.php\?forum=(\d+)', t)
    assert inst, "instance forum tak ketemu"
    inst = inst.group(1)
    p = moodle.get("/mod/forum/post.php?forum=%s" % inst).text
    m = re.search(r'<form[^>]*>(?:(?!</form>).)*_qf__mod_forum_post_form(?:(?!</form>).)*</form>', p, re.S)
    assert m, "form diskusi tak ketemu (instance %s)" % inst
    fields = formpost.parse_form(m.group(0))
    data = formpost.apply(fields, {"subject": SEED_SUBJ, "message[text]": SEED, "message[format]": "1"})
    data.append(("submitbutton", "Post to forum"))
    r = moodle.sess().post(moodle.BASE + "/mod/forum/post.php", data=data, timeout=120)
    t = moodle.get("/mod/forum/view.php?id=%d" % fcm).text
    d = re.search(r'discuss\.php\?d=(\d+)', t)
    return "SEED instance %s http%d d=%s" % (inst, r.status_code, d.group(1) if d else "GAGAL")


def step_page(exit_cmid):
    label = "AP1 P2"
    for lb, rel, per_class, needle in edit_modul.TARGETS:
        if lb != label:
            continue
        cmid, ph = per_class["A"]
        ph = dict(ph)
        ph["TUGAS2"] = ph["TUGAS2"].replace("{EXIT}", str(exit_cmid))
        body = edit_modul.load(os.path.join(edit_modul.BASE_DIR, rel), ph)
        r = edit_modul.repost(cmid, {"page[text]": body, "introeditor[text]": edit_modul.INTRO[label]})
        v = moodle.get("/mod/page/view.php?id=%d" % cmid).text
        ok = "27 September 2026" in v and "Fitts" in v
        return "PAGE %d http%d -> %s" % (cmid, r.status_code, "OK" if ok else "GAGAL")


def step_label():
    d = dict(formpost.parse_form(moodle.formfields(491627)))
    t = d.get("introeditor[text]", "")
    if "�" not in t:
        return "LABEL tidak ada U+FFFD"
    r = nlp_p2_due.repost(491627, {"introeditor[text]": t.replace("�", "-")})
    d2 = dict(formpost.parse_form(moodle.formfields(491627)))
    return "LABEL http%d -> %s" % (r.status_code, "OK" if "�" not in d2.get("introeditor[text]", "") else "GAGAL")


if __name__ == "__main__":
    sweep_pma.ensure_login()
    print(step_t1())
    print(step_kontrak())
    print(step_show())
    ucm, msg = step_url(); print(msg, ucm)
    fcm, msg = step_forum(); print(msg, fcm)
    if fcm:
        print(step_seed(fcm))
        print(step_page(fcm))
    print(step_label())
    print("S2 sekarang:", section_mods(2))
    print("S3 sekarang:", section_mods(3))
