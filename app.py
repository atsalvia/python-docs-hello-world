from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential

from flask import Flask, jsonify
app = Flask(__name__)

sp_secrets = {
    'tenant_id': '2ded5d7e-fbb1-4835-83cb-40787153c2a0',
    'client_id': '765b4adb-7aec-42aa-8b2b-3543a8f63b7f',
    'client_secret': '935qEUijK_mIpDh-oR.3dGNGg~E-Hr4B~h'
}

class AzureServicePrincipal():
    def __init__(self):
        self.client = None
        self._azure_auth()

    def _azure_auth(self):
        credentials = ClientSecretCredential(
            tenant_id = sp_secrets['tenant_id'],
            client_id = sp_secrets['client_id'],
            client_secret = sp_secrets['client_secret']
        )
        self.client = SecretClient(
            vault_url = 'https://akv-newsanlab.vault.azure.net/',
            credential = credentials
        )

    def get_secret(self, key):
        return self.client.get_secret(key)


@app.route("/")
def main():
    azure_kv = AzureServicePrincipal()
    # Let's create a secret holding bank account credentials valid for 1 year.
    # if the secret already exists in the Key Vault, then a new version of the secret is created.
    secret = azure_kv.get_secret("PruebaXXXX1234")
    return jsonify({"secret": secret.value}), 200

@app.route("/ping")
def index():
    return jsonify({"status": "ok"}), 200
