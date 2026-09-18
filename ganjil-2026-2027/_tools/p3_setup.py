# -*- coding: utf-8 -*-
"""Pasang Pertemuan 3 di PM A (7218) dan NLP A (7226) - 18 Sep 2026.

TEMUAN 18 Sep: section 3 TIDAK kosong. Ia berisi warisan impor 2025 yang selama ini
tersembunyi: satu label, satu page "Materi ...", satu forum "Diskusi ...". Kedua forum
warisan berisi NOL diskusi, jadi aman dipakai ulang.

Karena itu skrip ini MEMAKAI ULANG, bukan menambah duplikat:
  1. tampilkan section 3 + beri nama (butuh edit mode untuk dapat dbid section)
  2. URL folder Drive Pertemuan 3          (dibuat baru - belum ada)
  3. page warisan  -> diisi modul_p3.html + diganti namanya
  4. forum warisan -> jadi Exit-ticket P3, rating point 100, lalu di-seed

Konten ASCII saja (em-dash mentah korup jadi U+FFFD di DB); entity HTML boleh.
"""
import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, formpost, ap1_addmods

BASE_DIR = r"D:\documents\ebelajar\ganjil-2026-2027"
SEC = 3

COURSES = {
    "PM A": dict(
        cid=7218,
        rel="pembelajaran-mesin/modul_p3.html",
        secname="Pertemuan 3 - Encoding & Feature Thinking",
        page_cmid=491682, forum_cmid=491683,
        pagename="Materi: Encoding & Feature Thinking",
        pageintro=("Bab Pertemuan 3: menyandikan kategori tanpa menyelundupkan klaim palsu, "
                   "dan membuat fitur turunan yang memperbaiki kolom yang menyesatkan."),
        drive="https://drive.google.com/drive/folders/1h8QxqSRIxa9xzKc6Xn0qquVJtCtDNF2o",
        lks="https://colab.research.google.com/drive/1tCPukd9SPQF_mnh0kOKs5xEI_t6GGIcO",
        exitname="Exit-ticket Pertemuan 3 (Encoding & Feature Thinking)",
        seedsubj="Exit-ticket Pertemuan 3 - jawab tiga pertanyaan ini",
        seed=("<p>Balas diskusi ini sebelum meninggalkan kelas (2-3 kalimat per nomor). "
              "Dinilai skala 0-100 dan masuk gradebook.</p><ol>"
              "<li>Satu contoh <strong>kebocoran data</strong> yang berhasil Anda hindari hari ini: "
              "langkah apa yang tadinya akan Anda kerjakan di luar pipeline?</li>"
              "<li>Fitur baru <strong>terbaik</strong> Anda: nama fitur, alasan domainnya, dan bukti "
              "metrik (angka sebelum vs sesudah).</li>"
              "<li>Satu rencana eksperimen lanjutan untuk Pertemuan 4 (evaluasi &amp; metrik).</li>"
              "</ol><p><em>Bonus (opsional):</em> dari dataset transaksi e-commerce berisi "
              "<code>timestamp</code>, <code>id_produk</code>, dan <code>harga</code>, sebutkan dua fitur "
              "turunan yang menurut Anda paling berguna untuk memprediksi penjualan, dan alasannya.</p>"),
        marker="kebocoran data</strong> yang berhasil Anda hindari",
    ),
    "NLP A": dict(
        cid=7226,
        rel="nlp/modul_p3.html",
        secname="Pertemuan 3 - Stemming & Lemmatization",
        page_cmid=491788, forum_cmid=491789,
        pagename="Materi: Stemming dan Lemmatization",
        pageintro=("Bab Pertemuan 3: menyeragamkan bentuk kata dengan stemming (Sastrawi) dan "
                   "lemmatization (NLTK WordNet) - dan menghitung apa yang hilang karenanya."),
        drive="https://drive.google.com/drive/folders/14fspLWwgKmTOxrJnNs7d01-isrnW7oxY",
        lks="https://colab.research.google.com/drive/1BzpZ4VtrCF6YCAEw5w2RIfbufdKKKLh3",
        exitname="Exit-ticket Pertemuan 3 (Stemming & Lemmatization)",
        seedsubj="Exit-ticket Pertemuan 3 - jawab tiga pertanyaan ini",
        seed=("<p>Balas diskusi ini sebelum meninggalkan kelas (2-3 kalimat per nomor). "
              "Dinilai skala 0-100 dan masuk gradebook.</p><ol>"
              "<li>Satu kata bahasa Indonesia yang hasil stemming-nya menurut Anda <strong>merusak "
              "makna</strong>: tulis kata, hasil stem-nya, dan makna apa yang hilang.</li>"
              "<li>Mengapa <code>lemmatize('better')</code> mengembalikan <em>better</em>, dan apa yang "
              "harus ditambahkan supaya hasilnya <em>good</em>?</li>"
              "<li>Berapa persen kosakata menyusut di teks percobaan Anda (BI dan EN), dan menurut Anda "
              "apakah penyusutan itu menolong atau merugikan tugas yang Anda bayangkan?</li>"
              "</ol>"),
        marker="merusak makna</strong>: tulis kata",
    ),
}

