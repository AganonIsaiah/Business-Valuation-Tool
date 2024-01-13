# main.py

from flask import Flask, render_template, request
from business_val import BusinessValuation
from chart_gen import generate_chart  # Import your chart generation function

app = Flask(__name__)

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

            # Perform the DCF analysis
            present_value_result = business_valuation_instance.calculate_present_value()

            # Generate chart data
            chart_encoded = generate_chart(business_valuation_instance.cash_flows)

            # Render the result page with the calculated present value and chart data
            return render_template('dcf.html',
                                   show_results=True,
                                   num_cash_flows=num_cash_flows,
                                   discount_rate=discount_rate,
                                   present_value=round(present_value_result, 2),
                                   valuation_report=business_valuation_instance.generate_valuation_report(),
                                   chart_encoded=chart_encoded)

        except ValueError as e:
            # Handle invalid input error
            print("Error:", e)
            return render_template('dcf.html', error_message="Invalid input. Please enter valid numeric values.")

    # Render the index.html template for the initial GET request
    return render_template('dcf.html', show_results=False)

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
