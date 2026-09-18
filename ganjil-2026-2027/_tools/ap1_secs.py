import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, formpost, sweep_pma, check_tugas_dates as ctd
sweep_pma.ensure_login()
for sn in range(2, 8):
    t = moodle.get("/course/view.php?id=7278&section=%d" % sn).text
    body = t.split('id="section-%d"' % sn, 1)[-1]
    sec = re.search(r'<h3 class="sectionname[^"]*"[^>]*>(.*?)</h3>', body, re.S)
    print("=== S%d %s" % (sn, sec and html.unescape(re.sub("<[^>]+>","",sec.group(1)))))
    for m in re.finditer(r'<li class="activity ([a-z]+)[^"]*" id="module-(\d+)">(.*?)</li>', body, re.S):
        nm = re.search(r'instancename">(.*?)<', m.group(3))
        txt = html.unescape(re.sub(r"\s+"," ",re.sub("<[^>]+>"," ",m.group(3))))[:200]
        print(" ", m.group(1), m.group(2), html.unescape(nm.group(1)) if nm else ("LABEL: " + txt))
        if m.group(1) == "assign":
            f = formpost.parse_form(moodle.formfields(int(m.group(2))))
            d = dict(f)
            print("     ", " ".join("%s=%s" % (k[:12], ctd.fmt(f, k) or "OFF") for k in ctd.DATE_KEYS), "| teamsub", d.get("teamsubmission"))
