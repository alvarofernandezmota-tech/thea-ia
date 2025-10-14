import sys
from pathlib import Path

# Inserta 'src' en sys.path para que 'import src.theaia' funcione
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
