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
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 2 Oktober 2026 | GPT | Meminta penjelasan umum tentang multithreading dan race condition | Mendapat penjelasan terkait lock dan race condition | Analisis ditulis dan disesuaikan sendiri |
