import urllib.parse
from typing import Optional


def build_quicklink(aff_code: str, dest_url: str, unique: Optional[str] = None) -> str:
    base = "https://event.2performant.com/events/click"
    params = {
        "ad_type": "quicklink",
        "aff_code": aff_code,
        "redirect_to": urllib.parse.quote(dest_url, safe=""),
    }
    if unique:
        params["unique"] = unique
    order = ["ad_type", "aff_code", "unique", "redirect_to"]
    parts = [f"{k}={params[k]}" for k in order if k in params]
    return f"{base}?" + "&".join(parts)

