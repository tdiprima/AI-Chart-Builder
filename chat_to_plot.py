"""
🤖 Example Prompts:
Show a histogram of age
Scatter plot of height vs age
Line chart of age over index
Bar chart of age
Box plot of age
Pie chart of age

Author: Tammy DiPrima
"""
import dash
from dash import html, dcc, Input, Output, State
from openai import OpenAI
import plotly.express as px
import pandas as pd
import re

client = OpenAI()

# Sample Data
df = pd.DataFrame({
    "age": [22, 35, 58, 44, 36, 40, 23, 29, 65, 31],
    "height": [170, 180, 160, 165, 177, 175, 172, 169, 168, 174]
})

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
        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a Python developer writing Plotly Express code using a DataFrame called 'df'.  You are to respond with just the code; no additional explanation or text.  Do not include the '```' characters."},
            {"role": "user", "content": f"Create a plot based on this prompt: {prompt}"}
        ],
        max_tokens=200)
        code = response.choices[0].message.content
        code = re.sub(r"```(?:python)?|```", "", code).strip()
        print(code)
        local_vars = {'df': df, 'px': px}
        exec(code, {}, local_vars)
        return local_vars['fig'], ''
    except Exception as e:
        return dash.no_update, f"Error: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
