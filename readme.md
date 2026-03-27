# 🔭 NetScope
### Professional Network Investigation Tool

> *Transform raw Nmap power into structured, actionable intelligence.*

NetScope is a feature-rich GUI frontend for [Nmap](https://nmap.org/) built for authorized penetration testers, security researchers, and network administrators. It wraps Nmap's command-line engine in a clean, dark-themed interface — delivering real-time scan output, automatic result parsing, vulnerability extraction, and scan history management — all without writing a single command.

---

## 📑 Table of Contents

- [Why NetScope?](#-why-netscope)
- [Features](#-features)
- [Screenshots / Interface Overview](#-interface-overview)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Scan Profiles](#-scan-profiles)
- [Advanced Options](#-advanced-options)
- [Tabs & Panels](#-tabs--panels)
- [Exporting & Importing Results](#-exporting--importing-results)
- [Keyboard Shortcuts](#-keyboard-shortcuts)
- [Scan History](#-scan-history)
- [Built-in Documentation](#-built-in-documentation)
- [Ethical & Legal Notice](#️-ethical--legal-notice)
- [Contributing](#-contributing)
- [License](#-license)

---

## 💡 Why NetScope?

Nmap is the gold standard for network scanning — but its command-line interface can be a barrier for teams who need speed, consistency, and organized reporting. NetScope solves this by:

| Problem | NetScope Solution |
|---|---|
| Memorizing Nmap flags | Pre-defined scan profiles with one-click access |
| Parsing raw terminal output | Automatic extraction into structured tables |
| Losing scan results | Persistent scan history and export/import |
| Switching between windows | All data organized in a single tabbed interface |
| Reproducing past scans | History panel with quick recall |

---

## ✨ Features

### Core Capabilities
- **Intuitive Dark-Themed GUI** — Clean, professional interface designed for extended use during security assessments.
- **Pre-defined Scan Profiles** — Eight ready-to-use scan configurations covering the most common Nmap workflows.
- **Live Output Streaming** — Real-time terminal-style display of Nmap output as the scan progresses.
- **Automatic Result Parsing** — Discovered hosts, open ports, and vulnerabilities are parsed and categorized automatically.
- **Vulnerability Extraction** — CVE identifiers and risk descriptions are pulled directly from Nmap script output.
- **Network Topology View** — Textual map of host relationships relative to the detected gateway.
- **Scan History** — Timestamped log of all previous scans with quick-recall functionality.
- **Export / Import** — Save results to disk or reload previous scans for review or reporting.
- **Built-in Documentation** — Quick reference guide covering scan types, script categories, timing templates, and evasion techniques.
- **Keyboard Shortcuts** — Speed up your workflow with hotkey support.

---

## 🖥️ Interface Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  NetScope — Professional Network Investigation Tool             │
├─────────────────────────────────────────────────────────────────┤
│  Target: [ 192.168.1.0/24          ] [localhost] [subnet] [all] │
│  Profile: [ Intense Scan ▾ ]   [⚙ Advanced Options]            │
│                                  [ ▶ START SCAN ] [ ■ STOP ]   │
├───────────────┬─────────────────────────────────────────────────┤
│  Scan Results │ Discovered Hosts │ Open Ports │ Vulns │ Topology│
├───────────────┴─────────────────────────────────────────────────┤
│  [Live Nmap output streams here in real time...]                │
│                                                                 │
│  Starting Nmap 7.94 ( https://nmap.org )                        │
│  Nmap scan report for 192.168.1.1                               │
│  Host is up (0.0023s latency).                                  │
│  PORT     STATE SERVICE VERSION                                 │
│  22/tcp   open  ssh     OpenSSH 8.9                             │
│  80/tcp   open  http    nginx 1.24.0                            │
│  ...                                                            │
└─────────────────────────────────────────────────────────────────┘
```

| Panel | Description |
|---|---|
| **Target Entry** | IP address, CIDR range (e.g. `192.168.1.0/24`), or hostname. Quick buttons for `localhost`, `subnet`, and broadcast targets. |
| **Scan Profile** | Dropdown of preset scan configurations. |
| **Advanced Options** | Custom port range, timing slider (T0–T5), and feature toggles. |
| **Scan Results** | Raw, live-streamed Nmap terminal output. |
| **Discovered Hosts** | Table: IP address, host status, OS fingerprint, service count. |
| **Open Ports** | Table: port number, protocol, service name, detected version. |
| **Vulnerabilities** | Extracted CVEs and risk descriptions from `--script vuln` output. |
| **Network Topology** | Textual map of hosts relative to the gateway. |
| **History** | Timestamped list of all previously run scans. |

---

## 📋 Requirements

### System Requirements
- **Python** 3.6 or higher
- **Nmap** installed and accessible in the system `PATH`
- **Operating System:** Linux, macOS, or Windows

### Python Dependencies
All dependencies are from the Python standard library — no `pip install` required:

| Module | Purpose |
|---|---|
| `tkinter` | GUI framework (usually included with Python) |
| `subprocess` | Spawning and communicating with Nmap process |
| `threading` | Non-blocking scan execution |
| `queue` | Thread-safe output streaming |
| `re` | Regular expression parsing of Nmap output |
| `json` | Scan history and result serialization |
| `os` | File and path operations |

> **Note for Linux users:** If `tkinter` is missing, install it with:
> ```bash
> sudo apt install python3-tk       # Debian / Ubuntu
> sudo dnf install python3-tkinter  # Fedora / RHEL
> ```

---

## 📦 Installation

### 1. Install Nmap

**Linux (Debian / Ubuntu)**
```bash
sudo apt update && sudo apt install nmap
```

**Linux (Fedora / RHEL)**
```bash
sudo dnf install nmap
```

**macOS (Homebrew)**
```bash
brew install nmap
```

**Windows**
Download the official installer from [nmap.org/download.html](https://nmap.org/download.html).
During installation, ensure **"Add Nmap to PATH"** is selected.

Verify installation:
```bash
nmap --version
```

### 2. Get NetScope

**Clone via Git:**
```bash
git clone https://github.com/Athexblackhat/NetScope.git
cd NetScope
chmod +x *
```

### 3. Run NetScope

```bash
sudo python3 NetScope.py
```

On Windows:
```cmd
python NetScope.py
```

> **Linux / macOS Note:** Many scan profiles (SYN stealth, OS detection, UDP) require root privileges:
> ```bash
> sudo python3 NetScope.py
> ```

---

## 🚀 Quick Start

1. **Launch NetScope:**
   ```bash
   python3 NetScope.py
   ```

2. **Enter a target** in the Target field:
   - Single host: `192.168.1.1`
   - CIDR range: `192.168.1.0/24`
   - Hostname: `example.com`
   - Multiple hosts: `192.168.1.1,192.168.1.5`

3. **Select a Scan Profile** from the dropdown (e.g. *Quick Scan* for a fast overview).

4. **Optionally configure Advanced Options** — port range, timing, and feature toggles.

5. **Click `START SCAN`** or press `Ctrl+N`.

6. **Watch live output** in the *Scan Results* tab while results populate automatically in other tabs.

7. **Export your results** via *File → Export Results* when the scan completes.

---

## 🔍 Scan Profiles

NetScope ships with eight pre-defined scan profiles, each mapped to a common Nmap use case:

| Profile | Nmap Flags | Use Case |
|---|---|---|
| **Quick Scan** | `-T4 -F` | Fast sweep of the 100 most common ports. Ideal for initial discovery. |
| **Intense Scan** | `-T4 -A -v` | Full fingerprinting: OS detection, version detection, scripts, and traceroute. |
| **Vulnerability Scan** | `--script vuln` | Runs Nmap's NSE vulnerability scripts against the target. Extracts CVEs. |
| **Stealth Scan** | `-sS` | TCP SYN (half-open) scan. Less likely to appear in target logs. Requires root. |
| **OS Detection** | `-O` | Attempts to identify the operating system of each discovered host. Requires root. |
| **Service Version** | `-sV` | Detects service names and version numbers on open ports. |
| **UDP Scan** | `-sU` | Scans UDP ports (slower). Useful for finding DNS, SNMP, DHCP, etc. Requires root. |
| **Aggressive Scan** | `-A` | Enables OS detection, version detection, script scanning, and traceroute. |

> 💡 **Tip:** For a complete network assessment, start with *Quick Scan* to discover live hosts, then run *Intense Scan* or *Vulnerability Scan* on specific targets of interest.

---

## ⚙️ Advanced Options

Fine-tune scan behavior beyond the preset profiles:

### Port Range
Specify custom ports instead of Nmap's default selection:

| Input Format | Example | Effect |
|---|---|---|
| Single port | `80` | Scan only port 80 |
| Port range | `1-1024` | Scan ports 1 through 1024 |
| Comma-separated | `22,80,443,8080` | Scan specific ports |
| Combined | `22,80,1000-2000` | Mix of individual and ranges |
| All ports | `1-65535` | Complete port sweep (slow) |

### Timing Template (T0–T5)

Controls scan speed and aggressiveness. Higher values are faster but more detectable:

| Template | Name | Description |
|---|---|---|
| T0 | Paranoid | Extremely slow. Evades most IDS. |
| T1 | Sneaky | Very slow. Good for IDS evasion. |
| T2 | Polite | Slows down to reduce bandwidth. |
| T3 | Normal | Default Nmap timing. |
| T4 | Aggressive | Faster scans. Assumes a reliable network. |
| T5 | Insane | Fastest. May miss results on unreliable networks. |

### Feature Toggles

| Toggle | Nmap Flag | Description |
|---|---|---|
| SYN Stealth | `-sS` | Half-open TCP scan. Requires root. |
| Version Detection | `-sV` | Identify service versions. |
| OS Fingerprinting | `-O` | Detect operating systems. Requires root. |
| Default Scripts | `-sC` | Run Nmap's default NSE script set. |

---

## 📤 Exporting & Importing Results

### Export
Go to **File → Export Results** to save the current scan output and parsed data to a file for reporting or later review.

### Import
Go to **File → Load Results** to import a previously saved scan file and view its parsed data in all tabs.

> Exported files are stored in JSON format, making them easy to process with external tools or scripts.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+N` | Start a new scan |
| `Ctrl+S` | Export current results *(if implemented)* |

---

## 🕓 Scan History

NetScope automatically saves a timestamped record of every scan you run. The **History** tab displays:

- Scan timestamp
- Target used
- Profile selected
- Quick-recall button to reload results

This is especially useful during longer engagements where you need to revisit earlier findings or reproduce a scan exactly.

---

## 📚 Built-in Documentation

Access the built-in reference guide via **Help → Documentation**. It covers:

- Common Nmap scan types and flags
- NSE script categories (`auth`, `vuln`, `discovery`, `exploit`, etc.)
- Timing template explanations
- Basic evasion techniques
- Output format options

For full Nmap documentation, visit: [nmap.org/docs.html](https://nmap.org/docs.html)

---

## ⚠️ Ethical & Legal Notice

> **NetScope is intended solely for authorized security testing and educational purposes.**

Scanning networks or systems **without explicit written authorization** from the owner is:
- **Illegal** in most jurisdictions (including under laws such as the CFAA in the USA, the Computer Misuse Act in the UK, and equivalent legislation globally).
- **Unethical** and a violation of responsible disclosure norms.
- **Potentially harmful** to the availability and integrity of target systems.

**Before using NetScope against any target:**
- Obtain explicit written authorization from the system/network owner.
- Ensure your testing scope is clearly defined and agreed upon.
- Follow responsible disclosure practices if vulnerabilities are discovered.
- Comply with all applicable local, national, and international laws.

The developer assumes **no liability** for any misuse of this tool. Use responsibly.

---

## 🤝 Contributing

**Ways to contribute:**
- Bug reports and reproducible test cases
- New scan profile suggestions
- UI/UX improvements
- Additional Nmap output parsing (new NSE scripts, output formats)
- Documentation improvements

Please open an **Issue** before starting large changes to discuss the approach.

---

## 📄 License

This project is provided for **educational and authorized security testing purposes only**.

Use responsibly and in compliance with all applicable laws and regulations.

© 2026 — All Rights Reserved.

---

<div align="center">

**NetScope — See your network. Scope your security.**

[Report a Bug](../../issues) · [Request a Feature](../../issues) · [Nmap Documentation](https://nmap.org/docs.html)

</div>