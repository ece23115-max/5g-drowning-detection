
# Real-Time Drowning Detection via 5G Edge Computing

## 📌 Project Overview
This project architecture mitigates local network constraints and reduces hardware requirements on endpoint camera sensors by offloading heavy computer vision workflows to a centralized 5G Edge Computing server. The AI pipeline processes high-definition video feeds to detect drowning indicators in real-time with ultra-low latency.

## 🛠️ Tech Stack & Tools
* **Programming Language:** Python
* **Computer Vision / AI:** YOLOv8, OpenCV
* **Networking Simulation:** Mininet, Open vSwitch (OVS), SDN Controller
* **OS & Kernel Routing:** Linux (iptables, NAT MASQUERADE, USB Tethering)

## 🚀 Key Features
* **Edge AI Offloading:** Shifts computational strain away from local capture devices to an edge cloud server.
* **SDN-Driven 5G Topology:** Simulated high-frequency UDP video streaming over a Software-Defined Network core without dropping packets.
* **Firewall & Isolation Bypass:** Configured network address translation (NAT) to safely tunnel past restrictive local firewalls and AP isolation rules.
