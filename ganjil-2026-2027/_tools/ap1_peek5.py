import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, formpost, sweep_pma
sweep_pma.ensure_login()
d = dict(formpost.parse_form(moodle.formfields(491624)))
i = d["introeditor[text]"].find("5%")
print(repr(d["introeditor[text]"][max(0,i-150):i+80]))
print("gd enabled:", d.get("gradingduedate[enabled]"))
