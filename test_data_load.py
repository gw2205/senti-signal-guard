import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "sentibot")))

from data_parser import load_sources_and_messages

data = load_sources_and_messages()
print(f"\n✅ Loaded {len(data)} entries\n")
for i, entry in enumerate(data[:5]):
    print(f"{i+1}. {entry['token']} — {entry['source_type']}")
