# run_bot.py

import os
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import and run bot
from theaia.adapters.telegram.bot import main

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 THEA IA - Telegram Bot")
    print("=" * 60)
    main()
