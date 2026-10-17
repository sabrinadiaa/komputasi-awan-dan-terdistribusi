# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4:

Kendala saat mengisi TODO 1-4 adalah saat pengisian proses election agar tidak looping. Selain itu, sempat muncul PING yang berulang saat monitoring leader dan Node 5 tidak langsung terlihat sebagai leader karena hampir semua node melakukan election hampir bersamaan. Saat melakukan pengujian, sempat muncul output yang kurang sesuai, yaitu Node 4 menampilkan Node 3 sebagai leader.

## Skenario 1: Start normal
- Leader yang terpilih: Node 5
- Log/observasi:

Node dengan ID rendah akan mengirim message election ke node yang lebih tinggi. Node 5 tidak memiliki node dengan ID lebih tinggi, sehingga Node 5 mendeklarasikan dirinya sendiri sebagai leader dan mengirim message coordinator ke Node 1–4. Selanjutnya, Node 1–4 akan mencatat Node 5 sebagai leader.

## Skenario 2: Leader dimatikan
- Leader awal: Node 5
- Leader baru yang terpilih: Node 4
- Berapa lama waktu sampai leader baru terdeteksi: **[isi berdasarkan hasil pengukuran timestamp]**
- Log/observasi:

Saat Node 5 sebagai leader dimatikan, node lain mendeteksi bahwa leader tidak lagi merespons. Proses election kemudian dijalankan untuk memilih leader baru. Berdasarkan hasil pengujian, Node 4 terpilih sebagai leader baru karena merupakan node dengan ID tertinggi yang masih aktif.

Waktu yang dibutuhkan sampai leader baru terdeteksi akan dicatat berdasarkan timestamp pada output program saat leader lama terdeteksi tidak aktif dan saat Node 4 dinyatakan sebagai leader baru.

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 13 Oktober 2026 | GPT | Bantu saya memahami bagian TODO pada simulasi Bully Algorithm | Menjelaskan alur election, ok, coordinator serta proses pemilihan leader | Kami gunakan untuk referensi memahami alur program dan menyesuaikan implementasinya pada kode |
| 15 Oktober 2026 | GPT | Bantu cek mengapa output belum sesuai | Menemukan masalah pada proses election terutama saat program menampilkan output terus-menerus atau looping | Cek kembali kode untuk running ulang dan output sesuai ketentuan |
