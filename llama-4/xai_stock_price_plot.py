"""
Llama-4 fake data
"""
import pandas as pd
import plotly.express as px

data = {
    "Date": ["2023-08-01", "2023-09-01", "2023-10-01", "2023-11-01", "2023-12-01", "2024-01-01", "2024-02-01", "2024-03-01"],
    "Open": [100, 110, 120, 130, 140, 150, 160, 170],
    "High": [105, 115, 125, 135, 145, 155, 165, 175],
    "Low": [95, 105, 115, 125, 135, 145, 155, 165],
    "Close": [102, 112, 122, 132, 142, 152, 162, 172]
}

df = pd.DataFrame(data)
df["Date"] = pd.to_datetime(df["Date"])

# Plot all price lines
fig = px.line(df, x="Date", y=["Open", "High", "Low", "Close"], title="xAI Stock Price over the Past Year (2023-08-01 to 2024-03-01)")

fig.update_layout(xaxis_title="Date", yaxis_title="Stock Price (USD)")
fig.show()
