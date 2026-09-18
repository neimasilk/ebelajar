# Handoff Dokumen — Grading Kelas A ebelajar STIKI

**Terakhir dikerjakan:** 2026-04-22
**Status:** Sesi 1 selesai — DKV-A P3 (3/3 submission dinilai). KB-A dan CV-A belum dimulai.

---

## Konteks Singkat

Dosen Mukhlis Amien (STIKI/UBHINUS) mengajar 3 mata kuliah, masing-masing punya 2 kelas paralel:
- **Kelas P (Profesional)** — self-paced learning, tidak dinilai manual
- **Kelas A (Reguler)** — tentatif, ada tugas/kuis per pertemuan → **ini yang perlu dinilai**

Target sesi: menilai tugas di **P1–P7 ketiga MK kelas A**. Pelan-pelan, dicicil, propose→approve→submit per mahasiswa.

---

## Akses & Kredensial

- **Platform:** https://ebelajar.stiki.ac.id
- **Username login Moodle:** `amien@stiki.ac.id` (USERNAME, bukan email aktif)
- **Email aktif dosen (untuk feedback mahasiswa):** `amien@ubhinus.ac.id`
- **Password:** tidak tersimpan di disk; user login manual di window Playwright

---

## Course IDs Kelas A (2025 Genap)

| MK | Kode Moodle | Course ID |
|---|---|---|
| IF24KK42 Kecerdasan Buatan A | IF24KK42-A-2025-Genap | **7057** |
| IF24KK61 Computer Vision A | IF24KK61-A-2025-Genap | **7030** |
| DK24KB61 Desain Berbasis AI A | DK24KB61-A-2025-Genap | **7016** |

(Kelas P untuk referensi: KB=6951, CV=6925, DKV=6923)

---

## Aturan Penilaian (dari user)

**Rubrik (0–100):**
- Minimum **60** jika mahasiswa sudah mengerjakan (ada submission apapun)
- **Jangan kejam** — beri benefit of the doubt
- **Belum submit → jangan dinilai** (biarkan kosong)

**Mode operasi wajib: propose → approve → submit**
1. Claude baca isi submission
2. Claude usulkan: nilai + alasan + komentar feedback ke user
3. User approve/revisi
4. Baru Claude input ke Moodle (Grade + Feedback comments + Notify students checked)
5. Update `GRADING_LOG.md` per mahasiswa

**Submission Google Docs/Drive private:**
- Claude tidak punya akses (Google Drive MCP terhubung akun beda)
- Coba buka lewat Playwright; jika Access Denied, tawarkan 2 opsi ke user:
  - (a) buka tab baru di window Playwright, paste link — karena user sudah login Google, content terbuka, Claude switch tab & baca
  - (b) kasih **nilai sementara 60** + komentar minta share ke `amien@ubhinus.ac.id`, catat di log "sementara, revisi setelah akses terbuka"

---

## Progress Sesi 2026-04-22

### DKV-A P3 Text to Image generator (cmid 488861) — ✅ COMPLETED 3/3

| # | Nama | NIM | userId | Nilai | Status |
|---|---|---|---|---|---|
| 1 | Muhammad Haikal Rifqi | 202111005 | 1622 | **70** | Final (terlambat 3j32m, hanya 1 prompt) |
| 2 | Gebby Rhatu Leransevfia | 232111023 | 12252 | **60** | **Sementara** — GDocs private |
| 3 | Muhammad Ilham Ridllo Kurnia | 242111018 | 12444 | **60** | **Sementara** — GDrive folder private |

**Follow-up:** revisi Gebby & Ilham setelah mereka buka akses ke `amien@ubhinus.ac.id`.

---

## Yang Tersisa (Todo)

### KB-A (course 7057) — 4 submission total

| Pert | CMID | Nama Tugas | Submitter |
|---|---|---|---|
| P2 | 486146 | Tugas 1: Identifikasi Masalah & Metode AI | 2 |
| P4 | 486152 | Tugas 2: Analisis Komparatif Metode AI | 1 |
| P5 | 486155 | Tugas 3: Implementasi Algoritma Pencarian A* | 1 |
| P7 | 486161 | Tugas 4: Implementasi & Optimasi Model Prediktif | 0 (skip) |
| P6 | 486158 | Kuis 1 (auto-grade) | — (skip) |

### CV-A (course 7030) — 40 submission total

| Pert | CMID | Nama Tugas | Submitter |
|---|---|---|---|
| P2 | 487010 | Praktikum Modul 2 Computer Vision | 13 |
| P3 | 487332 | Tugas Praktik: Morfologi & Analisis Wilayah | 8 |
| P4 | 487338 | Tugas Praktik: Peningkatan Kualitas Citra | 7 |
| P5 | 487344 | Tugas Praktik: Deteksi Tepi & Segmentasi | 10 |
| P6 | 487350 | Tugas Evaluasi: Menghitung PSNR | 2 |

---

## Teknik Input Nilai ke Moodle (yang sudah terbukti)

URL grader: `https://ebelajar.stiki.ac.id/mod/assign/view.php?id=<CMID>&action=grader&userid=<USERID>`

Selector form:
- Grade input: `#id_grade`
- Feedback editor (Atto contenteditable): `#id_assignfeedbackcomments_editoreditable`
- Feedback hidden textarea (sync ini juga): `#id_assignfeedbackcomments_editor`
- Notify students checkbox: `input[name="sendstudentnotifications"]`
- Save button: `button[name="savechanges"]`

**Catatan penting:** Notify checkbox kadang tidak toggle via click DOM atau Playwright click. Set langsung pakai JS: `notify.checked = true; notify.dispatchEvent(new Event('change', {bubbles:true}))`.

Konfirmasi sukses: dialog `"Changes saved"` muncul + `#id_grade` berubah ke format `"XX.00"`.

---

## File Terkait

- `D:\documents\ebelajar\HANDOFF.md` — handoff fase 1 (isi konten & iframe section)
- `D:\documents\ebelajar\HANDOFF_GRADING.md` — file ini
- `D:\documents\ebelajar\GRADING_LOG.md` — log detail per mahasiswa (selalu update setelah submit)
- Memory: `project_elearning_stiki.md`, `feedback_grading_workflow.md`, `user_contact.md`

---

## Strategi Sesi Berikutnya (saran)

1. Mulai dari **KB-A** (4 sub, cepat selesai) sebagai warming up
2. Lanjut **CV-A P6** (2 sub, kecil)
3. Tackle batch besar CV-A P2/P3/P4/P5 (38 sub) — bisa dipecah per pertemuan, satu pertemuan per sesi
4. Sambil menunggu follow-up dari Gebby & Ilham untuk revisi DKV-A
