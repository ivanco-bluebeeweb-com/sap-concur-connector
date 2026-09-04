"""Pydantic schemas for SAP Concur Connector (C29. Expense Management & Corporate Cards)."""
from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field

class NoParams(BaseModel):
    """Empty parameter model."""
    pass

class ConnectParams(BaseModel):
    label: str = Field(default="", description="Friendly connection label, e.g. Acme SAP Concur.")
    api_key: str = Field(description="Corporate Expense API Key or OAuth Token.")
    base_url: str = Field(default="", description="Optional custom base URL or instance domain.")

class ConnectionIdParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier (empty uses active connection).")

class ConnectionRecord(BaseModel):
    id: str
    label: str
    masked_key: str
    base_url: str
    is_active: bool

class ConnectionList(BaseModel):
    connections: list[ConnectionRecord]
    total: int

class DeleteResult(BaseModel):
    id: str
    deleted: bool
    message: str

class ListExpenseParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetExpenseParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    expense_id: str = Field(description="Unique identifier of the expense.")

class CreateExpenseParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateExpenseParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    expense_id: str = Field(description="Unique identifier of the expense.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteExpenseParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    expense_id: str = Field(description="Unique identifier of the expense.")

class ExpenseRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class ExpenseList(BaseModel):
    items: list[ExpenseRecord]
    total: int
    next_cursor: Optional[str] = None

class ListCardParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetCardParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    card_id: str = Field(description="Unique identifier of the card.")

class CreateCardParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateCardParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    card_id: str = Field(description="Unique identifier of the card.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteCardParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    card_id: str = Field(description="Unique identifier of the card.")

class CardRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class CardList(BaseModel):
    items: list[CardRecord]
    total: int
    next_cursor: Optional[str] = None

class ListReportParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetReportParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    report_id: str = Field(description="Unique identifier of the report.")

class CreateReportParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateReportParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    report_id: str = Field(description="Unique identifier of the report.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteReportParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    report_id: str = Field(description="Unique identifier of the report.")

class ReportRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class ReportList(BaseModel):
    items: list[ReportRecord]
    total: int
    next_cursor: Optional[str] = None

class ListPolicyParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetPolicyParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    policy_id: str = Field(description="Unique identifier of the policy.")

class CreatePolicyParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdatePolicyParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    policy_id: str = Field(description="Unique identifier of the policy.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeletePolicyParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    policy_id: str = Field(description="Unique identifier of the policy.")

class PolicyRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class PolicyList(BaseModel):
    items: list[PolicyRecord]
    total: int
    next_cursor: Optional[str] = None

class ListMerchantParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetMerchantParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    merchant_id: str = Field(description="Unique identifier of the merchant.")

class CreateMerchantParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateMerchantParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    merchant_id: str = Field(description="Unique identifier of the merchant.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteMerchantParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    merchant_id: str = Field(description="Unique identifier of the merchant.")

class MerchantRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class MerchantList(BaseModel):
    items: list[MerchantRecord]
    total: int
    next_cursor: Optional[str] = None

class ListReimbursementParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetReimbursementParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    reimbursement_id: str = Field(description="Unique identifier of the reimbursement.")

class CreateReimbursementParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateReimbursementParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    reimbursement_id: str = Field(description="Unique identifier of the reimbursement.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteReimbursementParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    reimbursement_id: str = Field(description="Unique identifier of the reimbursement.")

class ReimbursementRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class ReimbursementList(BaseModel):
    items: list[ReimbursementRecord]
    total: int
    next_cursor: Optional[str] = None

class AuditSpendComplianceResult(BaseModel):
    summary: str
    metrics: dict[str, Any]
    timestamp: str

class GetSpendOverviewResult(BaseModel):
    summary: str
    metrics: dict[str, Any]
    timestamp: str
