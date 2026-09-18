# -*- coding: utf-8 -*-
"""Forum Exit-ticket P2 AP1 A: duplikat Diskusi Umum (502324) -> rename/rating -> pindah S2 -> seed -> page P2."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle, formpost, sweep_pma, nlp_p2_due
import ap1_p2_setup as S
import ap1_move

FCM = 502324

if __name__ == "__main__":
    sweep_pma.ensure_login()
    d = dict(formpost.parse_form(moodle.formfields(FCM)))
    if d.get("name") != S.EXIT_NAME:
        r = nlp_p2_due.repost(FCM, {"name": S.EXIT_NAME, "introeditor[text]": S.EXIT_INTRO,
                                    "assessed": "1", "scale[modgrade_type]": "point",
                                    "scale[modgrade_point]": "100"})
        d = dict(formpost.parse_form(moodle.formfields(FCM)))
        print("rename http%d ->" % r.status_code, d.get("name"), "| type", d.get("type"),
              "| assessed", d.get("assessed"), d.get("scale[modgrade_point]"))
    if FCM not in [c for _, c, _ in S.section_mods(2)]:
        ap1_move.move(FCM, 2)
    print("S0:", [x for x in S.section_mods(0) if x[1] == FCM])
    print("S2:", S.section_mods(2))
    print(S.step_seed(FCM))
    print(S.step_page(FCM))
