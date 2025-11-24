import os
import subprocess


def run_script(path: str):
    print(f"Running {path}...")
    result = subprocess.run(["python3", path], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise SystemExit(result.returncode)


def main():
    base = os.path.dirname(__file__)
    run_script(os.path.join(base, "aaec", "aaec_analyze.py"))
    run_script(os.path.join(base, "argkp", "argkp_analyze.py"))


if __name__ == "__main__":
    main()



