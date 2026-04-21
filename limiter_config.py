"""
limiter_config.py

Provides route-level rate limiting.
No global limits are applied.
Each endpoint defines its own limits.
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Limiter without default limits
limiter = Limiter(key_func=get_remote_address)

def init_limiter(app):
    limiter.init_app(app)