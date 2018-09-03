from typing import List

import requests
from django.conf import settings
from requests import Response


def get(endpoint: str):
    header = {
        "Authorization": f"Bearer {settings.PUBG_API_TOKEN}",
        "Accept": "application/vnd.api+json",
    }
    return requests.get(endpoint, headers=header)


def player_information(nick: str) -> List[Response]:
    endpoints = [
        f'{settings.PUBG_API_BASE_URL}/shards/{shard}/players?filter[playerNames]={nick}'
        for shard in settings.PUBG_SHARDS
    ]
    responses = [get(endpoint) for endpoint in endpoints]
    return responses
