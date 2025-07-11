#RSA_GUI.py

import socket
import struct
import random
import math
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from sympy import isprime

# --- RSA Implementation ---
def random_prime(start, end):
    primes = [n for n in range(start, end + 1) if isprime(n)]
    return random.choice(primes)

def random_e(phi):
    candidates = [i for i in range(3, phi, 2) if math.gcd(i, phi) == 1]
    return random.choice(candidates)

class RSA:
    def __init__(self):
        self.p = random_prime(50, 100)
        self.q = random_prime(50, 100)
        while self.q == self.p:
            self.q = random_prime(50, 100)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = random_e(self.phi)
        self.d = pow(self.e, -1, self.phi)

    def get_public_key(self):
        return self.n, self.e

    def decrypt(self, c):
        return pow(c, self.d, self.n)

# --- GUI Chat Application ---
class ChatApp:
    def __init__(self, master, role):
        self.master = master
        self.role = role
        master.title(f"RSA Chat - {role.title()}")
        master.configure(bg='#2E3440')  # dark background

        # style configurations
        self.btn_style = {'bg': '#88C0D0', 'fg': '#2E3440', 'activebackground': '#81A1C1', 'font': ('Helvetica', 10, 'bold')}
        self.entry_style = {'bg': '#D8DEE9', 'fg': '#2E3440', 'font': ('Helvetica', 10)}
        self.txt_bg = '#3B4252'
        self.txt_fg = '#ECEFF4'

        # Connection frame
        frm = tk.Frame(master, bg='#4C566A')
        frm.pack(padx=10, pady=5, fill='x')
        tk.Label(frm, text="Host:", bg=frm['bg'], fg=self.txt_fg, font=('Helvetica', 10, 'bold')).grid(row=0, column=0)
        self.host_entry = tk.Entry(frm, **self.entry_style)
        self.host_entry.grid(row=0, column=1, padx=5)
        self.host_entry.insert(0, 'localhost')
        tk.Label(frm, text="Port:", bg=frm['bg'], fg=self.txt_fg, font=('Helvetica', 10, 'bold')).grid(row=0, column=2)
        self.port_entry = tk.Entry(frm, width=6, **self.entry_style)
        self.port_entry.grid(row=0, column=3, padx=5)
        self.port_entry.insert(0, '12345')
        self.btn_conn = tk.Button(frm, text="Start Server" if role=='server' else "Connect", command=self.start, **self.btn_style)
        self.btn_conn.grid(row=0, column=4, padx=5)

        # Chat display
        self.txt = ScrolledText(master, state='disabled', width=60, height=20, bg=self.txt_bg, fg=self.txt_fg, font=('Consolas', 10))
        self.txt.pack(padx=10, pady=5)
        # define tags for different speakers
        self.txt.tag_config('me', foreground='#A3BE8C')
        self.txt.tag_config('peer', foreground='#BF616A')
        self.txt.tag_config('log', foreground='#EBCB8B')

        # Message entry
        frm2 = tk.Frame(master, bg='#4C566A')
        frm2.pack(padx=10, pady=5, fill='x')
        self.msg_entry = tk.Entry(frm2, width=50, **self.entry_style)
        self.msg_entry.grid(row=0, column=0, padx=5)
        self.msg_entry.bind('<Return>', lambda e: self.send_message())
        self.btn_send = tk.Button(frm2, text="Send", command=self.send_message, state='disabled', **self.btn_style)
        self.btn_send.grid(row=0, column=1, padx=5)

        # RSA setup
        self.rsa = RSA()
        self.n, self.e = self.rsa.get_public_key()

    def start(self):
        host, port = self.host_entry.get(), int(self.port_entry.get())
        self.sock = socket.socket()
        if self.role == 'server':
            self.sock.bind((host, port)); self.sock.listen(1)
            self.log(f"Server listening on {host}:{port}", 'log')
            conn, _ = self.sock.accept(); self.conn = conn
            self.log("Client connected", 'log')
            # exchange keys
            self.send_public_key(); self.client_n, self.client_e = self.receive_public_key()
        else:
            self.sock.connect((host, port)); self.conn = self.sock
            self.log(f"Connected to server {host}:{port}", 'log')
            server_n, server_e = self.receive_public_key(); self.log(f"Received server key n={server_n}, e={server_e}", 'log')
            self.send_public_key(); self.log(f"Sent client key n={self.n}, e={self.e}", 'log')
            self.client_n, self.client_e = server_n, server_e

        for w in (self.host_entry, self.port_entry, self.btn_conn): w.config(state='disabled')
        self.btn_send.config(state='normal')
        self.terminate = threading.Event()
        threading.Thread(target=self.recv_loop, daemon=True).start()

    def send_public_key(self):
        self.conn.sendall(struct.pack('>II', self.n, self.e))

    def receive_public_key(self):
        data = self.conn.recv(8); return struct.unpack('>II', data)

    def encrypt_message(self, message):
        cts = [pow(ord(ch), self.client_e, self.client_n) for ch in message]
        self.log(f"Encrypted ciphertexts: {cts}", 'log'); return cts

    def decrypt_message(self, cts):
        msg = ''.join(chr(self.rsa.decrypt(c)) for c in cts)
        self.log(f"Decrypted message: {msg}", 'log'); return msg

    def send_message(self):
        msg = self.msg_entry.get().strip();
        if not msg: return
        self.log(f"Me: {msg}", 'me')
        cts = self.encrypt_message(msg)
        self.conn.sendall(struct.pack('>I', len(cts)))
        for c in cts: self.conn.sendall(struct.pack('>I', c))
        self.log("Sent encrypted message", 'log')
        self.msg_entry.delete(0, 'end')
        if msg.lower() == 'quit': self.terminate.set(); self.master.quit()

    def recv_loop(self):
        while not self.terminate.is_set():
            try:
                k_data = self.conn.recv(4)
                if not k_data: break
                k = struct.unpack('>I', k_data)[0]
                cts = [struct.unpack('>I', self.conn.recv(4))[0] for _ in range(k)]
                self.log(f"Received ciphertexts: {cts}", 'log')
                msg = self.decrypt_message(cts)
                self.master.after(0, self.log, f"Peer: {msg}", 'peer')
                if msg.lower() == 'quit': self.terminate.set(); self.master.after(0, self.master.quit)
            except: break

    def log(self, text, tag='log'):
        self.txt.config(state='normal')
        self.txt.insert('end', text + '\n', tag)
        self.txt.config(state='disabled'); self.txt.yview('end')

if __name__ == '__main__':
    role = input("Run as server or client? (s/c): ").lower()
    root = tk.Tk(); app = ChatApp(root, 'server' if role=='s' else 'client'); root.mainloop()
