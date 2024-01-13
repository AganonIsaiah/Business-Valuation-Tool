import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_chart(cash_flows):
    # Create a DataFrame for plotting
    df = pd.DataFrame({'Year': range(1, len(cash_flows) + 1), 'Cash Flow': cash_flows})
    
    # Plot historical cash flows
    plt.figure(figsize=(8, 5))
    plt.plot(df['Year'], df['Cash Flow'], marker='o')
    plt.title('Historical Cash Flows')
    plt.xlabel('Year')
    plt.ylabel('Cash Flow')
    plt.grid(True)
    plt.tight_layout()
    
    # Save the plot to a BytesIO object
    chart_buffer = BytesIO()
    plt.savefig(chart_buffer, format='png')
    plt.close()
    
    # Encode the image for HTML rendering
    chart_encoded = base64.b64encode(chart_buffer.getvalue()).decode('utf-8')
    
    return chart_encoded
