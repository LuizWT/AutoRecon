from pathlib import Path
from config import OUTPUT_DIR

def create_output_file(script_name):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR / f"{script_name}_output.log"


