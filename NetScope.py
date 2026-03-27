#!/usr/bin/env python3
"""
Professional Nmap GUI - Advanced Network Investigation Tool
For Authorized Security Testing Only
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import threading
import re
import json
import os
from datetime import datetime
import queue

class NmapProGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Nmap Professional Investigator Tool")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e1e')
        
        # Set dark theme colors
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'accent': '#0078d4',
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'terminal': '#2d2d2d'
        }
        
        self.scan_history = []
        self.current_scan = None
        self.scan_queue = queue.Queue()
        
        self.setup_ui()
        self.check_nmap()
        
    def setup_ui(self):
        """Create the professional interface"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Scan", command=self.new_scan, accelerator="Ctrl+N")
        file_menu.add_command(label="Load Results", command=self.load_results)
        file_menu.add_command(label="Export Results", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        scan_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Scan", menu=scan_menu)
        scan_menu.add_command(label="Quick Scan", command=lambda: self.run_quick_scan())
        scan_menu.add_command(label="Intense Scan", command=lambda: self.run_intense_scan())
        scan_menu.add_command(label="Vulnerability Scan", command=lambda: self.run_vuln_scan())
        scan_menu.add_command(label="Stealth Scan", command=lambda: self.run_stealth_scan())
        
        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Network Topology", command=self.show_topology)
        tools_menu.add_command(label="Service Detection", command=self.service_detection)
        tools_menu.add_command(label="OS Fingerprinting", command=self.os_fingerprinting)
        tools_menu.add_command(label="Script Engine", command=self.script_engine)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.show_docs)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Scan Controls
        left_panel = ttk.Frame(main_frame, width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Target Input
        target_frame = ttk.LabelFrame(left_panel, text="🎯 Target", padding=10)
        target_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(target_frame, text="Target IP/Range:").pack(anchor=tk.W)
        self.target_entry = ttk.Entry(target_frame, font=('Consolas', 10))
        self.target_entry.pack(fill=tk.X, pady=(5, 0))
        self.target_entry.insert(0, "192.168.1.0/24")
        
        # Quick target buttons
        quick_targets = ttk.Frame(target_frame)
        quick_targets.pack(fill=tk.X, pady=5)
        ttk.Button(quick_targets, text="Local Network", 
                  command=lambda: self.target_entry.insert(0, "192.168.1.0/24")).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_targets, text="Localhost", 
                  command=lambda: self.target_entry.insert(0, "127.0.0.1")).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_targets, text="Scanme", 
                  command=lambda: self.target_entry.insert(0, "scanme.nmap.org")).pack(side=tk.LEFT, padx=2)
        
        # Scan Profile
        profile_frame = ttk.LabelFrame(left_panel, text="⚡ Scan Profile", padding=10)
        profile_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.scan_profile = ttk.Combobox(profile_frame, values=[
            "Quick Scan (-T4 -F)",
            "Intense Scan (-T4 -A -v)",
            "Ping Scan (-sn)",
            "Port Scan (-p 1-1000)",
            "Service Version (-sV)",
            "OS Detection (-O)",
            "Vulnerability Scan (--script vuln)",
            "Stealth Scan (-sS)",
            "UDP Scan (-sU)",
            "Aggressive Scan (-A)"
        ], state="readonly")
        self.scan_profile.pack(fill=tk.X)
        self.scan_profile.current(0)
        
        # Advanced Options
        advanced_frame = ttk.LabelFrame(left_panel, text="🔧 Advanced Options", padding=10)
        advanced_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Port Range
        ttk.Label(advanced_frame, text="Port Range:").pack(anchor=tk.W)
        self.port_entry = ttk.Entry(advanced_frame)
        self.port_entry.pack(fill=tk.X, pady=(0, 5))
        self.port_entry.insert(0, "1-1000")
        
        # Timing Template
        ttk.Label(advanced_frame, text="Timing (T0-T5):").pack(anchor=tk.W)
        self.timing = ttk.Scale(advanced_frame, from_=0, to=5, orient=tk.HORIZONTAL)
        self.timing.set(4)
        self.timing.pack(fill=tk.X)
        
        # Checkboxes
        self.syn_check = ttk.Checkbutton(advanced_frame, text="SYN Stealth Scan (-sS)")
        self.syn_check.pack(anchor=tk.W)
        
        self.version_check = ttk.Checkbutton(advanced_frame, text="Version Detection (-sV)")
        self.version_check.pack(anchor=tk.W)
        
        self.os_check = ttk.Checkbutton(advanced_frame, text="OS Detection (-O)")
        self.os_check.pack(anchor=tk.W)
        
        self.script_check = ttk.Checkbutton(advanced_frame, text="Default Scripts (-sC)")
        self.script_check.pack(anchor=tk.W)
        
        # Scan Button
        self.scan_btn = ttk.Button(left_panel, text="▶ START SCAN", 
                                   command=self.start_scan, style="Accent.TButton")
        self.scan_btn.pack(fill=tk.X, pady=10)
        
        # History
        history_frame = ttk.LabelFrame(left_panel, text="📋 Scan History", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        self.history_list = tk.Listbox(history_frame, bg='#2d2d2d', fg='#ffffff',
                                       selectmode=tk.SINGLE)
        self.history_list.pack(fill=tk.BOTH, expand=True)
        self.history_list.bind('<<ListboxSelect>>', self.load_history_scan)
        
        # Right panel - Results
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Output Tab
        self.output_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.output_frame, text="📊 Scan Results")
        
        self.output_text = scrolledtext.ScrolledText(
            self.output_frame, 
            bg='#1e1e1e', 
            fg='#00ff00',
            insertbackground='white',
            font=('Consolas', 10)
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Hosts Tab
        self.hosts_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.hosts_frame, text="💻 Discovered Hosts")
        
        # Hosts Tree
        self.hosts_tree = ttk.Treeview(self.hosts_frame, columns=('IP', 'Status', 'OS', 'Services'), show='tree headings')
        self.hosts_tree.heading('IP', text='IP Address')
        self.hosts_tree.heading('Status', text='Status')
        self.hosts_tree.heading('OS', text='Operating System')
        self.hosts_tree.heading('Services', text='Services')
        self.hosts_tree.pack(fill=tk.BOTH, expand=True)
        
        # Ports Tab
        self.ports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ports_frame, text="🔌 Open Ports")
        
        self.ports_tree = ttk.Treeview(self.ports_frame, columns=('Port', 'Protocol', 'Service', 'Version'), show='tree headings')
        self.ports_tree.heading('Port', text='Port')
        self.ports_tree.heading('Protocol', text='Protocol')
        self.ports_tree.heading('Service', text='Service')
        self.ports_tree.heading('Version', text='Version')
        self.ports_tree.pack(fill=tk.BOTH, expand=True)
        
        # Vulnerabilities Tab
        self.vuln_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.vuln_frame, text="⚠️ Vulnerabilities")
        
        self.vuln_text = scrolledtext.ScrolledText(
            self.vuln_frame,
            bg='#1e1e1e',
            fg='#ff6b6b',
            font=('Consolas', 10)
        )
        self.vuln_text.pack(fill=tk.BOTH, expand=True)
        
        # Topology Tab
        self.topology_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.topology_frame, text="🌐 Network Topology")
        
        self.topology_text = scrolledtext.ScrolledText(
            self.topology_frame,
            bg='#1e1e1e',
            fg='#ffffff',
            font=('Consolas', 10)
        )
        self.topology_text.pack(fill=tk.BOTH, expand=True)
        
        # Status Bar
        self.status_bar = ttk.Label(
            self.root,
            text="Ready | Nmap Professional Investigator",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_scan())
        
    def check_nmap(self):
        """Verify Nmap is installed"""
        try:
            subprocess.run(['nmap', '--version'], capture_output=True, check=True)
            self.update_status("✓ Nmap detected - Ready for investigation")
        except:
            messagebox.showerror(
                "Nmap Not Found",
                "Nmap is not installed or not in PATH.\n\n"
                "Install with: sudo apt install nmap\n"
                "Or download from: https://nmap.org"
            )
            self.update_status("✗ Nmap not found - Please install Nmap")
            
    def start_scan(self):
        """Start the scan in a separate thread"""
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("No Target", "Please enter a target IP or range")
            return
            
        self.scan_btn.config(state=tk.DISABLED, text="⏳ SCANNING...")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"[*] Starting investigation on {target}\n")
        self.output_text.insert(tk.END, f"[*] Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.output_text.insert(tk.END, "="*60 + "\n\n")
        
        # Start scan thread
        thread = threading.Thread(target=self.perform_scan, args=(target,))
        thread.daemon = True
        thread.start()
        
    def perform_scan(self, target):
        """Execute the Nmap scan"""
        try:
            # Build command based on profile and options
            profile = self.scan_profile.get()
            cmd = ['nmap']
            
            # Parse profile
            if "Quick Scan" in profile:
                cmd.extend(['-T4', '-F'])
            elif "Intense Scan" in profile:
                cmd.extend(['-T4', '-A', '-v'])
            elif "Ping Scan" in profile:
                cmd.extend(['-sn'])
            elif "Port Scan" in profile:
                cmd.extend(['-p', self.port_entry.get()])
            elif "Service Version" in profile:
                cmd.extend(['-sV'])
            elif "OS Detection" in profile:
                cmd.extend(['-O'])
            elif "Vulnerability Scan" in profile:
                cmd.extend(['--script', 'vuln'])
            elif "Stealth Scan" in profile:
                cmd.extend(['-sS'])
            elif "UDP Scan" in profile:
                cmd.extend(['-sU'])
            elif "Aggressive Scan" in profile:
                cmd.extend(['-A'])
                
            # Add advanced options
            if self.syn_check.instate(['selected']):
                cmd.append('-sS')
            if self.version_check.instate(['selected']):
                cmd.append('-sV')
            if self.os_check.instate(['selected']):
                cmd.append('-O')
            if self.script_check.instate(['selected']):
                cmd.append('-sC')
                
            # Add timing
            timing_val = int(self.timing.get())
            cmd.append(f'-T{timing_val}')
            
            # Add target
            cmd.append(target)
            
            # Update status
            self.root.after(0, lambda: self.update_status(f"Running: {' '.join(cmd)}"))
            
            # Run scan
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Read output line by line
            output_lines = []
            for line in process.stdout:
                output_lines.append(line)
                self.root.after(0, lambda l=line: self.output_text.insert(tk.END, l))
                self.root.after(0, lambda: self.output_text.see(tk.END))
                
                # Parse hosts and ports
                self.parse_output_line(line)
                
            process.wait()
            
            # Save to history
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.root.after(0, lambda: self.history_list.insert(0, f"{timestamp} - {target}"))
            
            # Complete
            self.root.after(0, lambda: self.scan_btn.config(state=tk.NORMAL, text="▶ START SCAN"))
            self.root.after(0, lambda: self.update_status("✓ Scan complete"))
            self.root.after(0, lambda: self.output_text.insert(tk.END, "\n\n[*] Scan completed successfully\n"))
            
            # Parse vulnerabilities if any
            self.parse_vulnerabilities('\n'.join(output_lines))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Scan Error", str(e)))
            self.root.after(0, lambda: self.scan_btn.config(state=tk.NORMAL, text="▶ START SCAN"))
            
    def parse_output_line(self, line):
        """Parse scan output for hosts and ports"""
        # Parse hosts
        host_match = re.search(r'Nmap scan report for ([\d\.]+)', line)
        if host_match:
            ip = host_match.group(1)
            self.hosts_tree.insert('', 'end', values=(ip, 'Up', 'Unknown', 'Scanning...'))
            
        # Parse open ports
        port_match = re.search(r'(\d+)/(tcp|udp)\s+open\s+(\S+)', line)
        if port_match:
            port = port_match.group(1)
            proto = port_match.group(2)
            service = port_match.group(3)
            self.ports_tree.insert('', 'end', values=(port, proto, service, 'Unknown'))
            
    def parse_vulnerabilities(self, output):
        """Parse vulnerability scan results"""
        vuln_patterns = [
            (r'VULNERABLE:\s*(.+?)\n', 'red'),
            (r'CVE-\d{4}-\d+', 'yellow'),
            (r'Risk:\s*(.+?)\n', 'orange')
        ]
        
        for pattern, color in vuln_patterns:
            matches = re.findall(pattern, output, re.IGNORECASE)
            for match in matches:
                self.vuln_text.insert(tk.END, f"⚠️ {match}\n")
                
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=f"  {message}")
        
    def new_scan(self):
        """Clear for new scan"""
        self.output_text.delete(1.0, tk.END)
        self.hosts_tree.delete(*self.hosts_tree.get_children())
        self.ports_tree.delete(*self.ports_tree.get_children())
        self.vuln_text.delete(1.0, tk.END)
        self.topology_text.delete(1.0, tk.END)
        
    def run_quick_scan(self):
        """Run quick scan preset"""
        self.scan_profile.set("Quick Scan (-T4 -F)")
        self.start_scan()
        
    def run_intense_scan(self):
        """Run intense scan preset"""
        self.scan_profile.set("Intense Scan (-T4 -A -v)")
        self.start_scan()
        
    def run_vuln_scan(self):
        """Run vulnerability scan"""
        self.scan_profile.set("Vulnerability Scan (--script vuln)")
        self.start_scan()
        
    def run_stealth_scan(self):
        """Run stealth scan"""
        self.scan_profile.set("Stealth Scan (-sS)")
        self.start_scan()
        
    def show_topology(self):
        """Generate network topology"""
        self.notebook.select(self.topology_frame)
        self.topology_text.delete(1.0, tk.END)
        self.topology_text.insert(tk.END, "Network Topology View\n" + "="*50 + "\n\n")
        
        # Parse hosts and build topology
        hosts = []
        for item in self.hosts_tree.get_children():
            values = self.hosts_tree.item(item)['values']
            if values:
                hosts.append(values[0])
                
        if hosts:
            self.topology_text.insert(tk.END, "Discovered Network Structure:\n\n")
            gateway = "192.168.1.1"  # Default gateway assumption
            self.topology_text.insert(tk.END, f"├─ Gateway: {gateway}\n")
            
            for i, host in enumerate(hosts):
                if host != gateway:
                    if i == len(hosts) - 1:
                        self.topology_text.insert(tk.END, f"   └─ Host: {host}\n")
                    else:
                        self.topology_text.insert(tk.END, f"   ├─ Host: {host}\n")
                        
    def service_detection(self):
        """Focus on service detection"""
        self.scan_profile.set("Service Version (-sV)")
        self.start_scan()
        
    def os_fingerprinting(self):
        """Focus on OS detection"""
        self.scan_profile.set("OS Detection (-O)")
        self.start_scan()
        
    def script_engine(self):
        """Open script engine dialog"""
        script_window = tk.Toplevel(self.root)
        script_window.title("NSE Script Engine")
        script_window.geometry("600x400")
        script_window.configure(bg='#1e1e1e')
        
        ttk.Label(script_window, text="Nmap Scripting Engine", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
                 
        script_categories = [
            "auth", "broadcast", "brute", "default", "discovery",
            "dos", "exploit", "external", "fuzzer", "intrusive",
            "malware", "safe", "version", "vuln"
        ]
        
        frame = ttk.Frame(script_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        for i, cat in enumerate(script_categories):
            ttk.Checkbutton(frame, text=cat).grid(row=i//3, column=i%3, sticky=tk.W, pady=2)
            
    def load_results(self):
        """Load previous scan results"""
        filename = filedialog.askopenfilename(
            title="Load Scan Results",
            filetypes=[("Nmap files", "*.nmap *.xml"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'r') as f:
                content = f.read()
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, content)
                
    def export_results(self):
        """Export scan results"""
        filename = filedialog.asksaveasfilename(
            title="Export Scan Results",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("Nmap files", "*.nmap"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w') as f:
                f.write(self.output_text.get(1.0, tk.END))
            messagebox.showinfo("Export Complete", f"Results exported to {filename}")
            
    def load_history_scan(self, event):
        """Load a scan from history"""
        selection = self.history_list.curselection()
        if selection:
            # In a real app, you'd load the actual scan data
            pass
            
    def show_docs(self):
        """Show documentation"""
        docs_window = tk.Toplevel(self.root)
        docs_window.title("Nmap Documentation")
        docs_window.geometry("600x500")
        docs_window.configure(bg='#1e1e1e')
        
        text = scrolledtext.ScrolledText(
            docs_window,
            bg='#1e1e1e',
            fg='#ffffff',
            font=('Consolas', 10)
        )
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        docs = """NMAP PROFESSIONAL INVESTIGATOR - QUICK REFERENCE

SCAN TYPES:
• SYN Stealth (-sS) - Half-open scan, less detectable
• TCP Connect (-sT) - Full connection, more detectable
• UDP Scan (-sU) - Scan UDP ports (slower)
• Ping Sweep (-sn) - Discover live hosts
• Version Detection (-sV) - Identify service versions
• OS Detection (-O) - Identify operating system
• Aggressive (-A) - Enable OS, version, scripts, traceroute

SCRIPT CATEGORIES:
• auth - Authentication credentials
• broadcast - Network broadcast discovery
• brute - Brute force attacks
• default - Default script set
• discovery - Service and host discovery
• dos - Denial of service testing
• exploit - Exploit vulnerabilities
• external - External services
• fuzzer - Protocol fuzzing
• intrusive - May crash services
• malware - Malware detection
• safe - Non-intrusive scripts
• version - Version detection
• vuln - Vulnerability detection

TIMING TEMPLATES:
• T0 (Paranoid) - Extremely slow, IDS evasion
• T1 (Sneaky) - Quite slow, IDS evasion
• T2 (Polite) - Slower, less bandwidth
• T3 (Normal) - Default speed
• T4 (Aggressive) - Fast, assumes good network
• T5 (Insane) - Very fast, may miss ports

OUTPUT FORMATS:
• -oN - Normal output
• -oX - XML output
• -oG - Grepable output
• -oA - All formats

FIREWALL EVASION:
• -f - Fragment packets
• --mtu - Set custom MTU
• -D - Decoy scans
• --source-port - Use specific source port
• --data-length - Append random data
• --ttl - Set TTL value

IMPORTANT NOTES:
• Always have authorization before scanning
• Use responsibly and ethically
• Document all findings thoroughly
• Verify vulnerabilities manually
• Follow all applicable laws

"""
        text.insert(tk.END, docs)
        text.config(state=tk.DISABLED)
        
    def show_about(self):
        """Show about dialog"""
        about_text = """Nmap Professional Investigator (GUI).

Advanced Network Security Analysis Tool
For Authorized Security Testing Only

POWERED BY ATHEX BLACK HAT.

© 2026 - All Rights Reserved
"""
        messagebox.showinfo("About", about_text)

def main():
    root = tk.Tk()
    
    # Set style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure colors
    style.configure('TLabel', background='#1e1e1e', foreground='#ffffff')
    style.configure('TFrame', background='#1e1e1e')
    style.configure('TLabelframe', background='#1e1e1e', foreground='#ffffff')
    style.configure('TButton', background='#0078d4', foreground='#ffffff')
    style.map('TButton', background=[('active', '#005a9e')])
    style.configure('Accent.TButton', background='#28a745', foreground='#ffffff')
    style.map('Accent.TButton', background=[('active', '#218838')])
    style.configure('TCombobox', fieldbackground='#2d2d2d', background='#2d2d2d', foreground='#ffffff')
    style.configure('Treeview', background='#2d2d2d', foreground='#ffffff', fieldbackground='#2d2d2d')
    style.map('Treeview', background=[('selected', '#0078d4')])
    
    app = NmapProGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()