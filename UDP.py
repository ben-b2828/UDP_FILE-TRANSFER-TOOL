import os
import socket
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

CHUNK_SIZE = 1024
DEFAULT_RECEIVED_DIR = "received_files"

if not os.path.exists(DEFAULT_RECEIVED_DIR):
    os.makedirs(DEFAULT_RECEIVED_DIR)

class UDPFileTransferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UDP File Transfer Tool")


        sender_frame = tk.LabelFrame(root, text="Sender")
        sender_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(sender_frame, text="File:").grid(row=0, column=0, sticky="e")
        self.file_path_var = tk.StringVar()
        tk.Entry(sender_frame, textvariable=self.file_path_var, width=40).grid(row=0, column=1, padx=5)
        tk.Button(sender_frame, text="Browse", command=self.browse_file).grid(row=0, column=2)

        tk.Label(sender_frame, text="Receiver IP:").grid(row=1, column=0, sticky="e")
        self.receiver_ip_var = tk.StringVar()
        tk.Entry(sender_frame, textvariable=self.receiver_ip_var).grid(row=1, column=1, padx=5)

        tk.Label(sender_frame, text="Port:").grid(row=1, column=2, sticky="e")
        self.receiver_port_var = tk.StringVar()
        tk.Entry(sender_frame, textvariable=self.receiver_port_var, width=7).grid(row=1, column=3)

        tk.Button(sender_frame, text="Send File", command=self.send_file).grid(row=2, column=1, pady=5)

        # Receiver Frame
        receiver_frame = tk.LabelFrame(root, text="Receiver")
        receiver_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(receiver_frame, text="Listen Port:").grid(row=0, column=0)
        self.listen_port_var = tk.StringVar()
        tk.Entry(receiver_frame, textvariable=self.listen_port_var, width=7).grid(row=0, column=1)
        tk.Button(receiver_frame, text="Start Listening", command=self.start_receiving_default).grid(row=0, column=2, padx=5)
        tk.Button(receiver_frame, text="Receive File Now", command=self.start_receiving_manual).grid(row=0, column=3, padx=5)

        # Log Output
        self.log = scrolledtext.ScrolledText(root, height=15, width=70)
        self.log.pack(padx=10, pady=5)

    def log_message(self, msg):
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_var.set(file_path)

    def send_file(self):
        try:
            file_path = self.file_path_var.get()
            receiver_ip = self.receiver_ip_var.get()
            receiver_port = int(self.receiver_port_var.get())

            ip_resolved = socket.gethostbyname(receiver_ip)
            self.log_message(f"[INFO] Resolved IP: {ip_resolved}")

            if not os.path.exists(file_path):
                raise FileNotFoundError("File does not exist.")

            file_name = os.path.basename(file_path)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


            try:
                sock.sendto(f"FILENAME:{file_name}".encode(), (ip_resolved, receiver_port))
                time.sleep(0.1)
            except Exception as e:
                raise Exception(f"Failed to send filename: {e}")


            try:
                with open(file_path, "rb") as f:
                    while chunk := f.read(CHUNK_SIZE):
                        sock.sendto(chunk, (ip_resolved, receiver_port))
                        time.sleep(0.01)
            except Exception as e:
                raise Exception(f"Failed to read or send file content: {e}")


            try:
                sock.sendto(b"__END__", (ip_resolved, receiver_port))
            except Exception as e:
                raise Exception(f"Failed to send end marker: {e}")

            self.log_message(f"[SUCCESS] File '{file_name}' sent successfully.")

        except Exception as e:
            self.log_message(f"[ERROR] File send failed: {str(e)}")

    def receive_file(self, port, dest_folder):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(("0.0.0.0", port))
            self.log_message(f"[INFO] Listening on port {port}...")

            file_data = []
            file_name = None
            sock.settimeout(10)

            while True:
                try:
                    data, addr = sock.recvfrom(CHUNK_SIZE + 100)
                except socket.timeout:
                    raise TimeoutError("Receiving timed out. No data received.")
                except Exception as e:
                    raise Exception(f"Error receiving data: {e}")

                if data == b"__END__":
                    break
                elif data.startswith(b"FILENAME:"):
                    try:
                        file_name = data.decode().split("FILENAME:")[1]
                        self.log_message(f"[INFO] Receiving file: {file_name} from {addr}")
                    except UnicodeDecodeError:
                        raise ValueError("Filename decoding failed.")
                else:
                    file_data.append(data)

            if not file_name:
                raise Exception("Filename not received properly.")
            if not file_data:
                raise Exception("No file data received.")

            os.makedirs(dest_folder, exist_ok=True)
            full_path = os.path.join(dest_folder, f"received_{file_name}")

            try:
                with open(full_path, "wb") as f:
                    for chunk in file_data:
                        f.write(chunk)
            except Exception as e:
                raise Exception(f"Error saving received file: {e}")

            self.log_message(f"[SUCCESS] File saved to '{full_path}'.")

        except Exception as e:
            self.log_message(f"[ERROR] File receive failed: {str(e)}")

    def start_receiving_default(self):
        try:
            port = int(self.listen_port_var.get())
            threading.Thread(target=self.receive_file, args=(port, DEFAULT_RECEIVED_DIR), daemon=True).start()
        except Exception as e:
            self.log_message(f"[ERROR] {str(e)}")

    def start_receiving_manual(self):
        try:
            port = int(self.listen_port_var.get())
            dest_folder = filedialog.askdirectory(title="Select folder to save received file")
            if dest_folder:
                threading.Thread(target=self.receive_file, args=(port, dest_folder), daemon=True).start()
            else:
                self.log_message("[INFO] No folder selected. Operation cancelled.")
        except Exception as e:
            self.log_message(f"[ERROR] {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UDPFileTransferApp(root)
    root.mainloop()
