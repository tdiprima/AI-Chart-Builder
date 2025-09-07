"""
AI Chart Builder (Combined Azure, Groq, and OpenAI)
This app uses different AI services (Azure, Groq, or OpenAI) to generate charts based on user input and Plotly to render the charts.

Author: Tammy DiPrima
"""

import datetime
import os
import re

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader as pdr
import plotly.express as px
from dash import Input, Output, State, dcc, exceptions, html
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# TODO: Choose AI provider (comment out the ones you don't want to use)
AI_PROVIDER = "openai"  # Options: "azure", "groq", "openai"

# Define the system message content once
SYSTEM_MESSAGE_CONTENT = (
    "You are a Python developer tasked with generating only Plotly Express code. "
    "Your response must contain ONLY the Python code with no explanations, comments, "
    "or additional text. Do not include backticks, markdown, or any other formatting. "
    "The code should include all necessary data definitions (e.g., DataFrames or dictionaries), "
    "REAL data, python imports, and variable assignments. You MUST provide all data. "
    "Verify the existence of data being asked for, before attempting to plot. "
    'If there is no data, draw an empty chart with title saying "No data found". '
    "Do not reference any csv files. If you use package yfinance, be sure to return a 'fig' and do 'fig.show()'. "
    'You should convert the 2D array of shape (252, 1) into a 1D array, which is what plotly.express expects.  Example: y=data["Close"].squeeze(). '
    "ALWAYS give the date or dates of the data in the title."
)

# ==============================
# Unified AI Service Configuration
# ==============================


def get_ai_client():
    """Initialize and return the appropriate AI client based on AI_PROVIDER"""
    if AI_PROVIDER == "azure":
        from openai import AzureOpenAI

        return AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("OPENAI_API_VERSION"),
        )
    elif AI_PROVIDER == "groq":
        from groq import Groq

        return Groq(api_key=os.getenv("GROQ_API_KEY"))
    elif AI_PROVIDER == "openai":
        from openai import OpenAI

        return OpenAI()
    else:
        raise ValueError("Invalid AI_PROVIDER. Choose 'azure', 'groq', or 'openai'.")


def get_ai_response(client, prompt, selected_model=None):
    """Get AI response with provider-specific configurations"""
    messages = [
        {"role": "system", "content": SYSTEM_MESSAGE_CONTENT},
        {
            "role": "user",
            "content": f"Generate only the Plotly Express Python code for: {prompt}. No explanations or text, just the code.",
        },
    ]

    # Provider-specific configurations
    configs = {
        "azure": {
            "model": os.getenv("DEPLOYMENT_NAME"),
            "max_tokens": 500,
            "temperature": 0.2,
            "top_p": 0.1,
        },
        "groq": {
            "model": "compound-beta-mini",
            "max_tokens": 4096,
            "temperature": 0.05,
            "top_p": 0.05,
            "timeout": 30,
        },
        "openai": {
            "model": selected_model or "gpt-4o",
            "max_tokens": 500,
            "temperature": 0.2,
            "top_p": 0.1,
        },
    }

    return client.chat.completions.create(messages=messages, **configs[AI_PROVIDER])


def clean_generated_code(code):
    """Clean and filter the generated code"""
    # Remove markdown formatting
    code = re.sub(r"```(?:python)?|```", "", code).strip()

    # Remove specific unwanted lines
    unwanted_lines = [
        "YF.download() has changed argument auto_adjust default to True",
        "[*********************100%***********************]  1 of 1 completed",
    ]
    for unwanted in unwanted_lines:
        code = code.replace(unwanted, "")

    # Filter out lines with unwanted starts
    unwanted_starts = ["here is", "below is", "the code", "this code", "note:"]
    code_lines = [
        line
        for line in code.split("\n")
        if not any(line.lower().startswith(start.lower()) for start in unwanted_starts)
        and line.strip()
    ]

    return "\n".join(code_lines)


# Initialize client once
client = get_ai_client()

