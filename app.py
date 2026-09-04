"""Extension declaration, capabilities, health check for SAP Concur Connector."""
from __future__ import annotations
import json
from imperal_sdk import ChatExtension, Extension

ext = Extension(
    "sap-concur-connector",
    version="0.1.0",
    display_name="SAP Concur",
    icon="icon.svg",
    capabilities=["sap_concur:manage"],
    description="Official Imperal connector for SAP Concur (C29. Expense Management & Corporate Cards). Manage operations securely."
)

chat = ChatExtension(ext)

@ext.health_check
async def health_check(ctx) -> dict:
    raw = await ctx.secrets.get("sap_concur_connections")
    try:
        count = len(json.loads(raw)) if raw else 0
    except Exception:
        count = 0
    return {
        "healthy": True,
        "detail": f"{count} SAP Concur connection(s) configured." if count else "Not connected yet."
    }
