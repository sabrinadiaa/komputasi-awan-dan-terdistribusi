"""
Tugas 5 - Simulasi Node untuk Bully Algorithm

Infrastruktur jaringan (socket server/client) sudah disediakan.
Logika Bully Algorithm (bagian # TODO) harus kalian lengkapi sendiri.

Contoh menjalankan (5 terminal terpisah):
    python3 node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
    python3 node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
    ... dst untuk id 3, 4, 5
"""

import argparse
import socket
import threading
import time

ELECTION_TIMEOUT = 2.0  # detik menunggu balasan OK sebelum menyatakan diri leader


class Node:
    def __init__(self, node_id: int, port: int, peers: dict):
        self.node_id = node_id
        self.port = port
        # peers: dict {peer_id: peer_port} untuk semua node LAIN
        self.peers = peers
        self.leader_id = None
        self.lock = threading.Lock()
        
        #menambahkan flag untuk tahu apakah ada node lebih tinggi yang merespons
        self.received_ok = False
        self.election_running = False

    # ---------- Infrastruktur jaringan (SUDAH LENGKAP, jangan diubah) ----------

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", self.port))
        server.listen()
        print(f"[Node {self.node_id}] Listening di port {self.port}")
        while True:
            conn, _ = server.accept()
            threading.Thread(target=self.handle_connection, args=(conn,), daemon=True).start()

    def handle_connection(self, conn: socket.socket):
        with conn:
            data = conn.recv(1024).decode()
            if not data:
                return
            sender_id, msg_type = data.split(":")
            self.on_message(int(sender_id), msg_type)

    def send_message(self, target_port: int, msg_type: str) -> bool:
        """Kirim pesan ke node lain. Return False jika node target tidak merespons (dianggap mati)."""
        try:
            with socket.create_connection(("localhost", target_port), timeout=1.0) as s:
                s.sendall(f"{self.node_id}:{msg_type}".encode())
            return True
        except (ConnectionRefusedError, socket.timeout, OSError):
            return False

    # ---------- Logika Bully Algorithm (LENGKAPI BAGIAN INI) ----------

    def on_message(self, sender_id: int, msg_type: str):
        """Dipanggil setiap kali node ini menerima pesan dari node lain."""
        # Todo 1: tangani tiga jenis pesan berikut:
        #   - "ELECTION": node lain memulai election. Jika node_id kita LEBIH BESAR
        #     dari sender_id, balas dengan mengirim "OK" ke sender, lalu mulai
        #     election kita sendiri (start_election()) karena kita berpotensi jadi leader.
        #   - "OK": tandai bahwa ada node lebih tinggi yang masih hidup, sehingga
        #     kita TIDAK boleh mendeklarasikan diri sebagai leader.
        #   - "COORDINATOR": simpan sender_id sebagai leader_id yang baru
        
        if msg_type != "PING":
            print(f"[Node {self.node_id}] " f"Menerima pesan '{msg_type}' dari node {sender_id}")
        # todo 1: tangani tiga jenis pesan berikut:
        #   - "ELECTION": node lain memulai election. 
        # Jika menerima ELECTION
        if msg_type == "ELECTION":

             #Jika sudah ada leader, abaikan election lama
            if self.leader_id is not None:
                return
            
            # Jika ID kita lebih besar, balas OK
            if self.node_id > sender_id:

                sender_port = self.peers[sender_id]

                self.send_message(
                    sender_port,
                    "OK"
                )

                print(
                    f"[Node {self.node_id}] "
                    f"Mengirim OK ke node {sender_id}"
                )

                # Mulai election sendiri jika belum berjalan
                with self.lock:
                    already_running = self.election_running

                if not already_running:

                    threading.Thread(
                        target=self.start_election,
                        daemon=True
                    ).start()


        # Jika menerima OK
        elif msg_type == "OK":

            with self.lock:
                self.received_ok = True

            print(
                f"[Node {self.node_id}] "
                "Menerima OK, ada node lebih tinggi"
            )


        # Jika menerima COORDINATOR
        elif msg_type == "COORDINATOR":

            with self.lock:
                self.leader_id = sender_id
                self.election_running = False

            print(
                f"[Node {self.node_id}] "
                f"Leader baru = Node {sender_id}"
            )


        # Jika menerima PING
        elif msg_type == "PING":
            pass
        
    def start_election(self):
        """Dipanggil saat node ini mendeteksi leader tidak ada / tidak merespons."""
        # Todo 2: kirim "ELECTION" ke SEMUA peer dengan id LEBIH BESAR dari node_id kita.
        # Tunggu ELECTION_TIMEOUT detik untuk balasan "OK" (gunakan flag/event yang
        # diset di on_message saat menerima "OK").
        # Jika TIDAK ADA balasan "OK" dalam waktu tersebut -> panggil declare_leader().
        
        # Reset status OK sebelum election dimulai
        with self.lock:
            if self.election_running:
                return
            self.election_running = True
            self.received_ok = False
            self.leader_id = None

        # Ambil node dengan ID lebih tinggi
        higher_peers = {
            pid: port
            for pid, port in self.peers.items()
            if pid > self.node_id
        }

        # Kirim pesan ELECTION
        for pid, port in higher_peers.items():
            self.send_message(port, "ELECTION")

        # Tunggu balasan OK
        time.sleep(ELECTION_TIMEOUT)

        # Cek apakah ada node lebih tinggi
        with self.lock:
            got_ok = self.received_ok

        # Jika tidak ada OK, node ini menjadi leader
        # Jika tidak ada OK, node ini menjadi leader
        if not got_ok:
            with self.lock:
                current_leader = self.leader_id

            # Pastikan belum ada leader baru
            if current_leader is None:
                self.declare_leader()

        else:
            with self.lock:
                self.election_running = False    
                
    def declare_leader(self):
        """Node ini menyatakan dirinya leader dan memberi tahu semua node lain."""
        # Todo 3: set self.leader_id = self.node_id, lalu kirim "COORDINATOR"
        # ke SEMUA peer (bukan cuma yang lebih tinggi).
        # Jadikan diri sendiri leader
        with self.lock:
            self.leader_id = self.node_id
            self.election_running = False

        # Broadcast COORDINATOR ke semua node
        for pid, port in self.peers.items():
            self.send_message(port, "COORDINATOR")
            
    def monitor_leader(self):
        """Loop periodik: cek apakah leader masih hidup, trigger election jika mati."""
        while True:
            time.sleep(3)
            # Todo 4: jika self.leader_id sudah diketahui, coba ping node tsb
            # (mis. kirim pesan "PING" atau cukup coba connect). Jika gagal
            # (leader mati) dan node ini belum tahu leader baru, panggil
            # start_election().
            # Jika sudah ada leader
            if self.leader_id is not None and self.leader_id != self.node_id:
                # Ambil port leader
                leader_port = self.peers.get(self.leader_id)

                # Coba koneksi ke leader
                alive = self.send_message(
                    leader_port,
                    "PING"
                )

                # Jika leader mati
                if not alive:

                    print(
                        f"[Node {self.node_id}] "
                        "Leader mati, mulai election"
                    )

                    with self.lock:
                        self.leader_id = None


                    threading.Thread(
                        target=self.start_election,
                        daemon=True
                    ).start()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--peers", type=str, required=True,
                         help="daftar port peer dipisah koma, mis. 5002,5003,5004,5005")
    args = parser.parse_args()

    # Asumsi konvensi port: id N selalu di port 5000+N (lihat contoh perintah di README).
    peer_ports = [int(p) for p in args.peers.split(",")]
    peers = {port - 5000: port for port in peer_ports}

    node = Node(args.id, args.port, peers)

    threading.Thread(target=node.start_server, daemon=True).start()
    threading.Thread(target=node.monitor_leader, daemon=True).start()

    time.sleep(1)  # beri waktu semua node lain start dulu sebelum election awal
    node.start_election()

    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
