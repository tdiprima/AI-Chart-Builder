"""
Simple Plot based on OpenAI data
This app creates a bar chart of the top 5 countries by GDP.
Date: 2025-03-31
Author: Tammy DiPrima
"""
import plotly.express as px

# Data
data = {
    "x_data": ["United States", "China", "Japan", "Germany", "United Kingdom"],
    "y_data": [21433226, 14342903, 5081770, 3861123, 2826441]
}

# Create the bar chart
fig = px.bar(
    x=data["x_data"],
    y=data["y_data"],
    title="Top 5 Countries by GDP",
    labels={"x": "Country", "y": "GDP ($)"}
)

# Show the plot
fig.show()
