import requests

def get_access_token():
    auth_endpoint = "https://auth.akuya.tech/api/auth/login"
    credentials = {
        "email": "sapphirejudith@gmail.com",
        "password": "sapphire"
    }

    response = requests.post(auth_endpoint, json=credentials)
    if response.status_code == 200:
        response_data = response.json()
        access_token = response_data.get("data", {}).get("token")
        if access_token:
            return access_token
        else:
            raise Exception("Access token not found in response data")
    else:
        raise Exception("Failed to obtain access token")



