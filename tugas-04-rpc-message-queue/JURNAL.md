# Jurnal Proses — Tugas 4

## Jalur yang dipilih

- **Jalur B — Message Queue / Message-Oriented Middleware (MQ/MOM)**

  Kelompok memilih Jalur B karena skenario notifikasi pembayaran dari
  modul Pembayaran ke modul Kurir/Notifikasi membutuhkan komunikasi
  asynchronous. Modul Pembayaran tidak perlu menunggu modul Kurir selesai
  memproses notifikasi.

  Implementasi menggunakan **RabbitMQ yang dijalankan melalui Docker**.
  Event pembayaran dikirim oleh `publisher.py` ke queue
  `pembayaran_berhasil`, kemudian diproses oleh `consumer.py` ketika
  consumer tersedia.

## Kendala teknis

- Pada saat menjalankan Docker Compose muncul peringatan bahwa atribut
  `version` pada `docker-compose.yml` sudah obsolete/deprecated. Namun
  peringatan tersebut tidak menghambat proses dan container RabbitMQ tetap
  berhasil dibuat dan dijalankan.

- RabbitMQ berhasil dijalankan menggunakan Docker dengan container
  `mq-rabbitmq-1`.

- RabbitMQ Management Dashboard berhasil diakses melalui
  `http://localhost:15672`.

- Consumer dan publisher berhasil terhubung ke RabbitMQ dan menggunakan
  queue dengan nama `pembayaran_berhasil`.

## Uji "Pesan Tidak Hilang"
### Langkah pengujian

1. Menjalankan RabbitMQ menggunakan Docker Compose.
2. Menjalankan `consumer.py` untuk memastikan consumer dapat menerima event.
3. Menghentikan `consumer.py` menggunakan `Ctrl+C`.
4. Menjalankan `publisher.py` ketika consumer dalam keadaan mati.
5. Publisher berhasil mengirim event pembayaran ke RabbitMQ.
6. Membuka RabbitMQ Management Dashboard dan memeriksa queue
   `pembayaran_berhasil`.
7. Dashboard menunjukkan terdapat 3 pesan dengan status `Ready`.
8. Menjalankan kembali `consumer.py`.
9. Consumer menerima dan memproses ketiga pesan yang sebelumnya tersimpan
   di antrean.
10. Setelah pesan diproses, jumlah pesan `Ready` pada queue menjadi 0.

### Hasil yang diamati

Pengujian menunjukkan bahwa pesan tidak hilang ketika consumer sedang
tidak aktif. Publisher tetap dapat mengirim event pembayaran ke RabbitMQ
tanpa harus menunggu consumer.

RabbitMQ menyimpan pesan tersebut pada queue `pembayaran_berhasil`.
Ketika consumer dijalankan kembali, pesan yang tersimpan berhasil
diterima dan diproses oleh modul Kurir/Notifikasi.

Pada RabbitMQ Management Dashboard, terdapat 3 pesan dengan status
`Ready` ketika consumer dimatikan. Setelah consumer dijalankan kembali,
ketiga pesan tersebut berhasil diproses dan jumlah pesan pada queue
menjadi 0.

Hasil tersebut membuktikan adanya **asynchronous decoupling**, yaitu
publisher dan consumer tidak harus aktif pada waktu yang sama.

## Analisis Pemilihan Pola Komunikasi

Message Queue sesuai digunakan untuk skenario notifikasi pembayaran
karena modul Pembayaran tidak membutuhkan respons langsung dari modul
Kurir/Notifikasi.

Publisher dapat mengirim event ke RabbitMQ kemudian melanjutkan
proses lainnya tanpa menunggu consumer. RabbitMQ menyimpan pesan di
dalam queue sampai consumer siap memprosesnya.

Penggunaan Docker membantu menyediakan RabbitMQ secara lokal sehingga
broker dapat dijalankan dan dihentikan dengan mudah selama pengujian.

Jika komunikasi menggunakan RPC untuk skenario notifikasi tersebut,
modul Pembayaran harus menunggu respons dari modul Kurir. Jika modul
Kurir sedang sibuk, lambat, atau tidak tersedia, proses pada modul
Pembayaran dapat ikut mengalami keterlambatan atau timeout.

Dengan menggunakan Message Queue, publisher dan consumer menjadi lebih
terpisah (decoupled), sehingga sistem lebih sesuai untuk komunikasi
notifikasi yang bersifat asynchronous.

## Log Penggunaan AI (Level 2)

> AI digunakan sebagai bantuan brainstorming, pemahaman konsep, dan
> penyusunan outline. Implementasi program, pengujian, dan penyesuaian
> akhir dilakukan dan diverifikasi sendiri.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 6 Oktober 2026 | GPT | Meminta panduan langkah-langkah pengerjaan menggunakan Message Queue/RabbitMQ | Mendapat penjelasan mengenai alur publisher, RabbitMQ queue, consumer, Docker, dan asynchronous decoupling | Langkah pengujian dilakukan sendiri melalui VS Code, Docker, RabbitMQ Dashboard, `publisher.py`, dan `consumer.py` |
| 6 Oktober 2026 | GPT | Meminta penjelasan tentang pengujian pesan tidak hilang ketika consumer dimatikan | Mendapat ide untuk mematikan consumer, menjalankan publisher, melihat pesan berstatus Ready pada RabbitMQ, kemudian menyalakan kembali consumer | Skenario dijalankan sendiri dan hasil pengujian dicatat berdasarkan output terminal dan RabbitMQ Dashboard |
