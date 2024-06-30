import os
from os import environ as env
import logging

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

#logging.basicConfig(level=logging.DEBUG)

client = None

keys = {"env", "storage-connection-string"}

results = {}

def init():
    global client
    azure_env = env.get("AZURE_ENV", "development")  # developement or production   // the syntax error is due to resource name error in azure!
    keyVaultName = f"pickmypic-kv-{azure_env}"

    KeyVaultUri = f"https://{keyVaultName}.vault.azure.net"
    credential = DefaultAzureCredential()  # looks for proper credential in both CLI and AppServer
    client = SecretClient(vault_url=KeyVaultUri, credential=credential)
    results["env"] = azure_env


def get_secret(key):
    global client
    if client == None:
        init()
    lower_key = key.lower()
    if lower_key in results:
        return results[lower_key]

    value = client.get_secret(key).value #ResourceNotFoundError exception if key not exist

    results[lower_key] = value
    return value

def get_container_root_url():
    storage_account_name = get_secret("storage-account-name")
    return f'https://{storage_account_name}.blob.core.windows.net'

def print_version():
    str = "****************keyvalut print*********"
    print(str)
    logging.info(str)
    return str

if __name__ == '__main__':
    print(get_secret("env"))
    print(get_secret("env"))
    print(get_secret("storage-account-connection-string"))
    print(get_secret("Storage-account-connection-strinG"))
    print(get_secret("Some-strinG"))
    print(get_secret("Some-string"))

    init()

