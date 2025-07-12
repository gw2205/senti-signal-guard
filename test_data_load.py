import sys
import os

# 👇 הוספת תיקיית הפרויקט לשורת החיפוש של פייתון
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from sentibot.data_parser import load_sources_and_messages

data = load_sources_and_messages()
print(f"\n✅ Loaded {len(data)} entries\n")

for i, entry in enumerate(data[:5]):
    print(f"{i+1}. {entry['token']} – {entry['source_type']}")
