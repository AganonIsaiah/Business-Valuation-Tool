# business_val.py

import numpy as np

class BusinessValuation:
    def __init__(self, cash_flows, discount_rate):
        self.cash_flows = cash_flows
        self.discount_rate = discount_rate

    def calculate_present_value(self):
        # Calculate the discounted cash flows and present value
        discounted_cash_flows = [cf / (1 + self.discount_rate)**i for i, cf in enumerate(self.cash_flows)]
        present_value = sum(discounted_cash_flows)
        return present_value

    def generate_valuation_report(self):
        # Generate a comprehensive valuation report
        report = f"Valuation Report\n\nAssumptions:\n- Discount Rate: {self.discount_rate}\n- Cash Flows: {self.cash_flows}\n\n"
        report += f"Key Metrics:\n- Present Value: {self.calculate_present_value()}\n\n"
        report += "Summary:\n- The business valuation was conducted using a discounted cash flow analysis, taking into account the provided assumptions."

        return report
