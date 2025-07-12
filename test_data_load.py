import sys
import os

# הוספת הנתיב הנכון לסקריפט כדי שפייתון יזהה את קובץ data_parser.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "sentibot", "utils")))

from data_parser import load_sources_and_messages

data = load_sources_and_messages()
print(f"\n✅ Loaded {len(data)} entries\n")

for i, entry in enumerate(data[:5]):
    print(f"{i+1}. {entry['token']} – {entry['source_type']}")
