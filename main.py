from flask import Flask, render_template, request, redirect, session, url_for
from business_val import BusinessValuation
from chart_gen import generate_chart  

app = Flask(__name__)
app.secret_key = 'secret_key'   


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Extract user input from the form
            num_cash_flows = int(request.form['num_cash_flows'])
            discount_rate = float(request.form['discount_rate'])
            cash_flows = [float(request.form[f'cash_flow_{i}']) for i in range(1, num_cash_flows + 1)]

            # Create an instance of the BusinessValuation class
            business_valuation_instance = BusinessValuation(cash_flows, discount_rate)

            # Perform cash flow-related operations
            present_value_result = business_valuation_instance.calculate_present_value()
            chart_encoded = generate_chart(business_valuation_instance.cash_flows)
            valuation_report = business_valuation_instance.generate_valuation_report()

            # Store necessary data in session for later use
            session['business_valuation_instance'] = business_valuation_instance.to_json()

            # Render the result page with the calculated present value and chart data
            return render_template('dcf.html',
                                   show_results=True,
                                   num_cash_flows=num_cash_flows,
                                   discount_rate=discount_rate,
                                   present_value=round(present_value_result, 2),
                                   valuation_report=valuation_report,
                                   chart_encoded=chart_encoded
            )

        except ValueError as e:
            # Handle invalid input error
            print("Error:", e)
            return render_template('dcf.html', error_message="Invalid input. Please enter valid numeric values.")


    # Render the index.html template for the initial GET request
    return render_template('dcf.html', show_results=False)


@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if 'business_valuation_instance' not in session:
        # Redirect to the index page if the necessary data is not available
        return redirect(url_for('dcf'))

    business_valuation_instance_data = session['business_valuation_instance']
    business_valuation_instance = BusinessValuation.from_json(business_valuation_instance_data)


    # Check if the form is submitted for Monte Carlo simulation
    if request.method == 'POST' and 'monte_carlo' in request.form:
        num_simulations = int(request.form['num_simulations'])
        monte_carlo_results = business_valuation_instance.monte_carlo_simulation(num_simulations)
        return render_template('analysis.html', monte_carlo_results=monte_carlo_results)

    # Check if the form is submitted for Sensitivity Analysis
    elif request.method == 'POST' and 'sensitivity_analysis' in request.form:
        discount_rate_range = (float(request.form['discount_rate_start']), float(request.form['discount_rate_end']))
        cash_flows_range = (float(request.form['cash_flows_start']), float(request.form['cash_flows_end']))
        num_points = int(request.form['num_points'])
        sensitivity_results = business_valuation_instance.sensitivity_analysis(
            discount_rate_range, cash_flows_range, num_points
        )
        return render_template('analysis.html', sensitivity_results=sensitivity_results)

    # Render the analysis.html template for the initial GET request
    return render_template('analysis.html', monte_carlo_results=None, sensitivity_results=None)

@app.route('/scenario_analysis', methods=['GET', 'POST'])
def scenario_analysis():
    if 'business_valuation_instance' not in session:
        # Redirect to the index page if the necessary data is not available
        return redirect(url_for('dcf'))

    business_valuation_instance_data = session['business_valuation_instance']
    business_valuation_instance = BusinessValuation.from_json(business_valuation_instance_data)

    # Check if the form is submitted for Scenario Analysis
    if request.method == 'POST' and 'scenario_analysis' in request.form:
        # Parse scenario parameters from the form
        scenarios = []
        for i in range(1, int(request.form['num_scenarios']) + 1):
            discount_rate_key = f'discount_rate_{i}'
            cash_flows_key = f'cash_flows_{i}'

            discount_rate = float(request.form[discount_rate_key])

            # Split the cash flows string into individual values and convert to float
            cash_flows_str = request.form[cash_flows_key]
            cash_flows = [float(value.strip()) for value in cash_flows_str.split(',')]

            scenarios.append({
                'discount_rate': discount_rate,
                'cash_flows': cash_flows
            })

        # Perform scenario analysis
        scenario_results = business_valuation_instance.scenario_analysis(scenarios)

        # Add an index to each result to use in the template
        scenario_results_with_index = list(enumerate(scenario_results))

        return render_template('scenario_analysis.html', scenario_results=scenario_results_with_index)

    # Render the scenario_analysis.html template for the initial GET request
    return render_template('scenario_analysis.html', scenario_results=None)



if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
