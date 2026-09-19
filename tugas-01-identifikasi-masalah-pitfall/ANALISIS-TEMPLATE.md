# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [nama kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| Nadia Sabrina Khoiriyah | 103072400087 | [pitfall/bagian yang dikerjakan] |
| Fadhil Rizqi Adiyatma | 103072400021 | [pitfall/bagian yang dikerjakan] |
| M. Naufal Falih Alhaqi | 103072400027 | pitfall/bagian 3 |

## Pitfall 1: [nama pitfall] — ditulis oleh [nama]

**Bukti di skenario:** [kutip/paraphrase bagian skenario]

**Kenapa ini keliru:** [penjelasan]

**Dampak ke FoodGo:** [mekanisme kegagalan konkret]

**Solusi desain awal:** [usulan solusi]

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 3: Single point of failure karena arsitektur monolitik  — ditulis oleh Naufal Falih

**Bukti**

Pada case foodGo saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama. Case juga menyebutkan bahwa backend terkadang mengalami crash dan membutuhkan restart secara manual. 

**Masalah design** 

Menaruh semua modul dalam 1 proses akan berpengaruh saat 1 modul bermasalah maka modul itu ikut menghabiskan resource Bersama (CPU, memori dan thread pool) sehingga modul sehat lain akan terdampak. 

**Dampak** 

Ketika server atau proses monolitik mengalami overload atau crash, beberapa fungsi FoodGo seperti order, payment, dan courier notification dapat ikut terganggu secara bersamaan. Sehingga kegagalan pada satu tempat dapat berdampak pada banyak fungsi yang sebenarnya berbeda. 

**Solusi** 

Memisahkan modul utama menjadi service yang terpisah, misalnya Order Service, Payment Service, dan Courier Notification Service. Jadi beban dan kegagalan pada satu service dapat terisolasi sehingga tidak langsung memengaruhi seluruh fungsi aplikasi. 

**Trade off** 

Pemisahan service membuat sistem menjadi lebih kompleks karena service harus berkomunikasi melalui jaringan. Sehingga sistem juga perlu menangani masalah seperti latency, timeout, dan kegagalan jaringan. 

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
