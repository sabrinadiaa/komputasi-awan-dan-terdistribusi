# Tugas 2 (Pekan 2) — Perancangan Arsitektur untuk FoodGo

**Materi terkait:** Architectural style (Layered, SOA, Peer-to-Peer, Publish-Subscribe).

## Studi Kasus

Melanjutkan Tugas 1: FoodGo butuh sistem yang **decoupled** agar tim kurir dan tim resto tidak saling mengganggu ketika salah satu modul diperbarui/deploy ulang. Saat ini semua modul (pesanan, pembayaran, notifikasi kurir, katalog resto) berjalan sebagai satu aplikasi monolitik — sekali deploy, semua modul ikut restart dan berisiko downtime total.

## Tugas Kelompok
1. Pemilihan gaya arsitektur
   Kami memilih Service Oriented Architectur (SOA) untuk service inti dan publish-subscribe untuk notifikasi. SOA digunakan untuk proses inti (order, payment, dan catalog) yang membutuhkan komunikasi langsung. Kami memilih SOA karena transaksi pesanan dan pembayaran membutuhkan komunikasi sinkron dan konsistensi data, selain itu customer perlu mendapatkan konfirmasi langsung terkait berhasil atau tidaknya payment. Sedangkan pub-sub untuk notifikasi resto dan kurir karena notif kurir sifatnya asinkron dan tidak memblokir proses utama, pub-sub digunakan untuk penyebaran informasi atau notifikasi, seperti informasi pesanan baru ke resto atau penugasan ke kurir.

   Kombinasi SOA dan pub-sub ini kami pilih karena foodGo tidak hanya butuh pemisahan modul, tapi juga komunikasi yang tidak bergantung satu sama lain. Dengan memisahkan tiap fungsi menjadi service jika terjadi gangguan di satu service tidak langsung membuat seluruh sistem berhenti. Service juuga tidak perlu tahu siapa yang menerima notifikasi.

2. Diagram arsitektur
   ```mermaid
   graph LR
      C[Pelanggan]
      O[Order Service]
      K[Catalog Service]
      P[Payment Service]
      B[Message Broker]
      R[Restaurant Service]
      Q[Courier notification service]

      C -->|HTTP Request| O

      O -->|Sinkron: Request| K
      K -->|Sinkron: Request| O

      O -->|Sinkron: Request| P
      P -->|Sinkron: Request| O

      O -->|Asinkron: OrderCreated| B
      B -->|Asinkron| R

      R -->|Asinkron: OrderReady| B
      B -->|Asinkron| Q

      Q -->|Asinkron: CourierAssigned| B
      B -->|Asinkron| O

      O -->|Status Pesanan|C
   ```

3. Alur end-to-end saat customer membuat pesanan

   Part 1 - Customer membuat pesanan

   Customer memilih menu di aplikasi FoodGo, lalu order service meminta informasi menu dan kesediaan dari Catalog Service. Komunikasi saat customer memilih pesanan tersebut menggunakan sinkron/request-response karena service pesanan membutuhkan informasi terbaru untuk melanjutkan proses selanjutnya.

   Part 2 - Customer melakukan pembayaran

   Setelah pesanan berhasil dibuat, order service meminta payment service untuk memproses pembayaran customer. Jika berhasil payment service akan memunculkan konfirmasi pembayaran berhasil dan event dikirim ke message broker. Payment service harus menggunakan timeout dan retry mechanism sesuai masalah di tugas 1 untuk menghindari thread order service menunggu tanpa batas.

   Part 3 - Pesanan diteruskan ke resto

   Restaurant service melakukan subscribe di event OrderCreated dari message broker. Dengan mechanisme ini, order service tidak perlu mengetahui detail implementasi dari restaurant service.

   Part 4 - Resto menyelesaikan pesanan

   Setelah pesanan selesai maka informasi diterbitkan sebagai event OrderReady dan dikirim ke message broker. Courier notification service lalu menerima event dan melakukan subscribe terhadap event OrderReady. Event OrderReady memungkinkan proses selanjutnya berjalan dan order service tidak menunggu respon langsung dari restaurannya.

   Part 5 - Penugasan kurir

   Setelah kurir ditentukan, Courier notification service menerbitkan event CourierAssigned dan dikirim melalui message broker juga. Order service dapat memperbarui status pesanan. Courir notification service juga menerima event OrderReady yang melakukan proses pencarian kurir. Setelah ditentukan, service menerbitkan event CourierAssigned.

4. Gaya kombinasi arsitektur SOA dan pub-sub ini dapat mengurangi coupling di FoodGo dengan memisahkan beberapa service yang memiliki tanggung jawab berbeda. Beberapa modul seperti order service, payment service, catalog service, dan notifikasi kurir bisa dikembangkan dan diuji tanpa restart seluruh aplikasi.

Pada komunikasi sinkron, service tetap berinteraksi untuk proses yang membutuhkan respon segera, misalnya validasi pembayaran. Sedangkan pada komunikasi asinkron yang menggunakan pub-sub, service producer tidak perlu mengetahui customer secara langsung. Contohnya Order Service hanya menerbitkan event OrderCreated melalui message broker tanpa mengetahui restaurant service memproses event tersebut. Jadi sistem lebih fleksibel saat adanya perubahan.
   
   
