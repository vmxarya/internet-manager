# Internet Manager

A Python-based smart multi-WAN failover manager designed to improve internet reliability by monitoring multiple connections and automatically switching between them when needed.

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
- Basic API foundation

## Run

Clone the repository:

```bash
git clone https://github.com/vmxarya/internet-manager.git
cd internet-manager
```

Create and activate the virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Run Internet Manager:

```bash
python main.py
```

Stop the program with:

```text
Ctrl + C
```

## Current Architecture

```
Internet Manager
│
├── Core Engine (Python)
│   ├── Network detection
│   ├── Quality monitoring
│   ├── Decision engine
│   └── Router control
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
- Cross-platform support (Linux first, Windows planned)

## Roadmap

- [x] v0.1.0 Prototype
- [ ] v0.2.0 Web Dashboard
- [ ] v0.3.0 Background Service Mode
- [ ] v0.4.0 Windows Support
- [ ] v0.5.0 Patience / Fast Track Switching Modes
- [ ] v1.0.0 Stable Release

## Development

Built with:

- Python
- Linux networking tools
- Git

## License

MIT License (planned)
