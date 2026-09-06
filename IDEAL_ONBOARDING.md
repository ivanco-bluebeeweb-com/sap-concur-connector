# SAP Concur Connector — Ideal Onboarding Experience

1. **Prerequisites**:
   - Access to SAP Concur App Center or Company Administration portal.
   - Company Web Services permissions enabled.
2. **Obtaining Credentials**:
   - Create a Company App in SAP Concur Developer Portal or obtain a Company Request Token.
   - Exchange for a long-lived Access Token or use the provisioned API Bearer Token.
3. **Connecting in Imperal**:
   - Open SAP Concur Connector sidebar.
   - Enter an optional connection label and paste the Bearer/Access Token.
   - Click **Connect SAP Concur**.
4. **Verification**:
   - Imperal runs automated handshake with `/profile/identity/v4/Users/me` and confirms tenant readiness.