URLNAME = "Bahan Pertemuan 3 di Google Drive (modul, LKS, video)"
URLINTRO = ("Semua bahan Pertemuan 3 &mdash; <strong>Modul Mandiri P3 (PDF)</strong>, "
            "<strong>LKS Colab</strong>, dan dua video &mdash; ada di satu folder Google Drive. "
            "eBelajar hanya menautkan supaya salinannya cuma satu dan selalu terbaru.")
EXIT_INTRO = ("<p>Jawab di akhir kelas (5 menit), satu balasan per mahasiswa. "
              "Dinilai skala 0-100 dan langsung masuk gradebook.</p>")


def section_mods(cid, sn):
    t = moodle.get("/course/view.php?id=%d&section=%d" % (cid, sn)).text
    body = t.split('id="section-%d"' % sn, 1)[-1]
    out = []
    for m in re.finditer(r'<li class="activity ([a-z]+)[^"]*" id="module-(\d+)">(.*?)</li>', body, re.S):
        nm = re.search(r'instancename">(.*?)<', m.group(3))
        out.append((m.group(1), int(m.group(2)), html.unescape(nm.group(1)) if nm else ""))
    return out


def repost(cmid, ov):
    """Kirim ulang seluruh form modedit dengan sebagian field ditimpa."""
    fields = formpost.parse_form(moodle.formfields(cmid))
    data = formpost.apply(fields, ov)
    data = [(k, v) for k, v in data if k != "cancel"]
    data.append(("submitbutton2", "Save and return to course"))
    return moodle.sess().post(moodle.BASE + "/course/modedit.php", data=data, timeout=180)


def step_show_and_name(cid, secname):
    sk = moodle.sesskey()
    moodle.get("/course/view.php?id=%d&show=%d&sesskey=%s" % (cid, SEC, sk))
    moodle.get("/course/view.php?id=%d&edit=on&sesskey=%s" % (cid, sk))   # edit mode ON
    t = moodle.get("/course/view.php?id=%d" % cid).text
    blk = t.split('id="section-%d"' % SEC, 1)[-1]
    m = re.search(r'editsection\.php\?id=(\d+)', blk)
    if not m:
        moodle.get("/course/view.php?id=%d&edit=off&sesskey=%s" % (cid, sk))
        return "SECTION3 dbid tak ketemu"
    dbid = m.group(1)
    ft = moodle.get("/course/editsection.php?id=%s" % dbid).text
    fm = re.search(r'<form[^>]*action="[^"]*editsection\.php"[^>]*>.*?</form>', ft, re.S)
    fields = formpost.parse_form(fm.group(0) if fm else ft)
    data = formpost.apply(fields, {"name[value]": secname, "name[customize]": "1"})
    data = [(k, v) for k, v in data if k != "cancel"]
    data.append(("submitbutton", "Save changes"))
    r = moodle.sess().post(moodle.BASE + "/course/editsection.php", data=data, timeout=120)
    moodle.get("/course/view.php?id=%d&edit=off&sesskey=%s" % (cid, sk))   # edit mode OFF
    t2 = moodle.get("/course/view.php?id=%d" % cid).text
    blk2 = t2.split('id="section-%d"' % SEC, 1)[-1][:1200]
    got = re.search(r'sectionname[^"]*"[^>]*>(?:<span[^>]*>)?(.*?)</', blk2, re.S)
    nm = html.unescape(re.sub(r"<[^>]+>", "", got.group(1))).strip() if got else "?"
    return "SECTION3 dbid=%s http%d nama=%r" % (dbid, r.status_code, nm)


def step_url(cid, cfg):
    for typ, cmid, nm in section_mods(cid, SEC):
        if typ == "url" and nm.startswith("Bahan Pertemuan 3"):
            return cmid, "URL sudah ada"
    r = ap1_addmods.add_url(cid, SEC, URLNAME, cfg["drive"], URLINTRO)
    for typ, cmid, nm in section_mods(cid, SEC):
        if typ == "url" and nm.startswith("Bahan Pertemuan 3"):
            return cmid, "URL dibuat http%d" % r.status_code
    return None, "URL GAGAL http%d" % r.status_code


