# -*- coding: utf-8 -*-
"""Nilai TUGAS 1 AP1 A (491624) - 6 submission tepat waktu, belum dinilai.

Resep 21 Sep: form nilai = GET view.php?action=grade&userid=X&rownum=Y,
POST balik grade + assignfeedbackcomments_editor[text]+[format] + savegrade.
404-tapi-tersimpan adalah pola biasa; read-back wajib.
Konten ASCII saja (tanpa em-dash).
"""
import sys, os, re, html, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, formpost, sweep_pma

TUGAS1 = 491624
GRADES = [
    # (nama persis di tabel grading, nilai, catatan)
    ("DAFFA MUHAMMAD RAMADHAN", 90,
     "Terlengkap dari semua submission: wireframe desktop dengan UX Note 1-8, "
     "perhatian ke state (empty/error/placeholder), hierarki CTA jelas. Catatan: "
     "(1) kalau ada bagian yang dibantu AI, wajib ditulis di disclosure seperti "
     "ketentuan kelas; (2) berikutnya kirim PDF wireframe saja dengan nama sesuai "
     "konvensi NRP_Nama_Wireframe, data kelompok jangan digabung; (3) lanjut ke "
     "style guide + mockup P3, standar kualitas ini layak dipertahankan."),
    ("BOBBY EKA ANGGA KUSUMA", 88,
     "Bagus: empty state dan error state dipikirkan walau tidak diwajibkan, "
     "alasan desain per elemen jelas, disclosure penggunaan ChatGPT untuk "
     "merapikan tulisan sudah jujur dan itu benar. Catatan: nama berkas pakai "
     "konvensi AP1_P1_NRP_Nama_Wireframe, bukan nama kelompok (ini tugas "
     "individu). Lanjutkan ke mockup P3 dengan ketelitian yang sama."),
    ("KIRANA YASYA RAYYA RAHARJA", 88,
     "Dokumen paling tertata: bagian a/b/c lengkap, anotasi 9 bagian, narasi "
     "hierarki-konsistensi-keterbacaan, disclosure AI jujur. Data Tugas 1b "
     "digabung dalam satu berkas dengan alasan yang masuk akal; ke depan tetap "
     "pisahkan kalau memungkinkan. Lanjut: style guide P3 bisa langsung "
     "diturunkan dari palet dan tipografi wireframe ini."),
    ("TEKIU NEWEGALEN", 85,
     "Wireframe digital rapi, anotasi 7 bagian, paragraf penjelasan cukup. "
     "Catatan penting: berkas ini atas nama tiga orang (Ferdi, Tekiu, "
     "Nopianus) padahal Tugas 1 individu. Tekiu sudah tercakup; FERDI dan "
     "NOTOPIANUS wajib mengumpulkan berkas versi sendiri (bisa turunan "
     "desain yang sama asal ada bagian individu masing-masing). Tanpa itu, "
     "nilai mereka untuk Tugas 1 kosong."),
    ("JOVAN NI'AM FAIRUZ ZAKY", 80,
     "Ada kerja individu nyata: versi beranotasi 13 elemen plus narasi alasan "
     "desain di halaman 3. Catatan: foto wireframe dasar identik dengan "
     "submission Andrean (kertas kelompok RAWON yang sama). Untuk tugas "
     "individu berikutnya (mockup P3), hasilnya harus benar-benar milik "
     "sendiri, tidak cukup menambahkan anotasi di atas karya bersama."),
    ("ANDREAN SATRIA BAGASKARA", 70,
     "Yang dikumpulkan hanya foto wireframe kertas kelompok yang sama dengan "
     "milik Jovan, tanpa anotasi, tanpa narasi, tanpa tambahan individu "
     "apapun. Tugas 1 ini individu. Nilai 70 karena kelengkapan data kelompok "
     "dan tepat waktu, tapi kontribusi individu tidak terlihat. Mulai Tugas 3 "
     "wajib kerja individu yang jelas; diskusikan di kelas kalau ada kendala."),
]

plain = lambda s: s  # catatan sudah ASCII


def find_row(t, name):
    for m in re.finditer(r'<tr[^>]*>(.*?)</tr>', t, re.S):
        row = m.group(1)
        mm = re.search(r'Select (\S+) ([^<]+)<', row)
        if mm and mm.group(2).strip() == name:
            # userid numerik dari link profil di baris yang sama (bukan email)
            um = re.search(r'user/view\.php\?id=(\d+)', row)
            rid = re.search(r'mod_assign_grading_r(\d+)_c0', row)
            if um:
                return um.group(1), int(rid.group(1)) if rid else None
    return None, None


def grade_one(cmid, uid, rownum, nilai, catatan):
    url = "/mod/assign/view.php?id=%d&action=grade&userid=%s&rownum=%d" % (cmid, uid, rownum)
    r = moodle.get(url)
    m = re.search(r'<form[^>]*class="[^"]*gradeform[^"]*"[^>]*action="([^"]+)"', r.text)
    if not m:
        m = re.search(r'<form[^>]*id="mform1"[^>]*action="([^"]+)"', r.text)
    if not m:
        return "form tidak ketemu (len=%d)" % len(r.text)
    act = html.unescape(m.group(1))
    if not act.startswith("http"):
        act = moodle.BASE + ("/" + act.lstrip("/"))
    fields = formpost.parse_form(r.text)
    data = formpost.apply(fields, {
        "grade": str(nilai),
        "assignfeedbackcomments_editor[text]": plain(catatan),
        "assignfeedbackcomments_editor[format]": "1",
    })
    data = [(k, v) for k, v in data if not k.startswith("cancel")]
    data.append(("savegrade", "Save changes"))
    rr = moodle.sess().post(act, data=data, timeout=120)
    return "http%d" % rr.status_code


def readback(cmid, uid):
    r = moodle.get("/mod/assign/view.php?id=%d&action=grade&userid=%s&rownum=0" % (cmid, uid))
    m = re.search(r'name="grade"[^>]*value="([^"]*)"', r.text)
    cm = re.search(r'assignfeedbackcomments_editor\[text\][^>]*>([^<]{0,60})', r.text)
    return (m.group(1) if m else "?"), (html.unescape(cm.group(1))[:40] if cm else "?")


if __name__ == "__main__":
    sweep_pma.ensure_login()
    rg = moodle.get("/mod/assign/view.php?id=%d&action=grading" % TUGAS1).text
    for name, nilai, catatan in GRADES:
        uid, rownum = find_row(rg, name)
        if uid is None:
            print("%-30s TIDAK KETEMU di tabel" % name)
            continue
        res = grade_one(TUGAS1, uid, rownum or 0, nilai, catatan)
        g, c = readback(TUGAS1, uid)
        print("%-30s -> %s | read-back grade=%s catatan=%s" % (name, res, g, c))
