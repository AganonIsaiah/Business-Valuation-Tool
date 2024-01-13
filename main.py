# main.py

from flask import Flask, render_template, request
from business_val import BusinessValuation
from chart_gen import generate_chart

app = Flask(__name__)

def extract_cash_flows(request):
    num_cash_flows = int(request.form['num_cash_flows'])
    return [float(request.form[f'cash_flow_{i}']) for i in range(1, num_cash_flows + 1)]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Extract user input from the form
            cash_flows = extract_cash_flows(request)
            discount_rate = float(request.form['discount_rate'])

            # Create an instance of the BusinessValuation class
            business_valuation_instance = BusinessValuation(cash_flows, discount_rate)

            # Perform the DCF analysis
            present_value_result = business_valuation_instance.calculate_present_value()

            # Generate chart using the generate_chart function from chart_gen.py
            chart_encoded = generate_chart(cash_flows)

            # Render the result.html template with the calculated present value and chart
            return render_template('result.html', 
                                   present_value=round(present_value_result, 2),
                                   chart_encoded=chart_encoded)

        except ValueError as e:
            # Handle invalid input error
            return render_template('index.html', error_message="Invalid input. Please enter valid numeric values.")

    # Render the index.html template for the initial GET request
    return render_template('index.html')

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