def step_forum(cid, cfg):
    """Pakai ulang forum warisan: ganti nama + intro + nyalakan rating."""
    cmid = cfg["forum_cmid"]
    d = dict(formpost.parse_form(moodle.formfields(cmid)))
    if d.get("name") == cfg["exitname"] and d.get("assessed") == "1":
        return cmid, "FORUM sudah siap (nama+rating)"
    r = repost(cmid, {"name": cfg["exitname"], "introeditor[text]": EXIT_INTRO,
                      "introeditor[format]": "1", "assessed": "1",
                      "scale[modgrade_type]": "point", "scale[modgrade_point]": "100"})
    d2 = dict(formpost.parse_form(moodle.formfields(cmid)))
    ok = d2.get("name") == cfg["exitname"] and d2.get("assessed") == "1" and d2.get("type") == d.get("type")
    return cmid, "FORUM http%d nama=%r assessed=%s type=%s -> %s" % (
        r.status_code, d2.get("name"), d2.get("assessed"), d2.get("type"), "OK" if ok else "CEK")


def step_seed(fcm, cfg):
    t = moodle.get("/mod/forum/view.php?id=%d" % fcm).text
    if cfg["seedsubj"] in html.unescape(t):
        d = re.search(r'discuss\.php\?d=(\d+)', t)
        return "SEED sudah ada d=%s" % (d.group(1) if d else "?")
    inst = re.search(r'name="forum" value="(\d+)"', t) or re.search(r'post\.php\?forum=(\d+)', t)
    if not inst:
        return "SEED GAGAL: instance forum tak ketemu"
    inst = inst.group(1)
    p = moodle.get("/mod/forum/post.php?forum=%s" % inst).text
    m = re.search(r'<form[^>]*>(?:(?!</form>).)*_qf__mod_forum_post_form(?:(?!</form>).)*</form>', p, re.S)
    if not m:
        return "SEED GAGAL: form diskusi tak ketemu (instance %s)" % inst
    fields = formpost.parse_form(m.group(0))
    data = formpost.apply(fields, {"subject": cfg["seedsubj"], "message[text]": cfg["seed"],
                                   "message[format]": "1"})
    data.append(("submitbutton", "Post to forum"))
    r = moodle.sess().post(moodle.BASE + "/mod/forum/post.php", data=data, timeout=120)
    t = moodle.get("/mod/forum/view.php?id=%d" % fcm).text
    d = re.search(r'discuss\.php\?d=(\d+)', t)
    ok = cfg["marker"] in html.unescape(t) if d else False
    return "SEED instance %s http%d d=%s isi_tampil=%s" % (
        inst, r.status_code, d.group(1) if d else "GAGAL", ok)


def step_page(cid, cfg, exit_cmid):
    cmid = cfg["page_cmid"]
    body = open(os.path.join(BASE_DIR, cfg["rel"]), encoding="utf-8").read()
    body = (body.replace("{DRIVE}", cfg["drive"])
                .replace("{LKS}", cfg["lks"])
                .replace("{EXIT}", "%s/mod/forum/view.php?id=%d" % (moodle.BASE, exit_cmid)))
    for ph in ("{DRIVE}", "{LKS}", "{EXIT}"):
        assert ph not in body, "placeholder %s tersisa" % ph
    r = repost(cmid, {"name": cfg["pagename"], "page[text]": body,
                      "introeditor[text]": cfg["pageintro"], "introeditor[format]": "1"})
    v = html.unescape(moodle.get("/mod/page/view.php?id=%d" % cmid).text)
    ok = "Poin kunci" in v and "Uji pemahaman" in v and "Kegiatan" in v and "\ufffd" not in v
    return "PAGE %d http%d nama=%r -> %s%s" % (
        cmid, r.status_code, cfg["pagename"], "OK" if ok else "CEK",
        "  [ADA U+FFFD!]" if "\ufffd" in v else "")


if __name__ == "__main__":
    moodle.sess()
    for label, cfg in COURSES.items():
        cid = cfg["cid"]
        print("\n" + "=" * 72)
        print("%s (course %d)" % (label, cid))
        print(" ", step_show_and_name(cid, cfg["secname"]))
        ucm, msg = step_url(cid, cfg); print("  %s %s" % (msg, ucm))
        fcm, msg = step_forum(cid, cfg); print("  %s" % msg)
        print(" ", step_seed(fcm, cfg))
        print(" ", step_page(cid, cfg, fcm))
        print("  S3 sekarang:")
        for typ, cmid, nm in section_mods(cid, SEC):
            print("     %-7d %-7s %s" % (cmid, typ, nm))
