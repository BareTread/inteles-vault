import os
import time
from typing import Dict, Any, List, Optional

import requests


class TwoPerformantClient:
    """
    Minimal 2Performant API client for affiliate usage.

    Auth flow:
      - POST /users/sign_in.json with {"user": {"email", "password"}}
      - Save access-token, client, uid from response headers
      - For each subsequent request, send headers and refresh tokens with new values
    """

    def __init__(self, base_url: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None, session: Optional[requests.Session] = None):
        self.base_url = (base_url or os.getenv("TWO_P_BASE") or "https://api.2performant.com").rstrip("/")
        self.email = email or os.getenv("TWO_P_EMAIL")
        self.password = password or os.getenv("TWO_P_PASSWORD")
        self.session = session or requests.Session()
        self.tokens: Dict[str, str] = {}

    def login(self) -> None:
        url = f"{self.base_url}/users/sign_in.json"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        # Try email first
        payload = {"user": {"email": self.email, "password": self.password}}
        r = self.session.post(url, json=payload, headers=headers, timeout=30)
        if r.status_code == 401:
            # Fallback: some accounts require 'login' instead of 'email'
            payload = {"user": {"login": self.email, "password": self.password}}
            r = self.session.post(url, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        self._update_tokens_from_response(r)

    def _update_tokens_from_response(self, r: requests.Response) -> None:
        for key in ["access-token", "client", "uid", "token-type", "expiry"]:
            val = r.headers.get(key)
            if val:
                self.tokens[key] = val

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        for k in ["access-token", "client", "uid"]:
            v = self.tokens.get(k)
            if v:
                headers[k] = v
        return headers

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        r = self.session.get(url, headers=self._headers(), params=params, timeout=60)
        self._update_tokens_from_response(r)
        r.raise_for_status()
        return r.json()

    def list_affiliate_programs(self, relation: Optional[str] = None, page: int = 1, per_page: int = 50) -> Dict[str, Any]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if relation:
            params["filter.relation"] = relation
        return self._get("/affiliate/programs.json", params=params)

    def list_all_affiliate_programs(self, relation: Optional[str] = None, per_page: int = 100) -> List[Dict[str, Any]]:
        page = 1
        results: List[Dict[str, Any]] = []
        while True:
            data = self.list_affiliate_programs(relation=relation, page=page, per_page=per_page)
            programs = data.get("programs") or data.get("data") or []
            if not programs:
                break
            results.extend(programs)
            meta = data.get("metadata") or data.get("meta") or {}
            pag = meta.get("pagination") if isinstance(meta, dict) else None
            pages = (pag or {}).get("pages") if pag else None
            if pages and page >= int(pages):
                break
            page += 1
            time.sleep(0.2)
        return results

    def list_advertiser_promotions(self, page: int = 1, per_page: int = 50, program_id: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if program_id is not None:
            params["filter.program_id"] = program_id
        return self._get("/affiliate/advertiser_promotions.json", params=params)
