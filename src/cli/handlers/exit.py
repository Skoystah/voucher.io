import sys
from config import Config

def handle_exit(config: Config, *args) -> None:
    print("Exiting application...")
    sys.exit(0)
