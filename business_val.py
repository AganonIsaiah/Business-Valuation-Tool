import numpy as np
from scipy.stats import norm
import json

class BusinessValuation:
    def __init__(self, cash_flows, discount_rate):
        self.cash_flows = cash_flows
        self.discount_rate = discount_rate

    def to_dict(self):
        return {
            'cash_flows': self.cash_flows,
            'discount_rate': self.discount_rate
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(data['cash_flows'], data['discount_rate'])

    def calculate_present_value(self):
        present_value = 0

        for i in range(1, len(self.cash_flows) + 1):
            discounted_cash_flow = self.cash_flows[i - 1] / ((1 + self.discount_rate) ** i)
            present_value += discounted_cash_flow

        return present_value

    def monte_carlo_simulation(self, num_simulations, custom_cash_flows=None):
        if custom_cash_flows is None:
            custom_cash_flows = self.cash_flows

        # Perform Monte Carlo simulation to model uncertainty
        simulations = np.random.normal(loc=1, scale=0.1, size=(num_simulations, len(custom_cash_flows)))
        simulated_cash_flows = [custom_cash_flows * simulation for simulation in simulations.T]
        simulated_present_values = [sum(cf / (1 + self.discount_rate)**i for i, cf in enumerate(simulated_cf)) for simulated_cf in simulated_cash_flows]
        return simulated_present_values

    def sensitivity_analysis(self, discount_rate_range, cash_flows_range, num_points=10, custom_cash_flows=None):
        if custom_cash_flows is None:
            custom_cash_flows = self.cash_flows

        # Perform sensitivity analysis and return results
        discount_rate_values = np.linspace(*discount_rate_range, num=num_points)
        cash_flows_values = np.linspace(*cash_flows_range, num=num_points)

        sensitivity_results = []

        for rate in discount_rate_values:
            for flows in cash_flows_values:
                present_value = self.calculate_present_value()
                sensitivity_results.append({
                    'Discount Rate': rate,
                    'Cash Flows': flows,
                    'Present Value': present_value
                })

        return sensitivity_results
    

    def scenario_analysis(self, scenarios):
        scenario_results = []

        for scenario in scenarios:
            discount_rate = scenario['discount_rate']
            cash_flows = scenario['cash_flows']

            # Create an instance of the BusinessValuation class for the current scenario
            scenario_instance = BusinessValuation(cash_flows, discount_rate)

            # Calculate present value for the current scenario
            present_value = scenario_instance.calculate_present_value()

            # Store scenario results
            scenario_result = {
                'Discount Rate': discount_rate,
                'Cash Flows': cash_flows,
                'Present Value': present_value
            }

            scenario_results.append(scenario_result)

        return scenario_results

    def generate_valuation_report(self):
        report = f"Valuation Report\n\n"
        report += f"Assumptions:\n- Discount Rate: {self.discount_rate:.2%}\n- Cash Flows: {', '.join(map(str, self.cash_flows))}\n\n"
        
        present_value = self.calculate_present_value()
        report += f"Key Metrics:\n- Present Value: {present_value:.2f}\n\n"
        
        report += "Summary:\n- The business valuation was conducted using a discounted cash flow analysis, taking into account the provided assumptions."

        return report
