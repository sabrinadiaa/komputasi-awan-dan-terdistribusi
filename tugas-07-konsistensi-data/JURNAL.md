# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan:

  Eventual consistency cocok untuk data yang boleh tertinggal sementara, seperti jumlah like atau ulasan. Namun argumen ini bertentangan dengan kasus saldo e-wallet. Keterlambatan replikasi Jakarta-Bandung membuat pelanggan yang baru top-up tetap membaca saldo lama, sehingga pembayarannya ditolak. Karena berkaitan dengan uang maka kejadian ini dapat merusak pengalaman dan kepercayaan pelanggan. Menurut kami eventual consistency saja tidak cukup sehingga sequential consistency diperlukan untuk menjaga urutan semua debit dan kredit dalam satu akun agar tidak terjadi konflik. Selain itu, bug di soal terjadi karena pelanggan tidak melihat hasil top-up-nya sendiri setelah pindah ke server Bandung, sehingga cukup dijaga per klien dengan Read-Your-Writes. Batasannya, Read-Your-Writes tidak mencegah double-spend antar-perangkat, sehingga pengurangan saldo tetap harus divalidasi di satu sumber saldo yang otoritatif.
- Kesimpulan akhir & alasan:

  Read-your-writes (client-centric) digunakan sebagai solusi utama untuk pelanggan yang berpindah dari server Jakarta ke Bandung. Server Bandung memeriksa versi terakhir yang dimiliki klien, lalu menunggu singkat atau meneruskan pembacaan ke Jakarta bila replikanya belum sinkron. Untuk operasi keuangan, debit dan kredit diurutkan lewat satu primary per akun dengan pemeriksaan dan pengurangan saldo yang atomik. Dengan begitu pembayaran tidak ditolak karena saldo usang, dan risiko double-spend tetap tertutup.
## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
