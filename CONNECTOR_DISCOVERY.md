# SAP Concur Connector — Connector Discovery

## Target System Overview
- **System Name:** SAP Concur
- **Category:** C29. Expense Management & Corporate Cards
- **API Protocol:** RESTful JSON APIs (v4)
- **Official Documentation:** `developer.concur.com` / `us.api.concursolutions.com`

## Authentication & Security
- **Auth Type:** OAuth2 Bearer Token / API Access Token
- **Headers:** `Authorization: Bearer <token>`, `Accept: application/json`
- **Security Guardrails:**
  - Zero hardcoded credentials in codebase.
  - Safe error masking preventing token exposure in logs and tool returns.
  - Granular multi-tenant isolation with unique `connection_id`.

## Object Model Mapping
- **Expenses:** `GET/POST/PUT/DELETE /expensereports/v4/expenses`
- **Cards:** `GET/POST/PUT/DELETE /payment/v4/cards`
- **Reports:** `GET/POST/PUT/DELETE /expensereports/v4/reports`
- **Policies:** `GET/POST/PUT/DELETE /expense/v4/policies`
- **Merchants:** `GET/POST/PUT/DELETE /receipts/v4/merchants`
- **Reimbursements:** `GET/POST/PUT/DELETE /expensereports/v4/reimbursements`
- **Compliance & Auditing:** Automated detection of non-compliant claims and expense pattern audits.
