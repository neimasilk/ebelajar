import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, formpost, sweep_pma
sweep_pma.ensure_login()
for cmid in (491624, 491632):
    f = formpost.parse_form(moodle.formfields(cmid))
    print("==", cmid)
    for k, v in f:
        if any(x in k for x in ("date", "submission", "visible", "grade", "sendnot", "requiresub", "attempt", "blind", "markingwork", "completion", "section", "filetypes", "maxbytes")) and "text" not in k:
            print("  ", k, "=", v[:60])
