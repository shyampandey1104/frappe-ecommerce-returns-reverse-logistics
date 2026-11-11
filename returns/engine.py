"""Reverse Logistics RMA Generation, Warehouse Quality Inspection & Automated Refund Engine."""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ReturnRequest(BaseModel):
    rma_number: str
    original_order_id: str
    customer_id: str
    customer_name: str
    sku: str
    quantity: int
    item_unit_price: float
    return_reason: str  # DEFECTIVE, WRONG_ITEM_SHIPPED, SIZE_NOT_FITTING, BUYER_REMORSE
    return_type: str    # CUSTOMER_RETURN or UNDELIVERED_RTO (Return to Origin)
    status: str = "PICKUP_SCHEDULED"  # PICKUP_SCHEDULED, IN_TRANSIT, RECEIVED_AT_HUB, QC_COMPLETED, REFUNDED


class QualityInspectionRecord(BaseModel):
    inspection_id: str
    rma_number: str
    sku: str
    tested_condition: str  # PRISTINE_SEALED, MINOR_COSMETIC_DAMAGE, BROKEN_DAMAGED, COUNTERFEIT_SWAPPED
    disposition_grade: str # RESTOCKABLE_GRADE_A, REFURBISH_OUTLET_GRADE_B, WRITE_OFF_SCRAP, FRAUD_REJECT
    restock_warehouse: Optional[str] = None
    approved_refund_amount: float
    inspector_notes: str


class ReverseLogisticsEngine:
    """Manages e-commerce return merchandise authorizations, returns QC grading, and refund vouchers."""

    def __init__(self):
        self.returns_db: Dict[str, ReturnRequest] = {}
        self.inspections: Dict[str, QualityInspectionRecord] = {}

    def initiate_return_request(
        self,
        order_id: str,
        customer_id: str,
        customer_name: str,
        sku: str,
        quantity: int,
        unit_price: float,
        reason: str,
        return_type: str = "CUSTOMER_RETURN"
    ) -> ReturnRequest:
        rma = f"RMA-{uuid.uuid4().hex[:8].upper()}"
        req = ReturnRequest(
            rma_number=rma,
            original_order_id=order_id,
            customer_id=customer_id,
            customer_name=customer_name,
            sku=sku,
            quantity=quantity,
            item_unit_price=unit_price,
            return_reason=reason,
            return_type=return_type,
            status="PICKUP_SCHEDULED"
        )
        self.returns_db[rma] = req
        return req

    def process_warehouse_quality_inspection(
        self,
        rma_number: str,
        condition: str,
        inspector_notes: str = "Standard QC verified"
    ) -> QualityInspectionRecord:
        req = self.returns_db.get(rma_number)
        if not req:
            raise ValueError(f"RMA {rma_number} not found.")

        total_paid = req.quantity * req.item_unit_price

        # Disposition Grading Logic:
        # Pristine / Undelivered RTO -> 100% Refund, Restock in Primary WH
        # Minor cosmetic / opened box -> 100% Refund to customer, Restock to Clearance/Outlet WH
        # Counterfeit / Swapped item -> 0% Refund, Fraud rejection
        # Broken / Damaged by user -> 0% to Partial
        cond_upper = condition.upper()
        if cond_upper in ("PRISTINE_SEALED", "UNOPENED_RTO"):
            disp = "RESTOCKABLE_GRADE_A"
            refund = total_paid
            target_wh = "Finished Goods - Main Warehouse"
        elif cond_upper == "MINOR_COSMETIC_DAMAGE":
            disp = "REFURBISH_OUTLET_GRADE_B"
            refund = total_paid
            target_wh = "Factory Outlet - Clearance Store"
        elif cond_upper == "COUNTERFEIT_SWAPPED":
            disp = "FRAUD_REJECT"
            refund = 0.0
            target_wh = None
        else:  # BROKEN_DAMAGED
            disp = "WRITE_OFF_SCRAP"
            refund = total_paid if req.return_reason == "DEFECTIVE" else 0.0
            target_wh = "Scrap & Disposal Store"

        insp_id = f"QC-{uuid.uuid4().hex[:8].upper()}"
        record = QualityInspectionRecord(
            inspection_id=insp_id,
            rma_number=rma_number,
            sku=req.sku,
            tested_condition=cond_upper,
            disposition_grade=disp,
            restock_warehouse=target_wh,
            approved_refund_amount=round(refund, 2),
            inspector_notes=inspector_notes
        )
        self.inspections[rma_number] = record

        req.status = "QC_COMPLETED" if refund == 0 else "REFUNDED"
        return record
