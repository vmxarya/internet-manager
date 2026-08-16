# Internet Manager

A Python-based smart multi-WAN failover manager designed to improve internet reliability by monitoring multiple connections and automatically switching between them when needed.

**Now with Windows support!** 🎉

## Overview

Internet Manager helps manage multiple ISP connections using a smart failover strategy.

The main goal is not only keeping the internet online, but improving real browser usage by detecting connection problems and choosing the better available route.

## Current Features (v0.1.0)

- Monitor multiple internet connections
- Detect network interfaces and gateways
- Internet quality testing
- Quality scoring system
- Automatic ISP failover decision logic
- Automatic return to primary connection
- Route switching support
- **Cross-platform support (Linux & Windows)**
- Basic API foundation

## Quick Start

### Linux

```bash
git clone https://github.com/vmxarya/internet-manager.git
cd internet-manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Windows

```bash
git clone https://github.com/vmxarya/internet-manager.git
cd internet-manager
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Note:** For Windows route switching, run with Administrator privileges. See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for detailed setup.

## Platform Support

### Linux
- Full support for interface-specific routing
- Uses `ip route` for route management
- Interface-specific ping testing

### Windows
- Full support for multi-WAN failover
- Uses `netsh` for route management
- Quality testing via default gateway
- Requires Administrator privileges for route switching

See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for Windows-specific configuration and troubleshooting.

## Configuration

Edit `main.py` to configure your connections:

### Linux Configuration
```python
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
```

### Windows Configuration
```python
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
```

## Current Architecture

```
Internet Manager
│
├── Core Engine (Python)
│   ├── Network detection (cross-platform)
│   ├── Quality monitoring
│   ├── Decision engine
│   └── Router control (platform-specific)
│
├── Platform Adapters
│   ├── Linux (quality_*.py, router.py, network.py)
│   └── Windows (quality_windows.py, router_windows.py, network_windows.py)
│
├── API
│   └── Status interface
│
└── Dashboard (planned)
```

## Design Goals

- Primary connection: normal daily usage
- Backup connection: instant recovery when the primary connection performs poorly
- Stable browsing experience instead of simple ping-based switching
- Cross-platform support (Linux and Windows)

## Roadmap

- [x] v0.1.0 Prototype (Linux)
- [x] v0.2.0 Windows Support
- [ ] v0.3.0 Web Dashboard
- [ ] v0.4.0 Background Service Mode
- [ ] v0.5.0 Patience / Fast Track Switching Modes
- [ ] v1.0.0 Stable Release

## Development

Built with:

- Python 3.8+
- Cross-platform libraries (psutil, requests)
- Native OS commands (netsh for Windows, ip for Linux)
- Git

## Troubleshooting

### Windows
- See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for detailed Windows troubleshooting
- Ensure running with Administrator privileges
- Verify network adapter names with `ipconfig`

### Linux
- Check network interfaces: `ip link show`
- View routing table: `ip route show`
- Test ping: `ping -I <interface> 8.8.8.8`

## Stop the program

Press `Ctrl + C` to stop.

## License

MIT License (planned)
