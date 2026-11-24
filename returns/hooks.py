# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "returns"
app_title = "Frappe Ecommerce Returns Reverse Logistics"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Ecommerce Returns Reverse Logistics - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/returns/css/returns.bundle.css"
app_include_js = "/assets/returns/js/returns.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Frappe Ecommerce Returns Reverse Logistics Entry": {
        "validate": "returns.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "returns.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "returns.tasks.hourly_sync"
    ],
    "daily": [
        "returns.tasks.daily_reconciliation"
    ],
    "weekly": [
        "returns.tasks.weekly_digest"
    ]
}
