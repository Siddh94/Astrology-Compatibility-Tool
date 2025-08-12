import os
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st  # type: ignore
    SECRETS = dict(st.secrets) if hasattr(st, "secrets") else {}
except Exception:  # pragma: no cover
    SECRETS = {}


def _get_config_value(key: str, default: str | None = None) -> str | None:
    if key in SECRETS:
        return str(SECRETS.get(key))
    return os.getenv(key, default)


# Google API Key
GOOGLE_API_KEY = _get_config_value("GOOGLE_API_KEY")

# AWS S3 Config
AWS_ACCESS_KEY = _get_config_value("AWS_ACCESS_KEY")
AWS_SECRET_KEY = _get_config_value("AWS_SECRET_KEY")
S3_BUCKET = _get_config_value("S3_BUCKET")
REGION = _get_config_value("REGION")
