"""
🫀🔥 Heartbeat line going red alert... Mod activated to make that line red using Plotly Express 🎨
"""
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

data = pd.DataFrame({
    'Date': [datetime.now().date() - timedelta(days=i) for i in range(7)],
    'Heart Rate': [70, 72, 68, 75, 71, 73, 69]
})

fig = px.line(
    data,
    x='Date',
    y='Heart Rate',
    title=f'Average Patient Heart Rate Over 7 Days (Data as of {datetime.now().date()})',
    color_discrete_sequence=['red']  # 🔴 Line color set to red
)

fig.show()
