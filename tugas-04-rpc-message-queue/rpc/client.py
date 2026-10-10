"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import time


def main():
    # TODO 1: buat ServerProxy ke http://localhost:8000
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000", allow_none=True)

    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    start = time.time()
    # TODO 2: panggil proxy.cek_saldo("user1") dan cetak hasilnya + waktu tempuh
    saldo = proxy.cek_saldo("user1")
    print(f" -> saldo user 1: {saldo} (waktu tempuh: {time.time() - start:.2f} detik)")

    print("Memanggil proses_pembayaran('user1', 20000) ...")
    # TODO 3: panggil proxy.proses_pembayaran("user1", 20000) dan cetak hasilnya
    hasil = proxy.proses_pembayaran("user1", 2000)
    print(f" -> hasil: {hasil}")

    print("jika user x (user tidak ada)")
    try:
        proxy.cek_saldo("user_x")
    except xmlrpc.client.Fault as e:
        printf(f" -> server error: {e.faultStriing}")


if __name__ == "__main__":
    main()
