# AI Chart Builder

## Overview

The `ai_chart_builder.py` script is a unified application that generates charts based on user prompts using different AI services: Azure OpenAI, Groq, and OpenAI. It leverages Plotly for chart rendering and Dash for the web interface, allowing users to input prompts (e.g., "Line chart of average patient heart rate over 7 days") and generate visualizations dynamically.

This script combines the functionality of three previous versions (Azure, Groq, and OpenAI) into a single file, making it easy to switch between AI providers by commenting out unused sections or configuring a single variable.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.8 or higher
- Required Python packages (listed in the "Installation" section below)
- An API key and endpoint for at least one of the following AI services:
  - Azure OpenAI
  - Groq
  - OpenAI

## Installation

### 1. Clone or Download the Script

Download the `ai_chart_builder.py` file to your local machine or clone the repository if it’s part of a larger project.

### 2. Install Dependencies

Install the required Python packages using pip. Run the following command in your terminal or command prompt:

```bash
pip install dash dash-bootstrap-components pandas plotly pandas-datareader openai groq python-dotenv
```

### 3. Set Up Environment Variables

Create a `.env` file in the same directory as the script to store your API keys and endpoints. The file should include the following variables (use only the ones relevant to the AI provider you plan to use):

```env
# For Azure OpenAI
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_KEY=your_azure_api_key
OPENAI_API_VERSION=your_api_version  # e.g., "2023-05-15"

# For Groq
GROQ_API_KEY=your_groq_api_key

# For OpenAI
# No additional variables needed if using default OpenAI configuration
```

Replace `your_azure_endpoint`, `your_azure_api_key`, `your_api_version`, and `your_groq_api_key` with your actual API credentials and endpoints.

## Usage

### 1. Configure the AI Provider

Open `ai_chart_builder.py` and locate the following line near the top of the file:

```python
AI_PROVIDER = "openai"  # Options: "azure", "groq", "openai"
```

Set `AI_PROVIDER` to the AI service you want to use:

- `"azure"` for Azure OpenAI
- `"groq"` for Groq
- `"openai"` for OpenAI

If you only want to use one provider, comment out the configuration blocks for the other providers. For example, to use only OpenAI, comment out the `if AI_PROVIDER == "azure":` and `elif AI_PROVIDER == "groq":` blocks (including their `client` definitions and API call sections in the `generate_chart` function).

### 2. Run the Script

Launch the script by running the following command in your terminal or command prompt from the directory containing the script:

```bash
python ai_chart_builder.py
```

This will start a local web server, and the Dash app will be accessible in your web browser at `http://127.0.0.1:8050/` (or another port if 8050 is in use).

### 3. Use the Web Interface

Once the app is running:

- You’ll see a web interface with a text area where you can enter a prompt (e.g., "Line chart of average patient heart rate over 7 days").
- If using OpenAI or Azure, you can select a model from the dropdown menu (e.g., "GPT-4o", "GPT-3.5 Turbo").
- Click the "Generate Chart" button to create a chart based on your prompt.
- If there’s an error, an error message will appear, and you can click "Retry" to try again.

### 4. Switching Providers

To switch between AI providers:

- Change the `AI_PROVIDER` variable at the top of the script.
- Ensure the corresponding API keys and endpoints are set in your `.env` file.
- Comment out unused provider blocks to avoid import errors or unnecessary code execution.

For example, if you only want to use Groq, comment out the Azure and OpenAI blocks as shown below:

```python
# Comment out these blocks if not using:
# if AI_PROVIDER == "azure":
#     from openai import AzureOpenAI
#     client = AzureOpenAI(...)

# Only keep this block if using OpenAI:
elif AI_PROVIDER == "openai":
    from openai import OpenAI
    client = OpenAI()
```

## Features

- Supports multiple AI providers (Azure, Groq, OpenAI) in a single script.
- Generates Plotly Express charts based on user prompts.
- Includes error handling for API failures, invalid code, and data issues.
- Provides a user-friendly Dash web interface with loading indicators and retry options.
- Allows model selection for OpenAI and Azure (via dropdown).

## Troubleshooting

- **API Errors**: If you see errors related to API keys or network connections, check your `.env` file for correct credentials and ensure your internet connection is stable.
- **Invalid Code**: If the AI generates invalid Python code, refine your prompt or try a different AI provider/model. The error message will guide you (e.g., "The AI generated invalid code. Please refine your prompt and try again.").
- **No Data Found**: If the chart shows "No data found," ensure your prompt requests existing data or adjust the prompt to use sample data.
- **Dependencies Missing**: If you encounter import errors, verify that all required packages are installed (see "Installation" above).

## Contributing

If you’d like to contribute to this script, feel free to fork the repository, make changes, and submit pull requests. Bug reports and feature requests are also welcome!

## License

This script is provided under the MIT License. See the [LICENSE](LICENSE) file for more details.
