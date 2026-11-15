# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi

- Argumen yang dipertimbangkan:

  Eventual Consistency cocok untuk data yang boleh tertinggal sementara, seperti jumlah like atau ulasan. Namun, model ini kurang tepat jika diterapkan pada kasus saldo e-wallet. Keterlambatan replikasi Jakarta-Bandung membuat pelanggan yang baru melakukan top-up tetap membaca saldo lama, sehingga pembayarannya ditolak meskipun saldo sebenarnya mencukupi.

  Karena berkaitan dengan uang, kejadian ini dapat merusak pengalaman dan kepercayaan pelanggan. Menurut kami, Eventual Consistency saja tidak cukup. Sequential Consistency diperlukan sebagai pendekatan yang lebih kuat untuk menjaga urutan operasi pada data saldo. Selain itu, masalah utama dalam studi kasus adalah pelanggan tidak melihat hasil top-up miliknya sendiri setelah berpindah ke server Bandung. Oleh karena itu, diperlukan Client-Centric Consistency berupa Read-Your-Writes.

  Batasannya, Read-Your-Writes tidak mencegah double-spending antarperangkat, sehingga pengurangan saldo tetap harus divalidasi pada satu sumber saldo yang otoritatif.

  Sequential consistency dipertimbangkan agar urutan operasi perubahan saldo secara konsisten. Namun, karena Sequential consistency tidak menjamin urutan berdasarkan waktu nyata, model ini saja belum cukup untuk memastikan pelanggan langsung melihat saldo setelah top up. Jad9 kami menerapkan read-your-writes sebagai jaminan khusus bagi pelanggan, serta menggunakan primary otoritatif dengan operasi debit atomik untuk menjaga keamanan transaksi keuangan.

- Kesimpulan akhir & alasan:

  Read-Your-Writes (Client-Centric Consistency) digunakan sebagai solusi utama untuk pelanggan yang berpindah dari server Jakarta ke Bandung. Server Bandung memeriksa versi terakhir yang dimiliki klien, lalu mengarahkan pembacaan ke Jakarta apabila replikanya belum sinkron.

  Untuk operasi keuangan, debit dan kredit diurutkan melalui satu primary per akun dengan pemeriksaan dan pengurangan saldo secara atomik. Dengan begitu, pembayaran tidak ditolak karena saldo usang dan risiko double-spending dapat dikurangi.
  
  Mekanisme read-your-writes diterapkan dengan memberikan nomor versi pada setiap pembaruan saldo. Setelah top up berhasil, server Jakarta mengembalikan nomor versi terbaru kepada pelanggan. Ketika pelanggan mengakses server Bandung, aplikasi membawa nomor versi tersebut sebagai versi minimal yang harus dipenuhi. Jika versi saldo Bandung lebih rendah, pembacaan dialihkan ke Jakarta. Dengan mekanisme ini, pelanggan tetap mendapatkan saldo terbaru meskipun proses replikasi belum selesai.

- Sequence Diagram
  Sequence diagram menggambarkan perbedaan alur untuk skenario saat bug terjadi dan skenario dengan solusi yang kelompok kami usulkan
  1. saat bug terjadi

```mermaid
%%{init: {"sequence": {"actorMargin": 120}}}%%
sequenceDiagram
    autonumber
    actor P as Pelanggan
    participant J as Server Jakarta
    participant R as Proses Replikasi
    participant B as Server Bandung

    Note over J,B: Saldo awal Rp20.000 (v1)

    P->>J: Top-up Rp50.000
    J->>J: Update saldo menjadi Rp70.000 (v2)
    J-->>P: Top-up berhasil
    J-->>R: Kirim update saldo v2

    Note over R,B: Replikasi tertunda, Bandung masih menyimpan v1

    P->>B: Pesan makanan Rp60.000
    B->>B: Membaca saldo lokal Rp20.000 (v1)

    rect rgb(225, 220, 220)
        B-->>P: Transaksi ditolak (saldo tidak cukup)
        Note over P,B: BUG - Saldo sebenarnya Rp70.000
    end

    R-->>B: Replikasi saldo Rp70.000 (v2)
    B->>B: Update saldo menjadi Rp70.000
```

2. skenario dengan solusi kelompok

