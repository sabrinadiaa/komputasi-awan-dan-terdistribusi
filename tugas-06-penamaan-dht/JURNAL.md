# Jurnal Proses — Tugas 6

## Implementasi find_successor

- **Kesalahan pertama yang ditemui:** Pada awal pengerjaan, fungsi `find_successor()` belum memiliki logika untuk menentukan node yang bertanggung jawab terhadap suatu key. Selain itu, perlu diperhatikan kondisi ketika hash key lebih besar daripada seluruh ID node yang tersedia di dalam ring.

- **Cara memperbaikinya:** Saya menggunakan fungsi `sorted()` untuk mengurutkan ID node dari yang terkecil hingga terbesar. Kemudian, program mencari node dengan ID terkecil yang lebih besar atau sama dengan hash key. Jika tidak ditemukan node yang memenuhi kondisi tersebut, program mengembalikan node dengan ID terkecil sebagai successor melalui mekanisme wrap-around. Dengan cara ini, proses pencarian tetap berjalan sesuai aturan Chord.

## Skenario join/leave

### 1. Hasil sebelum dan sesudah node baru bergabung

Pada kondisi awal, terdapat empat node yang bergabung ke dalam ring, yaitu:

| Nama Node | Hash ID | Alamat IP |
|---|---:|---|
| node-jakarta-1 | 177 | 10.0.0.1 |
| node-jakarta-2 | 102 | 10.0.0.2 |
| node-bandung-1 | 40 | 10.0.0.3 |
| node-surabaya-1 | 136 | 10.0.0.4 |

Setelah seluruh node bergabung, saya mendaftarkan tiga kurir ke dalam sistem:

| ID Kurir | Hash ID | IP Kurir | Node Penanggung Jawab |
|---|---:|---|---:|
| kurir-001 | 50 | 192.168.1.10 | 102 |
| kurir-002 | 25 | 192.168.1.11 | 40 |
| kurir-003 | 104 | 192.168.1.12 | 136 |

Hasil lookup sebelum perubahan topologi menunjukkan bahwa alamat IP kurir berhasil ditemukan.

```text
--- Lookup sebelum perubahan topologi ---
kurir-001 -> 192.168.1.10
kurir-002 -> 192.168.1.11
```

Selanjutnya, node Medan dengan ID 123 dan alamat IP 10.0.0.5 bergabung ke dalam ring.

```text
--- Node baru bergabung ---
[JOIN] Node 'node-medan-1' (id=123) bergabung, alamat 10.0.0.5
kurir-001 -> 192.168.1.10
```

Pada skenario ini, tidak ada mapping kurir yang berpindah ke node Medan karena hash key kurir yang didaftarkan tidak berada pada rentang yang menjadi tanggung jawab node baru. Meskipun demikian, lookup tetap berhasil menemukan alamat IP kurir.

### 2. Hasil sebelum dan sesudah node keluar

Pada pengujian leave, saya mengeluarkan node Jakarta-2 dengan ID 102 dari ring.

Sebelum node tersebut keluar, kurir-001 dengan hash 50 berada di bawah tanggung jawab node 102. Setelah node 102 keluar, successor baru dari kurir-001 adalah node Medan dengan ID 123.

Hasil pengujian program menunjukkan:

```text
--- Sebuah node keluar ---
[LEAVE] Node 'node-jakarta-2' (id=102) keluar dari ring.
[TRANSFER] kurir-001: node 102 -> node 123
kurir-001 -> 192.168.1.10
kurir-002 -> 192.168.1.11
```

Output `[TRANSFER]` menjadi bukti bahwa tanggung jawab mapping kurir-001 berpindah dari node 102 ke node 123.

Meskipun node yang bertanggung jawab mengalami perubahan, alamat IP kurir tetap sama, yaitu 192.168.1.10. Hal ini menunjukkan bahwa lookup berdasarkan ID Kurir tetap dapat dilakukan setelah perubahan topologi.

**Kesimpulan pengujian:** Implementasi Chord DHT berhasil menentukan successor, melakukan lookup ID Kurir, serta menunjukkan perubahan tanggung jawab mapping ketika node keluar dari ring.

### 3. Bukti pengujian

Screenshot hasil running program disimpan pada folder `bukti/`.

Screenshot tersebut memperlihatkan:

- Node Medan bergabung ke dalam ring.
- Lookup kurir sebelum perubahan topologi.
- Node Jakarta-2 keluar dari ring.
- Perpindahan mapping kurir-001 dari node 102 ke node 123.
- Lookup setelah node keluar tetap menghasilkan alamat IP yang benar.

Nama file bukti:

`bukti/hasil-simulasi-join-leave.png`

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 1 November 2026 | ChatGPT | Membantu memahami implementasi `find_successor()`, `join()`, dan `leave()` pada simulasi Chord DHT. | Mendapatkan saran mengenai mekanisme successor, wrap-around, serta cara menguji perpindahan tanggung jawab mapping ketika node bergabung atau keluar. | Saya mempelajari saran yang diberikan, kemudian menyesuaikannya dengan skeleton program yang disediakan dosen. Saya menjalankan program menggunakan Python, mengamati hasil lookup dan perpindahan mapping, serta menyusun penjelasan berdasarkan hasil pengujian yang saya lakukan. |
