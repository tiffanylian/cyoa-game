"""Configuration management for storing API keys securely."""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any


class ConfigManager:
    """Manages game configuration including API keys."""

    CONFIG_DIR = Path.home() / ".cyoa-game"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    @classmethod
    def ensure_config_dir(cls):
        """Ensure the config directory exists."""
        cls.CONFIG_DIR.mkdir(exist_ok=True, mode=0o700)  # Only user can read/write

    @classmethod
    def load_config(cls) -> Dict[str, Any]:
        """Load configuration from file."""
        cls.ensure_config_dir()
        if cls.CONFIG_FILE.exists():
            try:
                with open(cls.CONFIG_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    @classmethod
    def save_config(cls, config: Dict[str, Any]):
        """Save configuration to file."""
        cls.ensure_config_dir()
        try:
            with open(cls.CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=2)
            # Set restrictive permissions
            os.chmod(cls.CONFIG_FILE, 0o600)  # Only owner can read/write
        except Exception as e:
            print(f"Warning: Could not save config: {e}")

    @classmethod
    def get_api_key(cls, provider: str) -> Optional[str]:
        """Get API key from environment or config file."""
        provider = provider.lower()

        # First check environment variables
        env_var = "OPENAI_API_KEY" if provider == "openai" else "ANTHROPIC_API_KEY"
        env_key = os.getenv(env_var)
        if env_key:
            return env_key

        # Then check config file
        config = cls.load_config()
        return config.get(f"{provider}_api_key")

    @classmethod
    def set_api_key(cls, provider: str, api_key: str, save: bool = True):
        """Store API key in config file."""
        provider = provider.lower()
        config = cls.load_config()
        config[f"{provider}_api_key"] = api_key
        if save:
            cls.save_config(config)

    @classmethod
    def clear_api_key(cls, provider: str):
        """Remove stored API key."""
        provider = provider.lower()
        config = cls.load_config()
        if f"{provider}_api_key" in config:
            del config[f"{provider}_api_key"]
            cls.save_config(config)

    @classmethod
    def get_or_prompt_api_key(cls, provider: str) -> str:
        """Get API key or prompt user to enter it."""
        provider = provider.lower()

        # Try to get existing key
        api_key = cls.get_api_key(provider)
        if api_key:
            print(f"✓ Using stored {provider.upper()} API key\n")
            return api_key

        # Prompt user
        env_var = "OPENAI_API_KEY" if provider == "openai" else "ANTHROPIC_API_KEY"
        print(f"\n{env_var} not found.")

        if provider == "openai":
            print("Get your key from: https://platform.openai.com/api-keys")
        else:
            print("Get your key from: https://console.anthropic.com/")

        api_key = input("\nEnter your API key: ").strip()

        if not api_key:
            raise ValueError("API key is required to play.")

        # Ask if user wants to save it
        save_choice = input("\nSave this API key for future use? (yes/no): ").strip().lower()
        if save_choice in ["yes", "y"]:
            cls.set_api_key(provider, api_key, save=True)
            print(
                f"✓ API key saved to {cls.CONFIG_FILE}\n"
                f"  (Config file permissions: 600 - only you can access)\n"
            )
        else:
            print("Note: You'll need to enter your API key again next time.\n")

        return api_key

    @classmethod
    def reset_api_key(cls, provider: str):
        """Interactively reset stored API key."""
        provider = provider.lower()
        cls.clear_api_key(provider)
        print(f"Cleared stored {provider.upper()} API key.\n")
        return cls.get_or_prompt_api_key(provider)
