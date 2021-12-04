from pathlib import Path
import sys
import generator

source_path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path("cli", "example.txt")
source = source_path.read_text()
result = generator.generate(source, words_count=300, sample_size=6)
print(result)