# Dash App Setup
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Model options only for OpenAI/Azure
model_options = (
    [
        {"label": "GPT-3.5 Turbo", "value": "gpt-3.5-turbo"},
        {"label": "GPT-4o", "value": "gpt-4o"},
        {"label": "GPT-4o Mini", "value": "gpt-4o-mini"},
        {"label": "GPT-4.5 Preview", "value": "gpt-4.5-preview"},
        {"label": "o1 Mini", "value": "o1-mini"},
    ]
    if AI_PROVIDER in ("openai", "azure")
    else []
)

app.layout = html.Div(
    [
        html.H2("AI Chart Builder", style={"textAlign": "center"}),
        dcc.Dropdown(
            id="model-dropdown",
            options=model_options,
            value="gpt-4o" if model_options else None,
            style={
                "width": "100%",
                "marginBottom": 10,
                "display": "block" if model_options else "none",
            },
        ),
        dcc.Textarea(
            id="prompt",
            placeholder='Ask for a chart (e.g., "Line chart of average patient heart rate over 7 days")',
            style={"width": "100%", "height": 100},
        ),
        html.Button(
            "Generate Chart", id="submit", n_clicks=0, className="btn btn-primary"
        ),
        dcc.Loading(id="loading", type="circle", children=dcc.Graph(id="output-chart")),
        html.Div(id="feedback", style={"marginTop": 10}),
        html.Div(
            id="error",
            style={
                "color": "red",
                "marginTop": 10,
                "padding": 10,
                "border": "1px solid #ffcccc",
                "borderRadius": 5,
            },
        ),
        html.Button(
            "Retry",
            id="retry",
            n_clicks=0,
            className="btn btn-secondary",
            style={"display": "none", "marginTop": 10},
        ),
    ],
    style={"maxWidth": "800px", "margin": "auto", "padding": 20},
)


@app.callback(
    [
        Output("output-chart", "figure"),
        Output("error", "children"),
        Output("feedback", "children"),
        Output("retry", "style"),
    ],
    [Input("submit", "n_clicks"), Input("retry", "n_clicks")],
    [State("prompt", "value"), State("model-dropdown", "value")],
    prevent_initial_call=True,
)
def generate_chart(submit_clicks, retry_clicks, prompt, selected_model):
    """Generate chart based on user prompt using selected AI model"""
    ctx = dash.callback_context

    if not ctx.triggered:
        raise exceptions.PreventUpdate

    # Initialize outputs
    fig = {}
    error_msg = ""
    feedback = ""
    retry_style = {"display": "none"}

    # Validate prompt
    if not prompt or not prompt.strip():
        return fig, "Error: Please enter a prompt.", feedback, retry_style

    feedback = "Generating chart... This may take a moment."

    try:
        # Get AI response
        response = get_ai_response(client, prompt, selected_model)

        # Extract and clean code
        code = response.choices[0].message.content.strip()
        code = clean_generated_code(code)

        # Validate code exists
        if not code:
            raise ValueError("No valid code remaining after filtering.")

        # Execute the code
        local_vars = {"px": px, "pd": pd, "pdr": pdr, "datetime": datetime}
        exec(code, {}, local_vars)

        # Validate figure was created
        if "fig" not in local_vars or local_vars["fig"] is None:
            raise ValueError(
                "Failed to generate a valid Plotly figure. The figure object is None."
            )

        return local_vars["fig"], "", "", {"display": "none"}

    except Exception as e:
        error_msg = generate_error_message(e)
        print(e)  # For debugging
        return {}, error_msg, "", {"display": "block"}


def generate_error_message(error):
    """Generate user-friendly error messages based on exception type"""
    error_str = str(error)

    if "API" in error_str or any(
        provider in error_str.lower() for provider in ("azure", "groq", "openai")
    ):
        return "Error: An issue occurred while generating the chart. Please check your API key or network connection."
    elif "invalid syntax" in error_str or "NameError" in error_str:
        return "Error: The AI generated invalid code. Please refine your prompt and try again."
    elif "unexpected text" in error_str:
        return "Error: The AI included extra text instead of just code. Please try again or adjust the prompt."
    elif (
        "No valid code" in error_str
        or "Failed to generate a valid Plotly figure" in error_str
    ):
        return "Error: The chart could not be created. Check if the data or prompt is valid, or try a different chart type."
    return f"Error: Unexpected error: {error_str}. Please try a different prompt or contact support."


if __name__ == "__main__":
    app.run(debug=True)
