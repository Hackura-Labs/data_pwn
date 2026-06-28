#!/bin/bash
# ============================================================
# Data Pwn - Installation Script
# ============================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}║   ██████╗  █████╗ ████████╗ █████╗     ██████╗ ██╗    ██╗███╗   ██╗${NC}"
echo -e "${BLUE}║   ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗    ██╔══██╗██║    ██║████╗  ██║${NC}"
echo -e "${BLUE}║   ██║  ██║███████║   ██║   ███████║    ██████╔╝██║ █╗ ██║██╔██╗ ██║${NC}"
echo -e "${BLUE}║   ██║  ██║██╔══██║   ██║   ██╔══██║    ██╔═══╝ ██║███╗██║██║╚██╗██║${NC}"
echo -e "${BLUE}║   ██████╔╝██║  ██║   ██║   ██║  ██║    ██║     ╚███╔███╔╝██║ ╚████║${NC}"
echo -e "${BLUE}║   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝    ╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}║              DATA PWN - Installation Script                   ║${NC}"
echo -e "${BLUE}║                    Version 1.0                                ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ============================================================
# CHECK SYSTEM
# ============================================================

echo -e "${YELLOW}[*] Checking system...${NC}"

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}[!] Warning: This script is optimized for Linux systems${NC}"
    echo -e "${YELLOW}[*] You may need to manually install dependencies on your OS${NC}"
    echo ""
fi

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python version: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}[!] Python3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check if running as root (optional)
if [[ $EUID -eq 0 ]]; then
    echo -e "${YELLOW}⚠ Running as root - this is optional${NC}"
fi

echo ""

# ============================================================
# CREATE VIRTUAL ENVIRONMENT
# ============================================================

echo -e "${YELLOW}[*] Creating virtual environment...${NC}"

# Check if venv exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
    read -p "Remove and recreate? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
    else
        echo -e "${YELLOW}✓ Using existing virtual environment${NC}"
    fi
fi

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# ============================================================
# INSTALL PYTHON DEPENDENCIES
# ============================================================

echo -e "${YELLOW}[*] Installing Python dependencies...${NC}"

# Upgrade pip
pip install --upgrade pip --quiet

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo -e "${YELLOW}⚠ requirements.txt not found, installing defaults...${NC}"
    pip install requests paramiko mysql-connector-python psycopg2-binary colorama
fi

echo -e "${GREEN}✓ Python dependencies installed${NC}"
echo ""

# ============================================================
# INSTALL KALI TOOLS (if on Kali)
# ============================================================

echo -e "${YELLOW}[*] Checking for Kali Linux...${NC}"

if [[ -f /etc/os-release ]] && grep -q "Kali" /etc/os-release; then
    echo -e "${GREEN}✓ Kali Linux detected${NC}"
    echo -e "${YELLOW}[*] Installing Kali tools...${NC}"
    
    sudo apt update --quiet
    
    # Install tools one by one (skip if already installed)
    TOOLS="nmap sqlmap hydra gobuster wpscan nikto dnsrecon sublist3r whatweb sshpass"
    
    for tool in $TOOLS; do
        if command -v $tool &> /dev/null; then
            echo -e "${GREEN}✓ $tool already installed${NC}"
        else
            echo -e "${YELLOW}[*] Installing $tool...${NC}"
            sudo apt install -y $tool --quiet
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✓ $tool installed${NC}"
            else
                echo -e "${RED}[!] Failed to install $tool${NC}"
            fi
        fi
    done
    
    echo -e "${GREEN}✓ Kali tools installation complete${NC}"
else
    echo -e "${YELLOW}⚠ Not running Kali Linux${NC}"
    echo -e "${YELLOW}[*] Installing available tools...${NC}"
    
    # Try to install common tools if on Debian/Ubuntu
    if command -v apt &> /dev/null; then
        sudo apt update --quiet 2>/dev/null || true
        
        # Install only essential tools
        TOOLS="nmap hydra gobuster sshpass"
        
        for tool in $TOOLS; do
            if command -v $tool &> /dev/null; then
                echo -e "${GREEN}✓ $tool already installed${NC}"
            else
                echo -e "${YELLOW}[*] Installing $tool...${NC}"
                sudo apt install -y $tool --quiet 2>/dev/null || true
            fi
        done
    else
        echo -e "${YELLOW}⚠ apt not available - skipping tool installation${NC}"
    fi
fi

echo ""

# ============================================================
# OPTIONAL: INSTALL WORDLISTS
# ============================================================

echo -e "${YELLOW}[*] Would you like to install common wordlists? (optional)${NC}"
INSTALL_WORDLISTS="n"
if [ -t 0 ]; then
    read -p "Install wordlists? (y/n): " -n 1 -r
    echo
    INSTALL_WORDLISTS="$REPLY"
else
    echo -e "${YELLOW}⚠ Non-interactive shell detected - skipping wordlist prompt${NC}"
