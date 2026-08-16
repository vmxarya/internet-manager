# Windows Setup Guide

## System Requirements

- Windows 10 or later
- Python 3.8 or later
- Administrator privileges (for route switching)
- Two or more network adapters (for multi-WAN setup)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/vmxarya/internet-manager.git
cd internet-manager
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### Required packages

The application requires:

- **psutil** - Cross-platform system and process utilities
- **requests** - HTTP library for website testing

Install via pip:

```bash
pip install psutil requests
```

## Configuration

### Network Interfaces on Windows

Unlike Linux, Windows uses adapter names like "Ethernet", "WiFi", etc.

#### Finding your network adapter names

#### Method 1: Using ipconfig

```bash
ipconfig
```

Look for adapter names like:
- Ethernet
- WiFi
- Ethernet 2
- Local Area Connection

#### Method 2: Using Command Prompt

```bash
netsh interface show interface
```

This will show all interfaces and their status (Connected/Disconnected)

#### Method 3: Using PowerShell

```powershell
Get-NetAdapter | Select-Object Name, InterfaceDescription, Status
```

### Configuring Internet Manager for Windows

Edit `main.py` and update the connections dictionary:

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

Replace:
- `Primary` and `Backup` with your connection names
- `192.168.1.1` and `192.168.2.1` with your actual gateway IPs
- `"Ethernet"` and `"WiFi"` with your actual adapter names

### Finding Gateway IP on Windows

#### Method 1: Using ipconfig

```bash
ipconfig
```

Look for "Default Gateway" under each adapter

#### Method 2: Using route command

```bash
route print
```

The default route (0.0.0.0) shows the gateway

#### Method 3: Using PowerShell

```powershell
Get-NetRoute -DestinationPrefix 0.0.0.0/0 | Select-Object NextHop, InterfaceAlias
```

## Running Internet Manager

### As a regular Python application

```bash
python main.py
```

The application will:
1. Auto-detect Windows platform
2. Load network configuration
3. Start monitoring connections
4. Print quality scores every 10 seconds
5. Switch routes when necessary

### Running with Administrator privileges

For route switching to work, you may need to run with admin:

```bash
# Using Command Prompt as Administrator
python main.py
```

Or create a batch script to run as admin:

**run_as_admin.bat**
```batch
@echo off
python main.py
pause
```

Then right-click → Run as administrator

### As Windows Background Service (Advanced)

To run as a Windows Service, use `nssm` (Non-Sucking Service Manager):

1. Download nssm: https://nssm.cc/download
2. Extract to a folder
3. Open Command Prompt as Administrator:

```bash
cd C:\path\to\nssm\win64
nssm install InternetManager "C:\path\to\venv\Scripts\python.exe" "C:\path\to\main.py"
nssm start InternetManager
```

To view service status:

```bash
nssm status InternetManager
```

To remove:

```bash
nssm remove InternetManager
```

## Monitoring Output

Example output:

```
============================================================
Internet Manager - Platform Detected: Windows
Release: 10.0.19045
============================================================

Configuring for Windows...
Note: Route switching requires Administrator privileges

Monitoring connections: ['Primary', 'Backup']
Check interval: 10 seconds
Press Ctrl+C to stop

Checking internet quality...
Primary: 85
Backup: 72

Current ISP: Primary
```

## Troubleshooting

### Routes won't switch

**Problem**: Routes don't change despite quality differences

**Solutions**:
1. Ensure you're running with Administrator privileges
2. Check gateway IPs are correct with `ipconfig`
3. Verify adapter names match exactly (case-sensitive)
4. Try manually switching with netsh to test permissions:
   ```bash
   netsh interface ip add route 0.0.0.0 mask 0.0.0.0 <gateway>
   ```

### No network connectivity detected

**Problem**: Quality scores show online: false

**Solutions**:
1. Ensure both adapters have internet connectivity
2. Check firewall isn't blocking ping
3. Test connectivity manually: `ping 8.8.8.8`
4. Run as Administrator for network diagnostics

### Module not found errors

**Problem**: `ModuleNotFoundError: No module named 'psutil'`

**Solution**:
```bash
# Ensure virtual environment is activated
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Windows Firewall blocking

**Problem**: Network tests fail even with internet

**Solution**:
Allow Python through Windows Firewall:
1. Windows Security → Firewall & network protection
2. Allow an app through firewall
3. Add Python from your venv folder

## Platform Differences

### Quality Testing

- **Linux**: Pings use interface binding (`-I interface`)
- **Windows**: Pings use default route (interface binding unavailable)

### Route Switching

- **Linux**: Uses `ip route replace` command
- **Windows**: Uses `netsh interface ip` commands

### Network Detection

- **Cross-platform**: psutil handles interface detection
- **Windows-specific**: `netsh` and `ipconfig` for detailed info

## Additional Resources

- [Python psutil documentation](https://psutil.readthedocs.io/)
- [Windows netsh commands](https://docs.microsoft.com/en-us/windows-server/networking/technologies/netsh/netsh)
- [Windows routing guide](https://docs.microsoft.com/en-us/windows-server/networking/technologies/routing/routing-basics)

## Support

For issues specific to Windows support, please check:
1. Administrator privileges
2. Network adapter names and IPs
3. Firewall rules
4. Virtual environment activation
