"""
Tugas 3 - Simulasi Pesanan Masuk dengan Multithreading

Program mensimulasikan banyak pesanan yang diproses
secara konkuren menggunakan multithreading.

Program juga menyediakan dua mode:
- USE_LOCK=0 -> tanpa Lock, untuk menunjukkan race condition
- USE_LOCK=1 -> menggunakan Lock, untuk memperbaiki race condition
"""

import threading
import random
import time
import os


NUM_ORDERS = 100
NUM_WORKERS = 10

# Counter bersama untuk menghitung total pesanan yang berhasil diproses.
processed_count = 0

# Lock untuk melindungi processed_count.
lock = threading.Lock()

# Mode dapat diubah melalui environment variable:
# USE_LOCK=0 -> tanpa Lock
# USE_LOCK=1 -> dengan Lock
USE_LOCK = os.getenv("USE_LOCK", "1") == "1"


def process_order(order_id: int) -> None:
    """Proses satu pesanan. Dipanggil oleh tiap thread pekerja."""
    global processed_count

    # Simulasikan pekerjaan nyata.
    time.sleep(random.uniform(0.001, 0.01))

    if USE_LOCK:
        # Versi aman menggunakan Lock.
        with lock:
            processed_count += 1
    else:
        # Versi sengaja tidak aman untuk menunjukkan race condition.
        current = processed_count

        # Memberikan kesempatan thread lain mengambil alih
        # sehingga race condition lebih mudah terjadi.
        time.sleep(random.uniform(0.001, 0.01))

        processed_count = current + 1


def worker(order_ids: list) -> None:
    """Satu thread pekerja memproses sekumpulan order_id."""
    for order_id in order_ids:
        process_order(order_id)


def main() -> None:
    order_ids = list(range(1, NUM_ORDERS + 1))

    threads = []

    # Membagi pesanan menjadi beberapa bagian untuk setiap worker.
    chunk = NUM_ORDERS // NUM_WORKERS

    for i in range(NUM_WORKERS):
        start = i * chunk

        if i == NUM_WORKERS - 1:
            end = NUM_ORDERS
        else:
            end = start + chunk

        worker_orders = order_ids[start:end]

        thread = threading.Thread(
            target=worker,
            args=(worker_orders,)
        )

        threads.append(thread)
        thread.start()

    # Menunggu semua thread selesai.
    for thread in threads:
        thread.join()

    print(
        f"Total pesanan diproses: "
        f"{processed_count} (seharusnya {NUM_ORDERS})"
    )

    if processed_count != NUM_ORDERS:
        print("RACE CONDITION TERDETEKSI - tanpa Lock.")
    else:
        print("PEMROSESAN BERHASIL - semua pesanan berhasil diproses.")


if __name__ == "__main__":
    main()