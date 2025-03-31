"""
AI Chart Builder
This app uses OpenAI's GPT-4 to generate chart specifications based on user input and Plotly to render the charts.

Author: Tammy DiPrima
"""
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Create a Dash app
app = dash.Dash(__name__)

# Set your OpenAI API key

def parse_chart_request(input_text):
    # Prompt for OpenAI to interpret chart requests
    system_prompt = """You are a chart creation assistant. Convert the user's text into a JSON specification for a chart.
    Do not include any explanation or other text. Do not use '```' characters. Just return JSON.
    Return only valid JSON with these fields:
    - chart_type: one of 'line', 'bar', 'scatter', 'pie'
    - x_data: list of data points for x-axis (categories, dates, or numbers)
    - y_data: list of corresponding numerical values
    - title: descriptive chart title
    - x_label: label for x-axis (optional)
    - y_label: label for y-axis (optional)
    
    For example, if asked about monthly sales:
    {"chart_type": "line", "x_data": ["Jan", "Feb", "Mar", "Apr", "May"], "y_data": [1200, 1350, 1100, 1400, 1600], "title": "Monthly Sales Trend", "x_label": "Month", "y_label": "Sales ($)"}"""

    try:
        print(f"Sending request to OpenAI for: {input_text}")
        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text}
        ],
        temperature=0.7)
        result = response.choices[0].message.content
        print(f"OpenAI response: {result}")
        return json.loads(result)
    except Exception as e:
        print(f"Error parsing chart request: {e}")
        return None

# Define a function to generate a chart based on user input
def generate_chart(input_text):
    # Get chart specification from OpenAI
    chart_spec = parse_chart_request(input_text)

    if not chart_spec:
        # Fallback to simple line chart if there's an error
        return px.line(x=[1, 2, 3], y=[1, 2, 3], title="Error creating chart")

    try:
        # Get optional axis labels
        x_label = chart_spec.get("x_label", "")
        y_label = chart_spec.get("y_label", "")
        
        # Create the appropriate chart based on the specification
        if chart_spec["chart_type"] == "bar":
            fig = px.bar(
                x=chart_spec["x_data"],
                y=chart_spec["y_data"],
                title=chart_spec["title"],
                labels={"x": x_label, "y": y_label}
            )
        elif chart_spec["chart_type"] == "line":
            fig = px.line(
                x=chart_spec["x_data"],
                y=chart_spec["y_data"],
                title=chart_spec["title"],
                labels={"x": x_label, "y": y_label}
            )
        elif chart_spec["chart_type"] == "scatter":
            fig = px.scatter(
                x=chart_spec["x_data"],
                y=chart_spec["y_data"],
                title=chart_spec["title"],
                labels={"x": x_label, "y": y_label}
            )
        elif chart_spec["chart_type"] == "pie":
            fig = px.pie(
                values=chart_spec["y_data"],
                names=chart_spec["x_data"],
                title=chart_spec["title"]
            )
        else:
            fig = px.line(x=[1, 2, 3], y=[1, 2, 3], title="Unsupported chart type")

        # Add some styling
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12)
        )
        return fig
    except Exception as e:
        print(f"Error creating chart: {e}")
        return px.line(x=[1, 2, 3], y=[1, 2, 3], title="Error creating chart")

# Create a Dash layout with a text input and a chart output
app.layout = html.Div([
    html.H1("AI Chart Builder", style={'textAlign': 'center', 'marginBottom': 30}),
    html.Div([
        html.Label("Describe the chart you want (e.g., 'Show me a bar chart of monthly sales'):", 
                  style={'marginBottom': 10}),
        dcc.Input(
            id="input-text",
            type="text",
            value="",
            style={'width': '100%', 'padding': '10px', 'marginBottom': '20px'}
        ),
    ], style={'width': '80%', 'margin': 'auto'}),
    html.Div([
        dcc.Graph(id="chart-output"),
    ], style={'width': '80%', 'margin': 'auto'}),
], style={'padding': '20px'})

# Define callback to update chart based on input text
@app.callback(
    Output("chart-output", "figure"),
    Input("input-text", "value")
)
def update_chart(input_text):
    if not input_text:
        return px.line(x=[1, 2, 3], y=[1, 2, 3], title="Enter a chart description to begin")
    return generate_chart(input_text)

# Run the Dash app
if __name__ == "__main__":
    app.run(debug=True)
