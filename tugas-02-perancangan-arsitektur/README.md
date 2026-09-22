# Tugas 2 (Pekan 2) — Perancangan Arsitektur untuk FoodGo

**Materi terkait:** Architectural style (Layered, SOA, Peer-to-Peer, Publish-Subscribe).

## Studi Kasus

Melanjutkan Tugas 1: FoodGo butuh sistem yang **decoupled** agar tim kurir dan tim resto tidak saling mengganggu ketika salah satu modul diperbarui/deploy ulang. Saat ini semua modul (pesanan, pembayaran, notifikasi kurir, katalog resto) berjalan sebagai satu aplikasi monolitik — sekali deploy, semua modul ikut restart dan berisiko downtime total.

## Tugas Kelompok
1. Pemilihan gaya arsitektur
   Kami memilih Service Oriented Architectur (SOA) untuk service inti dan publish-subscribe untuk notifikasi. SOA digunakan untuk proses inti (order, payment, dan catalog) yang membutuhkan komunikasi langsung. Kami memilih SOA karena transaksi pesanan dan pembayaran membutuhkan komunikasi sinkron dan konsistensi data, selain itu customer perlu mendapatkan konfirmasi langsung terkait berhasil atau tidaknya payment. Sedangkan pub-sub untuk notifikasi resto dan kurir karena notif kurir sifatnya asinkron dan tidak memblokir proses utama, pub-sub digunakan untuk penyebaran informasi atau notifikasi, seperti informasi pesanan baru ke resto atau penugasan ke kurir.
   Kombinasi SOA dan pub-sub ini kami pilih karena foodGo tidak hanya butuh pemisahan modul, tapi juga komunikasi yang tidak bergantung satu sama lain. Dengan memisahkan tiap fungsi menjadi service jika terjadi gangguan di satu service tidak langsung membuat seluruh sistem berhenti. Service juuga tidak perlu tahu siapa yang menerima notifikasi.
