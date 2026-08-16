# Windows Configuration Template
# Copy this file and update with your actual values

## Network Interfaces on Windows

# Common Windows interface names:
# - "Ethernet" (wired connection)
# - "WiFi" (wireless connection)
# - "Local Area Connection" (older Windows versions)
# - "Ethernet 2", "WiFi 2" (multiple adapters)

# To find your interface names, run:
# Command Prompt:    netsh interface show interface
# PowerShell:        Get-NetAdapter | Select-Object Name

## Gateway IPs

# To find gateway IPs, run:
# Command Prompt:    ipconfig
# Or look for "Default Gateway" under each adapter

## Configuration Example

```python
# In main.py, update the Windows connections section:

connections = {
    "Primary": {
        "gateway": "192.168.1.1",    # Your primary gateway
        "interface": "Ethernet"        # Your primary adapter name
    },

    "Backup": {
        "gateway": "192.168.2.1",     # Your backup gateway
        "interface": "WiFi"            # Your backup adapter name
    }
}
```

## More than 2 connections?

The current version supports Primary/Backup. For 3+ connections,
modify the engine initialization:

```python
# For 3 connections:
engine = DecisionEngine(
    "Primary",
    "Backup1",
    # Add third connection monitoring manually
)
```

## Firewall Configuration

If you get connection errors, allow Python through Windows Firewall:

1. Windows Security → Firewall & network protection
2. Allow an app through firewall
3. Click "Change settings"
4. Click "Allow another app"
5. Browse and select: venv\Scripts\python.exe
6. Click Open → OK

## Running as Administrator

For route switching to work, run Command Prompt as Administrator:

1. Right-click Command Prompt
2. Select "Run as administrator"
3. Activate venv and run: python main.py

Or use a batch file:

```batch
@echo off
REM Save as run_internet_manager.bat
cd /d "%~dp0"
call venv\Scripts\activate
python main.py
pause
```

Right-click the batch file → Run as administrator

## Monitoring Quality Scores

Output example:

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

Score meanings:
- 90+: Excellent
- 70-89: Good
- 50-69: Acceptable
- 30-49: Poor
- 0-29: Very Poor

## Automatic Switching Thresholds

From decision.py:
- Switches from Primary to Backup when:
  - Primary score < 60 for 3 consecutive checks (patience mode)
  - Backup score >= 70
  
- Returns to Primary when:
  - Primary score >= 80 for 120 seconds (patience mode)

To change these thresholds, modify core/decision.py
