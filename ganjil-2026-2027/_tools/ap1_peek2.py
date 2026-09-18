import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, formpost, sweep_pma
sweep_pma.ensure_login()
def txt(s): return re.sub(r"\s+"," ",html.unescape(re.sub("<[^>]+>"," ",s))).strip()
for cmid in (491624, 491632):
    d = dict(formpost.parse_form(moodle.formfields(cmid)))
    print("=== %d %s" % (cmid, d.get("name")))
    print(txt(d.get("introeditor[text]",""))[:2500])
    print("grade:", d.get("grade[modgrade_type]"), d.get("grade[modgrade_point]"), "| file:", d.get("assignsubmission_file_enabled"), d.get("assignsubmission_file_maxfiles"), "| online:", d.get("assignsubmission_onlinetext_enabled"), "| team:", d.get("teamsubmission"), "| visible:", d.get("visible"))
# status pengumpulan Tugas 1
t = moodle.get("/mod/assign/view.php?id=491624&action=grading").text
rows = re.findall(r'<tr[^>]*id="mod_assign_grading_r\d+"[^>]*>(.*?)</tr>', t, re.S)
print("\nTUGAS 1 grading rows:", len(rows))
for r in rows:
    cells = [txt(c) for c in re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)]
    print("  ", " | ".join(c[:40] for c in cells[2:8]))
m = re.search(r'Participants.*?(\d+)', txt(moodle.get("/mod/assign/view.php?id=491624").text))
print(txt(moodle.get("/mod/assign/view.php?id=491624").text)[-900:])
