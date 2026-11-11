# Frappe E-Commerce Returns & Reverse Logistics 🔄📦

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Frappe](https://img.shields.io/badge/Frappe-v14%20%7C%20v15-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

An enterprise Return Merchandise Authorization (RMA), Return-to-Origin (RTO) analytics, warehouse quality inspection grading, and automated customer refund engine for **Frappe Framework & ERPNext E-Commerce**.

---

## 🚀 Key Features

- **Automated RMA & Reverse Pickup**: Generates trackable RMA barcodes and synchronizes courier reverse manifests.
- **RTO (Return To Origin) Inwarding**: Differentiates between non-delivery buyer rejections and voluntary customer returns.
- **Warehouse Quality Grading Matrix**: Categorizes inspected returns into `RESTOCKABLE_GRADE_A`, `REFURBISH_OUTLET_GRADE_B`, or `WRITE_OFF_SCRAP`.
- **Anti-Fraud Swap Protection**: Flags counterfeit, dummy item, or weight tampering attempts to block fraudulent customer refunds.

---

## 📦 Installation & Setup

```bash
git clone https://github.com/shyampandey1104/frappe-ecommerce-returns-reverse-logistics.git
cd frappe-ecommerce-returns-reverse-logistics
pip install -r requirements.txt
```

---

## 🛠️ Usage Example

```python
from returns.engine import ReverseLogisticsEngine

engine = ReverseLogisticsEngine()

# Initiate RMA
rma = engine.initiate_return_request(
    order_id="ECOM-1002",
    customer_id="CUST-404",
    customer_name="Aakash Nair",
    sku="COTTON-SHIRT-M",
    quantity=1,
    unit_price=1499.0,
    reason="SIZE_NOT_FITTING"
)

# Hub QC Verification
qc = engine.process_warehouse_quality_inspection(rma.rma_number, condition="PRISTINE_SEALED")
print(f"Grade: {qc.disposition_grade} | Restock WH: {qc.restock_warehouse} | Refund: ₹{qc.approved_refund_amount}")
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📄 License
MIT License. Created with ❤️ by [Shyam Pandey](https://github.com/shyampandey1104).
