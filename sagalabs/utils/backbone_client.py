"""
    Backbone client libary for interaction with backbone
"""

import json
import requests
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from flask import Response

from sagalabs.utils.environment import environment

class BackboneClient():
    """
        Backbone class for interaction with backbone
    """

    _instance = None

    def __init__(self):
        #Expected environment values: local, dev and prod
        credential = DefaultAzureCredential()
        secret_client = SecretClient(vault_url=environment.KEYVAULT_URI, credential=credential)
        #Properties:
        self.x_server_key = secret_client.get_secret("backbone-serverkey").value
        self.backbone_url = environment.BACKBONE_URI
        self.redirect_url = environment.REDIRECT_URI


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BackboneClient, cls).__new__(cls)
            # Initialization code here
        return cls._instance


    def make_request(self, endpoint, method, sagalabs_auth, data=None):
        """
            Makes a request to an endpoint on the backbone, with auth details from azure.
            Returns response to endpoint request as (respons_text, response_headers)        
        """
        headers = {
            "X-Server-Key": self.x_server_key,
            "X-SagaLabs-Auth": sagalabs_auth
        }
        url = f"{self.backbone_url}{endpoint}"
        method = method.lower()

        #print(f"Making a {method.upper()} request to {url} with headers {headers} and data {data}")

        response = None

        if method == 'get':
            response = requests.get(url, headers=headers, params=data, timeout=30)
        elif method == 'post':
            response = requests.post(url, headers=headers, json=data, timeout=30)
        else:
            raise ValueError(f"Invalid method: {method}")

        try:
            # Try to decode as JSON
            response_data = response.json()
            response_data = json.dumps(response_data)  # Convert the data to a JSON string
            #print(f"Response body (JSON): {response_data}")
        except json.JSONDecodeError:
            # If it's not JSON, check if it's a file
            if 'application/octet-stream' in response.headers.get('Content-Type', ''):
                response_data = response.content

            else:
                response_data = response.text
        print(response.headers)
        return response_data, response.headers, response.status_code

    def proxy_request(self, endpoint: str, method: str, sagalabs_auth: str, data=None):
        """
            Proxies a request by requesting an endpoint on BackboneClient
            and returning a flask response of that request.
        """
        # Make request to backbone
        response_data, response_headers, response_status = self.make_request(endpoint, method, sagalabs_auth, data)
        # Create a Flask Response object
        response = Response(response_data, content_type='application/json', status=response_status)

        # Copy the headers
        for name, value in response_headers.items():
            # Skip the Transfer-Encoding and Content-Encoding headers
            if name.lower() not in ['transfer-encoding', 'content-encoding']:
                response.headers[name] = value
            # Ensure the Content-Length header is correct
            response.headers['Content-Length'] = len(response_data)

        return response
