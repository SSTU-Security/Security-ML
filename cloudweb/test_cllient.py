# Sender Code
import cv2
import socket
import pickle
import struct
import requests

def receive_video():
    # Create a socket connection
    data = requests.post("http://localhost:8000/giveSocket").json()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(data)
    server_socket.bind(("localhost", 8083))  # Use your desired IP and port
    server_socket.listen(5)
    requests.post("http://localhost:8000/update", json={"ip":"localhost", "port":8083}).json()
    print("Server listening...")

    # Accept a connection from a client
    connection, addr = server_socket.accept()

    print(f"Connection from {addr}")

    data = b""
    payload_size = struct.calcsize("Q")

    while True:
        while len(data) < payload_size:
            packet = connection.recv(4 * 1024)  # 4K buffer size
            if not packet:
                break
            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += connection.recv(4 * 1024)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Deserialize the frame
        frame = pickle.loads(frame_data)

        # Display the received frame (optional)
        cv2.imshow('Receiver', frame)
        cv2.waitKey(1)


if __name__ == "__main__":
    # Start sender and receiver in separate threads or processes
    import threading

    receiver_thread = threading.Thread(target=receive_video)

    receiver_thread.start()
