#!/bin/bash
# NetScope – Installer & Launcher
# For authorized security testing only.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# ----------------------------------------------------------------------
# ASCII Banner
# ----------------------------------------------------------------------
banner() {
    echo -e "${CYAN}"
echo "███╗   ██╗███████╗████████╗    ███████╗ ██████╗ ██████╗ ██████╗ ███████╗"
echo "████╗  ██║██╔════╝╚══██╔══╝    ██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝"
echo "██╔██╗ ██║█████╗     ██║       ███████╗██║     ██║   ██║██████╔╝█████╗  "
echo "██║╚██╗██║██╔══╝     ██║       ╚════██║██║     ██║   ██║██╔═══╝ ██╔══╝  "
echo "██║ ╚████║███████╗   ██║       ███████║╚██████╗╚██████╔╝██║     ███████╗"
echo "╚═╝  ╚═══╝╚══════╝   ╚═╝       ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚══════╝"                                                                        
echo -e "Professional Network Investigator Tool By ATHEX BLACK HAT.${NC}"
echo ""
}

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while ps -p "$pid" > /dev/null 2>&1; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep "$delay"
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

detect_pm() {
    if command -v apt &> /dev/null; then
        PM="apt"
        INSTALL_CMD="sudo apt install -y"
        UPDATE_CMD="sudo apt update"
    elif command -v yum &> /dev/null; then
        PM="yum"
        INSTALL_CMD="sudo yum install -y"
        UPDATE_CMD="sudo yum check-update"
    elif command -v dnf &> /dev/null; then
        PM="dnf"
        INSTALL_CMD="sudo dnf install -y"
        UPDATE_CMD="sudo dnf check-update"
    elif command -v pacman &> /dev/null; then
        PM="pacman"
        INSTALL_CMD="sudo pacman -S --noconfirm"
        UPDATE_CMD="sudo pacman -Sy"
    elif command -v brew &> /dev/null; then
        PM="brew"
        INSTALL_CMD="brew install"
        UPDATE_CMD="brew update"
    else
        echo -e "${RED}No supported package manager found. Please install nmap manually.${NC}"
        exit 1
    fi
}

install_nmap() {
    if ! command -v nmap &> /dev/null; then
        echo -e "${YELLOW}Nmap not found. Installing...${NC}"
        $UPDATE_CMD > /dev/null 2>&1 &
        spinner $!
        $INSTALL_CMD nmap > /dev/null 2>&1 &
        spinner $!
        echo -e "${GREEN}Nmap installed successfully.${NC}"
    else
        echo -e "${GREEN}Nmap is already installed.${NC}"
    fi
}

check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python3 is not installed. Please install Python3 and try again.${NC}"
        exit 1
    fi
    echo -e "${GREEN}Python3 found: $(python3 --version)${NC}"

    # Check for tkinter
    if python3 -c "import tkinter" &> /dev/null; then
        echo -e "${GREEN}tkinter is available.${NC}"
    else
        echo -e "${YELLOW}tkinter not found. Attempting to install...${NC}"
        case "$PM" in
            apt)
                $INSTALL_CMD python3-tk > /dev/null 2>&1 &
                spinner $!
                ;;
            yum|dnf)
                $INSTALL_CMD python3-tkinter > /dev/null 2>&1 &
                spinner $!
                ;;
            pacman)
                $INSTALL_CMD tk > /dev/null 2>&1 &
                spinner $!
                ;;
            brew)
                echo -e "${YELLOW}On macOS, tkinter may require XQuartz. Please install manually if needed.${NC}"
                ;;
        esac

        # Recheck
        if python3 -c "import tkinter" &> /dev/null; then
            echo -e "${GREEN}tkinter installed successfully.${NC}"
        else
            echo -e "${RED}Failed to install tkinter. Please install python3-tk manually.${NC}"
            exit 1
        fi
    fi
}

main() {
    banner
    detect_pm
    install_nmap
    check_python

    echo -e "${CYAN}All dependencies satisfied. Launching NetScope...${NC}"
    sleep 1

    if [[ -f "NetScope.py" ]]; then
        python3 NetScope.py
    else
        echo -e "${RED}NetScope.py not found in current directory.${NC}"
        exit 1
    fi
}

main