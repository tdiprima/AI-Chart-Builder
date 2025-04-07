import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output, State, exceptions
from openai import OpenAI
import re
import pandas_datareader as pdr
import datetime

client = OpenAI()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H2("AI Chart Builder", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='model-dropdown',
        options=[
            {'label': 'GPT-3.5 Turbo', 'value': 'gpt-3.5-turbo'},
            {'label': 'GPT-4o', 'value': 'gpt-4o'},
            {'label': 'GPT-4o Mini', 'value': 'gpt-4o-mini'},
            {'label': 'GPT-4.5 Preview', 'value': 'gpt-4.5-preview'},
            {'label': 'o1 Mini', 'value': 'o1-mini'}
        ],
        value='gpt-4o',  # Default model
        style={'width': '100%', 'marginBottom': 10}
    ),
    dcc.Textarea(
        id='prompt',
        placeholder='Ask for a chart (e.g., "Line chart of average patient heart rate over 7 days")',
        style={'width': '100%', 'height': 100}
    ),
    html.Button('Generate Chart', id='submit', n_clicks=0, className='btn btn-primary'),
    dcc.Loading(id="loading", type="circle", children=dcc.Graph(id='output-chart')),
    html.Div(id='feedback', style={'marginTop': 10}),
    html.Div(
        id='error',
        style={'color': 'red', 'marginTop': 10, 'padding': 10, 'border': '1px solid #ffcccc', 'borderRadius': 5}
    ),
    html.Button('Retry', id='retry', n_clicks=0, className='btn btn-secondary',
                style={'display': 'none', 'marginTop': 10}),
], style={'maxWidth': '800px', 'margin': 'auto', 'padding': 20})


@app.callback(
    [
        Output('output-chart', 'figure'),
        Output('error', 'children'),
        Output('feedback', 'children'),
        Output('retry', 'style')
    ],
    [
        Input('submit', 'n_clicks'),
        Input('retry', 'n_clicks')
    ],
    [
        State('prompt', 'value'),
        State('model-dropdown', 'value')  # Add the model dropdown state
    ],
    prevent_initial_call=True
)
def generate_chart(submit_clicks, retry_clicks, prompt, selected_model):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise exceptions.PreventUpdate

    # Clear error and chart first
    # (So the UI is wiped clean before generating a new chart or showing a new error)
    fig = {}
    error_msg = ""
    feedback = ""

    # Check if prompt is empty or just whitespace
    if not prompt or not prompt.strip():
        # Return now so we don't proceed with chart creation
        return fig, "Error: Please enter a prompt.", feedback, {'display': 'none'}

    # Provide initial feedback
    feedback = "Generating chart... This may take a moment."
    retry_style = {'display': 'none'}

    try:
        # Call OpenAI API with the selected model
        response = client.chat.completions.create(
            model=selected_model,  # Use the selected model from the dropdown
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a Python developer tasked with generating only Plotly Express code. "
                        "Your response must contain ONLY the Python code with no explanations, comments, or additional text. "
                        "Do not include backticks, markdown, or any other formatting. The code should include all "
                        "necessary data definitions (e.g., DataFrames or dictionaries), REAL data, python imports, and variable assignments. "
                        "You MUST provide all data. Do not reference any csv files. DO NOT USE package yfinance. "
                        "DO NOT GENERATE RANDOM DATA. If you cannot find any data, then return a chart with title saying \"No data found\". "
                        "Note the actual date of the dataset in the title of the chart. "
                        "Generate only the Plotly Express Python code. No explanations or text, just the code."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Generate only the Plotly Express Python code for: {prompt}. "
                        "No explanations or text, just the code."
                    )
                }
            ],
            temperature=0.2,  # Lower temperature for more focused, less creative responses
            top_p=0.1         # Narrow down the token selection
        )

        # Get the response content
        code = response.choices[0].message.content.strip()
        code = re.sub(r"```(?:python)?|```", "", code).strip()

        # Remove specific unwanted lines or text (e.g., yfinance messages)
        unwanted_lines = [
            "YF.download() has changed argument auto_adjust default to True",
            "[*********************100%***********************]  1 of 1 completed"
        ]
        for unwanted in unwanted_lines:
            code = code.replace(unwanted, "")

        # Filter out lines that start with unwanted keywords
        unwanted_starts = ['here is', 'below is', 'the code', 'this code', 'note:']
        code_lines = [
            line for line in code.split('\n')
            if not any(line.lower().startswith(start.lower()) for start in unwanted_starts)
            and line.strip()
        ]
        code = '\n'.join(code_lines)

        print(code)

        # Ensure there's still some code left to execute
        if not code:
            raise ValueError("No valid code remaining after filtering.")

        # Execute the cleaned code
        local_vars = {'px': px, 'pd': pd, 'pdr': pdr, 'datetime': datetime}
        exec(code, {}, local_vars)

        if 'fig' not in local_vars or local_vars['fig'] is None:
            raise ValueError("Failed to generate a valid Plotly figure. The figure object is None.")

        # Return the new figure, with cleared error and feedback
        return local_vars['fig'], "", "", {'display': 'none'}

    except Exception as e:
        error_msg = "Error: An issue occurred while generating the chart. "

        if "API" in str(e) or "OpenAI" in str(e):
            error_msg += "Please check your API key or network connection."
        elif "invalid syntax" in str(e) or "NameError" in str(e):
            error_msg += "The AI generated invalid code. Please refine your prompt and try again."
        elif "unexpected text" in str(e):
            error_msg += "The AI included extra text instead of just code. Please try again or adjust the prompt."
        elif "No valid code" in str(e) or "Failed to generate a valid Plotly figure" in str(e):
            error_msg += (
                "The chart could not be created. Check if the data or prompt is valid, "
                "or try a different chart type."
            )
        else:
            error_msg += (
                f"Unexpected error: {str(e)}. "
                "Please try a different prompt or contact support."
            )

        print(e)
        return {}, error_msg, "", {'display': 'block'}  # Show error, keep chart cleared


if __name__ == '__main__':
    app.run(debug=True)
