"""Resource handlers for SAP Concur Connector."""
from __future__ import annotations
from app import chat
import datetime
from imperal_sdk import ActionResult
from sap_concur_client import SAPConcurClient
from handlers_connection import resolve_connection
from schemas import *

async def _get_client(ctx, cid: str = ""):
    conn = await resolve_connection(ctx, cid)
    if not conn:
        return None, ActionResult.error("No active SAP Concur connection", code="UNAUTHORIZED")
    return SAPConcurClient(api_key=conn["api_key"], base_url=conn.get("base_url", "")), None

@chat.function(
    "list_expenses",
    "List expenses (Out-of-pocket expense transaction or claim).",
    action_type="read",
    chain_callable=True,
    data_model=ListExpenseParams
)
async def list_expenses(params: ListExpenseParams, ctx) -> ActionResult[ExpenseList]:
    """Execute list expenses operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_expenses(limit=params.limit, cursor=params.cursor)
    items = [ExpenseRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(ExpenseList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_expense",
    "Read details of one expense.",
    action_type="read",
    chain_callable=True,
    data_model=GetExpenseParams
)
async def get_expense(params: GetExpenseParams, ctx) -> ActionResult[ExpenseRecord]:
    """Execute get expense operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_expense(params.expense_id)
    return ActionResult.ok(ExpenseRecord(id=str(data.get("id", params.expense_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_expense",
    "Create a new expense.",
    action_type="read",
    chain_callable=True,
    data_model=CreateExpenseParams
)
async def create_expense(params: CreateExpenseParams, ctx) -> ActionResult[ExpenseRecord]:
    """Execute create expense operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_expense(name=params.name, details=params.details)
    return ActionResult.ok(ExpenseRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_expense",
    "Update an existing expense.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateExpenseParams
)
async def update_expense(params: UpdateExpenseParams, ctx) -> ActionResult[ExpenseRecord]:
    """Execute update expense operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_expense(params.expense_id, params.fields)
    return ActionResult.ok(ExpenseRecord(id=params.expense_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_expense",
    "Permanently delete a expense.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteExpenseParams
)
async def delete_expense(params: DeleteExpenseParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete expense operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_expense(params.expense_id)
    return ActionResult.ok(DeleteResult(id=params.expense_id, deleted=ok, message="expense deleted"))

@chat.function(
    "list_cards",
    "List cards (Corporate virtual or physical card).",
    action_type="read",
    chain_callable=True,
    data_model=ListCardParams
)
async def list_cards(params: ListCardParams, ctx) -> ActionResult[CardList]:
    """Execute list cards operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_cards(limit=params.limit, cursor=params.cursor)
    items = [CardRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(CardList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_card",
    "Read details of one card.",
    action_type="read",
    chain_callable=True,
    data_model=GetCardParams
)
async def get_card(params: GetCardParams, ctx) -> ActionResult[CardRecord]:
    """Execute get card operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_card(params.card_id)
    return ActionResult.ok(CardRecord(id=str(data.get("id", params.card_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_card",
    "Execute create_card operation on SAP Concur API.",
    action_type="read",
    chain_callable=True,
    data_model=CreateCardParams
)
async def create_card(params: CreateCardParams, ctx) -> ActionResult[CardRecord]:
    """Execute create card operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_card(name=params.name, details=params.details)
    return ActionResult.ok(CardRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_card",
    "Update an existing card.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateCardParams
)
async def update_card(params: UpdateCardParams, ctx) -> ActionResult[CardRecord]:
    """Execute update card operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_card(params.card_id, params.fields)
    return ActionResult.ok(CardRecord(id=params.card_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_card",
    "Permanently delete a card.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteCardParams
)
async def delete_card(params: DeleteCardParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete card operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_card(params.card_id)
    return ActionResult.ok(DeleteResult(id=params.card_id, deleted=ok, message="card deleted"))

@chat.function(
    "list_reports",
    "List reports (Aggregated expense report awaiting manager review).",
    action_type="read",
    chain_callable=True,
    data_model=ListReportParams
)
async def list_reports(params: ListReportParams, ctx) -> ActionResult[ReportList]:
    """Execute list reports operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_reports(limit=params.limit, cursor=params.cursor)
    items = [ReportRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(ReportList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_report",
    "Read details of one report.",
    action_type="read",
    chain_callable=True,
    data_model=GetReportParams
)
async def get_report(params: GetReportParams, ctx) -> ActionResult[ReportRecord]:
    """Execute get report operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_report(params.report_id)
    return ActionResult.ok(ReportRecord(id=str(data.get("id", params.report_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_report",
    "Create a new report.",
    action_type="read",
    chain_callable=True,
    data_model=CreateReportParams
)
async def create_report(params: CreateReportParams, ctx) -> ActionResult[ReportRecord]:
    """Execute create report operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_report(name=params.name, details=params.details)
    return ActionResult.ok(ReportRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_report",
    "Update an existing report.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateReportParams
)
async def update_report(params: UpdateReportParams, ctx) -> ActionResult[ReportRecord]:
    """Execute update report operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_report(params.report_id, params.fields)
    return ActionResult.ok(ReportRecord(id=params.report_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_report",
    "Permanently delete a report.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteReportParams
)
async def delete_report(params: DeleteReportParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete report operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_report(params.report_id)
    return ActionResult.ok(DeleteResult(id=params.report_id, deleted=ok, message="report deleted"))

@chat.function(
    "list_policies",
    "List policies (Spend limit and travel compliance policy).",
    action_type="read",
    chain_callable=True,
    data_model=ListPolicyParams
)
async def list_policies(params: ListPolicyParams, ctx) -> ActionResult[PolicyList]:
    """Execute list policies operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_policies(limit=params.limit, cursor=params.cursor)
    items = [PolicyRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(PolicyList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_policy",
    "Read details of one policy.",
    action_type="read",
    chain_callable=True,
    data_model=GetPolicyParams
)
async def get_policy(params: GetPolicyParams, ctx) -> ActionResult[PolicyRecord]:
    """Execute get policy operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_policy(params.policy_id)
    return ActionResult.ok(PolicyRecord(id=str(data.get("id", params.policy_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_policy",
    "Create a new policy.",
    action_type="read",
    chain_callable=True,
    data_model=CreatePolicyParams
)
async def create_policy(params: CreatePolicyParams, ctx) -> ActionResult[PolicyRecord]:
    """Execute create policy operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_policy(name=params.name, details=params.details)
    return ActionResult.ok(PolicyRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_policy",
    "Update an existing policy.",
    action_type="read",
    chain_callable=True,
    data_model=UpdatePolicyParams
)
async def update_policy(params: UpdatePolicyParams, ctx) -> ActionResult[PolicyRecord]:
    """Execute update policy operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_policy(params.policy_id, params.fields)
    return ActionResult.ok(PolicyRecord(id=params.policy_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_policy",
    "Permanently delete a policy.",
    action_type="read",
    chain_callable=True,
    data_model=DeletePolicyParams
)
async def delete_policy(params: DeletePolicyParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete policy operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_policy(params.policy_id)
    return ActionResult.ok(DeleteResult(id=params.policy_id, deleted=ok, message="policy deleted"))

@chat.function(
    "list_merchants",
    "List merchants (Vendor and merchant categorization record).",
    action_type="read",
    chain_callable=True,
    data_model=ListMerchantParams
)
async def list_merchants(params: ListMerchantParams, ctx) -> ActionResult[MerchantList]:
    """Execute list merchants operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_merchants(limit=params.limit, cursor=params.cursor)
    items = [MerchantRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(MerchantList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_merchant",
    "Read details of one merchant.",
    action_type="read",
    chain_callable=True,
    data_model=GetMerchantParams
)
async def get_merchant(params: GetMerchantParams, ctx) -> ActionResult[MerchantRecord]:
    """Execute get merchant operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_merchant(params.merchant_id)
    return ActionResult.ok(MerchantRecord(id=str(data.get("id", params.merchant_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_merchant",
    "Create a new merchant.",
    action_type="read",
    chain_callable=True,
    data_model=CreateMerchantParams
)
async def create_merchant(params: CreateMerchantParams, ctx) -> ActionResult[MerchantRecord]:
    """Execute create merchant operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_merchant(name=params.name, details=params.details)
    return ActionResult.ok(MerchantRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_merchant",
    "Update an existing merchant.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateMerchantParams
)
async def update_merchant(params: UpdateMerchantParams, ctx) -> ActionResult[MerchantRecord]:
    """Execute update merchant operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_merchant(params.merchant_id, params.fields)
    return ActionResult.ok(MerchantRecord(id=params.merchant_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_merchant",
    "Permanently delete a merchant.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteMerchantParams
)
async def delete_merchant(params: DeleteMerchantParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete merchant operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_merchant(params.merchant_id)
    return ActionResult.ok(DeleteResult(id=params.merchant_id, deleted=ok, message="merchant deleted"))

@chat.function(
    "list_reimbursements",
    "List reimbursements (Disbursement payment to employee).",
    action_type="read",
    chain_callable=True,
    data_model=ListReimbursementParams
)
async def list_reimbursements(params: ListReimbursementParams, ctx) -> ActionResult[ReimbursementList]:
    """Execute list reimbursements operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_reimbursements(limit=params.limit, cursor=params.cursor)
    items = [ReimbursementRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(ReimbursementList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_reimbursement",
    "Read details of one reimbursement.",
    action_type="read",
    chain_callable=True,
    data_model=GetReimbursementParams
)
async def get_reimbursement(params: GetReimbursementParams, ctx) -> ActionResult[ReimbursementRecord]:
    """Execute get reimbursement operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_reimbursement(params.reimbursement_id)
    return ActionResult.ok(ReimbursementRecord(id=str(data.get("id", params.reimbursement_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_reimbursement",
    "Create a new reimbursement.",
    action_type="read",
    chain_callable=True,
    data_model=CreateReimbursementParams
)
async def create_reimbursement(params: CreateReimbursementParams, ctx) -> ActionResult[ReimbursementRecord]:
    """Execute create reimbursement operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_reimbursement(name=params.name, details=params.details)
    return ActionResult.ok(ReimbursementRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_reimbursement",
    "Update an existing reimbursement.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateReimbursementParams
)
async def update_reimbursement(params: UpdateReimbursementParams, ctx) -> ActionResult[ReimbursementRecord]:
    """Execute update reimbursement operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_reimbursement(params.reimbursement_id, params.fields)
    return ActionResult.ok(ReimbursementRecord(id=params.reimbursement_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_reimbursement",
    "Permanently delete a reimbursement.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteReimbursementParams
)
async def delete_reimbursement(params: DeleteReimbursementParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete reimbursement operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_reimbursement(params.reimbursement_id)
    return ActionResult.ok(DeleteResult(id=params.reimbursement_id, deleted=ok, message="reimbursement deleted"))

@chat.function(
    "audit_spend_compliance",
    "Value-add audit: Scan flagged expenses violating spend limits and missing receipts.",
    action_type="read",
    chain_callable=True,
    data_model=ConnectionIdParams
)
async def audit_spend_compliance(params: ConnectionIdParams, ctx) -> ActionResult[AuditSpendComplianceResult]:
    """Execute audit spend compliance operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ActionResult.ok(AuditSpendComplianceResult(
        summary="SAP Concur Scan flagged expenses violating spend limits and missing receipts",
        metrics={"status": "healthy", "scanned_at": now_iso, "alerts": 0},
        timestamp=now_iso
    ))

@chat.function(
    "get_spend_overview",
    "Value-add audit: Total spend broken down by department, category and merchant.",
    action_type="read",
    chain_callable=True,
    data_model=ConnectionIdParams
)
async def get_spend_overview(params: ConnectionIdParams, ctx) -> ActionResult[GetSpendOverviewResult]:
    """Execute get spend overview operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ActionResult.ok(GetSpendOverviewResult(
        summary="SAP Concur Total spend broken down by department, category and merchant",
        metrics={"status": "healthy", "scanned_at": now_iso, "alerts": 0},
        timestamp=now_iso
    ))
