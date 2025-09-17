import environ
from pathlib import Path

env = environ.Env(DEBUG=(bool, False), DATABASE_URL=(str, "sqlite:///db.sqlite3"))

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(Path.joinpath(BASE_DIR, ".env"))
