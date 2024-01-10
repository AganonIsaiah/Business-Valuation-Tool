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

    def monte_carlo_simulation(self, num_simulations):
        # Perform Monte Carlo simulation to model uncertainty
        simulations = np.random.normal(loc=1, scale=0.1, size=(num_simulations, len(self.cash_flows)))
        simulated_cash_flows = [self.cash_flows * simulation for simulation in simulations.T]
        simulated_present_values = [sum(cf / (1 + self.discount_rate)**i for i, cf in enumerate(simulated_cf)) for simulated_cf in simulated_cash_flows]
        return simulated_present_values

    def sensitivity_analysis(self, discount_rate_range, cash_flows_range):
        # Perform sensitivity analysis and return results
        discount_rate_values = np.linspace(*discount_rate_range, num=100)
        cash_flows_values = np.linspace(*cash_flows_range, num=100)

        sensitivity_results = []

        for rate in discount_rate_values:
            for flows in cash_flows_values:
                present_value = self.calculate_present_value(discount_rate=rate, cash_flows=[flows] * len(self.cash_flows))
                sensitivity_results.append({
                    'Discount Rate': rate,
                    'Cash Flows': flows,
                    'Present Value': present_value
                })

        return sensitivity_results

    def generate_valuation_report(self):
        # Generate a comprehensive valuation report
        # Include details like assumptions, key metrics, and a summary of the analysis.
        report = f"Valuation Report\n\nAssumptions:\n- Discount Rate: {self.discount_rate}\n- Cash Flows: {self.cash_flows}\n\n"
        report += f"Key Metrics:\n- Present Value: {self.calculate_present_value()}\n\n"
        report += "Summary:\n- The business valuation was conducted using a discounted cash flow analysis, taking into account the provided assumptions."

        return report
