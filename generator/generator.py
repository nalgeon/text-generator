from collections import defaultdict
import random
from typing import Generator
from generator.tokenizer import tokenize, textify


def slice_corpus(corpus: list[str], sample_size: int) -> list[list[str, ...]]:
    """
    We need to slice the given source text into a set of `samples`.
    Each sample contains 2 or more `tokens` — words, spaces, or punctuation marks.
    The bigger `sampleSize` is, the more tokens are used to generate the next.

    More about transition matrix:
    @see https://dev.to/bespoyasov/text-generation-with-markov-chains-in-javascript-i38 in English
    @see https://bespoyasov.ru/blog/text-generation-with-markov-chains/ in Russian
    """
    samples = (corpus[idx : idx + sample_size] for idx, _ in enumerate(corpus))
    return [s for s in samples if len(s) == sample_size]


def collect_transitions(samples: list[list[str, ...]]) -> dict[str, list[str, ...]]:
    """
    Transition matrix is an object with samples' first tokens as keys
    and lists of their following tokens as values.
    This object will allow to randomly select one
    of the following tokens to “generate” the next word.
    """
    transitions = defaultdict(list)
    for sample in samples:
        state = "".join(sample[0:-1])
        next = sample[-1]
        transitions[state].append(next)
    return transitions


def create_chain(start_text: str, transitions: dict[str, list[str, ...]]) -> list[str]:
    """
    Initially, the chain is the tokenized `startText` if given,
    or a random sample—the key from the transition matrix.
    """
    head = start_text or random.choice(list(transitions.keys()))
    return tokenize(head)


def predict_next(chain: list[str], transitions: dict[str, list[str, ...]], sample_size: int) -> str:
    """
    When generating a next word,
    we take the (`sampleSize` - 1) number of last `tokens` from the chain.
    These tokens consist a key for the transition matrix,
    by which we get a list of possible next words,
    and randomly select one from them.
    """
    last_state = "".join(chain[-(sample_size - 1) :])
    next_words = transitions[last_state]
    return random.choice(next_words) if next_words else ""


def generate_chain(
    start_text: str, transitions: dict[str, list[str, ...]], sample_size: int
) -> Generator[str, None, None]:
    """
    Each time the generator is asked for a new word,
    it “predicts” the next `token` for the `chain` and yields it.
    If there are no following tokens, it removes the last token from the chain
    so the chain contains only sequences that can produce new words.
    """
    chain = create_chain(start_text, transitions)

    while True:
        state = predict_next(chain, transitions, sample_size)
        yield state

        if state:
            chain.append(state)
        else:
            chain = chain[:-1]


def generate(source: str, start: str = "", words_count: int = 200, sample_size: int = 3) -> str:
    if not source:
        raise ValueError("The source text cannot be empty.")
    if sample_size < 2:
        raise ValueError("Sample size must not be less than 2.")

    corpus = tokenize(source)
    samples = slice_corpus(corpus, sample_size)
    transitions = collect_transitions(samples)

    generator = generate_chain(start, transitions, sample_size)
    chain = [next(generator) for _ in range(words_count)]
    return textify(chain)
