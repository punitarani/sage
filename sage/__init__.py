"""sage package"""

import os
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent

if os.environ.get("env", "dev") != "prod":
    from dotenv import load_dotenv

    assert load_dotenv(PROJECT_DIR.joinpath(".env"))
