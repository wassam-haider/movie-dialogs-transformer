# LinkedIn post drafts

Two drafts for the two-part series: Day 1 covers the training work, Day 2
(two days later) covers wrapping it into a working chatbot. Edit these to
sound like you, and swap in real numbers if your final training run differs
from what's in the notebook right now.

---

## Post 1 — Building a Transformer from scratch

I built a Transformer encoder-decoder from scratch — no Hugging Face,
no pretrained weights, just PyTorch and the original "Attention Is All
You Need" architecture — and trained it as a chatbot on the Cornell
Movie-Dialogs Corpus.

What "from scratch" actually meant here:
- Implementing multi-head attention and scaled dot-product attention
  manually
- Sinusoidal positional encoding, since the model has no built-in sense
  of word order
- Separate encoder and decoder stacks, with masked self-attention in
  the decoder so it can't "see" future tokens while generating
- Padding masks so the model ignores the filler tokens used to make
  every sequence the same length

Setup: ~13.5M trainable parameters, 4 encoder + 4 decoder layers,
256-dim embeddings, 8 attention heads, trained on movie dialogue pairs
parsed straight from the raw Cornell corpus text files.

This run is still early — a handful of epochs in — and the loss curve
is still coming down, which is exactly what you'd expect this early.
The real value for me was building every piece by hand instead of
importing a library: attention finally clicked in a way it hadn't from
just reading the paper.

Next: wrapping this into an actual chatbot I can talk to. That's post 2.

#MachineLearning #DeepLearning #Transformers #NLP #PyTorch #AI
#Kaggle #LearningInPublic

---

## Post 2 — Wrapping it into a working chatbot

Two days ago I posted about training a Transformer from scratch on
movie dialogue. Today it's a chatbot I can actually talk to, running
end-to-end on my own laptop.

The stack:
- **FastAPI** backend that loads the trained checkpoint once at
  startup and serves it behind a `/chat` endpoint
- **React** frontend for the chat UI
- **Neon Postgres** (free, serverless) for chat history — the only
  part of this that isn't running locally

How a message gets answered: the text is cleaned and tokenized with
the same vocabulary the model was trained on, the encoder processes
it, and then the decoder generates a reply one token at a time,
feeding each predicted word back in as its own next input, until it
outputs an end-of-sequence token.

No GPU needed for any of this — at ~13.5M parameters the model runs
comfortably on CPU, which meant I could keep the entire project local
and only pay for the tiny bit of cloud (the database) that actually
needed to be online.

It's not a polished product — it's a from-scratch model still early in
training talking back to me in my own terminal-turned-webpage. That's
the whole point: understanding every layer between "type a message"
and "get a reply," instead of treating it as a black box.

#MachineLearning #FastAPI #React #FullStack #AI #NLP #BuildInPublic