```mermaid

%%{init: {"sequence": {"actorMargin": 120}}}%%
sequenceDiagram
    autonumber
    actor P as Pelanggan
    participant J as Server Jakarta
    participant R as Proses Replikasi
    participant B as Server Bandung

    Note over J,B: Saldo awal Rp20.000 (v1)

    P->>J: Top-up Rp50.000
    J->>J: Update saldo menjadi Rp70.000 (v2)
    J-->>P: Top-up berhasil, versi terbaru v2
    J-->>R: Jadwalkan replikasi saldo v2

    Note over R,B: Replikasi tertunda, Bandung masih menyimpan v1

    P->>B: Baca saldo dengan versi minimal v2
    B->>B: Periksa versi saldo lokal (v1)

    alt Versi Bandung lebih lama dari versi pelanggan
        rect rgb(220, 245, 225)
            B->>J: Minta saldo terbaru (redirect)
            J-->>B: Saldo Rp70.000 (v2)
            B-->>P: Tampilkan saldo Rp70.000
            Note over P,B: BERHASIL - Read-Your-Writes terpenuhi
        end
    else Versi Bandung sudah memenuhi v2
        B-->>P: Tampilkan saldo lokal terbaru
    end

    P->>B: Pesan makanan Rp60.000
    B->>J: Validasi dan debit Rp60.000
    J->>J: Periksa saldo dan debit secara atomik
    J->>J: Update saldo menjadi Rp10.000 (v3)
    J-->>B: Pembayaran berhasil
    B-->>P: Pesanan berhasil
    J-->>R: Jadwalkan replikasi saldo v3

    Note over R,B: Replikasi berlangsung dengan pemeriksaan versi

    R-->>B: Replikasi saldo Rp70.000 (v2)
    B->>B: Periksa versi dan simpan v2 jika lebih baru

    R-->>B: Replikasi saldo Rp10.000 (v3)
    B->>B: Periksa versi dan simpan v3 jika lebih baru

    Note over J,B: Kedua server akhirnya menyimpan saldo Rp10.000 (v3)
```
## Simulasi (jika dikerjakan)

- Hasil skenario naif vs Read-Your-Writes:

  Pada skenario naif, pelanggan melakukan top-up sebesar Rp50.000 melalui server Jakarta. Namun, ketika pelanggan membaca saldo melalui Bandung setelah 0,5 detik, saldo yang ditampilkan masih Rp0 karena replikasi belum selesai. Hal ini menunjukkan terjadinya inconsistent read.

  Pada skenario Read-Your-Writes, pelanggan kembali melakukan top-up sebesar Rp20.000 sehingga saldo menjadi Rp70.000 dengan versi 2. Ketika pelanggan membaca saldo melalui Bandung, sistem mendeteksi bahwa versi Bandung masih tertinggal. Oleh karena itu, pembacaan dialihkan ke server Jakarta yang sudah memiliki data terbaru.

  Hasilnya, pelanggan langsung mendapatkan saldo Rp70.000 tanpa harus menunggu replikasi selesai. Setelah proses replikasi berlangsung, kedua server memiliki saldo yang sama, yaitu Rp70.000.

  table hasil pengujian simulasi:

| No. | Skenario Pengujian | Hasil yang Diharapkan | Hasil Aktual | Status |
|---|---|---|---|---|
| 1 | Top-up pertama Rp50.000 di Jakarta | Saldo Jakarta menjadi Rp50.000 (v1) | Rp50.000 (v1) | Berhasil |
| 2 | Membaca saldo Bandung setelah 0,5 detik tanpa Read-Your-Writes | Saldo lama Rp0 terbaca akibat replikasi tertunda | Rp0 | Bug terdeteksi |
| 3 | Replikasi pertama ke Bandung setelah 2 detik | Saldo Bandung menjadi Rp50.000 (v1) | Rp50.000 (v1) | Berhasil |
| 4 | Top-up kedua Rp20.000 di Jakarta | Saldo Jakarta menjadi Rp70.000 (v2) | Rp70.000 (v2) | Berhasil |
| 5 | Pemeriksaan versi saldo Bandung | Sistem mendeteksi versi Bandung masih v1 | Versi Bandung 1, membutuhkan versi 2 | Berhasil |
| 6 | Read-Your-Writes melalui redirect ke Jakarta | Saldo terbaru Rp70.000 dapat dibaca | Rp70.000 | Berhasil |
| 7 | Replikasi kedua selesai | Saldo Jakarta dan Bandung sama-sama Rp70.000 | Jakarta Rp70.000, Bandung Rp70.000 | Berhasil |
## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 15 November 2026 | ChatGPT | Membantu memahami perbedaan Sequential Consistency, Eventual Consistency, dan Read-Your-Writes pada studi kasus saldo FoodGo. | Memberikan penjelasan mengenai dampak keterlambatan replikasi terhadap transaksi saldo serta pendekatan konsistensi yang relevan. | Digunakan sebagai bahan diskusi untuk memahami konsep dan menentukan pendekatan konsistensi yang sesuai dengan studi kasus. |
| 15 November 2026 | ChatGPT | Membantu memahami dan memperbaiki TODO pada simulasi `replica_simulation.py`. | Memberikan penjelasan mengenai penggunaan `threading.Timer()`, pemeriksaan versi replika, dan mekanisme redirect ke Jakarta. | Saran digunakan sebagai referensi untuk mempelajari implementasi, kemudian kode disesuaikan dengan skeleton tugas dan diuji secara mandiri. |
