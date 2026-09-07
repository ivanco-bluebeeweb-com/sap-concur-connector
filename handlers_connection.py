"""Connection lifecycle for SAP Concur Connector."""
from __future__ import annotations
import json, uuid
from imperal_sdk import ActionResult
from sap_concur_client import SAPConcurClient
from app import chat
from schemas import (
    NoParams,
    ConnectParams, ConnectionIdParams, ConnectionList, ConnectionRecord, DeleteResult
)

_SECRET = "sap_concur_connections"

def _mask(value: str) -> str:
    return value[:4] + "…" + value[-4:] if len(value) > 10 else "***"

async def _load_connections(ctx) -> list[dict]:
    raw = await ctx.secrets.get(_SECRET)
    if not raw: return []
    try: data = json.loads(raw)
    except: return []
    return data if isinstance(data, list) else []

async def _save_connections(ctx, conns: list[dict]) -> None:
    await ctx.secrets.set(_SECRET, json.dumps(conns))

async def resolve_connection(ctx, connection_id: str = "") -> dict | None:
    conns = await _load_connections(ctx)
    if not conns: return None
    if not connection_id:
        for c in conns:
            if c.get("is_active"):
                return c
        return conns[0]
    for c in conns:
        if c["id"] == connection_id:
            return c
    return None

@chat.function(
    "connect_sap_concur",
    "Connect SAP Concur account via credentials.",
    action_type="write",
    chain_callable=True,
    event="sap-concur-connector.connect_sap_concur",
    effects=["create:connection"],
    data_model=ConnectParams
)
async def connect_sap_concur(params: ConnectParams, ctx) -> ActionResult[ConnectionRecord]:
    """Execute connect_sap_concur lifecycle handler."""
    client = SAPConcurClient(api_key=params.api_key, base_url=params.base_url)
    await client.verify_auth()
    conns = await _load_connections(ctx)
    cid = f"conn_{uuid.uuid4().hex[:8]}"
    record = {
        "id": cid,
        "label": params.label or "SAP Concur Account",
        "api_key": params.api_key,
        "base_url": params.base_url,
        "is_active": True
    }
    for c in conns: c["is_active"] = False
    conns.append(record)
    await _save_connections(ctx, conns)
    return ActionResult.success(ConnectionRecord(id=cid, label=record["label"], masked_key=_mask(params.api_key), base_url=params.base_url, is_active=True), summary="Sap concur connected.")

@chat.function(
    "list_connections",
    "List connected SAP Concur accounts.",
    action_type="read",
    chain_callable=True,
    data_model=NoParams
)
async def list_connections(params: NoParams, ctx) -> ActionResult[ConnectionList]:
    """Execute list_connections lifecycle handler."""
    conns = await _load_connections(ctx)
    records = [ConnectionRecord(id=c["id"], label=c["label"], masked_key=_mask(c.get("api_key", "")), base_url=c.get("base_url", ""), is_active=c.get("is_active", False)) for c in conns]
    return ActionResult.success(ConnectionList(connections=records, total=len(records)), summary="Connections listed.")

@chat.function(
    "disconnect_sap_concur",
    "Disconnect SAP Concur account.",
    action_type="write",
    chain_callable=True,
    event="sap-concur-connector.disconnect_sap_concur",
    effects=["delete:connection"],
    data_model=ConnectionIdParams
)
async def disconnect_sap_concur(params: ConnectionIdParams, ctx) -> ActionResult[DeleteResult]:
    """Execute disconnect_sap_concur lifecycle handler."""
    conns = await _load_connections(ctx)
    target = await resolve_connection(ctx, params.connection_id)
    if not target:
        return ActionResult.error("Connection not found", code="NOT_FOUND")
    new_conns = [c for c in conns if c["id"] != target["id"]]
    if new_conns and target.get("is_active"):
        new_conns[0]["is_active"] = True
    await _save_connections(ctx, new_conns)
    return ActionResult.success(DeleteResult(id=target["id"], deleted=True, message="Disconnected successfully"), summary="Sap concur disconnected.")
