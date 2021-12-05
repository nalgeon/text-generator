import argparse
from pathlib import Path

import generator

parser = argparse.ArgumentParser(description="Generate a random text with Markov chain.")
parser.add_argument(
    "corpus", metavar="CORPUS", type=str, help="a path to the plain text corpus file"
)
parser.add_argument("--word-count", type=int, default=300, help="a number of words to generate")
parser.add_argument(
    "--sample-size", type=int, default=6, help="sampling size for building the chain"
)
args = parser.parse_args()

source_path = Path(args.corpus) if args.corpus else Path("cli", "example.txt")
source = source_path.read_text().strip()
result = generator.generate(source, words_count=args.word_count, sample_size=args.sample_size)
print(result)
