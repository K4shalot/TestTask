"""Art Institute of Chicago API client for validating artwork (place) ids."""

import requests

ARTIC_BASE = "https://api.artic.edu/api/v1"


def artwork_exists(artwork_id: str) -> bool:
    if not artwork_id or not str(artwork_id).strip():
        return False
    url = f"{ARTIC_BASE}/artworks/{artwork_id}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return False
        data = resp.json()
        return bool(data.get("data"))
    except (requests.RequestException, ValueError, KeyError):
        return False


def get_artwork(artwork_id: str) -> dict | None:
    if not artwork_id or not str(artwork_id).strip():
        return None
    url = f"{ARTIC_BASE}/artworks/{artwork_id}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        return data.get("data")
    except (requests.RequestException, ValueError, KeyError):
        return None
