from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote

import requests

from reco_engine.core.errors import ExternalServiceError


@dataclass(frozen=True)
class HAConnection:
    base_url: str
    token: str
    timeout_seconds: int = 20


class HAClient:
    def __init__(self, connection: HAConnection):
        self._conn = connection
        self._headers = {
            "Authorization": f"Bearer {self._conn.token}",
            "Content-Type": "application/json",
        }

    def _url(self, path: str) -> str:
        return f"{self._conn.base_url.rstrip('/')}{path}"

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        try:
            response = requests.request(
                method=method,
                url=self._url(path),
                headers=self._headers,
                timeout=self._conn.timeout_seconds,
                **kwargs,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            raise ExternalServiceError(f"Home Assistant API call failed: {method} {path}") from exc

    def fetch_states(self) -> list[dict[str, Any]]:
        payload = self._request("GET", "/api/states")
        if not isinstance(payload, list):
            raise ExternalServiceError("Unexpected /api/states response shape")
        return payload

    def fetch_state(self, entity_id: str) -> dict[str, Any]:
        payload = self._request("GET", f"/api/states/{entity_id}")
        if not isinstance(payload, dict):
            raise ExternalServiceError("Unexpected /api/states/<entity_id> response shape")
        return payload

    def fetch_logbook(
        self,
        start_time: datetime,
        end_time: datetime,
    ) -> list[dict[str, Any]]:
        if end_time <= start_time:
            raise ValueError("end_time must be later than start_time")
        start_token = quote(_to_utc_iso(start_time), safe="")
        end_token = quote(_to_utc_iso(end_time), safe="")
        path = f"/api/logbook/{start_token}?end_time={end_token}"
        payload = self._request("GET", path)
        if not isinstance(payload, list):
            raise ExternalServiceError("Unexpected logbook response shape")
        return payload

    def fetch_history(
        self,
        start_time: datetime,
        end_time: datetime,
        entity_ids: list[str],
    ) -> list[Any]:
        if not entity_ids:
            raise ValueError("entity_ids must not be empty")
        if end_time <= start_time:
            raise ValueError("end_time must be later than start_time")
        ids = quote(",".join(entity_ids), safe=",")
        start_token = quote(_to_utc_iso(start_time), safe="")
        end_token = quote(_to_utc_iso(end_time), safe="")
        path = (
            f"/api/history/period/{start_token}?"
            f"end_time={end_token}&filter_entity_id={ids}"
        )
        payload = self._request("GET", path)
        if not isinstance(payload, list):
            raise ExternalServiceError("Unexpected history response shape")
        return payload


def _to_utc_iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()
