# test_versions.py
import subprocess

def test_installed_versions(requirements_file="requirements.txt"):
    with open(requirements_file, "r") as f:
        for line in f:
            package = line.strip()
            if package:
                package_name, version = package.split("==")
                try:
                    result = subprocess.run(
                        ["pip", "show", package_name],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        print(f"{package_name} is not installed.")
                    else:
                        for line in result.stdout.splitlines():
                            if line.startswith("Version:"):
                                installed_version = line.split(": ")[1]
                                if installed_version == version:
                                    print(f"{package_name} version is correct: {installed_version}")
                                else:
                                    print(f"{package_name} version mismatch: expected {version}, found {installed_version}")
                except Exception as e:
                    print(f"Error checking {package_name}: {e}")

if __name__ == "__main__":
    test_installed_versions()
