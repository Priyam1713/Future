"""Explicit one-time download; chart calculation never accesses the network."""
from pathlib import Path
from urllib.request import urlretrieve
import hashlib
path = Path(__file__).resolve().parents[1]/'data/de440s.bsp'
path.parent.mkdir(exist_ok=True)
if not path.exists():
    urlretrieve('https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de440s.bsp',path)
print(hashlib.sha256(path.read_bytes()).hexdigest(), path)
