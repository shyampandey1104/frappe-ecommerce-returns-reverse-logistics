# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "returns"
app_title = "Frappe Ecommerce Returns Reverse Logistics"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Ecommerce Returns Reverse Logistics for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/returns/css/returns.bundle.css"
app_include_js = "/assets/returns/js/returns.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "returns.engine.on_document_submit",
        "on_cancel": "returns.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "returns.engine.daily_scheduled_sync"
    ]
}
