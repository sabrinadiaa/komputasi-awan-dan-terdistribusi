# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [nama kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| Nadia Sabrina Khoiriyah | 103072400087 | pitfall latency is zero/bagian 1 |
| Fadhil Rizqi Adiyatma | 103072400021 | pitfall the network is reliable/bagian 2 |
| M. Naufal Falih Alhaqi | 103072400027 | Single point of failure karena arsitektur monolitik/bagian 3 |

## Pitfall 1: [Latency is zero] — ditulis oleh [Nadia Sabrina Khoiriyah]

**Bukti di skenario:** 

Pada kasus FoodGo tidak ada timeout sama sekali pada pemanggilan antar service (order module memanggil payment module dan menunggu tanpa batas waktu)

**Kenapa ini keliru:**

Latency is zero menganggap kalau komunikasi antar service tidak mengalami keterlambatan yang perlu diperhatikan. Pemanggilan melalui jaringan membutuhkan waktu, dan waktu bisa berubah, contohnya saat service yang dituju mengalami beban tinggi. Jadi sistem tidak seharusnya menganggap respon dari service lain akan diterima cepat.

**Dampak ke FoodGo:**

Tidak adanya timeout akan menyebabkan request dari order module yang menunggu payment module terus menggunakan resource contohnya thread. Saat traffic meningkat maka semakin banyak request dalam kondisi menunggu yang dapat mengurangi kemampuan server saat menangani request baru dan akan mennyebabkan aplikasi semakin lambat dan terjadi timeout.

**Solusi desain awal:** 

Menerapkan timeout tiap pemanggilan antarservice. Jadi contohnya saat payment module tidak memberi respon maka order module akan berhenti menunggu dan menjalankan mekanisme penanganan kegagalan.

**Trade-off:**

Timeout yang terlalu singkat menyebabkan request gagal. Jadi batas waktu perlu ditentukan secara tepat.

---

## Pitfall 2: [the network is reliable] — ditulis oleh [Fadhil Rizqi Adiyatma]

**Bukti dari kasus**

Pada case foodGo network is always reliable, no need for retry, menunjukkan bahwa FoodGo menganggap komunikasi jaringan selalu dapat diandalkan sehingga tidak menyediakan mekanisme untuk mencoba kembali request yang gagal.  

**Kenapa keliru**

Jaringan tidak selalu 100% bisa diandalkan. Komunikasi antarservice dapat mengalami gangguan, misalnya koneksi terputus atau request dan response tidak berhasil sampai ke tujuan. Jadi perlu memiliki mekanisme untuk menangani kegagalan komunikasi. 

**Dampak** 

foodGo tidak memiliki retry dan akan berpengaruh jika terdapat komunikasi dengan service lain gagal maka tidak akan mendapat respon, dan request tidak otomatis untuk dicoba lagi 

**Solusi** 

Menerapkan mekanisme retry saat terjadi kegagalan komunikasi antarservice, karena retry bisa dikombinasikan dengan backoff jadi system akan memberikan jeda sebelum mencoba Kembali dan tidak langsung mengirim request berkali-kali. 

**Trade off**

Retry yang terlalu sering akan membuat request tambahan yang justru meningkatkan beban pada service yang mengalami masalah. Jadi percobaan dan jeda retry perlu dibatasi.

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
