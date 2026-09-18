import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, sweep_pma
sweep_pma.ensure_login()
def txt(s): return re.sub(r"\s+"," ",html.unescape(re.sub("<[^>]+>"," ",s))).strip()
t = moodle.get("/mod/assign/view.php?id=491624").text
m = re.search(r'Grading summary(.*?)</table>', t, re.S)
print(txt(m.group(1)) if m else "no summary")
t = moodle.get("/mod/assign/view.php?id=491624&action=grading").text
for m in re.finditer(r'<tr[^>]*class="[^"]*"[^>]*id="mod_assign_grading_r\d+[^"]*"[^>]*>(.*?)</tr>', t, re.S):
    cells = [txt(c)[:50] for c in re.findall(r'<td[^>]*>(.*?)</td>', m.group(1), re.S)]
    print(" | ".join(cells[2:9]))
