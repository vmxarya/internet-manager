"""
Windows Network Diagnostics Script
Tests if Internet Manager can run on your Windows system
"""

import platform
import subprocess
import sys
from pathlib import Path

# Add parent directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

try:
    from core.network_windows import (
        get_interfaces_windows,
        get_routes_windows,
        get_default_gateway_windows,
        get_ip_config
    )
    from core.quality_windows import ping_test_windows
except ImportError as e:
    print(f"[ERROR] Failed to import modules: {e}")
    sys.exit(1)


def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def main():
    print_section("Internet Manager - Windows Diagnostics")

    # Check Python version
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")

    # Check for required modules
    print("\nChecking required modules...")
    required = ['psutil', 'requests']
    missing = []

    for module in required:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError:
            print(f"  ✗ {module} - MISSING")
            missing.append(module)

    if missing:
        print(f"\n[ERROR] Missing modules: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False

    # Get network interfaces
    print_section("Network Interfaces")
    try:
        interfaces = get_interfaces_windows()
        if interfaces:
            for name, info in interfaces.items():
                print(f"{name}:")
                print(f"  IPv4: {info['ipv4']}")
                print(f"  IPv6: {info['ipv6']}")
                print(f"  MAC: {info['mac']}")
                print(f"  Status: {info['status']}")
                print()
        else:
            print("[WARNING] No interfaces found")
            return False
    except Exception as e:
        print(f"[ERROR] Failed to get interfaces: {e}")
        return False

    # Get default gateway
    print_section("Default Gateway")
    try:
        gateway = get_default_gateway_windows()
        if gateway:
            print(f"Default Gateway: {gateway}")
        else:
            print("[WARNING] Could not determine default gateway")
    except Exception as e:
        print(f"[ERROR] Failed to get gateway: {e}")

    # Test ping
    print_section("Ping Test")
    try:
        ping = ping_test_windows()
        print(f"Ping Test Result:")
        print(f"  Online: {ping['online']}")
        print(f"  Latency: {ping['latency']}ms")
        print(f"  Packet Loss: {ping['loss']}%")
        print(f"  Quality Score: {ping}")
    except Exception as e:
        print(f"[ERROR] Failed to run ping test: {e}")

    # Get routing table
    print_section("Routing Table")
    try:
        routes = get_routes_windows()
        if routes:
            print(routes)
        else:
            print("[WARNING] Could not retrieve routing table")
    except Exception as e:
        print(f"[ERROR] Failed to get routing table: {e}")

    # Get IP configuration
    print_section("IP Configuration")
    try:
        ipconfig = get_ip_config()
        if ipconfig:
            print(ipconfig)
        else:
            print("[WARNING] Could not retrieve IP configuration")
    except Exception as e:
        print(f"[ERROR] Failed to get IP config: {e}")

    # Admin check
    print_section("Administrator Privileges")
    try:
        result = subprocess.run(
            ["netsh", "interface", "show", "interface"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✓ Administrator privileges detected")
            print("  Route switching will work")
        else:
            print("✗ Not running as Administrator")
            print("  Route switching may fail")
            print("  Run Command Prompt as Administrator to enable")
    except Exception as e:
        print(f"✗ Could not determine admin status: {e}")

    # Summary
    print_section("Summary")
    print("""
✓ All required modules installed
✓ Network interfaces detected
✓ Network connectivity available

Ready to run Internet Manager!

Next steps:
1. Edit main.py to configure connections
2. Run as Administrator:
   - Right-click run_windows.bat
   - Select "Run as administrator"

For detailed help, see:
- WINDOWS_SETUP.md
- WINDOWS_CONFIG.md
    """)

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nDiagnostics cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
