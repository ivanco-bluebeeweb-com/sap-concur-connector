# SAP Concur Connector — Preparation

## Product Scope
Build a comprehensive Imperal connector for **SAP Concur** under category **C29. Expense Management & Corporate Cards**. The integration connects directly to the official **SAP Concur REST APIs** (`https://us.api.concursolutions.com`), enabling full visibility and governance across corporate credit cards, expense reports, line item expenses, spend policies, merchant categorization, employee reimbursements, and automated compliance auditing.

## Official API Specifications
- **API Architecture:** RESTful JSON API
- **Base URL:** `https://us.api.concursolutions.com`
- **Core Endpoints:**
  - `GET /profile/identity/v4/Users/me` — verify token privileges and company context
  - `GET /expensereports/v4/reports` — list expense reports with cursor pagination
  - `GET /expensereports/v4/reports/{id}` — detailed single expense report
  - `GET /expensereports/v4/expenses` — line item expense entries
  - `GET /payment/v4/cards` — corporate virtual and physical cards
  - `GET /expense/v4/policies` — compliance and expense limit policies
  - `GET /receipts/v4/merchants` — merchant classifications
  - `GET /expensereports/v4/reimbursements` — employee reimbursement disbursements
- **Authentication Model:** Bearer Token via `Authorization: Bearer <api_key>` (OAuth2 Access Token)
- **Mandatory Requirements:**
  - Strict error classification: HTTP 429 rate limits with Retry-After extraction, HTTP 401/403 differentiation (Standard B8/B10).
  - Sanitization of Bearer tokens in error traces and diagnostic payloads (Standard B8).
  - Multi-tenant connection tracking and isolation via `connection_id` (Standard B9).

## Delivery Gates
1. [x] Official API discovery completed with SAP Concur REST API specifications.
2. [x] Core resource endpoints and Bearer auth verified.
3. [x] Five mandatory specification documents authored.
4. [x] Client implemented with B8-B10 compliance, secret redaction, and 429/401 classification.
5. [x] Panel sidebar implemented conforming to UI_INTERFACE_STANDARD.md.
6. [x] Verification of functions, imports, and compilation.
