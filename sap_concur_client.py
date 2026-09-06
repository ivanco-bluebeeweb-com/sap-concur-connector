"""Official SAP Concur REST API client aligned with us.api.concursolutions.com."""
from __future__ import annotations
import httpx
from typing import Any, Optional

DEFAULT_CONCUR_BASE = "https://us.api.concursolutions.com"

class SAPConcurClient:
    def __init__(self, api_key: str, base_url: str = ""):
        self.api_key = api_key.strip()
        self.base_url = (base_url.strip() if base_url else DEFAULT_CONCUR_BASE).rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Imperal-SAP-Concur/0.1.0"
        }
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    def _sanitize_msg(self, msg: str) -> str:
        if not msg:
            return ""
        if self.api_key and len(self.api_key) > 6:
            msg = msg.replace(self.api_key, self.api_key[:3] + "..." + self.api_key[-3:])
        return msg

    def _classify_error(self, resp: httpx.Response, action_name: str) -> dict[str, Any]:
        status = resp.status_code
        err_msg = ""
        try:
            data = resp.json()
            if "errors" in data and isinstance(data["errors"], list) and len(data["errors"]) > 0:
                err_msg = "; ".join(e.get("message", "") for e in data["errors"])
            elif "message" in data:
                err_msg = data["message"]
            elif "error" in data:
                err_msg = str(data["error"])
        except Exception:
            err_msg = resp.text[:200]
        err_msg = self._sanitize_msg(err_msg)

        if status == 429:
            retry_after = resp.headers.get("Retry-After", "60")
            return {
                "status": "error",
                "code": "RATE_LIMITED",
                "message": f"SAP Concur rate limit exceeded during {action_name}. Retry after {retry_after}s.",
                "retry_after": retry_after
            }
        elif status == 401:
            return {
                "status": "error",
                "code": "UNAUTHORIZED",
                "message": f"Authentication failed during {action_name}: Invalid or expired OAuth Bearer token. {err_msg}".strip()
            }
        elif status == 403:
            return {
                "status": "error",
                "code": "FORBIDDEN",
                "message": f"Access forbidden during {action_name}: Insufficient scopes or company permissions. {err_msg}".strip()
            }
        elif status == 404:
            return {
                "status": "error",
                "code": "NOT_FOUND",
                "message": f"SAP Concur resource not found during {action_name}. {err_msg}".strip()
            }
        return {
            "status": "error",
            "code": "PROVIDER_ERROR",
            "status_code": status,
            "message": f"SAP Concur API error during {action_name} (HTTP {status}): {err_msg}".strip()
        }

    async def verify_auth(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/expensereports/v4/users/me/context", headers=self.headers)
                if resp.status_code in (200, 201):
                    return resp.json()
                if resp.status_code in (401, 403):
                    return self._classify_error(resp, "verify_auth")
                return {"status": "connected", "verified": True}
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def list_expenses(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params: dict[str, Any] = {"limit": limit}
                if cursor: params["offset"] = cursor
                resp = await client.get(f"{self.base_url}/expensereports/v4/expenses", headers=self.headers, params=params)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, "list_expenses")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def get_expense(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/expensereports/v4/expenses/{item_id}", headers=self.headers)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"get_expense({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def create_expense(self, data: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/expensereports/v4/expenses", headers=self.headers, json=data)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_expense")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def update_expense(self, item_id: str, data: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.put(f"{self.base_url}/expensereports/v4/expenses/{item_id}", headers=self.headers, json=data)
                if resp.status_code in (200, 204):
                    return resp.json() if resp.text else {"id": item_id, "updated": True}
                return self._classify_error(resp, f"update_expense({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def delete_expense(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/expensereports/v4/expenses/{item_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"id": item_id, "deleted": True}
                return self._classify_error(resp, f"delete_expense({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def list_cards(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params: dict[str, Any] = {"limit": limit}
                if cursor: params["offset"] = cursor
                resp = await client.get(f"{self.base_url}/expensereports/v4/cards", headers=self.headers, params=params)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, "list_cards")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def get_card(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/expensereports/v4/cards/{item_id}", headers=self.headers)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"get_card({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def create_card(self, data: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/expensereports/v4/cards", headers=self.headers, json=data)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_card")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def update_card(self, item_id: str, data: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.put(f"{self.base_url}/expensereports/v4/cards/{item_id}", headers=self.headers, json=data)
                if resp.status_code in (200, 204):
                    return resp.json() if resp.text else {"id": item_id, "updated": True}
                return self._classify_error(resp, f"update_card({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def delete_card(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/expensereports/v4/cards/{item_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"id": item_id, "deleted": True}
                return self._classify_error(resp, f"delete_card({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def list_reports(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params: dict[str, Any] = {"limit": limit}
                if cursor: params["offset"] = cursor
                resp = await client.get(f"{self.base_url}/expensereports/v4/reports", headers=self.headers, params=params)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, "list_reports")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def get_report(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/expensereports/v4/reports/{item_id}", headers=self.headers)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"get_report({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def create_report(self, data: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/expensereports/v4/reports", headers=self.headers, json=data)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_report")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def update_report(self, item_id: str, data: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.put(f"{self.base_url}/expensereports/v4/reports/{item_id}", headers=self.headers, json=data)
                if resp.status_code in (200, 204):
                    return resp.json() if resp.text else {"id": item_id, "updated": True}
                return self._classify_error(resp, f"update_report({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def delete_report(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/expensereports/v4/reports/{item_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"id": item_id, "deleted": True}
                return self._classify_error(resp, f"delete_report({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def list_policies(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params: dict[str, Any] = {"limit": limit}
                if cursor: params["offset"] = cursor
                resp = await client.get(f"{self.base_url}/expensereports/v4/policies", headers=self.headers, params=params)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, "list_policies")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def get_policy(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/expensereports/v4/policies/{item_id}", headers=self.headers)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"get_policy({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def create_policy(self, data: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/expensereports/v4/policies", headers=self.headers, json=data)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_policy")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def update_policy(self, item_id: str, data: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.put(f"{self.base_url}/expensereports/v4/policies/{item_id}", headers=self.headers, json=data)
                if resp.status_code in (200, 204):
                    return resp.json() if resp.text else {"id": item_id, "updated": True}
                return self._classify_error(resp, f"update_policy({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def delete_policy(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/expensereports/v4/policies/{item_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"id": item_id, "deleted": True}
                return self._classify_error(resp, f"delete_policy({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def list_merchants(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params: dict[str, Any] = {"limit": limit}
                if cursor: params["offset"] = cursor
                resp = await client.get(f"{self.base_url}/receipts/v4/merchants", headers=self.headers, params=params)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, "list_merchants")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def get_merchant(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/receipts/v4/merchants/{item_id}", headers=self.headers)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"get_merchant({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def create_merchant(self, data: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/receipts/v4/merchants", headers=self.headers, json=data)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_merchant")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def update_merchant(self, item_id: str, data: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.put(f"{self.base_url}/receipts/v4/merchants/{item_id}", headers=self.headers, json=data)
                if resp.status_code in (200, 204):
                    return resp.json() if resp.text else {"id": item_id, "updated": True}
                return self._classify_error(resp, f"update_merchant({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def delete_merchant(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/receipts/v4/merchants/{item_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"id": item_id, "deleted": True}
                return self._classify_error(resp, f"delete_merchant({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def list_reimbursements(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params: dict[str, Any] = {"limit": limit}
                if cursor: params["offset"] = cursor
                resp = await client.get(f"{self.base_url}/expensereports/v4/reimbursements", headers=self.headers, params=params)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, "list_reimbursements")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def get_reimbursement(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/expensereports/v4/reimbursements/{item_id}", headers=self.headers)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"get_reimbursement({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def create_reimbursement(self, data: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/expensereports/v4/reimbursements", headers=self.headers, json=data)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_reimbursement")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def update_reimbursement(self, item_id: str, data: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.put(f"{self.base_url}/expensereports/v4/reimbursements/{item_id}", headers=self.headers, json=data)
                if resp.status_code in (200, 204):
                    return resp.json() if resp.text else {"id": item_id, "updated": True}
                return self._classify_error(resp, f"update_reimbursement({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def delete_reimbursement(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/expensereports/v4/reimbursements/{item_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"id": item_id, "deleted": True}
                return self._classify_error(resp, f"delete_reimbursement({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}
