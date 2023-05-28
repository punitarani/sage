"""sage package"""

import os
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR.joinpath("data")

if os.environ.get("env", "dev") != "prod":
    from dotenv import load_dotenv

    load_dotenv(PROJECT_DIR.joinpath(".env"))
