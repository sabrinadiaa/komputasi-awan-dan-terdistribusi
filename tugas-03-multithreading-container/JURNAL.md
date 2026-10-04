# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat 5 kali percobaan:

19, 21, 17, 21, 19 yang seharusnya 100.  
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri):

Hasil percobaan tanpa lock menunjukkan jumlah perhitungan tidak selalu mencapai 100 karena beberapa thread membaca dan mengubah processed_count bersamaan. Saat 2 thread membaca nilai yang sama maka hasil pembaruan salah satu thread bisa menimpa thread lainnya. Saat melakukan perhitungan proses juga melewati sleep antara membaca dan menulis sehingga thread lain membaca nilai yang sama dan saling menimpa hasil satu sama lain. Bukti running tanpa lock terdapat pada bukti/1-bukti tanpa lock.png

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan:
100, 100, 100, 100, 100 (sesuai dengan target).

- Adanya lock menyebabkan hanya 1 thread yang boleh membaca, mengubah, dan menulis counter dalam 1 waktu. Sleep tetap di luar lock agar thread berjalan. Lock memastikan hanya 1 thread yang mengubah perhitungan di satu waktu, jadi tidak ada pembaruan counter yang hilang. Bukti hasil percobaan terdapat pada bukti/2-bukti dengan lock.png


## Kendala Docker
- Pada awal instalasi, WSL mengalami error `WININET_E_CONNECTION_ABORTED` saat mengunduh Ubuntu. Masalah tersebut diatasi dengan mengaktifkan fitur Windows Subsystem for Linux dan Virtual Machine Platform, kemudian menginstal Ubuntu secara manual menggunakan perintah `wsl --install -d Ubuntu`.
- Saat menjalankan `docker info`, sempat muncul error karena Docker daemon belum berjalan. Setelah Docker Desktop dijalankan dan Docker Engine aktif, Docker dapat digunakan kembali.
- Saat melakukan build, perintah harus dijalankan dari folder `tugas-03-multithreading-container` agar Dockerfile dapat ditemukan.
- Setelah konfigurasi selesai, image berhasil dibuat dengan perintah `docker build -t foodgo-order-sim .` dan container berhasil dijalankan menggunakan `docker run --rm foodgo-order-sim`.
- Hasil pengujian di dalam container menunjukkan `processed_count` sebesar 100 dari 100 pesanan sehingga program berhasil berjalan dengan Lock.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 2 Oktober 2026 | GPT | Meminta penjelasan umum tentang multithreading dan race condition | Mendapat penjelasan terkait lock dan race condition | Analisis ditulis dan disesuaikan sendiri |
| 4 Oktober 2026 | GPT | Meminta penjelasan mengenai implementasi multithreading dan penggunaan `threading.Lock()` pada simulasi pesanan | Mendapat penjelasan mengenai penggunaan Lock untuk mencegah race condition dan menjaga nilai `processed_count` | Konsep dipahami kembali, kemudian diterapkan dan diuji pada program secara langsung |
| 4 Oktober 2026 | GPT | Meminta bantuan memahami proses instalasi, build, dan menjalankan program menggunakan Docker | Mendapat panduan mengenai WSL, Dockerfile, `docker build`, dan `docker run` | Perintah dijalankan sendiri melalui terminal dan hasilnya diverifikasi sampai image dan container berhasil berjalan |
| 4 Oktober 2026 | GPT | Meminta bantuan troubleshooting ketika terdapat kendala pada WSL, Docker, dan lokasi folder project | Mendapat arahan untuk memeriksa konfigurasi dan memperbaiki langkah yang mengalami error | Langkah perbaikan dilakukan sendiri dan hasil akhirnya diuji melalui terminal |
