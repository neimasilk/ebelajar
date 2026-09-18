# -*- coding: utf-8 -*-
"""Repost seluruh form Moodle dengan hanya field tertentu ditimpa (strategi playbook)."""
import re, html as H


def parse_form(t):
    """Kembalikan list (name, value) dari seluruh input/select/textarea pada form HTML."""
    data = []

    def input_val(tag):
        v = re.search(r'value="([^"]*)"', tag)
        if not v:
            v = re.search(r"value='([^']*)'", tag)
        return H.unescape(v.group(1)) if v else ""

    for m in re.finditer(r'<input\b[^>]*>', t):
        tag = m.group(0)
        nm = re.search(r'name="([^"]+)"', tag)
        if not nm:
            continue
        name = nm.group(1)
        if name in ("submitbutton", "cancel"):
            continue
        typ = re.search(r'type="([^"]*)"', tag)
        typ = typ.group(1).lower() if typ else "text"
        if typ in ("checkbox", "radio"):
            if re.search(r'\bchecked\b', tag):
                data.append((name, input_val(tag)))
        elif typ in ("submit", "button", "image"):
            if name == "submitbutton2":
                data.append((name, "Save and return to course"))
        else:
            data.append((name, input_val(tag)))

    for m in re.finditer(r'<select\b[^>]*name="([^"]+)"[^>]*>(.*?)</select>', t, re.S):
        name, body = m.group(1), m.group(2)
        sel = None
        for om in re.finditer(r'<option\b([^>]*)>', body):
            if re.search(r'selected', om.group(1), re.I):
                vm = re.search(r'value="([^"]*)"', om.group(1))
                sel = vm.group(1) if vm else ""
                break
        if sel is None:
            om = re.search(r'<option\b[^>]*value="([^"]*)"', body)
            sel = om.group(1) if om else ""
        data.append((name, H.unescape(sel)))

    for m in re.finditer(r'<textarea\b[^>]*name="([^"]+)"[^>]*>(.*?)</textarea>', t, re.S):
        data.append((m.group(1), H.unescape(m.group(2))))

    return data


def overrides_dict(**kw):
    return dict(kw)


def apply(data_list, ov):
    out, seen = [], set()
    for name, val in data_list:
        if name in ov:
            out.append((name, ov[name]))
        else:
            out.append((name, val))
        seen.add(name)
    for name, val in ov.items():
        if name not in seen:
            out.append((name, val))
    return out
