"""
Art Institute of Chicago API client.
Used to validate that an artwork (place) exists before adding to a project.
API docs: https://api.artic.edu/docs/
"""

import requests

ARTIC_BASE = "https://api.artic.edu/api/v1"


def artwork_exists(artwork_id: str) -> bool:
    """
    Check if an artwork exists in the Art Institute API.
    Returns True if the artwork is found (HTTP 200 and has data), False otherwise.
    """
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
    """
    Fetch artwork by id from the Art Institute API.
    Returns the 'data' object (id, title, etc.) or None if not found.
    """
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
