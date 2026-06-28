import sys
from cli import parse_args
from utils.helpers import Color
from core.base import DataPwn

def main():
    args = parse_args()
    
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

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}[!] Interrupted by user{Color.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"{Color.RED}[!] Error: {e}{Color.ENDC}")
        sys.exit(1)