fi
if [[ $INSTALL_WORDLISTS =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}[*] Installing wordlists...${NC}"
    
    # Check if SecLists is available
    if [ -d "/usr/share/wordlists/SecLists" ]; then
        echo -e "${GREEN}✓ SecLists already installed${NC}"
    else
        echo -e "${YELLOW}[*] Cloning SecLists...${NC}"
        sudo git clone https://github.com/danielmiessler/SecLists.git /usr/share/wordlists/SecLists --quiet 2>/dev/null || echo -e "${YELLOW}⚠ SecLists clone failed (may already exist)${NC}"
    fi
    
    # Check for rockyou.txt
    if [ -f "/usr/share/wordlists/rockyou.txt" ]; then
        echo -e "${GREEN}✓ rockyou.txt already installed${NC}"
    else
        echo -e "${YELLOW}[*] Installing rockyou.txt...${NC}"
        if [ -f "/usr/share/wordlists/rockyou.txt.gz" ]; then
            sudo gunzip /usr/share/wordlists/rockyou.txt.gz
            echo -e "${GREEN}✓ rockyou.txt installed${NC}"
        else
            echo -e "${YELLOW}⚠ rockyou.txt not found - download manually if needed${NC}"
        fi
    fi
    
    echo -e "${GREEN}✓ Wordlists installation complete${NC}"
fi

echo ""

# ============================================================
# SYSTEM-WIDE INSTALLATION
# ============================================================

echo -e "${YELLOW}[*] Installing Data Pwn system-wide...${NC}"

# Get the absolute path of the current directory
INSTALL_DIR="$(pwd)"

# Create launcher script
sudo tee /usr/local/bin/data_pwn > /dev/null << EOF
#!/bin/bash
# Data Pwn Launcher
DIR="$INSTALL_DIR"
source "\$DIR/venv/bin/activate"
python3 "\$DIR/data_pwn.py" "\$@"
EOF

# Make launcher executable
sudo chmod +x /usr/local/bin/data_pwn

echo -e "${GREEN}✓ Data Pwn installed system-wide!${NC}"
echo ""

# ============================================================
# SETUP COMPLETE
# ============================================================

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}║              ${GREEN}INSTALLATION COMPLETE!${BLUE}                       ║${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ============================================================
# USAGE INSTRUCTIONS
# ============================================================

echo -e "${GREEN}✓ Data Pwn installed successfully!${NC}"
echo ""
echo -e "${YELLOW}┌─────────────────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│                    HOW TO USE                               │${NC}"
echo -e "${YELLOW}├─────────────────────────────────────────────────────────────┤${NC}"
echo -e "${YELLOW}│                                                               ${NC}"
echo -e "${YELLOW}│  Run from ANYWHERE (system-wide):                            ${NC}"
echo -e "${YELLOW}│    ${GREEN}data_pwn -t example.com${NC}                              ${NC}"
echo -e "${YELLOW}│                                                               ${NC}"
echo -e "${YELLOW}│  Or run locally:                                              ${NC}"
echo -e "${YELLOW}│    ${GREEN}source venv/bin/activate${NC}                            ${NC}"
echo -e "${YELLOW}│    ${GREEN}python3 data_pwn.py -t example.com${NC}                   ${NC}"
echo -e "${YELLOW}│                                                               ${NC}"
echo -e "${YELLOW}│  Full automatic attack:                                      ${NC}"
echo -e "${YELLOW}│    ${GREEN}data_pwn -t example.com -a${NC}                           ${NC}"
echo -e "${YELLOW}│                                                               ${NC}"
echo -e "${YELLOW}│  Stealth mode:                                               ${NC}"
echo -e "${YELLOW}│    ${GREEN}data_pwn -t example.com -a --stealth${NC}                   ${NC}"
echo -e "${YELLOW}│                                                               ${NC}"
echo -e "${YELLOW}│  Reconnaissance only:                                        ${NC}"
echo -e "${YELLOW}│    ${GREEN}data_pwn -t example.com -r${NC}                           ${NC}"
echo -e "${YELLOW}│                                                               ${NC}"
echo -e "${YELLOW}│  Help:                                                       ${NC}"
echo -e "${YELLOW}│    ${GREEN}data_pwn -h${NC}                                         ${NC}"
echo -e "${YELLOW}│                                                               ${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────────────────┘${NC}"
echo ""

# ============================================================
# CHECK IF SCRIPT IS EXECUTABLE
# ============================================================

if [ -f "data_pwn.py" ]; then
    chmod +x data_pwn.py
    echo -e "${GREEN}✓ data_pwn.py is executable${NC}"
fi

echo ""
echo -e "${YELLOW}⚠ Remember: Only use on systems you have permission to test!${NC}"
echo -e "${YELLOW}⚠ See LEGAL.md for complete legal disclaimer${NC}"
echo ""

echo -e "${GREEN}✓ Installation completed successfully!${NC}"
echo -e "${BLUE}============================================================${NC}"
echo -e "${GREEN}Happy Hacking! Remember to test responsibly! 🚀${NC}"
echo ""