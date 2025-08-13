# LDM - Link Discovery Manager

Ever wanted to know what switch port you're plugged into? This tool does exactly that - it's basically a software version of a NetAlly LinkRunner AT, but free and runs on Windows.

## What This Does

When you plug your computer into a network port, switches automatically send out discovery packets (LLDP or CDP) that tell you:
- **Switch Name** - What switch you're connected to
- **Port ID** - Which specific port (like "GigabitEthernet1/0/24")
- **Port Description** - Human readable description (like "Conference Room A")
- **System Description** - Switch model and info

This tool sniffs those packets and shows you the info in a clean GUI. No more guessing which port is which!

## Quick Start

### Option 1: Just Run It (Easiest)
1. Download the `LDM.exe` from the releases
2. Right-click → "Run as administrator"
3. Click "Start Discovery" and plug in your network cable
4. Watch the magic happen

### Option 2: Build It Yourself
```bash
pip install -r requirements.txt
python build_exe.py
```
The exe will be in the `dist/` folder.

### Option 3: Run from Source
```bash
pip install -r requirements.txt
python network_discovery_tool.py
```

## How to Use

1. **Run as administrator** (required for packet capture)
2. **Select protocols** - LLDP and CDP are both good to have
3. **Click "Start Discovery"**
4. **Plug in your network cable** or wait for existing traffic
5. **Watch the results** - switch info appears at the top, detailed logs below
6. **Use the blinking feature** - makes the switch port LED blink so you can find it physically

## What You'll See

The GUI shows you the discovered info in nice fields at the top:
- **Device Name** - Your computer's name
- **Switch Name** - The switch you're connected to
- **Port ID** - The specific port
- **Port Description** - What that port is labeled as
- **System Description** - Switch model and details

Plus a detailed log below showing all the raw packet data.

## Troubleshooting

**"No packets detected"**
- Make sure you're running as administrator
- Check that LLDP/CDP is enabled on the switch (most enterprise switches have it on by default)
- Try a different network port
- Some switches only send packets when they detect a device

**"Permission denied"**
- Right-click → "Run as administrator"
- Windows Defender might be blocking it - add an exception

**"Application crashes"**
- Make sure you have Python 3.8+ if running from source
- Try the pre-built exe instead

## Technical Stuff

### How It Works
- Uses Scapy to capture raw Ethernet frames
- Looks for LLDP packets (MAC: 01:80:c2:00:00:0e) and CDP packets (MAC: 01:00:0c:cc:cc:cc)
- Parses the TLV data to extract switch info
- Updates the GUI in real-time

### Requirements
- **Windows** (tested on Windows 10/11)
- **Administrator privileges** (for packet capture)
- **Npcap** - download from npcap.com if you get WinPcap errors
- **Network with LLDP/CDP enabled** (most enterprise networks)

### Protocols Supported
- **LLDP** - IEEE standard, works on most switches (Cisco, HP, Juniper, etc.)
- **CDP** - Cisco's protocol, works on Cisco devices

## Why I Built This

NetAlly was too expensive to buy for what I was doing

## Files

- `network_discovery_tool.py` - Main application
- `build_exe.py` - Script to build the exe
- `requirements.txt` - Python packages needed
- `LDM.exe` - The actual tool (in dist/ folder after building)

## Security Note

This tool only **receives** packets - it doesn't send anything. It's completely passive and safe to use on any network. You're just listening to what the switch is already broadcasting.

## License

Use it however you want. It's just a network tool for figuring out which port you're plugged into.

---

**Pro tip**: The blinking feature is super useful for finding the actual physical port on the switch. Start blinking, then go look for the flashing LED! 