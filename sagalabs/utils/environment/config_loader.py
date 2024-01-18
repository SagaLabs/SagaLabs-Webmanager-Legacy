"""
    Loads the config.yaml file based on environment
"""
import sys
import yaml
from dotenv import dotenv_values

# Load the config file on import
with open('sagalabs/config.yaml', 'r', encoding="utf-8") as file:
    _config = yaml.safe_load(file)

ENVIRONMENT = dotenv_values(".env").get("ENVIRONMENT")

# Checks if ENVIRONMENT is set, and if it's value exists in sagalabs/config.yaml
if not ENVIRONMENT:
    print('Error: ENVIRONMENT variable not found. Please set the ENVIRONMENT variable.')
    sys.exit(1)
if ENVIRONMENT not in _config:
    print(f'Error: the environment "{ENVIRONMENT}" not found in config file.')
    sys.exit(1)


def get_value(key):
    """
        Returns the value to a key, based on environment from config.yaml
    """

    # Try to get the value from the specific environment first
    value = _config[ENVIRONMENT].get(key)

    if value is None:
        # If not found, fall back to the global scope
        value = _config.get(key)

    if value is None:
        print(f'Error: the key "{key}" not found in the config.yaml for env: "{ENVIRONMENT}"')
        sys.exit(1)

    return value
