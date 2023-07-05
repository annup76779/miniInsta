import requests

def exchange_code_for_tokens(authorization_code, client_id, client_secret, redirect_uri):
    token_endpoint = 'https://oauth2.googleapis.com/token'
    
    payload = {
        'code': authorization_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    
    response = requests.post(token_endpoint, data=payload)
    tokens = response.json()
    
    return tokens

# Example usage
authorization_code = '4/0AZEOvhVJiFfN6MXvBK8OFmZV3PbPEIu60NJeN_XssnR8w3zwPLLsdr8FxHvVICgty9VFBQ'
client_id = '420422691379-6q4kd42f3c1g692lii9m353m3tbada4i.apps.googleusercontent.com'
client_secret = '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'
redirect_uri = 'http://localhost'

tokens = exchange_code_for_tokens(authorization_code, client_id, client_secret, redirect_uri)
print(tokens)
# # Access the tokens
# access_token = tokens['access_token']
# refresh_token = tokens['refresh_token']
# expires_in = tokens['expires_in']
