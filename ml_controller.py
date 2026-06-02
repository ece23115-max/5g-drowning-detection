import time
import os
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# The Mininet interfaces connected to our 3 users
INTERFACES = ['s1-eth1', 's1-eth2', 's1-eth3']

def get_traffic_stats(iface):
    """Reads raw bytes and packets directly from the Linux kernel."""
    try:
        with open(f"/sys/class/net/{iface}/statistics/rx_bytes", "r") as f:
            bytes_rx = int(f.read())
        with open(f"/sys/class/net/{iface}/statistics/rx_packets", "r") as f:
            pkts_rx = int(f.read())
        return bytes_rx, pkts_rx
    except FileNotFoundError:
        return 0, 0

def apply_network_slice(iface, slice_type):
    """Uses Linux Traffic Control (tc) to change bandwidth and latency."""
    if slice_type == "eMBB":
        # Heavy Download: 50 Mbps, 50ms delay
        os.system(f"tc qdisc replace dev {iface} root netem delay 50ms rate 50Mbit")
        print(f"[{iface}] Assigned eMBB Slice (50Mbps, 50ms)")
    elif slice_type == "URLLC":
        # Video Call: 10 Mbps, 10ms strict delay
        os.system(f"tc qdisc replace dev {iface} root netem delay 10ms rate 10Mbit")
        print(f"[{iface}] Assigned URLLC Slice (10Mbps, 10ms)")
    elif slice_type == "mMTC":
        # Web Surfing: 2 Mbps, 30ms delay
        os.system(f"tc qdisc replace dev {iface} root netem delay 30ms rate 2Mbit")
        print(f"[{iface}] Assigned mMTC Slice (2Mbps, 30ms)")

def run_ml_controller():
    print("🚀 Starting AI Network Slicing Controller...")
    scaler = StandardScaler()
    
    # Store previous stats to calculate per-second rates
    prev_stats = {iface: get_traffic_stats(iface) for iface in INTERFACES}
    
    while True:
        time.sleep(3) # Analyze traffic every 3 seconds
        
        live_data = []
        for iface in INTERFACES:
            curr_bytes, curr_pkts = get_traffic_stats(iface)
            prev_bytes, prev_pkts = prev_stats[iface]
            
            # Calculate Rate (Bytes/sec and Packets/sec)
            bytes_per_sec = (curr_bytes - prev_bytes) / 3
            pkts_per_sec = (curr_pkts - prev_pkts) / 3
            
            live_data.append([bytes_per_sec, pkts_per_sec])
            prev_stats[iface] = (curr_bytes, curr_pkts)
            
        X = np.array(live_data)
        X = np.array(live_data)

        # --- ADD THIS X-RAY VISION PRINT ---
        print(f"\nLive Data Matrix (Bytes/s, Packets/s):")
        print(f"h1 (eth1): {X[0]}")
        print(f"h2 (eth2): {X[1]}")
        print(f"h3 (eth3): {X[2]}")
        # -----------------------------------
        
        # If no traffic is flowing yet, skip ML processing
        if np.sum(X) == 0:
            continue
            
        print("\n--- Running K-Means Clustering ---")
        # 1. Scale the data (Crucial for K-Means distance geometry)
        X_scaled = scaler.fit_transform(X)
        
        # 2. Run K-Means
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        
        # 3. Analyze the Centroids to map Clusters to 5G Slices
        centroids = kmeans.cluster_centers_
        labels = kmeans.labels_
        
        # We find which cluster ID represents which traffic type based on max values
        # Column 0 is Bytes (Bandwidth), Column 1 is Packets (Frequency)
        embb_cluster = np.argmax(centroids[:, 0]) # Highest Bytes = Downloader
        urllc_cluster = np.argmax(centroids[:, 1]) # Highest Packets = Video Call
        
        # The remaining cluster is mMTC (Web Surfing)
        mmtc_cluster = list(set([0, 1, 2]) - {embb_cluster, urllc_cluster})[0]

        # 4. Apply the routing rules dynamically
        for i, iface in enumerate(INTERFACES):
            if labels[i] == embb_cluster:
                apply_network_slice(iface, "eMBB")
            elif labels[i] == urllc_cluster:
                apply_network_slice(iface, "URLLC")
            elif labels[i] == mmtc_cluster:
                apply_network_slice(iface, "mMTC")

if __name__ == "__main__":
    run_ml_controller()
