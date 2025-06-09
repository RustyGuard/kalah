import subprocess

paths = ["src", "tests"]
subprocess.call(["uv", "run", "ruff", "check", "--fix", *paths])
subprocess.call(["uv", "run", "ruff", "check", "--select", "I", "--fix", *paths])
subprocess.call(["uv", "run", "ruff", "format", *paths])
