#!/usr/bin/env python3
"""
Debug script to test all discovery methods
"""

import subprocess
import sys
import os

def test_ps_discovery():
    """Test PSDiscoveryProtocol directly"""
    print("\n=== Testing PSDiscoveryProtocol ===")
    try:
        from ps_discovery_wrapper import PSDiscoveryWrapper
        wrapper = PSDiscoveryWrapper()
        print(f"PSDiscoveryProtocol available: {wrapper.available}")
        
        if wrapper.available:
            print("Testing PSDiscoveryProtocol capture...")
            devices = wrapper.capture_lldp_cdp(timeout=15)
            print(f"Found {len(devices)} devices")
            for device in devices:
                print(f"  {device}")
        else:
            print("PSDiscoveryProtocol not available")
    except Exception as e:
        print(f"PSDiscoveryProtocol test failed: {e}")

def test_npcap():
    """Test Npcap/Scapy"""
    print("\n=== Testing Npcap/Scapy ===")
    try:
        from scapy.all import conf, get_if_list
        print(f"Scapy use_pcap: {conf.use_pcap}")
        
        interfaces = get_if_list()
        print(f"Found {len(interfaces)} interfaces")
        for iface in interfaces[:3]:  # Show first 3
            print(f"  {iface}")
    except Exception as e:
        print(f"Npcap/Scapy test failed: {e}")

def test_pktmon():
    """Test PKTMON"""
    print("\n=== Testing PKTMON ===")
    try:
        result = subprocess.run(['pktmon', 'help'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("PKTMON available")
            
            # Test component list
            comp_result = subprocess.run(['pktmon', 'comp', 'list'], capture_output=True, text=True, timeout=5)
            if comp_result.returncode == 0:
                print("PKTMON can list components")
                lines = comp_result.stdout.split('\n')
                for line in lines:
                    if 'Ethernet' in line or 'Wi-Fi' in line:
                        print(f"  {line.strip()}")
            else:
                print("PKTMON cannot list components (may need admin)")
        else:
            print("PKTMON not available")
    except Exception as e:
        print(f"PKTMON test failed: {e}")

def test_admin_status():
    """Test admin status"""
    print("\n=== Testing Admin Status ===")
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        print(f"Running as admin: {bool(is_admin)}")
        
        # Test System32 write access
        try:
            test_file = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32', 'test_write.tmp')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            print("Can write to System32: True")
        except:
            print("Can write to System32: False")
    except Exception as e:
        print(f"Admin test failed: {e}")

def main():
    print("=== LDM Discovery Debug ===")
    
    test_admin_status()
    test_ps_discovery()
    test_npcap()
    test_pktmon()
    
    print("\n=== Summary ===")
    print("If PSDiscoveryProtocol shows 'ADMIN_REQUIRED', you need to run as admin")
    print("If no LLDP packets are captured, your network may not be sending LLDP/CDP")

if __name__ == "__main__":
    main()
