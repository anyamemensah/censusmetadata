import re
import json
import requests
from typing import Optional
from censusmetadata.exceptions import FailedRequestError


def enforce_int(obj: int | None,
                obj_name: str,
                none_allowed: bool) -> Optional[int | None]:
    """Enforce integer type, with optional None allowed"""
    if obj is None:
        if none_allowed:
            return None
        else: 
            raise TypeError(f"{obj_name} cannot be None.")
    elif isinstance(obj, int):
            return obj
    else:
        raise TypeError(f"{obj_name} must be of type int.")
            

def enforce_str(obj: str | None,
                obj_name: str,
                none_allowed: bool) -> Optional[str | None]:
    """Enforce string type, with optional None allowed"""
    if obj is None:
        if none_allowed:
            return None
        else: 
            raise TypeError(f"{obj_name} cannot be None.")
    elif isinstance(obj, str):
            return obj
    else:
        raise TypeError(f"{obj_name} must be of type str.")
    

def enforce_bool(obj: str | None,
                 obj_name: str,
                 none_allowed: bool) -> Optional[bool | None]:
    """Enforce boolean type, with optional None allowed"""
    if obj is None:
        if none_allowed:
            return None
        else: 
            raise TypeError(f"{obj_name} cannot be None.")
    elif isinstance(obj, bool):
            return obj
    else:
        raise TypeError(f"{obj_name} must be of type bool.")
            

def enforce_list_str(obj: str | list[str] | None, 
                     obj_name: str,
                     none_allowed: bool) -> Optional[list[str]]:
    """
    Enforce str (converted to list) or list of string type, 
    with optional None allowed
    """
    if obj is None:
        if none_allowed:
            return None
        else: 
            raise TypeError(f"{obj_name} cannot be None.")
    elif isinstance(obj, str):
        return [obj]
    elif isinstance(obj, list) and all(isinstance(ele, str) for ele in obj):
        return obj
    else:
        raise TypeError(f"{obj_name} must be of type str or list of str.")
            

def validate_inputs(**kwargs):
    """Generalized function for validating 'get*' function inputs"""
    validated = []
    for key, (func, value, none_allowed) in kwargs.items():
        validated.append(
            func(
                obj = value,
                obj_name = key,
                none_allowed = none_allowed
            )
        )
    return tuple(validated)


def build_url(name: str | None = None, 
              vintage: int | None = None, 
              meta_type: str | None = None,
              group: str | None = None) -> str:
    """
    Creates the appropriate URL for making a request to the U.S.
    Census Breau API based on the specified parameters 
    """
    baseURL = "https://api.census.gov/data"
    
    parts = filter(
        None, 
        [ 
            str(vintage) if vintage is not None else None,
            name,
            f"groups/{group}" if group else meta_type
        ])
    
    path = re.sub("/{2,}", "/", "/".join(parts)) + ".json"
    
    return f"{baseURL}/{path}"


def status_messages(code: int, url: str): 
    """Unique messages based on response status code"""
    messages = {204: f"{code} - The request was processed successfully, but there is no data to return.", 
                400: f"{code} - Your request is incorrectly formatted and could not be processed.", 
                404: f"{code} - The requested resource could not be found." }
    
    if code not in messages:
        return f"{code} - An unknown error occurred. The url used for the call was: {url}."
    else:
        return f"{messages[code].format(code=code)}. The url used for the call was: {url}."


def check_response(url: str):
    """Checks the response from an HTTP GET request to a given URL."""
    response = requests.get(url)
    status = response.status_code

    if status in [200, 201, 202]:
        return json.loads(response.text)
    elif status == 204:
        print(status_messages(code = status, url = url))
    elif status in [400, 404]:
        raise FailedRequestError(status_messages(code = status, url = url))
    else:  # other status codes
        raise FailedRequestError(status_messages(code = status, url = url))
    
    