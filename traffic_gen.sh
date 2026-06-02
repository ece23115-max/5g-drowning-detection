#!/bin/bash
echo "Starting 5G User Traffic Simulation..."

# User 1 (h1): Video Call - UDP traffic, steady 5 Mbps, high packet rate
echo "h1 starting Video Call..."
iperf -u -c 10.0.0.10 -b 5M -t 3600 &

# User 2 (h2): Heavy Download - TCP traffic, maxing out the connection
echo "h2 starting Heavy Download..."
iperf -c 10.0.0.10 -t 3600 &

# User 3 (h3): Web Surfing - Small bursts of traffic
echo "h3 starting Web Surfing..."
while true; do ping -c 1 -s 64 10.0.0.10 > /dev/null; sleep 2; done &

echo "Traffic generation running in background."
