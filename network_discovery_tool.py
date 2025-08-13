import threading
import time
import socket
import struct
from datetime import datetime
import customtkinter as ctk
from scapy.all import *
import tkinter as tk
from tkinter import messagebox
import pyperclip

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class NetworkDiscoveryTool(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Link Discovery Manager")
        self.geometry("800x600")
        self.minsize(600, 400)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.is_sniffing = False
        self.sniff_thread = None
        self.discovered_devices = []
        self.packet_count = 0
        self.is_blinking = False
        self.blink_thread = None
        
        self.current_device = {
            'device_name': socket.gethostname(),
            'switch_name': 'Unknown',
            'port_id': 'Unknown',
            'port_description': 'Unknown',
            'system_description': 'Unknown'
        }
        
        self.create_widgets()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Link Discovery Manager", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(15, 8))
        
        subtitle_label = ctk.CTkLabel(
            main_frame, 
            text="Professional Network Port Discovery Tool", 
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 15))
        
        device_frame = ctk.CTkFrame(main_frame)
        device_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        device_title = ctk.CTkLabel(
            device_frame,
            text="DISCOVERED DEVICE INFORMATION",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="lightblue"
        )
        device_title.pack(pady=(12, 8))
        
        info_frame = ctk.CTkFrame(device_frame)
        info_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.create_device_info_fields(info_frame)
        
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        protocol_label = ctk.CTkLabel(control_frame, text="Protocols:", font=ctk.CTkFont(size=13, weight="bold"))
        protocol_label.pack(pady=(8, 4))
        
        protocol_checkboxes_frame = ctk.CTkFrame(control_frame)
        protocol_checkboxes_frame.pack(pady=(0, 10))
        protocol_checkboxes_frame.grid_columnconfigure(0, weight=1)
        protocol_checkboxes_frame.grid_columnconfigure(1, weight=1)
        
        self.lldp_var = ctk.BooleanVar(value=True)
        self.cdp_var = ctk.BooleanVar(value=True)
        
        lldp_checkbox = ctk.CTkCheckBox(
            protocol_checkboxes_frame, 
            text="LLDP", 
            variable=self.lldp_var,
            font=ctk.CTkFont(size=12)
        )
        lldp_checkbox.grid(row=0, column=0, padx=20, pady=5, sticky="ew")
        
        cdp_checkbox = ctk.CTkCheckBox(
            protocol_checkboxes_frame, 
            text="CDP", 
            variable=self.cdp_var,
            font=ctk.CTkFont(size=12)
        )
        cdp_checkbox.grid(row=0, column=1, padx=20, pady=5, sticky="ew")
        
        button_frame = ctk.CTkFrame(control_frame)
        button_frame.pack(pady=10)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        
        self.start_button = ctk.CTkButton(
            button_frame,
            text="Start Discovery",
            command=self.start_discovery,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=35
        )
        self.start_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="Stop Discovery",
            command=self.stop_discovery,
            font=ctk.CTkFont(size=14),
            height=35,
            state="disabled"
        )
        self.stop_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear Results",
            command=self.clear_results,
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.clear_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        blink_label = ctk.CTkLabel(
            control_frame,
            text="Switch Port Blinking:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        blink_label.pack(pady=(15, 4))
        
        self.blink_status_label = ctk.CTkLabel(
            control_frame,
            text="Status: Ready",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.blink_status_label.pack(pady=(0, 5))
        
        blink_options_frame = ctk.CTkFrame(control_frame)
        blink_options_frame.pack(pady=(0, 10))
        blink_options_frame.grid_columnconfigure(0, weight=1)
        blink_options_frame.grid_columnconfigure(1, weight=1)
        
        self.blink_type_var = ctk.StringVar(value="lldp")
        
        lldp_blink_radio = ctk.CTkRadioButton(
            blink_options_frame,
            text="LLDP Blink",
            variable=self.blink_type_var,
            value="lldp",
            font=ctk.CTkFont(size=12)
        )
        lldp_blink_radio.grid(row=0, column=0, padx=20, pady=5, sticky="ew")
        
        cdp_blink_radio = ctk.CTkRadioButton(
            blink_options_frame,
            text="CDP Blink",
            variable=self.blink_type_var,
            value="cdp",
            font=ctk.CTkFont(size=12)
        )
        cdp_blink_radio.grid(row=0, column=1, padx=20, pady=5, sticky="ew")
        
        self.blink_button = ctk.CTkButton(
            control_frame,
            text="Start Blinking",
            command=self.toggle_blink,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=35,
            fg_color="orange",
            hover_color="darkorange"
        )
        self.blink_button.pack(pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Ready to start discovery",
            font=ctk.CTkFont(size=12),
            text_color="green"
        )
        self.status_label.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        results_frame = ctk.CTkFrame(main_frame)
        results_frame.grid(row=5, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        results_label = ctk.CTkLabel(
            results_frame,
            text="Discovery Results",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        results_label.pack(pady=(12, 8))
        
        self.results_text = ctk.CTkTextbox(
            results_frame,
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            wrap="word"
        )
        self.results_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.results_text.insert("1.0", "Link Discovery Manager Ready\n")
        self.results_text.insert("end", "=" * 70 + "\n\n")
        self.results_text.insert("end", "INSTRUCTIONS:\n")
        self.results_text.insert("end", "1. Select protocols to monitor (LLDP/CDP)\n")
        self.results_text.insert("end", "2. Click 'Start Discovery' to begin\n")
        self.results_text.insert("end", "3. Connect network cable or wait for existing traffic\n")
        self.results_text.insert("end", "4. View real-time results below\n\n")
        self.results_text.insert("end", "REQUIREMENTS: Administrator privileges required for packet capture\n\n")
        self.results_text.insert("end", "=" * 70 + "\n\n")
        
    def create_device_info_fields(self, parent_frame):
        parent_frame.grid_columnconfigure(1, weight=1)
        
        device_name_label = ctk.CTkLabel(
            parent_frame,
            text="Device Name:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        device_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.device_name_field = ctk.CTkLabel(
            parent_frame,
            text=socket.gethostname(),
            font=ctk.CTkFont(size=12),
            text_color="white",
            bg_color="transparent"
        )
        self.device_name_field.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        switch_name_label = ctk.CTkLabel(
            parent_frame,
            text="Switch Name:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        switch_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.switch_name_field = ctk.CTkLabel(
            parent_frame,
            text="Unknown",
            font=ctk.CTkFont(size=12),
            text_color="white",
            bg_color="transparent"
        )
        self.switch_name_field.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        port_id_label = ctk.CTkLabel(
            parent_frame,
            text="Port ID:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        port_id_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.port_id_field = ctk.CTkLabel(
            parent_frame,
            text="Unknown",
            font=ctk.CTkFont(size=12),
            text_color="white",
            bg_color="transparent"
        )
        self.port_id_field.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        port_desc_label = ctk.CTkLabel(
            parent_frame,
            text="Port Description:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        port_desc_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        
        self.port_desc_field = ctk.CTkLabel(
            parent_frame,
            text="Unknown",
            font=ctk.CTkFont(size=12),
            text_color="white",
            bg_color="transparent"
        )
        self.port_desc_field.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        system_desc_label = ctk.CTkLabel(
            parent_frame,
            text="System Description:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        system_desc_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        
        self.system_desc_field = ctk.CTkLabel(
            parent_frame,
            text="Unknown",
            font=ctk.CTkFont(size=12),
            text_color="white",
            bg_color="transparent"
        )
        self.system_desc_field.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        
        copy_button = ctk.CTkButton(
            parent_frame,
            text="Copy",
            command=self.copy_device_info,
            font=ctk.CTkFont(size=11),
            height=25,
            width=80,
            fg_color="gray",
            hover_color="darkgray"
        )
        copy_button.grid(row=5, column=1, padx=10, pady=(10, 5), sticky="e")
        
    def update_device_info_display(self):
        def update():
            self.device_name_field.configure(text=self.current_device['device_name'])
            self.switch_name_field.configure(text=self.current_device['switch_name'])
            self.port_id_field.configure(text=self.current_device['port_id'])
            self.port_desc_field.configure(text=self.current_device['port_description'])
            self.system_desc_field.configure(text=self.current_device['system_description'])
            
        self.after(0, update)
        
    def copy_device_info(self):
        try:
            info_text = f"Device Name: {self.current_device['device_name']}\n"
            info_text += f"Switch Name: {self.current_device['switch_name']}\n"
            info_text += f"Port ID: {self.current_device['port_id']}\n"
            info_text += f"Port Description: {self.current_device['port_description']}\n"
            info_text += f"System Description: {self.current_device['system_description']}"
            
            pyperclip.copy(info_text)
            self.update_status("Device info copied to clipboard", "green")
        except Exception as e:
            self.update_status(f"Failed to copy: {str(e)}", "red")
        
    def toggle_blink(self):
        if self.is_blinking:
            self.stop_blinking()
        else:
            if not self.current_device['switch_name'] or self.current_device['switch_name'] == 'Unknown':
                result = messagebox.askyesno("No Switch Detected", 
                    "No switch has been detected yet. You can still start blinking to attempt to trigger switch port identification.\n\n"
                    "Do you want to continue with blinking?")
                if not result:
                    return
            
            self.start_blinking()
    
    def start_blinking(self):
        self.is_blinking = True
        self.blink_button.configure(text="Stop Blinking", fg_color="red", hover_color="darkred")
        
        blink_type = self.blink_type_var.get()
        self.blink_status_label.configure(text=f"Status: {blink_type.upper()} Blinking Active", text_color="orange")
        
        self.blink_thread = threading.Thread(target=self.blink_loop, daemon=True)
        self.blink_thread.start()
        
        self.update_status(f"{blink_type.upper()} port blinking started", "orange")
        self.results_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {blink_type.upper()} PORT BLINKING STARTED\n")
        self.results_text.insert("end", f"{'=' * 70}\n")
        
        if self.current_device['switch_name'] == 'Unknown':
            self.results_text.insert("end", f"Switch: Not detected yet\n")
            self.results_text.insert("end", f"Port: Not detected yet\n")
            self.results_text.insert("end", f"Protocol: {blink_type.upper()}\n")
            self.results_text.insert("end", f"Status: Blinking active - attempting to trigger switch detection\n")
        else:
            self.results_text.insert("end", f"Switch: {self.current_device['switch_name']}\n")
            self.results_text.insert("end", f"Port: {self.current_device['port_id']}\n")
            self.results_text.insert("end", f"Protocol: {blink_type.upper()}\n")
            self.results_text.insert("end", f"Status: Continuous blinking active - check switch port LED\n")
            
        self.results_text.insert("end", f"{'=' * 70}\n\n")
        self.results_text.see("end")
    
    def stop_blinking(self):
        self.is_blinking = False
        self.blink_button.configure(text="Start Blinking", fg_color="orange", hover_color="darkorange")
        
        self.blink_status_label.configure(text="Status: Ready", text_color="gray")
        
        blink_type = self.blink_type_var.get()
        self.update_status(f"{blink_type.upper()} port blinking stopped", "green")
        self.results_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {blink_type.upper()} PORT BLINKING STOPPED\n")
        self.results_text.insert("end", f"{'=' * 70}\n")
        
        if self.current_device['switch_name'] == 'Unknown':
            self.results_text.insert("end", f"Switch: Not detected\n")
            self.results_text.insert("end", f"Port: Not detected\n")
            self.results_text.insert("end", f"Protocol: {blink_type.upper()}\n")
            self.results_text.insert("end", f"Status: Blinking stopped\n")
        else:
            self.results_text.insert("end", f"Switch: {self.current_device['switch_name']}\n")
            self.results_text.insert("end", f"Port: {self.current_device['port_id']}\n")
            self.results_text.insert("end", f"Protocol: {blink_type.upper()}\n")
            self.results_text.insert("end", f"Status: Blinking stopped\n")
            
        self.results_text.insert("end", f"{'=' * 70}\n\n")
        self.results_text.see("end")
    
    def blink_loop(self):
        blink_type = self.blink_type_var.get()
        
        try:
            while self.is_blinking:
                if blink_type == "lldp":
                    lldp_packet = (
                        Ether(dst="01:80:c2:00:00:0e", src=get_if_hwaddr(conf.iface)) /
                        Raw(load=b'\x02\x07\x04\x00\x11\x22\x33\x44\x55\x66\x77' +
                                   b'\x04\x07\x04\x00\x11\x22\x33\x44\x55\x66\x77' +
                                   b'\x06\x02\x00\x78' +
                                   b'\x08\x0c' + socket.gethostname().encode() +
                                   b'\x0a\x0b' + b'LDM-Port-Blink' +
                                   b'\x0c\x0e' + b'Link Discovery Manager' +
                                   b'\x00\x00')
                    )
                    
                    sendp(lldp_packet, verbose=False)
                    
                elif blink_type == "cdp":
                    cdp_packet = (
                        Ether(dst="01:00:0c:cc:cc:cc", src=get_if_hwaddr(conf.iface)) /
                        LLC(dsap=0xaa, ssap=0xaa, ctrl=3) /
                        SNAP(OUI=0x00000c, code=0x2000) /
                        Raw(load=b'\x02\x00\x00\xb4' +
                                   b'\x00\x01\x00\x06' + socket.gethostname().encode() +
                                   b'\x00\x02\x00\x0b' + b'LDM-Port-Blink' +
                                   b'\x00\x03\x00\x0e' + b'Link Discovery Manager' +
                                   b'\x00\x04\x00\x08\x00\x00\x00\x01' +
                                   b'\x00\x05\x00\x0b' + b'LDM-Port-Blink' +
                                   b'\x00\x06\x00\x0e' + b'Link Discovery Manager')
                    )
                    
                    sendp(cdp_packet, verbose=False)
                
                time.sleep(1.0)
                
        except Exception as e:
            error_msg = f"Blinking error: {str(e)}"
            self.update_status(error_msg, "red")
            self.is_blinking = False
            self.blink_button.configure(text="Start Blinking", fg_color="orange", hover_color="darkorange")
        
    def start_discovery(self):
        if not self.lldp_var.get() and not self.cdp_var.get():
            messagebox.showwarning("Warning", "Please select at least one protocol (LLDP or CDP)")
            return
            
        self.is_sniffing = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_label.configure(text="Discovery active - listening for packets...", text_color="orange")
        
        self.packet_count = 0
        self.discovered_devices.clear()
        
        self.current_device = {
            'device_name': socket.gethostname(),
            'switch_name': 'Unknown',
            'port_id': 'Unknown',
            'port_description': 'Unknown',
            'system_description': 'Unknown'
        }
        self.update_device_info_display()
        
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", f"DISCOVERY STARTED: {datetime.now().strftime('%H:%M:%S')}\n")
        self.results_text.insert("end", "=" * 70 + "\n\n")
        self.results_text.insert("end", "STATUS: Listening for network packets...\n")
        self.results_text.insert("end", "STATUS: Monitoring LLDP and CDP traffic...\n\n")
        self.results_text.insert("end", "=" * 70 + "\n\n")
        
        self.sniff_thread = threading.Thread(target=self.sniff_packets, daemon=True)
        self.sniff_thread.start()
        
    def stop_discovery(self):
        self.is_sniffing = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_label.configure(text="Discovery stopped", text_color="red")
        
        if self.is_blinking:
            self.stop_blinking()
        
        if self.sniff_thread and self.sniff_thread.is_alive():
            self.results_text.insert("end", "\nSTATUS: Discovery stopped by user.\n")
            self.results_text.insert("end", "=" * 70 + "\n\n")
            
    def clear_results(self):
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", "STATUS: Results cleared.\n")
        self.results_text.insert("end", "=" * 70 + "\n\n")
        self.discovered_devices.clear()
        
        self.current_device = {
            'device_name': socket.gethostname(),
            'switch_name': 'Unknown',
            'port_id': 'Unknown',
            'port_description': 'Unknown',
            'system_description': 'Unknown'
        }
        self.update_device_info_display()
        
    def sniff_packets(self):
        try:
            filters = []
            if self.lldp_var.get():
                filters.append("ether dst 01:80:c2:00:00:0e")
            if self.cdp_var.get():
                filters.append("ether dst 01:00:0c:cc:cc:cc")
            
            if not filters:
                return
                
            packet_filter = " or ".join(filters)
            
            sniff(
                prn=self.process_packet,
                store=0,
                filter=packet_filter,
                stop_filter=lambda p: not self.is_sniffing
            )
            
        except Exception as e:
            self.update_status(f"Error during discovery: {str(e)}", "red")
            
    def process_packet(self, packet):
        if not self.is_sniffing:
            return
            
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            if packet.haslayer(Ether) and packet[Ether].dst == "01:80:c2:00:00:0e":
                self.process_lldp_packet(packet, timestamp)
                
            elif packet.haslayer(Ether) and packet[Ether].dst == "01:00:0c:cc:cc:cc":
                self.process_cdp_packet(packet, timestamp)
                
        except Exception as e:
            self.update_status(f"Error processing packet: {str(e)}", "red")
            
    def process_lldp_packet(self, packet, timestamp):
        try:
            switch_name = "Unknown"
            port_id = "Unknown"
            port_desc = "Unknown"
            system_desc = "Unknown"
            
            if packet.haslayer(Raw):
                lldp_data = packet[Raw].load
                
                offset = 0
                while offset < len(lldp_data) - 2:
                    tlv_type = (lldp_data[offset] >> 1) & 0x7F
                    tlv_length = ((lldp_data[offset] & 0x01) << 8) | lldp_data[offset + 1]
                    
                    if tlv_length == 0:
                        break
                        
                    if offset + 2 + tlv_length > len(lldp_data):
                        break
                        
                    tlv_value = lldp_data[offset + 2:offset + 2 + tlv_length]
                    
                    if tlv_type == 5:
                        try:
                            switch_name = tlv_value.decode('utf-8', errors='ignore')
                        except:
                            pass
                    elif tlv_type == 2:
                        try:
                            port_id = tlv_value.decode('utf-8', errors='ignore')
                        except:
                            pass
                    elif tlv_type == 4:
                        try:
                            port_desc = tlv_value.decode('utf-8', errors='ignore')
                        except:
                            pass
                    elif tlv_type == 6:
                        try:
                            system_desc = tlv_value.decode('utf-8', errors='ignore')
                        except:
                            pass
                    
                    offset += 2 + tlv_length
            
            self.current_device['switch_name'] = switch_name
            self.current_device['port_id'] = port_id
            self.current_device['port_description'] = port_desc
            self.current_device['system_description'] = system_desc
            
            self.update_device_info_display()
            
            result = f"[{timestamp}] LLDP PACKET DETECTED\n"
            result += f"{'=' * 70}\n"
            result += f"Switch Name:     {switch_name}\n"
            result += f"Port ID:         {port_id}\n"
            result += f"Port Description: {port_desc}\n"
            result += f"System Description: {system_desc}\n"
            result += f"{'=' * 70}\n\n"
            
            device_info = f"{switch_name} - {port_id}"
            if device_info not in self.discovered_devices:
                self.discovered_devices.append(device_info)
            
            self.packet_count += 1
            self.update_results(result)
            self.update_summary()
            
        except Exception as e:
            self.update_status(f"Error processing LLDP packet: {str(e)}", "red")
            
    def process_cdp_packet(self, packet, timestamp):
        try:
            device_id = "Unknown"
            port_id = "Unknown"
            platform = "Unknown"
            capabilities = "Unknown"
            
            result = f"[{timestamp}] CDP PACKET DETECTED\n"
            result += f"{'=' * 70}\n"
            result += f"Device ID:       {device_id}\n"
            result += f"Port ID:         {port_id}\n"
            result += f"Platform:        {platform}\n"
            result += f"Capabilities:    {capabilities}\n"
            result += f"Note:            CDP packet detected but detailed parsing not implemented\n"
            result += f"{'=' * 70}\n\n"
            
            self.update_results(result)
            
        except Exception as e:
            self.update_status(f"Error processing CDP packet: {str(e)}", "red")
            
    def update_results(self, text):
        def update():
            self.results_text.insert("end", text)
            self.results_text.see("end")
            
        self.after(0, update)
        
    def update_status(self, text, color="green"):
        def update():
            self.status_label.configure(text=text, text_color=color)
            
        self.after(0, update)
        
    def update_summary(self):
        def update():
            summary_text = f"Discovery active - {self.packet_count} packets, {len(self.discovered_devices)} unique devices"
            self.status_label.configure(text=summary_text, text_color="orange")
            
        self.after(0, update)
        
    def on_closing(self):
        if self.is_sniffing:
            self.stop_discovery()
        if self.is_blinking:
            self.stop_blinking()
        self.quit()

def main():
    try:
        app = NetworkDiscoveryTool()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")

if __name__ == "__main__":
    main() 