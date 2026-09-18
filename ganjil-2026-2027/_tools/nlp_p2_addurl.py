# -*- coding: utf-8 -*-
"""NLP A: tambah URL resource 'Bahan Pertemuan 2 di Google Drive' di section 2 (course 7226)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sweep_pma  # noqa: F401  (ensure_login: isi moodle.PASS dari .env)
from ap1_addmods import add_url, cmids
import moodle

COURSE = 7226
SECTION = 2
NAME = "Bahan Pertemuan 2 di Google Drive"
TARGET = "https://drive.google.com/drive/folders/1ozSzshC8eBpPGU1R5uZx_zsVkJmj0oBS"
INTRO = ("Slide Pertemuan 2, Modul Mandiri, dan video ada di satu folder Google Drive ini. "
         "eBelajar hanya menautkan supaya salinannya cuma satu dan selalu terbaru.")

if __name__ == "__main__":
    sweep_pma.ensure_login()
    r = add_url(COURSE, SECTION, NAME, TARGET, INTRO)
    print("http", r.status_code)
    print(cmids(COURSE, [NAME]))
