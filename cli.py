import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Data Pwn - Ultimate Data Extraction Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 -m data_pwn -t example.com              # Interactive mode
  python3 -m data_pwn -t example.com -a           # Full auto
  python3 -m data_pwn -t example.com -a --stealth # Stealth mode
  python3 -m data_pwn -t example.com -r           # Recon only
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
    
    return parser.parse_args()
