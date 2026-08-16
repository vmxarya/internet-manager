import time
import platform

from core.decision import DecisionEngine
from core.router import RouterController
from core.quality import check_quality
from platforms import get_os_info, is_windows

# Detect platform and set configuration
os_info = get_os_info()
print(f"\n{'='*60}")
print(f"Internet Manager - Platform Detected: {os_info['system']}")
print(f"Release: {os_info['release']}")
print(f"{'='*60}\n")

if is_windows():
    print("Configuring for Windows...")
    print("Note: Route switching requires Administrator privileges\n")
    
    connections = {

        "Primary": {
            "gateway": "192.168.1.1",
            "interface": "Ethernet"
        },

        "Backup": {
            "gateway": "192.168.2.1",
            "interface": "WiFi"
        }

    }

else:
    print("Configuring for Linux...\n")
    
    connections = {

        "TCI": {
            "gateway": "192.168.1.1",
            "interface": "wlx1cbfce2def95"
        },


        "Irancell": {
            "gateway": "192.168.2.1",
            "interface": "enp4s0"
        }

    }

# Get connection names
conn_names = list(connections.keys())

engine = DecisionEngine(
    conn_names[0],
    conn_names[1]
)


router = RouterController(connections)

print(f"Monitoring connections: {conn_names}")
print("Check interval: 10 seconds")
print("Press Ctrl+C to stop\n")

try:
    while True:

        print("\nChecking internet quality...")

        # Get quality scores for each connection
        scores = {}
        
        for connection_name in conn_names:
            if is_windows():
                score = check_quality()
            else:
                interface = connections[connection_name]["interface"]
                score = check_quality(interface)
            
            scores[connection_name] = score

        # Decide which connection to use
        active = engine.decide(scores)

        print(
            f"Current ISP: {active}"
        )

        time.sleep(10)

except KeyboardInterrupt:
    print("\n\nShutting down Internet Manager...")
    print("Goodbye!")
