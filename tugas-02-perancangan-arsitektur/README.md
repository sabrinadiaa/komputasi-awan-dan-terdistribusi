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
      O[Service Pesanan]
      K[Service Katalog Resto]
      P[Service Pembayaran]
      B[Message Broker]
      R[Resto]
      Q[Service Kurir/notif]

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

   Customer memilih menu di aplikasi FoodGo, lalu service pesanan meminta informasi menu dan kesediaan dari service katalog resto. Komunikasi saat customer memilih pesanan tersebut menggunakan sinkron/request-response karena service pesanan membutuhkan informasi untuk melanjutkan proses selanjutnya.

   Part 2 - Customer melakukan pembayaran

   Setelah pesanan berhasil dibuat, service pesanan meminta service pembayaran untuk memproses pembayaran customer. Jika berhasil service pembayaran akan memunculkan konfirmasi pembayaran berhasil dan event dikirim ke message broker.

   Part 3 - Pesanan diteruskan ke resto

   Service resto akan melakukan subscribe terhadap event yang relevan. Resto tidak perlu melakukan request terus menerus ke service pesanan utnuk mengetahui pesanan baru.

   Part 4 - Resto menyelesaikan pesanan

   Setelah pesanan selesai maka informasi diterbitkan sebagai event OrderReady dan dikirim ke message broker. Service kurir lalu menerima event dan melakukan subscribe terhadap event OrderReady.

   Part 5 - Penugasan kurir

   Setelah kurir ditentukan, service kurir menerbitkan event CourierAssigned dan dikirim melalui message broker juga. Service Pesanan dapat memperbarui status pesanan.
   
   
