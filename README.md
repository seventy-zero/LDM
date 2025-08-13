# Network Port Discovery Tool

A professional GUI application for detecting LLDP (Link Layer Discovery Protocol) and CDP (Cisco Discovery Protocol) packets to identify network switch ports and device information.

## Features

- **Dual Protocol Support**: Detects both LLDP and CDP packets
- **Professional GUI**: Modern dark-themed interface using CustomTkinter
- **Real-time Discovery**: Live packet capture and analysis
- **Detailed Information**: Extracts switch names, port IDs, descriptions, and system information
- **Thread-safe**: Non-blocking GUI with background packet processing
- **Easy to Use**: Simple one-click operation with clear status indicators

## What It Does

This tool listens for network discovery packets that switches automatically send out. When you plug your computer into a network port, the switch sends LLDP or CDP packets containing information about:

- **Switch/Device Name**: The name of the network device
- **Port ID**: Which specific port you're connected to
- **Port Description**: Human-readable description of the port
- **System Description**: Additional device information
- **Platform Information**: Device model and capabilities (CDP)

## Installation

### Option 1: Run from Source (Recommended for Development)

1. **Install Python 3.8+** if not already installed
2. **Clone or download** this repository
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application**:
   ```bash
   python network_discovery_tool.py
   ```

### Option 2: Build Executable

1. **Install build dependencies**:
   ```bash
   pip install pyinstaller
   ```
2. **Run the build script**:
   ```bash
   python build_exe.py
   ```
3. **Find the executable** in the `dist/` folder
4. **Run as administrator** for packet capture permissions

### Option 3: Use the Installer

1. **Run the build script** to create the installer
2. **Right-click** `install.bat` and select "Run as administrator"
3. **Follow the installation prompts**
4. **Use the desktop shortcut** to launch the tool

## Usage

### Basic Operation

1. **Launch the application** (as administrator)
2. **Select protocols** to monitor (LLDP and/or CDP)
3. **Click "Start Discovery"** to begin listening
4. **Plug in your network cable** or wait for existing traffic
5. **View results** in the text area
6. **Click "Stop Discovery"** when finished

### Understanding the Results

#### LLDP Packet Information:
```
[14:30:25] LLDP Packet Detected:
  Switch Name: SW-CORE-01
  Port ID: GigabitEthernet1/0/24
  Port Description: Conference Room A
  System Description: Cisco Catalyst 3850-24T
--------------------------------------------------
```

#### CDP Packet Information:
```
[14:30:25] CDP Packet Detected:
  Device ID: SW-CORE-01.company.local
  Port ID: GigabitEthernet1/0/24
  Platform: c3850-24T
  Capabilities: Router Switch IGMP
--------------------------------------------------
```

## Technical Details

### How It Works

1. **Packet Capture**: Uses Scapy library to capture raw Ethernet frames
2. **Protocol Filtering**: Filters for specific multicast MAC addresses:
   - LLDP: `01:80:c2:00:00:0e`
   - CDP: `01:00:0c:cc:cc:cc`
3. **Packet Parsing**: Extracts TLV (Type-Length-Value) data from packets
4. **GUI Updates**: Thread-safe updates to display results in real-time

### Network Requirements

- **Administrator Privileges**: Required for packet capture
- **Network Access**: Must be connected to a network with LLDP/CDP enabled
- **Switch Configuration**: Switches must have LLDP or CDP enabled

### Supported Protocols

#### LLDP (IEEE 802.1AB)
- **Standard**: IEEE 802.1AB
- **MAC Address**: 01:80:c2:00:00:0e
- **Vendor Support**: Most enterprise switches (Cisco, HP, Juniper, etc.)

#### CDP (Cisco Discovery Protocol)
- **Vendor**: Cisco Systems
- **MAC Address**: 01:00:0c:cc:cc:cc
- **Support**: Cisco devices and some compatible switches

## Troubleshooting

### Common Issues

**"No packets detected"**
- Ensure you're running as administrator
- Check that LLDP/CDP is enabled on the switch
- Try connecting to different network ports
- Verify network connectivity

**"Permission denied"**
- Right-click the executable and select "Run as administrator"
- Ensure Windows Defender or antivirus isn't blocking the application

**"Application crashes"**
- Check that all dependencies are installed correctly
- Ensure you have Python 3.8+ installed
- Try running from source instead of executable

### Network Configuration

**Enable LLDP on Cisco switches:**
```cisco
configure terminal
lldp run
interface GigabitEthernet1/0/24
 lldp transmit
 lldp receive
end
```

**Enable CDP on Cisco switches:**
```cisco
configure terminal
cdp run
interface GigabitEthernet1/0/24
 cdp enable
end
```

## Development

### Project Structure
```
├── network_discovery_tool.py    # Main application
├── build_exe.py                 # Build script for executable
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── install.bat                  # Installer script (generated)
```

### Key Components

- **NetworkDiscoveryTool**: Main GUI class
- **Packet Processing**: LLDP and CDP packet parsing functions
- **Threading**: Background packet capture with GUI responsiveness
- **Error Handling**: Comprehensive exception handling and user feedback

### Customization

You can easily extend the tool to:
- Add support for other discovery protocols
- Implement packet logging to files
- Add network interface selection
- Create custom packet filters
- Export results to different formats

## Security Considerations

- **Administrator Access**: Required for packet capture
- **Network Visibility**: Can see network topology information
- **No Data Transmission**: Tool only receives packets, doesn't send any
- **Local Use**: Designed for local network administration

## License

This project is provided as-is for educational and network administration purposes. Use responsibly and in accordance with your organization's network policies.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the tool. When contributing:

1. Test your changes thoroughly
2. Maintain the existing code style
3. Update documentation as needed
4. Ensure compatibility with existing functionality

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the technical details
3. Ensure you have the latest version
4. Test with different network configurations

---

**Note**: This tool is designed for network administrators and IT professionals. Always ensure you have proper authorization before monitoring network traffic in your organization. 