# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4:

Kendala saat mengisi TODO 1-4 adalah saat pengisian proses election agar tidak looping, selain itu sempat muncul PING yang berulang juga saat monitoring leader dan Node 5 tidak langsung terlihat sebagai leader karena hampir semua node melakukan election hampir bersamaaan. Saat melakukan pengujian sempat menampilkan output yang kurang sesuai yaitu node 4 menampilkan node 3 sebagai leader.

## Skenario 1: Start normal
- Leader yang terpilih: node 5
- Log/observasi:

Node dengan ID rendah akan mengirim message election ke node yang lebih tinggi. Node 5 tidak ada node setelahnya yang lebih tinggi, sehingga node 5 mendeklarasikan dirinya sendiri menjadi leader dan mengirim message coordinator ke node 1-4. Selanjutnya node 1-4 akan mencatat node 5 sebagai leader

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: node 4
**- Berapa lama waktu sampai leader baru terdeteksi: **

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 13 Oktober 2026 | GPT | Bantu saya memahami bagian TODO pada simulasi Bully Algorithm | Menjelaskan alur election, ok, coordinator serta proses pemilihan leader | Kami gunakan untuk referensi memahami alur program dan menyesuaikan implementasinya pada kode |
|15 Oktober 2026 | GPT | Bantu cek mengapa output belum sesuai | Menemukan masalah pada proses election terutama saat program menampilkan output terus menerus looping | Cek kembali kode untuk running ulang dan output sesuai ketentuan |
