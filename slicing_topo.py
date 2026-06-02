from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def create_5g_topology():
    # We MUST use TCLink (Traffic Control Link) to allow bandwidth/latency slicing
    net = Mininet(controller=Controller, switch=OVSKernelSwitch, link=TCLink)
    
    info("*** Adding SDN Controller\n")
    net.addController('c0')
    
    info("*** Adding 5G Base Station (Switch)\n")
    # This acts as our gNodeB (cell tower router)
    s1 = net.addSwitch('s1')
    
    info("*** Adding Virtual Hosts (Our 3 Users)\n")
    h1 = net.addHost('h1', ip='10.0.0.1') # User 1: Video Call
    h2 = net.addHost('h2', ip='10.0.0.2') # User 2: Heavy Download
    h3 = net.addHost('h3', ip='10.0.0.3') # User 3: Web Surfing
    
    info("*** Creating Default Network Slices\n")
    # Here we define the initial physical limits of the wires before the AI takes over.
    
    # h1 Slice (URLLC - Video): Max 10 Mbps, STRICT 10ms delay to prevent video lag
    net.addLink(h1, s1, bw=10, delay='10ms', jitter='2ms')
    
    # h2 Slice (eMBB - Download): Massive 50 Mbps pipe, but 50ms delay is fine for files
    net.addLink(h2, s1, bw=50, delay='50ms')
    
    # h3 Slice (mMTC - Web): Tiny 2 Mbps pipe, moderate 30ms delay
    net.addLink(h3, s1, bw=2, delay='30ms')
    
    info("*** Starting the 5G Network Simulation\n")
    net.start()
    
    info("*** Dropping into Mininet CLI...\n")
    CLI(net)
    
    info("*** Stopping Network\n")
    net.stop()

if __name__ == '__main__':
    # This tells Mininet to print what it's doing to the screen
    setLogLevel('info')
    create_5g_topology()
