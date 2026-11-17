"""
config.py
---------
Central place for every setting the app needs. Values are read from
environment variables (via a .env file) so the checkpoint path and
the Neon Postgres connection string never get hard-coded or committed.

Copy .env.example to .env and fill in your own values before running.
"""

import os
from dotenv import load_dotenv

# Loads variables from a ".env" file in the backend/ folder into the
# process environment. If the file doesn't exist, this just does nothing
# and os.getenv() below falls back to its defaults.
load_dotenv()

# Path to the checkpoint you trained on Kaggle (best_model.pt or an
# epoch_N.pt file). Drop the file in backend/checkpoints/ and point
# this at it.
CHECKPOINT_PATH = os.getenv("CHECKPOINT_PATH", "checkpoints/best_model.pt")

# Neon Postgres connection string, e.g.:
# postgresql+psycopg2://USER:PASSWORD@HOST/DBNAME?sslmode=require
# Get this from your Neon project dashboard -> Connection Details.
DATABASE_URL = os.getenv("DATABASE_URL")

# Which frontend origin is allowed to call this API (CORS). The Vite
# dev server defaults to http://localhost:5173.
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

# Device to run inference on. This model is small (~13.5M params) so
# "cpu" is perfectly fine and is the default — no GPU required.
DEVICE = os.getenv("DEVICE", "cpu")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Copy backend/.env.example to backend/.env "
        "and paste in your Neon Postgres connection string."
    )
