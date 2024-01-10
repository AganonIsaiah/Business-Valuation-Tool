# main.py

from flask import Flask, render_template, request

# Import the BusinessValuation class from business_val.py
from business_val import BusinessValuation

# Import the generate_chart function from chart_gen.py
from chart_gen import generate_chart

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Extract user input from the form
            cash_flows = [float(request.form[f'cash_flow_{i}']) for i in range(1, 6)]
            discount_rate = float(request.form['discount_rate'])
            num_simulations = int(request.form['num_simulations'])
            discount_rate_range = [float(val) for val in request.form['sensitivity_rate_range'].split(',')]
            cash_flows_range = [float(val) for val in request.form['sensitivity_flows_range'].split(',')]

            # Create an instance of the BusinessValuation class
            business_valuation_instance = BusinessValuation(cash_flows, discount_rate)
            
            # Perform the DCF analysis
            present_value_result = business_valuation_instance.calculate_present_value()

            # Perform Monte Carlo simulation
            simulated_values = business_valuation_instance.monte_carlo_simulation(num_simulations)

            # Perform sensitivity analysis
            sensitivity_results = business_valuation_instance.sensitivity_analysis(discount_rate_range, cash_flows_range)

            # Generate valuation report
            valuation_report = business_valuation_instance.generate_valuation_report()

            # Generate chart using the generate_chart function from chart_gen.py
            chart_encoded = generate_chart(cash_flows)

            # Render the result.html template with the calculated present value and chart
            return render_template('result.html', 
                                   present_value=round(present_value_result, 2),
                                   chart_encoded=chart_encoded,
                                   simulated_values=simulated_values,
                                   sensitivity_results=sensitivity_results,
                                   valuation_report=valuation_report)

        except ValueError as e:
            # Handle invalid input error
            return render_template('index.html', error_message="Invalid input. Please enter valid numeric values.")

    # Render the index.html template for the initial GET request
    return render_template('index.html')

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
