# ⚡ AI Chart Builder

Turn plain English into clean, dynamic charts — powered by GPT-4o, LLaMA 4, or whatever AI provider fits your vibe.

Built with Plotly + Dash. Just type your prompt ("Bar chart of sales by region"), and boom: chart.

## 🧠 What's Inside

- One unified script: `ai_chart_builder.py`  
- Choose from **Azure OpenAI**, **OpenAI**, or **Groq (LLaMA 4)**  
- Easy switch via a single `AI_PROVIDER` variable  
- Web UI with prompt box + model picker  
- Handles errors, shows retries, and gives you Plotly charts like magic

> *Heads-up:* Sometimes the model forgets to put the date in the title. Sometimes it hallucinates. Don't trust it with your taxes.

---

## 🚀 Quickstart

### 1. Clone it  
Download or clone the repo. Make sure you have Python 3.8+.

### 2. Install deps  
```bash
pip install dash dash-bootstrap-components pandas plotly pandas-datareader openai groq python-dotenv
```

### 3. Set up `.env`  
Create a `.env` file next to the script with any of these:

```env
# Azure
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_KEY=your_key
OPENAI_API_VERSION=2023-05-15

# Groq
GROQ_API_KEY=your_groq_key
```

(OpenAI uses your default config — no extra setup needed.)

### 4. Pick your AI provider  
At the top of `ai_chart_builder.py`:

```python
AI_PROVIDER = "openai"  # Options: "azure", "groq", "openai"
```

Comment out the config blocks for the providers you *don’t* use.

### 5. Run it  
```bash
python ai_chart_builder.py
```

Open [http://localhost:8050](http://localhost:8050) and go wild.

---

## 🛠 Features

- 🔄 Easily switch between providers  
- 📊 Natural language → Plotly charts  
- 🧠 Supports model selection (GPT-4o, 3.5, etc.)  
- 🧼 Handles errors + retries  
- 👁️‍🗨️ Clean Dash interface with spinner + logs  

---

## 🤯 Troubleshooting

- **API errors?** Check your `.env`.  
- **No data?** Prompt might be too vague.  
- **Weird chart?** That’s the AI being quirky. Try again or switch models.  
- **Missing packages?** Reinstall with `pip`.

---

## 🙌 Contribute

Fork, tweak, PR, repeat. Open to ideas, bug reports, and feature adds.

---

## 📄 License

[MIT](LICENSE). Go nuts.
