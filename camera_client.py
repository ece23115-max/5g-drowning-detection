import cv2
import socket
import struct
import pickle
import time

# --- PURE WIRELESS HTTP STREAM ---
PHONE_CAMERA_URL = "http://172.31.181.147:8080/video" 
# ---------------------------------

def start_camera(server_ip='192.168.50.2', port=9999):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Connecting to Edge Server at {server_ip}...")
    client_socket.connect((server_ip, port))
    
    print(f"Grabbing Live Video from {PHONE_CAMERA_URL}...")
    vid = cv2.VideoCapture(PHONE_CAMERA_URL)
    vid.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not vid.isOpened():
        print("❌ ERROR: Could not connect to phone! Check the IP address.")
        return

    while vid.isOpened():
        # Buffer drain
        for _ in range(4): 
            vid.grab() 
        
        ret, frame = vid.read()
        if not ret: break

        # Send to AI Server
        frame_resized = cv2.resize(frame, (640, 480))
        a = pickle.dumps(frame_resized)
        message = struct.pack("Q", len(a)) + a

        send_time = time.time()
        client_socket.settimeout(None)
        client_socket.sendall(message)

        # Wait for Alarm
        client_socket.settimeout(2.0) 
        try:
            response = client_socket.recv(1024).decode('utf-8')
            if "DISPATCH_DRONE" in response:
                total_rtt = (time.time() - send_time) * 1000 
                print(f"🚨 ALARM! {response} | Total Latency: {total_rtt:.2f} ms")
        except socket.timeout:
            pass 
            
        time.sleep(0.03)

    vid.release()
    client_socket.close()

if __name__ == "__main__":
    start_camera()
