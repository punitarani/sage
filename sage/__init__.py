"""sage package"""

from pathlib import Path

from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).parent.parent

assert load_dotenv(PROJECT_DIR.joinpath(".env"))
