"""One validated base URL for root, project-path, and custom-domain builds."""
from pathlib import Path
from urllib.parse import urlsplit
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]
settings = json.loads((ROOT / 'site.json').read_text(encoding='utf-8'))
SITE_URL = os.environ.get('SITE_URL', settings['site_url']).rstrip('/')
parts = urlsplit(SITE_URL)
if (
    parts.scheme != 'https'
    or not parts.hostname
    or parts.username is not None
    or parts.password is not None
    or parts.query
    or parts.fragment
    or not re.fullmatch(r'[A-Za-z0-9.-]+', parts.netloc)
    or not re.fullmatch(r'(?:/[A-Za-z0-9._~-]+)*', parts.path)
    or any(segment in ('.', '..') for segment in parts.path.split('/'))
    or any(character.isspace() for character in SITE_URL)
):
    raise ValueError('site_url must be an HTTPS site URL, optionally with a repository path, without credentials, query, or fragment.')
BASE_PATH = parts.path


def prefix_local_urls(html):
    """Prefix only local URL attributes, leaving anchors and remote URLs intact."""
    if not BASE_PATH:
        return html
    return re.sub(
        r'\b(href|src|action)="(/(?!/)[^"]*)"',
        lambda match: f'{match[1]}="{BASE_PATH}{match[2]}"',
        html,
    )
