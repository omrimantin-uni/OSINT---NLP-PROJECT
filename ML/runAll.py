import subprocess
import os
import sys

scripts = [
    "dataMaker.py",
    "toDocBin.py",
    "initConfig.py",
    "train_and_test.py"
]

print("\n========================")
print("🚀 Running NER pipeline")
print("========================\n")

for script in scripts:
    print(f"▶️ Running: {script}")
    result = subprocess.run([sys.executable, os.path.join(os.getcwd(), script)])
    if result.returncode != 0:
        print(f"❌ Error running {script}. Stopping pipeline.")
        break
    print("✅ Done.\n")

print("🎉 All steps complete.")