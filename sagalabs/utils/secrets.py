"""
    This file loads secrets from azure, to be used by other files
"""
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

#Azure key vault client
_credential = DefaultAzureCredential()
_client = SecretClient(
    vault_url="https://sagalabskeyvault.vault.azure.net/",
    credential=_credential
)

# Firebase Service Account
FIREBASE_SERVICE_ACCOUNT_JSON = _client.get_secret("SagaLabs-Backbone-Firebase-privatekey-json").value

SELF_PROMOTE_KEY = _client.get_secret("sagalabs-manager-self-promotion-key").value
