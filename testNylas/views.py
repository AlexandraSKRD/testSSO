from django.shortcuts import render
from rest_framework.response import Response

from django.contrib.sites import requests
from nylas import APIClient
from rest_framework.decorators import api_view
import requests

@api_view(['POST'])
def authorize(request):

    api_client = APIClient(app_id="57j65z6aezdxuocajwwegvkyx", app_secret="du2z08iomhm6remzvzyhk8bz9")

    response_body = {
        "client_id": api_client.app_id,
        "name": "alexandra",
        "email_address": request.data.get('email'),
        "provider": "outlook",
        "settings": {
            "username": request.data.get('email'),
            "password": request.data.get('password'),
        }
    }

    nylas_authorize_resp = requests.post(
        "https://api.nylas.com/connect/authorize", json=response_body
    )
    print(nylas_authorize_resp.json())
    # nylas_code = nylas_authorize_resp.json()["code"]

    nylas_code ='d80cOfUCvwW-teOcAtvh'
    state = 'WM6D'
    nylas_token_data = {
        "client_id": api_client.app_id,
        "client_secret": api_client.app_secret,
        "code": nylas_code,
        "state": state
    }


    nylas_token_resp = requests.post(
        "https://api.nylas.com/connect/token", json=nylas_token_data
    )

    if not nylas_token_resp.ok:
        message = nylas_token_resp.json()["message"]
        return Response('Bad Request')

    nylas_access_token = nylas_token_resp.json()["access_token"]

    data = {
        "code": nylas_code,
        "access_token": nylas_access_token
    }
    return Response(data)


