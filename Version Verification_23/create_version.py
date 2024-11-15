# generate_requirements.py
import subprocess
from datetime import datetime

def create_requirements_file():
    # Get the current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'Date written to file: {timestamp}')
    
    with open("requirements.txt", "w") as f:
        # Write a comment line with the timestamp
        f.write(f"# Requirements file created on: {timestamp}\n\n")
        # Capture installed packages and versions
        subprocess.run(["pip", "freeze"], stdout=f)
        

if __name__ == "__main__":
    create_requirements_file()
    print("requirements.txt has been created with all installed packages, versions, and timestamp.")
