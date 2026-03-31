from dotenv import load_dotenv, dotenv_values
import os
import pathlib

base = pathlib.Path(__file__).parent
env_path = base / ".env"

print("ENV PATH:", env_path)
print("ENV EXISTS:", env_path.exists())
print("RAW .env VALUES:", dotenv_values(env_path))

load_dotenv(env_path)
print("TOKEN FROM os.getenv:", repr(os.getenv("DISCORD_TOKEN")))
