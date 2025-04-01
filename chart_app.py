"""
AI Chart Builder
This app uses OpenAI's GPT-4 to generate chart specifications based on user input and Plotly to render the charts.

Author: Tammy DiPrima
"""
import re

import dash
import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output, State
from openai import OpenAI

client = OpenAI()

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Textarea(id='prompt', placeholder='Ask for a chart...', style={'width': '100%', 'height': 100}),
    html.Button('Generate Chart', id='submit', n_clicks=0),
    dcc.Graph(id='output-chart'),
    html.Div(id='error', style={'color': 'red'})
])


@app.callback(
    Output('output-chart', 'figure'),
    Output('error', 'children'),
    Input('submit', 'n_clicks'),
    State('prompt', 'value'),
    prevent_initial_call=True
)
def generate_chart(n, prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Python developer writing Plotly Express code. You must include all necessary data definitions (e.g., DataFrames or dictionaries) and variable assignments in your response. Important: Respond with just the code; no additional explanation or text."},
                {"role": "user", "content": f"Create a plot based on this prompt: {prompt}"}
            ],
            max_tokens=500  # Increased to allow more data
        )
        code = response.choices[0].message.content
        code = re.sub(r"```(?:python)?|```", "", code).strip()
        print(code)
        local_vars = {'px': px, 'pd': pd}  # Provide px and pd, but no df
        exec(code, {}, local_vars)
        return local_vars['fig'], ''
    except Exception as e:
        return dash.no_update, f"Error: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
