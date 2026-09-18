import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, formpost, sweep_pma
sweep_pma.ensure_login()
for cmid in (491618, 491623):
    d = dict(formpost.parse_form(moodle.formfields(cmid)))
    print(cmid, d.get("name"), "| type", d.get("type"), "| assessed", d.get("assessed"), "| scale", d.get("scale[modgrade_type]"), d.get("scale[modgrade_point]"), "| visible", d.get("visible"))
t = moodle.get("/mod/forum/discuss.php?d=10663").text
i = t.find('id="p29083"')
print(re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", t[i:i+2500]))[:600])
for m in re.finditer(r'<form[^>]*id="postrating(\d+)"', t): print("ratingform", m.group(1))
print("rate.php" in t)
