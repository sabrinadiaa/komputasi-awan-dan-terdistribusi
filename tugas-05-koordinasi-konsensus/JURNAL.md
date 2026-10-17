# Jurnal Proses — Tugas 5

## Implementasi Bully

**Kendala saat mengisi TODO 1–4:**

Kendala saat mengisi TODO 1–4 adalah saat mengatur proses election agar tidak looping. Selain itu, sempat muncul pesan PING yang berulang saat monitoring leader. Node 5 juga tidak langsung terlihat sebagai leader karena hampir semua node melakukan election pada waktu yang hampir bersamaan. Saat pengujian, sempat muncul output yang kurang sesuai, yaitu Node 4 menampilkan Node 3 sebagai leader.

## Skenario 1: Start normal

- **Leader yang terpilih:** Node 5

**Log/observasi:**

Node dengan ID rendah mengirim pesan `ELECTION` ke node dengan ID lebih tinggi. Karena tidak ada node yang memiliki ID lebih tinggi dari Node 5, Node 5 mendeklarasikan dirinya sebagai leader dan mengirim pesan `COORDINATOR` ke Node 1–4. Selanjutnya, Node 1–4 mencatat Node 5 sebagai leader.

## Skenario 2: Leader dimatikan

- **Leader awal:** Node 5
- **Leader baru yang terpilih:** Node 4

**Waktu kemunculan output `Leader baru = Node 4`:**

- Node 1: 17,28 detik
- Node 2: 25,44 detik
- Node 3: 24,56 detik
- **Rata-rata: 22,43 detik**

**Log/observasi:**

Saat Node 5 sebagai leader dimatikan, node lain mendeteksi bahwa leader tidak lagi merespons dan memulai proses election. Berdasarkan hasil pengujian, Node 4 terpilih sebagai leader baru karena merupakan node dengan ID tertinggi yang masih aktif.

Output `Leader baru = Node 4` muncul pada waktu yang berbeda di setiap terminal. Perbedaan ini menunjukkan bahwa pesan diproses dan output ditampilkan pada waktu yang berbeda di masing-masing node.

Waktu di atas merupakan waktu kemunculan output yang diamati dari video, bukan durasi election yang terverifikasi sejak Node 5 dimatikan.

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah menjadi pekerjaan sendiri |
|---|---|---|---|---|
| 13 Oktober 2026 | GPT | Bantu saya memahami bagian TODO pada simulasi Bully Algorithm | Menjelaskan alur election, OK, coordinator, dan proses pemilihan leader | Digunakan sebagai referensi untuk memahami alur program dan menyesuaikan implementasi |
| 15 Oktober 2026 | GPT | Bantu cek mengapa output belum sesuai | Membahas masalah proses election yang menyebabkan output berulang atau looping | Kode diperiksa kembali dan program dijalankan ulang untuk mengecek kesesuaian output |
| 17 Oktober 2026 | GPT | Bantu menyusun catatan hasil pengujian skenario 2 saat leader dimatikan | Memberikan ide tentang informasi yang perlu dicatat, seperti leader awal, leader baru, dan waktu kemunculan output | Digunakan sebagai panduan untuk menyusun catatan berdasarkan hasil pengujian |
| 17 Oktober 2026 | GPT | Bantu memahami cara mencatat waktu pada skenario 2 | Menjelaskan penggunaan timestamp dan perbedaan waktu kemunculan output dengan durasi election | Digunakan sebagai referensi untuk mencatat dan menjelaskan hasil pengujian |

