import requests
import base64


def get_auth_headers(form_id, api_key):
    """
    Constructs and returns authentication headers for API requests.

    Args:
        form_id (str): The ID of the form.
        api_key (str): The API key for authentication.

    Returns:
        dict: Authentication headers.
    """
    if form_id and api_key:
        credentials = base64.b64encode(f"{form_id}:{api_key}".encode("utf-8")).decode(
            "utf-8"
        )
        return {"Authorization": f"Basic {credentials}"}
    return {}


def make_request(method, url, headers=None, params=None):
    """
    Makes an HTTP request to the specified URL.

    Args:
        method (function): The HTTP method to use (e.g., requests.get, requests.post).
        url (str): The URL to request.
        headers (dict, optional): Headers for the request. Defaults to None.
        params (dict, optional): Query parameters for the request. Defaults to None.

    Returns:
        dict: JSON response from the API.
    """
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        raise  # Re-raise the exception to propagate it further


def set_attributes_from_json(obj, json_response):
    """
    Sets attributes of an object from a JSON response.

    Args:
        obj (object): The object whose attributes will be set.
        json_response (dict): JSON response containing attribute-value pairs.
    """
    for key, value in json_response.items():
        setattr(obj, key, value)


def form_version_exists(form_versions, version_id):
    """
    Checks if a version ID exists in the form's versions.

    Args:
        form_versions (list): List of form versions.
        version_id (int): Version ID to check.

    Returns:
        bool: True if version ID exists, False otherwise.
    """
    return any(version.get("id") == version_id for version in form_versions)
