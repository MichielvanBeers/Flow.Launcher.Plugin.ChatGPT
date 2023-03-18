from tempfile import gettempdir
from urllib import request
from urllib.error import URLError
from pathlib import Path
from functools import wraps
import json
import os
from time import time
import socket
from concurrent.futures import ThreadPoolExecutor
import logging

logging = logging.getLogger(__name__)

URL_SCHEMA = [
    'http://',
    'https://',
]
socket.setdefaulttimeout(15)

def cache(file_name:str, max_age=30, dir=gettempdir()):
    """
    Cache decorator
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_file = Path(dir, file_name)
            if not Path(cache_file).is_absolute():
                cache_file = Path(gettempdir(), cache_file)
            if cache_file.exists() and file_age(cache_file) < max_age and cache_file.stat().st_size != 0:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    try:
                        cache = json.load(f)
                    except json.JSONDecodeError:
                        logging.warning('Unable to read cache file: %s', cache_file)
                        f.close()
                        os.remove(cache_file)
                    else:
                        return cache
            data = func(*args, **kwargs)
            if data is None:
                return None
            if len(data) != 0:
                try:
                    write_json(data, cache_file)
                except FileNotFoundError:
                    logging.warning('Unable to write cache file: %s', cache_file)
            return data
        return wrapper
    return decorator

def read_json(path:str):
    """
    Read json file
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

def write_json(data, path):
    if not Path(path).parent.exists():
        Path(path).parent.mkdir(parents=True)
    with open(path, 'w') as f:
        json.dump(data, f)

def file_age(path):
    age = time() - path.stat().st_mtime
    return age

def get_cache(path, max_age=0):
    if Path(path).exists() and file_age(path) < max_age and path.stat().st_size != 0:
        return read_json(path)
    return None

def refresh_cache(file_name:str, dir:str=gettempdir()):
    """
    Touch cache file
    """
    cache_file = Path(dir, file_name)
    if cache_file.exists():
        cache_file.touch()

def cache_path(file_name:str, dir:str=gettempdir()):
    """
    Return path to cache file
    """
    return Path(dir, file_name)

def remove_cache(file_name:str, dir:str=gettempdir()):
    """
    Remove cache file
    """
    cache_file = Path(dir, file_name)
    if cache_file.exists():
        cache_file.unlink()

def download_file(url:str, path, **kwargs):
    """
    Download file from url and save it to dir

    Args:
        url (str): image url.
        dir (str): directory to save image.
        file_name (str): file name to save image.

    Keyword Args:
        force_download (bool): Force download image even if it exists.
    """
    force_download = kwargs.pop('force_download', False)
    if not force_download and path.exists():
        return
    try:
        request.urlretrieve(url, path)
    except URLError as e:
        logging.exception(f'Unable to download: {url}')
    return Path(path)

def get_icon(url:str, path, file_name:str=None, **kwargs):
    for schema in URL_SCHEMA:
        if url.startswith(schema):
            break
    else:
        return url
    executor = kwargs.pop('executor', False)
    if file_name is None:
        file_name = url.split('/')[-1]
    if not Path(path).is_absolute():
        path = Path(gettempdir(), path)
    if not path.exists():
        path.mkdir(parents=True)
    full_path = Path(path, file_name)
    if not full_path.exists():
        if executor is False:
            download_file(url, full_path)
        else:
            executor.submit(download_file, url, full_path)
    return full_path