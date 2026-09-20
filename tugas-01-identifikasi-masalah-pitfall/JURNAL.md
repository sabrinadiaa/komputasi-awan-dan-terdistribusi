# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## 17 September 2026 (pembagian tugas)
- Peserta:
  Nadia Sabrina Khoiriyah, Fadhil Rizqi Adiyatma, M. Naufal Falih Alhaqi
- Poin diskusi:
  1. Membaca kasus kegagalan FoodGo saat jam makan siang (aplikasi lambat, crash, tidak ada timeout/retry, dan server monolitik)
  2. Menentukan 3 pitfall utama yang paling cocok dengan studi kasus yaitu Nadia mengambil pitfall Latency is zero (karena modul order menunggu modul payment tanpa batas), Fadhil mengambil pitfall The network is reliable (karena kode tim menulis asumsi tidak butuh retry), dan Naufal mengambil masalah desain arsitektur Single Point of Failure / monolitik (karena semua modul berjalan di satu server dan satu proses).
- Perbedaan pendapat (jika ada):

  Sempat bingung apakah masalah server monolitik masuk ke daftar 8 Fallacies resmi Peter Deutsch atau masalah desain terdistribusi secara umum. Akhirnya sepakat dipakai di poin 3 karena di panduan soal diperbolehkan memilih masalah desain seperti single point of failure.

## 19 September 2026 (review analisis)
- Peserta:
  Nadia Sabrina Khoiriyah, Fadhil Rizqi Adiyatma, M. Naufal Falih Alhaqi
- Poin diskusi:
  1. Menyatukan draft analisis dari masing-masing anggota
  2. Merumuskan bagian kesimpulan bersama terkait bagaimana perbaikan 3 pitfall ini menjadi jembatan menuju Tugas 2 (pemisahan service + komunikasi asinkron via message broker).
- Perbedaan pendapat (jika ada):

  Sempat bingung bagaimana cara menghubungkan kesimpulan dengan Tugas 2. Solusinya, kami memetakan bahwa pemisahan modul yang diusulkan Naufal akan menjadi arsitektur SOA, sementara penanganan timeout/retry akan dilengkapi dengan message broker untuk notifikasi kurir.

## Review Silang
- Nadia mengomentari analisis Fadhil:

Pada bagian dampak tidak ada retry, sebaiknya ditambahkan skenario nyata di bagian order, contohnya resiko transaksi menggantung atau pesanan langsung gagal saat koneksi terputus

- Naufal mengomentari analisis Nadia: Pada bagian dampak latency, perlu dijelaskan bahwa ketiadaan timeout membuat thread server tertahan (thread starvation) sehingga request pengguna lain ikut terkena dampak.


## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
