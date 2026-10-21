import sys
from pathlib import Path

# The suite uses flat imports ("from voucher.helper import ..."), so both the
# package root and the tests directory need to be importable.
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from base import config, db  # noqa: F401  (re-exported fixtures)
