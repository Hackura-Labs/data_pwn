#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████╗  █████╗ ████████╗ █████╗     ██████╗ ██╗    ██╗███╗   ██╗
║   ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗    ██╔══██╗██║    ██║████╗  ██║
║   ██║  ██║███████║   ██║   ███████║    ██████╔╝██║ █╗ ██║██╔██╗ ██║
║   ██║  ██║██╔══██║   ██║   ██╔══██║    ██╔═══╝ ██║███╗██║██║╚██╗██║
║   ██████╔╝██║  ██║   ██║   ██║  ██║    ██║     ╚███╔███╔╝██║ ╚████║
║   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝    ╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝
║                                                               ║
║                    DATA PWN - Ultimate Data Hunter            ║
║                    Version 1.0 - Kali Integration             ║
╚═══════════════════════════════════════════════════════════════╝
"""

import sys
import argparse
from utils.helpers import Color
from core.base import DataPwn


# ============================================================
# COMMAND LINE INTERFACE
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Data Pwn - Ultimate Data Extraction Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 data_pwn.py -t example.com              # Interactive mode
  python3 data_pwn.py -t example.com -a           # Full
  python3 data_pwn.py -t example.com -a --stealth # Stealth mode
  python3 data_pwn.py -t example.com -r           # Recon only
        """
    )
    
    parser.add_argument('-t', '--target', required=True, help='Target IP address or domain')
    parser.add_argument('-a', '--auto', action='store_true', help='Automatic mode (no menu)')
    parser.add_argument('-r', '--recon-only', action='store_true', help='Reconnaissance only')
    parser.add_argument('-w', '--web', action='store_true', help='Web attacks only')
    parser.add_argument('-s', '--services', action='store_true', help='Service attacks only')
    parser.add_argument('--stealth', action='store_true', help='Enable stealth mode')
    parser.add_argument('--report', action='store_true', help='Generate report only')
    parser.add_argument('-o', '--output', help='Custom output directory')
    
    args = parser.parse_args()
    
    # Create tool instance
    tool = DataPwn()
    tool.setup(args.target, args.stealth)
    
    if args.output:
        tool.output_dir = args.output
    
    if args.report:
        tool.generate_report()
        return
    
    if args.auto:
        tool.full_attack()
        return
    
    if args.recon_only:
        tool.recon_phase()
        tool.generate_report()
        return
    
    if args.web:
        tool.web_phase()
        tool.generate_report()
        return
    
    if args.services:
        tool.service_phase()
        tool.generate_report()
        return
    
    # Interactive mode
    tool.run()

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}[!] Interrupted by user{Color.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"{Color.RED}[!] Error: {e}{Color.ENDC}")
        sys.exit(1)