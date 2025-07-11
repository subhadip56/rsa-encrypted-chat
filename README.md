# 💬 RSA Encrypted Chat

A Python client-server chat application secured with 🔐 RSA encryption and a 🖥️ Tkinter GUI. This project was built to explore the fundamentals of cryptography and socket programming through an interactive, GUI-based chat interface.

---

## 🖥️ Overview

**RSA Encrypted Chat** allows two users to communicate over a secure channel using RSA public-key encryption. It features a clean Tkinter interface for ease of use and a single-threaded client-server architecture that handles encrypted message exchange in real-time.

Messages are encrypted using the recipient's public key and decrypted using the private key of the receiver, ensuring confidentiality and integrity throughout the chat session.

---

## ✨ Features

* 🔐 End-to-End RSA Public-Key Encryption
* 🖥️ Intuitive Tkinter GUI with dark theme
* 🌐 Socket Communication over TCP/IP
* 🧵 Threaded message receiver to keep UI responsive
* 🧩 Key exchange happens automatically on connect
* 🟢 Color-coded message log (Me / Peer / System)
* 🔚 Graceful shutdown with "quit" command

---

## 📦 Prerequisites

* Python 3.8 or higher
* Install required package:

```bash
pip install sympy
```

No other external dependencies are needed — GUI and networking use Python’s standard libraries.

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/subhadip56/rsa-encrypted-chat.git
cd rsa-encrypted-chat
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install sympy
```

---

## 🔧 Configuration

Before starting:

* **Host**: Default is `localhost`
* **Port**: Default is `12345`

Both can be modified in the GUI before you start the connection.

---

## 🚀 Usage

### Run as Server

```bash
python RSA_GUI.py
```

* Input `s` when prompted.
* In the GUI, click **Start Server**.
* Wait for a client to connect.

### Run as Client

```bash
python RSA_GUI.py
```

* Input `c` when prompted.
* Enter the server's host and port.
* Click **Connect**.

Once connected, the public keys are exchanged automatically, and you can start chatting securely!

> 💡 Type `quit` to end the session and close the app.

---

## 🏗️ Architecture & Design

### 🔑 RSA Module

* Generates 2 random primes `p` and `q`
* Computes public and private keys
* Encrypts each character as: `c = (ord(m)^e) % n`
* Decrypts: `m = (c^d) % n`

### 🌐 Socket Layer

* Server listens for a single connection
* Client initiates connection to server
* Messages are sent as:

  * 4-byte header (message length)
  * Series of encrypted 4-byte integers
* A background thread handles receiving

### 🎨 GUI (Tkinter)

* Connection section (host, port, connect/start)
* Scrollable text area for chat
* Input field and send button
* Color-coded messages:

  * Green: Sent by you
  * Red: Received from peer
  * Yellow: System log

---

## 🧐 Code Highlights

### `RSA` class

* `__init__()`: Generates keys
* `get_public_key()`: Returns `(n, e)`
* `decrypt(c)`: Performs decryption

### `ChatApp` class

* Handles the GUI, sockets, and messaging
* `start()`: Initializes role and key exchange
* `send_message()`: Encrypts and sends messages
* `recv_loop()`: Background listener for incoming messages

---

## 📜 Logging & Message Flow

* System events (like key exchange, connection info) are logged with the `log` tag.
* Sent messages are marked as `me` (green), received messages as `peer` (red).
* Logs auto-scroll as chat progresses.

---

## 🔄 Extending the Project

* 🔁 Add support for multiple clients (via threading on server)
* 🖼️ Add file/image transfer with encryption
* 🔒 Increase key size range for more secure RSA
* 🎨 Apply theming libraries like `ttkbootstrap` for advanced UI

---

## 🛠️ Troubleshooting

* ❌ **`ModuleNotFoundError: No module named 'sympy'`**

  * Run `pip install sympy`

* ❌ **`Connection refused`**

  * Ensure the server is running and the host/port are correct

* ❌ **App freezes after connection**

  * Ensure `recv_loop()` is running in a separate thread

---


## 👨‍💻 Author

**Subhadip Malakar**
🔗 GitHub: [subhadip56](https://github.com/subhadip56)
📧 Email: [subhadipmalakar98@gmail.com]

---



