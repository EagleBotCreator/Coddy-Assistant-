#!/usr/bin/env python3
"""Deployment and setup utility for Coddy."""
import subprocess
import sys

def main():
    print("🚀 Setting up Coddy locally...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
    print("✅ Coddy installed successfully in editable mode!")

if __name__ == "__main__":
    main()
