"""Configuration and setup utilities for the game."""

import os
import sys


def check_dependencies():
    """Check if required packages are installed."""
    missing = []

    try:
        import openai
    except ImportError:
        missing.append("openai")

    if missing:
        print("Missing required packages:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nInstall with:")
        print(f"  pip install {' '.join(missing)}")
        return False
    return True


def check_api_key(provider: str) -> bool:
    """Check if API key is set for the given provider."""
    if provider.lower() == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            print("\n⚠️  OPENAI_API_KEY environment variable not found.")
            print("Get a key from: https://platform.openai.com/api-keys")
            return False
    elif provider.lower() == "claude":
        if not os.getenv("ANTHROPIC_API_KEY"):
            print("\n⚠️  ANTHROPIC_API_KEY environment variable not found.")
            print("Get a key from: https://console.anthropic.com/")
            return False
    return True


def setup():
    """Run initial setup checks."""
    print("Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✓ All dependencies installed\n")
