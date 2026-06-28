from main import main
from utils.helpers import Color
import sys

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}[!] Interrupted by user{Color.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"{Color.RED}[!] Error: {e}{Color.ENDC}")
        sys.exit(1)
