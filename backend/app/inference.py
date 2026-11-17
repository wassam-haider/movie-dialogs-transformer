"""
inference.py
------------
Loads a trained checkpoint once and exposes a single method,
generate_reply(), that turns a user's message into the model's reply.

Loaded once at server startup and kept in memory (see main.py) —
never reload the checkpoint per-request, that would be slow and is
the single most common mistake when serving a model behind an API.

Decoding strategy: greedy, autoregressive, no KV-cache. That means
each new token re-runs the full encoder+decoder forward pass on the
growing sequence so far. For a 13.5M-param model on CPU with
max_seq_length=50 this is still fast (well under a second per reply)
— it's simple correctness over raw speed, which is the right tradeoff
for a small local demo.
"""

import torch

from .transformer_model import build_model
from .tokenizer import clean_text, encode, decode, PAD, SOS, EOS


class ChatbotEngine:
    def __init__(self, checkpoint_path: str, device: str = "cpu"):
        self.device = torch.device(device)

        checkpoint = torch.load(checkpoint_path, map_location=self.device)
        self.config = checkpoint["config"]
        self.vocab = checkpoint["vocab"]
        self.inv_vocab = {i: w for w, i in self.vocab.items()}
        self.max_len = self.config["max_seq_length"]

        self.model = build_model(self.config).to(self.device)
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.eval()  # disables dropout for inference

        print(
            f"Loaded checkpoint from epoch {checkpoint.get('epoch', '?')} "
            f"(val_loss={checkpoint.get('val_loss', float('nan')):.4f}) "
            f"on device={self.device}"
        )

    @torch.no_grad()
    def generate_reply(self, user_message: str) -> str:
        """Greedy decode: predict one token at a time, feed it back in,
        stop at <eos> or once max_len is reached."""
        cleaned = clean_text(user_message)
        src_ids = encode(cleaned, self.vocab, self.max_len)
        src = torch.tensor([src_ids], device=self.device)

        generated = [SOS]
        for _ in range(self.max_len - 1):
            tgt = torch.tensor([generated], device=self.device)
            logits = self.model(src, tgt)          # (1, seq_len, vocab_size)
            next_id = logits[0, -1].argmax().item()  # greedy: highest-probability token
            if next_id == EOS:
                break
            generated.append(next_id)

        reply_ids = generated[1:]  # drop the leading <sos>
        reply = decode(reply_ids, self.inv_vocab)

        if not reply:
            # Can happen with an under-trained model or an out-of-vocab input.
            reply = "(the model didn't generate anything for that — try a shorter message)"
        return reply
