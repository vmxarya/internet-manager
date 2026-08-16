# Quick Start Guide

## Windows Quick Start (2 Minutes)

1. **Double-click** `setup_windows.bat` to install dependencies
2. **Edit** `main.py` - Update connection names, gateways, and interface names
3. **Right-click** `run_windows.bat` → **Run as administrator**

Done! The app will start monitoring your connections.

## Linux Quick Start (2 Minutes)

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
nano main.py  # Edit your connections

# Run
python main.py
```

## Finding Your Configuration

### Windows

**Interface names:**
- Open Command Prompt
- Run: `netsh interface show interface`
- Look for "Ethernet", "WiFi", etc.

**Gateway IPs:**
- Run: `ipconfig`
- Look for "Default Gateway" under each adapter

### Linux

**Interface names:**
- Run: `ip link show`
- Look for interface names like `wlx1cbfce2def95`, `enp4s0`

**Gateway IPs:**
- Run: `ip route show`
- Look for default gateway

## Configuration Template

**main.py connections section:**

```python
connections = {
    "Primary": {
        "gateway": "192.168.1.1",
        "interface": "Ethernet"  # or WiFi on Windows, wlx... on Linux
    },
    "Backup": {
        "gateway": "192.168.2.1",
        "interface": "WiFi"
    }
}
```

## Understanding Quality Scores

- **90+** ✅ Excellent
- **70-89** ✅ Good (sufficient)
- **50-69** ⚠️ Acceptable
- **30-49** ⚠️ Poor
- **0-29** ❌ Very Poor

The app switches from Primary to Backup when Primary score < 60 for 3 checks.

## Troubleshooting

### Windows
- **Routes not switching?** Make sure to run `run_windows.bat` as Administrator
- **Network not detected?** Run `test_windows.py` for diagnostics
- See `WINDOWS_SETUP.md` for detailed troubleshooting

### Linux
- **Permission denied?** May need `sudo python main.py`
- **Interfaces not found?** Check interface names with `ip link show`
- See README.md for help

## File Structure

```
internet-manager/
├── main.py                    # Cross-platform entry point
├── platforms.py               # OS detection utilities
├── requirements.txt           # Python dependencies
│
├── core/
│   ├── quality.py            # Quality testing (auto-platform)
│   ├── quality_windows.py    # Windows quality tests
│   ├── router.py             # Route management (auto-platform)
│   ├── router_windows.py     # Windows route control
│   ├── network.py            # Network detection (auto-platform)
│   ├── network_windows.py    # Windows network utilities
│   ├── decision.py           # Failover decision engine
│   └── ...
│
├── Windows Tools/
│   ├── setup_windows.bat      # One-click setup
│   ├── run_windows.bat        # Run with admin check
│   └── test_windows.py        # Diagnostics
│
└── Documentation/
    ├── README.md              # Main documentation
    ├── WINDOWS_SETUP.md       # Windows detailed guide
    ├── WINDOWS_CONFIG.md      # Configuration reference
    └── IMPLEMENTATION.md      # Technical details
```

## Next Steps

1. ✅ Install dependencies (already done)
2. ✅ Configure connections (edit main.py)
3. ✅ Start monitoring (run main.py)
4. 📊 Watch quality scores
5. ⚡ Automatic failover when needed

## More Information

- Full Windows guide: `WINDOWS_SETUP.md`
- Configuration details: `WINDOWS_CONFIG.md`
- Implementation details: `IMPLEMENTATION.md`
- Main README: `README.md`

## Support

Run diagnostics to check everything:

**Windows:**
```bash
python test_windows.py
```

**Linux:**
```bash
python test_router.py
python test_decision.py
```
