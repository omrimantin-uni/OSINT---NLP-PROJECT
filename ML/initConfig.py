import subprocess
import os
import sys


if not os.path.exists("config.cfg"):
    subprocess.run([sys.executable,
        "python", "-m", "spacy", "init", "config", "config.cfg",
        "--lang", "en", "--pipeline", "ner", "--force"
    ])
    print("✅ config.cfg created.")
else:
    print("⚠️ config.cfg already exists.")
