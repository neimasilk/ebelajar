import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, sweep_pma
sweep_pma.ensure_login()
def txt(s): return re.sub(r"\s+"," ",html.unescape(re.sub("<[^>]+>"," ",s))).strip()
for did in (10664, 10663):
    t = moodle.get("/mod/forum/discuss.php?d=%d" % did).text
    print("=== d=%d" % did, len(t))
    for m in re.finditer(r'<a id="p(\d+)"></a>', t):
        print("  post", m.group(1))
    body = t[t.find('<div role="main"'):]
    print(txt(body)[:3000])
    for m in re.finditer(r'<form[^>]*id="(postrating\d+)"', t): print("  ratingform", m.group(1))
