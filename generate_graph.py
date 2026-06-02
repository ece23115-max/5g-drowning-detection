import matplotlib.pyplot as plt

# Your Project Data
labels = ['5G Edge Computing (Local)', 'Traditional Cloud (Remote)']
latencies = [93.0, 1035.9] # Milliseconds
colors = ['#2ca02c', '#d62728'] # Green for Edge, Red for Cloud

# Create the Bar Chart
plt.figure(figsize=(8, 6))
bars = plt.bar(labels, latencies, color=colors, width=0.5)

# Add Titles and Labels
plt.title('Autonomous Drone Dispatch: Edge vs. Cloud Latency', fontsize=14, fontweight='bold')
plt.ylabel('Total Action Round-Trip Latency (ms)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add the exact millisecond numbers on top of the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 5, f"{yval} ms", ha='center', fontsize=12, fontweight='bold')

# Save the graph as an image file
plt.savefig('latency_comparison_graph.png', dpi=300, bbox_inches='tight')
print("Graph successfully saved as 'latency_comparison_graph.png'")
