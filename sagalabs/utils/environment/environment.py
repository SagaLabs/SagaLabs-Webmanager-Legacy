"""
    This module handles the environment the application is running as.
    development/production/local
"""
from sagalabs.utils.environment.config_loader import get_value, ENVIRONMENT


BACKBONE_URI = get_value("BACKBONEURL")
REDIRECT_URI = get_value("REDIRECTURI")
KEYVAULT_URI = get_value("KEYVAULTURI")
KEYVAULT_FIREBASE_JSON = get_value("KEYVAULTFIREBASEJSON")
AUTH_COOKIE_NAME = get_value("AUTH_COOKIE")

IS_ENVIRONMENT_LOCAL = ENVIRONMENT == "local"
IS_ENVIRONMENT_DEV = ENVIRONMENT == "dev"
IS_ENVIRONMENT_PROD = ENVIRONMENT == "prod"
