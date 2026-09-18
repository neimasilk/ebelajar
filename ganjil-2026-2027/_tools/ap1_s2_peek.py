import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, formpost, sweep_pma, check_tugas_dates as ctd
sweep_pma.ensure_login()
r = moodle.get("/course/view.php?id=7278&section=2")
t = r.text
for m in re.finditer(r'/mod/([a-z]+)/view\.php\?id=(\d+)', t):
    pass
ids = []
for m in re.finditer(r'id="module-(\d+)"[^>]*class="([^"]*)"', t):
    ids.append((int(m.group(1)), m.group(2)))
print(ids)
for m in re.finditer(r'<li class="activity ([a-z]+)[^"]*" id="module-(\d+)">(.*?)</li>', t, re.S):
    nm = re.search(r'instancename">(.*?)<', m.group(3))
    print(m.group(1), m.group(2), html.unescape(nm.group(1)) if nm else "?")
    if m.group(1) == "assign":
        f = formpost.parse_form(moodle.formfields(int(m.group(2))))
        d = dict(f)
        print("   ", " ".join("%s=%s" % (k[:12], ctd.fmt(f, k) or "OFF") for k in ctd.DATE_KEYS), "| grade", d.get("grade[modgrade_point]"), "| teamsub", d.get("teamsubmission"))
sec = re.search(r'<h3 class="sectionname[^"]*"[^>]*>(.*?)</h3>', t, re.S)
print("SECTION:", sec and re.sub("<[^>]+>","",sec.group(1)))
open(os.path.join(os.environ.get("TEMP","."), "ap1_s2.html"), "w", encoding="utf-8").write(t)
