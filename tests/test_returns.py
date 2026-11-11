import unittest
from returns.engine import ReverseLogisticsEngine


class TestReverseLogisticsEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ReverseLogisticsEngine()

    def test_pristine_return_and_restock(self):
        req = self.engine.initiate_return_request(
            order_id="ORD-991", customer_id="C-101", customer_name="Meera Joshi",
            sku="RUNNING-SHOES-8", quantity=1, unit_price=2499.0,
            reason="SIZE_NOT_FITTING"
        )
        self.assertEqual(req.status, "PICKUP_SCHEDULED")

        # Warehouse QC confirms unopened box
        qc = self.engine.process_warehouse_quality_inspection(
            rma_number=req.rma_number, condition="PRISTINE_SEALED"
        )
        self.assertEqual(qc.disposition_grade, "RESTOCKABLE_GRADE_A")
        self.assertEqual(qc.approved_refund_amount, 2499.0)
        self.assertEqual(qc.restock_warehouse, "Finished Goods - Main Warehouse")
        self.assertEqual(self.engine.returns_db[req.rma_number].status, "REFUNDED")

    def test_counterfeit_swap_fraud_rejection(self):
        req = self.engine.initiate_return_request(
            order_id="ORD-992", customer_id="C-102", customer_name="Scam Buyer",
            sku="SMARTPHONE-PRO", quantity=1, unit_price=69999.0,
            reason="DEFECTIVE"
        )
        # Warehouse QC detects soap bar / fake replica swapped inside box
        qc = self.engine.process_warehouse_quality_inspection(
            rma_number=req.rma_number, condition="COUNTERFEIT_SWAPPED", inspector_notes="Dummy dummy weight dummy unit"
        )
        self.assertEqual(qc.disposition_grade, "FRAUD_REJECT")
        self.assertEqual(qc.approved_refund_amount, 0.0)


if __name__ == "__main__":
    unittest.main()
