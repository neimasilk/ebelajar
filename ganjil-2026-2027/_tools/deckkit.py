# -*- coding: utf-8 -*-
"""Helper slide-builder yang dipakai semua deck kuliah."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

NAVY  = RGBColor(0x10, 0x25, 0x45)
AMBER = RGBColor(0xE6, 0xA0, 0x23)
INK   = RGBColor(0x1A, 0x1F, 0x2B)
GREY  = RGBColor(0x5A, 0x63, 0x72)
LIGHT = RGBColor(0xF5, 0xF7, 0xFA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED   = RGBColor(0xB3, 0x2D, 0x2D)


import re as _re
_INLINE = _re.compile(r'\[([^\]]+)\]\(([^)]+)\)|\*\*(.+?)\*\*|\*(.+?)\*')


def _emit(p, raw, size, base, accent):
    """Tulis raw ke paragraph p, tafsirkan **tebal** dan *miring*."""
    pos = 0
    for m in _INLINE.finditer(raw):
        if m.start() > pos:
            r = p.add_run(); r.text = raw[pos:m.start()]
            r.font.size = Pt(size); r.font.color.rgb = base
        if m.group(1) is not None:                      # [teks](url)
            r = p.add_run(); r.text = m.group(1)
            r.font.size = Pt(size); r.font.bold = True
            r.font.underline = True
            r.hyperlink.address = m.group(2)
        elif m.group(3) is not None:                    # **tebal**
            r = p.add_run(); r.text = m.group(3)
            r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = accent
        else:                                           # *miring*
            r = p.add_run(); r.text = m.group(4)
            r.font.size = Pt(size); r.font.italic = True; r.font.color.rgb = base
        pos = m.end()
    if pos < len(raw):
        r = p.add_run(); r.text = raw[pos:]
        r.font.size = Pt(size); r.font.color.rgb = base


def new_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def _blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def _tb(slide, l, t, w, h):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    return tf


def _rect(slide, l, t, w, h, color):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = color
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def _bg(slide, color):
    _rect(slide, 0, 0, 13.333, 7.5, color)


def _notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def title_slide(prs, kicker, title, subtitle, footer):
    s = _blank(prs)
    _bg(s, NAVY)
    _rect(s, 0, 0, 0.28, 7.5, AMBER)
    for txt, top, size, bold, col in (
        (kicker,   1.9, 20, True,  AMBER),
        (title,    2.5, 50, True,  WHITE),
        (subtitle, 4.5, 24, False, RGBColor(0xC8, 0xD4, 0xE6)),
        (footer,   6.3, 16, False, RGBColor(0x8F, 0xA3, 0xBF)),
    ):
        tf = _tb(s, 1.1, top, 11.2, 1.4 if size > 30 else 1.0)
        p = tf.paragraphs[0]; p.text = txt
        p.font.size = Pt(size); p.font.bold = bold; p.font.color.rgb = col
    return s


def section_slide(prs, num, title, sub=""):
    s = _blank(prs)
    _bg(s, NAVY)
    _rect(s, 1.1, 3.05, 1.6, 0.10, AMBER)
    tf = _tb(s, 1.1, 2.2, 11.2, 0.8)
    p = tf.paragraphs[0]; p.text = num
    p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = AMBER
    nline = title.count(chr(10)) + 1
    tf = _tb(s, 1.1, 3.35, 11.2, 0.75 * nline + 0.65)
    p = tf.paragraphs[0]; p.text = title
    p.font.size = Pt(44); p.font.bold = True; p.font.color.rgb = WHITE
    if sub:
        # judul 2+ baris butuh ruang ekstra, kalau tidak subjudul tertimpa
        tf = _tb(s, 1.1, 4.7 + 0.72 * (nline - 1), 11.2, 1.0)
        p = tf.paragraphs[0]; p.text = sub
        p.font.size = Pt(22); p.font.color.rgb = RGBColor(0xC8, 0xD4, 0xE6)
    return s


def content_slide(prs, title, bullets, sub=None, note=None, body_size=22):
    s = _blank(prs)
    _bg(s, WHITE)
    _rect(s, 0, 0, 13.333, 0.14, NAVY)
    tf = _tb(s, 0.85, 0.45, 11.8, 1.0)
    p = tf.paragraphs[0]; p.text = title
    p.font.size = Pt(34); p.font.bold = True; p.font.color.rgb = NAVY
    top = 1.55
    if sub:
        tf = _tb(s, 0.85, 1.35, 11.8, 0.6)
        p = tf.paragraphs[0]; p.text = sub
        p.font.size = Pt(19); p.font.color.rgb = GREY; p.font.italic = True
        top = 2.05
    tf = _tb(s, 0.85, top, 11.8, 7.3 - top - 0.35)
    first = True
    for b in bullets:
        lvl, txt = b if isinstance(b, tuple) else (0, b)
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        size = body_size if lvl == 0 else body_size - 3
        base = INK if lvl == 0 else GREY
        if txt.startswith("__"):
            raw = txt[2:]
        else:
            raw = ("•  " if lvl == 0 else "–  ") + txt
        p.level = lvl
        p.space_before = Pt(3) if lvl else Pt(11)
        _emit(p, raw, size, base, NAVY)
    if note:
        _notes(s, note)
    return s


def table_slide(prs, title, headers, rows, col_w=None, sub=None, note=None, fs=16):
    s = _blank(prs)
    _bg(s, WHITE)
    _rect(s, 0, 0, 13.333, 0.14, NAVY)
    tf = _tb(s, 0.85, 0.45, 11.8, 1.0)
    p = tf.paragraphs[0]; p.text = title
    p.font.size = Pt(34); p.font.bold = True; p.font.color.rgb = NAVY
    top = 1.5
    if sub:
        tf = _tb(s, 0.85, 1.3, 11.8, 0.5)
        p = tf.paragraphs[0]; p.text = sub
        p.font.size = Pt(18); p.font.color.rgb = GREY; p.font.italic = True
        top = 1.95
    nrow, ncol = len(rows) + 1, len(headers)
    height = min(5.2, 0.40 * nrow + 0.18)
    gt = s.shapes.add_table(nrow, ncol, Inches(0.85), Inches(top),
                            Inches(11.65), Inches(height)).table
    if col_w:
        total = sum(col_w)
        for i, w in enumerate(col_w):
            gt.columns[i].width = Emu(int(Inches(11.65) * (w / total)))
    for j, h in enumerate(headers):
        c = gt.cell(0, j); c.text = h
        c.fill.solid(); c.fill.fore_color.rgb = NAVY
        pr = c.text_frame.paragraphs[0]
        pr.font.size = Pt(fs); pr.font.bold = True; pr.font.color.rgb = WHITE
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            c = gt.cell(i, j)
            v = str(val)
            bold = v.startswith("*")
            c.text = v.lstrip("*") if bold else v
            c.fill.solid(); c.fill.fore_color.rgb = LIGHT if i % 2 else WHITE
            pr = c.text_frame.paragraphs[0]
            pr.font.size = Pt(fs)
            pr.font.bold = bold
            pr.font.color.rgb = NAVY if bold else INK
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
    if note:
        _notes(s, note)
    return s


def statement_slide(prs, big, small="", color=NAVY, note=None):
    s = _blank(prs)
    _bg(s, LIGHT)
    _rect(s, 0.85, 2.45, 0.14, 2.2, AMBER)
    tf = _tb(s, 1.35, 2.35, 10.9, 2.3)
    p = tf.paragraphs[0]; p.text = big
    p.font.size = Pt(38); p.font.bold = True; p.font.color.rgb = color
    if small:
        tf = _tb(s, 1.35, 4.85, 10.9, 1.5)
        p = tf.paragraphs[0]; p.text = small
        p.font.size = Pt(21); p.font.color.rgb = GREY
    if note:
        _notes(s, note)
    return s


def code_slide(prs, title, lines, caption=None, note=None):
    s = _blank(prs)
    _bg(s, WHITE)
    _rect(s, 0, 0, 13.333, 0.14, NAVY)
    tf = _tb(s, 0.85, 0.45, 11.8, 1.0)
    p = tf.paragraphs[0]; p.text = title
    p.font.size = Pt(34); p.font.bold = True; p.font.color.rgb = NAVY
    h = min(4.6, 0.32 * len(lines) + 0.5)
    _rect(s, 0.85, 1.55, 11.65, h, RGBColor(0x14, 0x1A, 0x26))
    tf = _tb(s, 1.1, 1.72, 11.2, h - 0.2)
    first = True
    for ln in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.text = ln
        p.font.size = Pt(15); p.font.name = "Consolas"
        p.font.color.rgb = RGBColor(0xD8, 0xE2, 0xF0)
    if caption:
        tf = _tb(s, 0.85, 1.65 + h, 11.65, 0.9)
        p = tf.paragraphs[0]; p.text = caption
        p.font.size = Pt(19); p.font.color.rgb = GREY; p.font.italic = True
    if note:
        _notes(s, note)
    return s


def dual_table_slide(prs, title, headers, rows, col_w=None, sub=None, note=None, fs=14):
    """Satu tabel panjang dipecah jadi dua tabel berdampingan."""
    s = _blank(prs)
    _bg(s, WHITE)
    _rect(s, 0, 0, 13.333, 0.14, NAVY)
    tf = _tb(s, 0.85, 0.45, 11.8, 1.0)
    p = tf.paragraphs[0]; p.text = title
    p.font.size = Pt(34); p.font.bold = True; p.font.color.rgb = NAVY
    top = 1.5
    if sub:
        tf = _tb(s, 0.85, 1.3, 11.8, 0.5)
        p = tf.paragraphs[0]; p.text = sub
        p.font.size = Pt(17); p.font.color.rgb = GREY; p.font.italic = True
        top = 1.95
    half = (len(rows) + 1) // 2
    chunks = [rows[:half], rows[half:]]
    width = 5.7
    for k, chunk in enumerate(chunks):
        left = 0.85 + k * (width + 0.25)
        nrow, ncol = len(chunk) + 1, len(headers)
        gt = s.shapes.add_table(nrow, ncol, Inches(left), Inches(top),
                                Inches(width), Inches(0.34 * nrow)).table
        if col_w:
            tot = sum(col_w)
            for i, w in enumerate(col_w):
                gt.columns[i].width = Emu(int(Inches(width) * (w / tot)))
        for j, h in enumerate(headers):
            c = gt.cell(0, j); c.text = h
            c.fill.solid(); c.fill.fore_color.rgb = NAVY
            pr = c.text_frame.paragraphs[0]
            pr.font.size = Pt(fs); pr.font.bold = True; pr.font.color.rgb = WHITE
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
        for i, row in enumerate(chunk, start=1):
            for j, val in enumerate(row):
                c = gt.cell(i, j)
                v = str(val); bold = v.startswith("*")
                c.text = v.lstrip("*") if bold else v
                c.fill.solid(); c.fill.fore_color.rgb = LIGHT if i % 2 else WHITE
                pr = c.text_frame.paragraphs[0]
                pr.font.size = Pt(fs); pr.font.bold = bold
                pr.font.color.rgb = NAVY if bold else INK
                c.vertical_anchor = MSO_ANCHOR.MIDDLE
    if note:
        _notes(s, note)
    return s


def links_slide(prs, title, rows, sub=None, note=None):
    """rows: list of (label, url). Tabel dua kolom dengan hyperlink hidup."""
    s = _blank(prs)
    _bg(s, WHITE)
    _rect(s, 0, 0, 13.333, 0.14, NAVY)
    tf = _tb(s, 0.85, 0.45, 11.8, 1.0)
    p = tf.paragraphs[0]; p.text = title
    p.font.size = Pt(34); p.font.bold = True; p.font.color.rgb = NAVY
    top = 1.5
    if sub:
        tf = _tb(s, 0.85, 1.3, 11.8, 0.5)
        p = tf.paragraphs[0]; p.text = sub
        p.font.size = Pt(18); p.font.color.rgb = GREY; p.font.italic = True
        top = 1.95
    tf = _tb(s, 0.85, top, 11.8, 7.3 - top - 0.3)
    first = True
    for label, url in rows:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_before = Pt(10)
        r = p.add_run(); r.text = "▸  "
        r.font.size = Pt(20); r.font.color.rgb = AMBER; r.font.bold = True
        r = p.add_run(); r.text = label
        r.font.size = Pt(20); r.font.bold = True
        r.font.underline = True
        r.hyperlink.address = url
    if note:
        _notes(s, note)
    return s
