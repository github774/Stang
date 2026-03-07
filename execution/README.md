# Execution Scripts

This folder contains **deterministic Python scripts** that do the actual work.

## Purpose

Execution scripts are the "doing" layer of the 3-layer architecture. They:

- Handle API calls
- Process data
- Perform file operations
- Interact with databases or cloud services

## Rules

- Scripts must be **deterministic and reliable** — same inputs → same outputs
- Each script should be **well-commented**
- Scripts load config from `.env` (never hardcode secrets)
- Always check if a relevant script already exists before creating a new one

## Naming Convention

```
execution/
├── scrape_single_site.py
├── send_email.py
├── process_csv.py
├── requirements.txt      # Python dependencies
└── ...
```

## Running Scripts

```bash
# Install dependencies
pip install -r execution/requirements.txt

# Run a script
python execution/script_name.py --arg value
```

## Template

```python
"""
Script: script_name.py
Purpose: One-sentence description.
Inputs:  CLI args or environment variables
Outputs: Description of output
"""

import os
import argparse
from dotenv import load_dotenv

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="...")
    parser.add_argument("--input", required=True, help="...")
    args = parser.parse_args()

    # --- Core logic ---
    pass

if __name__ == "__main__":
    main()
```
