"""
tokenizer.py
------------
Reproduces the exact text cleaning + word-to-id encoding used while
building the training data, so a message typed by a user goes through
the same transformation the model was trained on.

The vocabulary itself isn't hard-coded here — it's loaded straight out
of the checkpoint (checkpoint["vocab"]), because that's the exact
word->id mapping the model's embedding layers were trained against.
"""

import re

# These four ids are reserved and fixed by the training notebook —
# don't change them, they're baked into every saved checkpoint.
PAD, SOS, EOS, UNK = 0, 1, 2, 3


def clean_text(text: str) -> str:
    """Same normalization used before building the vocab during training:
    lowercase, space out punctuation, strip anything that isn't a letter
    or . ! ? '"""
    text = text.lower().strip()
    text = re.sub(r"([.!?])", r" \1", text)
    text = re.sub(r"[^a-zA-Z.!?']+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def encode(text: str, vocab: dict, max_len: int) -> list[int]:
    """Text -> list of token ids, wrapped in <sos>/<eos> and padded to max_len."""
    tokens = [vocab.get(w, UNK) for w in text.split()]
    tokens = [SOS] + tokens[: max_len - 2] + [EOS]
    tokens += [PAD] * (max_len - len(tokens))
    return tokens


def decode(token_ids: list[int], inv_vocab: dict) -> str:
    """List of token ids -> readable text. Drops padding/special tokens."""
    words = [
        inv_vocab.get(i, "<unk>")
        for i in token_ids
        if i not in (PAD, SOS, EOS)
    ]
    return " ".join(words)
